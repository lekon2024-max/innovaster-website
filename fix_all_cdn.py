#!/usr/bin/env python3
"""Fix all CDN references across ALL HTML pages - download assets and rewrite."""
import os, re, time, hashlib
from pathlib import Path
import requests
from bs4 import BeautifulSoup

BASE = Path("/Users/kensui/innovaster-static")
ASSETS = BASE / "assets"
CDN_DOMAIN = "vhost-hk-s05-cdn.hcwebsite.com"
CDN_PREFIX = "114cc7512acdb6c246325f263e191b62"

session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

downloaded = {}
stats = {"pages": 0, "images": 0, "css_js": 0}


def download_cdn_asset(cdn_url: str) -> str:
    """Download CDN asset, return /assets/xxx.ext path."""
    if cdn_url in downloaded:
        return downloaded[cdn_url]

    # Build full URL
    if cdn_url.startswith("//"):
        full_url = "https:" + cdn_url
    elif cdn_url.startswith("http"):
        full_url = cdn_url
    else:
        full_url = "https://" + CDN_DOMAIN + "/" + CDN_PREFIX + "/" + cdn_url

    # Download
    content = None
    for u in [full_url, full_url.split("?")[0]]:
        try:
            resp = session.get(u, timeout=30)
            if resp.status_code == 200:
                content = resp.content
                break
        except:
            continue

    if content is None:
        downloaded[cdn_url] = cdn_url  # Don't retry
        return cdn_url

    # Extension
    ext = os.path.splitext(full_url.split("?")[0])[1].lower()
    if not ext:
        if content[:4] == b'\x89PNG': ext = '.png'
        elif content[:2] == b'\xff\xd8': ext = '.jpeg'
        elif content[:6] in (b'GIF87a', b'GIF89a'): ext = '.gif'
        elif b'html' in content[:200].lower(): ext = '.html'
        else: ext = '.bin'

    url_hash = hashlib.md5(full_url.encode()).hexdigest()[:12]
    local_name = f"{url_hash}{ext}"
    local_path = ASSETS / local_name

    if not local_path.exists():
        local_path.write_bytes(content)
        if ext in ('.css', '.js'):
            stats["css_js"] += 1
        else:
            stats["images"] += 1

    result = f"/assets/{local_name}"
    downloaded[cdn_url] = result
    return result


def fix_page(filepath: Path):
    """Fix all CDN references in a single HTML page."""
    html = filepath.read_text(encoding='utf-8')
    soup = BeautifulSoup(html, 'lxml')
    changed = False

    # --- <img src/data-src/data-lazy> ---
    for tag in soup.find_all('img'):
        for attr in ('src', 'data-src', 'data-lazy'):
            val = tag.get(attr)
            if val and CDN_DOMAIN in str(val):
                tag[attr] = download_cdn_asset(val)
                changed = True

    # --- <link href> ---
    for tag in soup.find_all('link', href=True):
        val = tag['href']
        if val and CDN_DOMAIN in str(val):
            tag['href'] = download_cdn_asset(val)
            changed = True

    # --- <script src> ---
    for tag in soup.find_all('script', src=True):
        val = tag['src']
        if val and CDN_DOMAIN in str(val):
            tag['src'] = download_cdn_asset(val)
            changed = True

    # --- <source src/srcset> ---
    for tag in soup.find_all('source'):
        for attr in ('src', 'srcset'):
            val = tag.get(attr)
            if val and CDN_DOMAIN in str(val):
                tag[attr] = download_cdn_asset(val)
                changed = True

    html_out = str(soup)

    # --- Inline JSON/Script data with CDN URLs ---
    cdn_pattern = re.compile(r'//vhost-hk-s05-cdn\.hcwebsite\.com/114cc7512acdb6c246325f263e191b62/[^"\'\\\s<>]+')
    matches = set(cdn_pattern.findall(html_out))
    for cdn_url in sorted(matches, key=len, reverse=True):
        local = download_cdn_asset(cdn_url)
        html_out = html_out.replace(cdn_url, local)
        changed = True

    # Also handle protocol-prefixed
    cdn_pattern2 = re.compile(r'https?://vhost-hk-s05-cdn\.hcwebsite\.com/114cc7512acdb6c246325f263e191b62/[^"\'\\\s<>]+')
    matches2 = set(cdn_pattern2.findall(html_out))
    for cdn_url in sorted(matches2, key=len, reverse=True):
        local = download_cdn_asset(cdn_url)
        html_out = html_out.replace(cdn_url, local)
        changed = True

    if changed:
        filepath.write_text(html_out, encoding='utf-8')
        stats["pages"] += 1

    return changed


def main():
    print("Fixing CDN references across ALL pages...\n")
    html_files = list(BASE.rglob("*.html"))
    total = len(html_files)

    for i, fp in enumerate(sorted(html_files)):
        rel = str(fp.relative_to(BASE))
        changed = fix_page(fp)
        if changed:
            print(f"  [{i+1:3d}/{total}] FIXED: {rel}")

    # Check remaining
    remaining = 0
    for fp in BASE.rglob("*.html"):
        html = fp.read_text(encoding='utf-8')
        remaining += html.count(CDN_DOMAIN)

    print(f"\n{'='*60}")
    print(f"Pages fixed: {stats['pages']}")
    print(f"New assets: {stats['images']} images, {stats['css_js']} CSS/JS")
    print(f"Remaining CDN references: {remaining}")
    print(f"Total cached assets: {len(downloaded)}")


if __name__ == '__main__':
    main()
