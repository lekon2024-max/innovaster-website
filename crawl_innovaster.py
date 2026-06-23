#!/usr/bin/env python3
"""
Crawler for innovaster-tech.com → static site migration.
Downloads all pages and assets, rewrites links for local serving.
"""

import os
import re
import sys
import time
import json
import hashlib
import urllib.parse
from pathlib import Path
from collections import deque

import requests
from bs4 import BeautifulSoup

# ── Config ──────────────────────────────────────────────
BASE_URL = "https://www.innovaster-tech.com"
OUTPUT_DIR = Path("/Users/kensui/innovaster-static")
ASSETS_DIR = "assets"

# Domains we're allowed to crawl
ALLOWED_DOMAINS = {
    "www.innovaster-tech.com",
    "innovaster-tech.com",
    "es.innovaster-tech.com",
    "vhost-hk-s05-cdn.hcwebsite.com",
}

# File extensions that are "assets" (not pages)
ASSET_EXTENSIONS = {
    '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico',
    '.woff', '.woff2', '.ttf', '.eot', '.otf',
    '.pdf', '.doc', '.docx', '.xls', '.xlsx',
    '.mp4', '.webm', '.mp3',
    '.webp', '.bmp',
}

# URLs we've already seen (page URLs → local file path)
visited_pages: dict[str, Path] = {}
# Asset URLs we've downloaded (url → local file path)
downloaded_assets: dict[str, Path] = {}
# Queue of page URLs to crawl
url_queue: deque[str] = deque()

# Stats
stats = {"pages": 0, "assets": 0, "errors": 0}

# Session with retries
session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
})

# ── Helpers ─────────────────────────────────────────────

def url_to_filepath(url: str, is_asset: bool = False) -> Path:
    """Convert a URL to a local file path."""
    parsed = urllib.parse.urlparse(url)
    path = parsed.path.lstrip('/')

    if not path or path.endswith('/'):
        path = path + 'index.html'

    # If the path has no extension and it's a page, treat as .html
    if not is_asset and '.' not in path.split('/')[-1]:
        path = path.rstrip('/') + '.html'

    return OUTPUT_DIR / path


def asset_local_path(url: str) -> Path:
    """
    Generate a local path for a downloaded asset.
    Uses a hash to avoid collisions + preserves extension.
    """
    parsed = urllib.parse.urlparse(url)
    path = parsed.path
    # Get extension
    ext = os.path.splitext(path)[1].lower()
    if not ext:
        ext = '.bin'
    # Hash the full URL for uniqueness
    url_hash = hashlib.md5(url.encode()).hexdigest()[:12]
    return OUTPUT_DIR / ASSETS_DIR / f"{url_hash}{ext}"


def is_internal(url: str) -> bool:
    """Check if URL belongs to our allowed domains."""
    parsed = urllib.parse.urlparse(url)
    domain = parsed.netloc.lower()
    # Handle protocol-relative URLs
    if not domain:
        return True  # relative URL
    return domain in ALLOWED_DOMAINS


def is_asset_url(url: str) -> bool:
    """Check if a URL points to a static asset."""
    parsed = urllib.parse.urlparse(url)
    path = parsed.path.lower()
    ext = os.path.splitext(path)[1]
    # Also check query params for image indicators
    if ext in ASSET_EXTENSIONS:
        return True
    # CDN paths with /res/, /data/, /tpl/ are likely assets
    if any(seg in path for seg in ['/res/', '/data/', '/tpl/', 'assets/images', 'assets/css', 'assets/js']):
        return True
    return False


def normalize_url(url: str, base_url: str) -> str:
    """Normalize a URL: resolve relative, strip fragments."""
    # Remove fragment
    url = url.split('#')[0]
    if not url:
        return ''
    # Resolve relative
    full = urllib.parse.urljoin(base_url, url)
    # Remove trailing query params we don't need for pages
    return full


def download_file(url: str, max_retries: int = 3):  # returns bytes or None
    """Download a file with retries."""
    for attempt in range(max_retries):
        try:
            resp = session.get(url, timeout=30)
            if resp.status_code == 200:
                return resp.content
            elif resp.status_code in (404, 403, 410):
                return None
            else:
                time.sleep(1)
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"  ERROR downloading {url}: {e}")
                return None
            time.sleep(2)
    return None


def save_file(path: Path, content):  # bytes or str
    """Save content to a file, creating dirs as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, str):
        path.write_text(content, encoding='utf-8')
    else:
        path.write_bytes(content)


def rewrite_html(html: str, page_url: str) -> str:
    """
    Rewrite HTML to use local paths for assets and internal links.
    Also downloads referenced assets.
    """
    soup = BeautifulSoup(html, 'lxml')

    # ── Rewrite <a href> ──
    for tag in soup.find_all('a', href=True):
        href = tag['href'].strip()
        if href.startswith('javascript:') or href.startswith('mailto:') or href.startswith('tel:') or href.startswith('whatsapp:'):
            continue
        if href == '#':
            continue

        full_url = normalize_url(href, page_url)
        if not full_url:
            continue

        # Is it an internal page?
        if is_internal(full_url) and not is_asset_url(full_url):
            # Queue it for crawling if new
            if full_url not in visited_pages:
                url_queue.append(full_url)
            # Rewrite link to local path
            local = url_to_filepath(full_url)
            tag['href'] = '/' + str(local.relative_to(OUTPUT_DIR))
        elif is_internal(full_url) and is_asset_url(full_url):
            # Download asset and rewrite
            local = download_and_save_asset(full_url)
            if local:
                tag['href'] = '/' + str(local.relative_to(OUTPUT_DIR))

    # ── Rewrite <img src> ──
    for tag in soup.find_all('img', src=True):
        src = tag['src'].strip()
        if src.startswith('data:'):
            continue
        full_url = normalize_url(src, page_url)
        if full_url and is_internal(full_url):
            local = download_and_save_asset(full_url)
            if local:
                tag['src'] = '/' + str(local.relative_to(OUTPUT_DIR))
        # Also handle srcset
        if tag.get('srcset'):
            # Simple approach: just use the main src
            del tag['srcset']

    # ── Rewrite <link href> (CSS, icons) ──
    for tag in soup.find_all('link', href=True):
        href = tag['href'].strip()
        full_url = normalize_url(href, page_url)
        if full_url and is_internal(full_url):
            local = download_and_save_asset(full_url)
            if local:
                tag['href'] = '/' + str(local.relative_to(OUTPUT_DIR))

    # ── Rewrite <script src> ──
    for tag in soup.find_all('script', src=True):
        src = tag['src'].strip()
        full_url = normalize_url(src, page_url)
        if full_url and is_internal(full_url):
            local = download_and_save_asset(full_url)
            if local:
                tag['src'] = '/' + str(local.relative_to(OUTPUT_DIR))

    # ── Rewrite <source src> and <source srcset> ──
    for tag in soup.find_all('source', src=True):
        src = tag['src'].strip()
        full_url = normalize_url(src, page_url)
        if full_url and is_internal(full_url):
            local = download_and_save_asset(full_url)
            if local:
                tag['src'] = '/' + str(local.relative_to(OUTPUT_DIR))

    # ── Rewrite inline styles (background-image, etc.) ──
    for tag in soup.find_all(style=True):
        style_text = tag['style']
        # Find url() references
        def replace_style_url(match):
            url = match.group(1).strip('\'"')
            if url.startswith('data:'):
                return match.group(0)
            full_url = normalize_url(url, page_url)
            if full_url and is_internal(full_url):
                local = download_and_save_asset(full_url)
                if local:
                    return f"url('/{local.relative_to(OUTPUT_DIR)}')"
            return match.group(0)
        tag['style'] = re.sub(r'url\(([^)]+)\)', replace_style_url, style_text)

    # ── Rewrite <meta> content URLs ──
    for tag in soup.find_all('meta', content=True):
        if tag.get('property') in ('og:image', 'og:url') or tag.get('name') in ('twitter:image',):
            content = tag['content'].strip()
            full_url = normalize_url(content, page_url)
            if full_url and is_internal(full_url) and is_asset_url(full_url):
                local = download_and_save_asset(full_url)
                if local:
                    tag['content'] = '/' + str(local.relative_to(OUTPUT_DIR))

    # ── Rewrite <form action> ──
    for tag in soup.find_all('form', action=True):
        action = tag['action'].strip()
        full_url = normalize_url(action, page_url)
        if full_url and is_internal(full_url) and not full_url in visited_pages:
            url_queue.append(full_url)

    return str(soup)


def download_and_save_asset(url: str):  # returns Path or None
    """Download an asset and return its local path."""
    if url in downloaded_assets:
        return downloaded_assets[url]

    print(f"  [asset] {url}")
    content = download_file(url)
    if content is None:
        stats["errors"] += 1
        return None

    local_path = asset_local_path(url)
    save_file(local_path, content)
    downloaded_assets[url] = local_path
    stats["assets"] += 1
    return local_path


def crawl_page(url: str):
    """Crawl a single page."""
    if url in visited_pages:
        return

    print(f"\n[page] {url}")
    content = download_file(url)
    if content is None:
        stats["errors"] += 1
        return

    # Decode
    try:
        html = content.decode('utf-8')
    except UnicodeDecodeError:
        html = content.decode('latin-1')

    # Rewrite HTML (downloads assets and queues new pages)
    html = rewrite_html(html, url)

    # Save
    local_path = url_to_filepath(url)
    save_file(local_path, html)
    visited_pages[url] = local_path
    stats["pages"] += 1


def discover_more_pages():
    """After initial crawl, try to find more pages via sitemap and nav patterns."""
    extra_urls = set()

    # Try sitemap.xml
    for sitemap_url in [
        "https://www.innovaster-tech.com/sitemap.xml",
        "https://www.innovaster-tech.com/sitemap.html",
    ]:
        try:
            resp = session.get(sitemap_url, timeout=30)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.content, 'lxml')
                for loc in soup.find_all('loc'):
                    url = loc.text.strip()
                    if is_internal(url) and not is_asset_url(url):
                        extra_urls.add(url)
                for a in soup.find_all('a', href=True):
                    url = normalize_url(a['href'], sitemap_url)
                    if is_internal(url) and not is_asset_url(url):
                        extra_urls.add(url)
        except:
            pass

    # Common URL patterns to try
    patterns = [
        "/who-we-are.html",
        "/missions-values.html",
        "/production-facilities.html",
        "/what-we-do.html",
        "/canned-meat-1.html",
        "/parts-and-services.html",
        "/thermal-validation.html",
        "/training-technical-support.html",
        "/spare-parts.html",
        "/news.html",
        "/contact.html",
        "/automatic-loading-unloading.html",
        "/ready-to-eat-drink-1.html",
        "/canned-fish-solutions.html",
        "/baby-food-1.html",
        "/pet-food-1.html",
        "/canned-vegetables.html",
        "/faq.html",
        "/thermal-processing-equipment-guide.html",
        "/spices-steam-sterilizer.html",
        "/retort-machines-innovaster.html",
        "/product-new.html",
        "/success-stories.html",
        "/product.html",
        "/product/retorts-autoclaves.html",
        "/product/water-spray-retorts.html",
        "/product/water-immersion-retorts.html",
        "/product/steam-retorts.html",
        "/product/steam-air-retorts.html",
        "/product/rotary-retorts-model.html",
        "/product/water-cascade-retorts.html",
        "/product/pilot-retorts-model.html",
        "/product/retort-accessories.html",
        "/product/shuttle-and-loading-unloading-machine.html",
        "/product/semi-auto-loader-unloader.html",
        "/product/retort-shuttle-rgv.html",
        "/product/retort-loader-unloader.html",
        "/product/industrial-vacuum-fryer.html",
        "/product/automatic-vacuum-fryer.html",
        "/hot-water-spray-retort.html",
        "/index.php?c=cart",
    ]
    for path in patterns:
        url = BASE_URL + path
        if url not in visited_pages:
            extra_urls.add(url)

    return extra_urls


def rewrite_css_urls(css_content: str, css_url: str) -> str:
    """Rewrite url() references in CSS files to point to local assets."""
    def replace_url(match):
        url = match.group(1).strip('\'"').strip()
        if not url or url.startswith('data:'):
            return match.group(0)
        full_url = normalize_url(url, css_url)
        if full_url and is_internal(full_url):
            local = download_and_save_asset(full_url)
            if local:
                return f"url('/{local.relative_to(OUTPUT_DIR)}')"
        return match.group(0)

    return re.sub(r'url\(([^)]+)\)', replace_url, css_content)


# ── Main ────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("Innovaster Crawler — migrating to innovaster.cn")
    print("=" * 60)
    print(f"Output: {OUTPUT_DIR}")

    # Create output dirs
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / ASSETS_DIR).mkdir(parents=True, exist_ok=True)

    # Start with homepage
    url_queue.append(BASE_URL + "/")

    # Also queue the Spanish subdomain
    url_queue.append("https://es.innovaster-tech.com/")

    # Discover extra pages
    print("\n── Discovering pages via sitemap and patterns... ──")
    for url in discover_more_pages():
        url_queue.append(url)
    print(f"  Discovered {len(url_queue)} initial URLs")

    # Crawl loop
    print("\n── Crawling pages... ──")
    while url_queue:
        url = url_queue.popleft()
        try:
            crawl_page(url)
        except Exception as e:
            print(f"  ERROR crawling {url}: {e}")
            stats["errors"] += 1

        # Progress
        if stats["pages"] % 10 == 0:
            print(f"  ... {stats['pages']} pages, {stats['assets']} assets, {len(url_queue)} queued")

    # ── Post-crawl: process downloaded CSS files ──
    print("\n── Processing CSS files... ──")
    for url, local_path in list(downloaded_assets.items()):
        if local_path.suffix == '.css':
            try:
                css = local_path.read_text(encoding='utf-8')
                css = rewrite_css_urls(css, url)
                local_path.write_text(css, encoding='utf-8')
            except Exception as e:
                print(f"  ERROR processing CSS {url}: {e}")

    # ── Generate sitemap.xml ──
    print("\n── Generating sitemap.xml... ──")
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url, path in sorted(visited_pages.items()):
        # Use innovaster.cn in sitemap
        rel = str(path.relative_to(OUTPUT_DIR))
        cn_url = f"https://innovaster.cn/{rel}"
        sitemap += f"  <url><loc>{cn_url}</loc></url>\n"
    sitemap += '</urlset>\n'
    save_file(OUTPUT_DIR / 'sitemap.xml', sitemap)

    # ── Generate robots.txt ──
    print("── Generating robots.txt... ──")
    robots = "User-agent: *\nAllow: /\nSitemap: https://innovaster.cn/sitemap.xml\n"
    save_file(OUTPUT_DIR / 'robots.txt', robots)

    # ── Summary ──
    print("\n" + "=" * 60)
    print("CRAWL COMPLETE")
    print(f"  Pages crawled:   {stats['pages']}")
    print(f"  Assets downloaded: {stats['assets']}")
    print(f"  Errors:          {stats['errors']}")
    print(f"  Output:          {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == '__main__':
    main()
