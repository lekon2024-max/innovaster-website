#!/usr/bin/env python3
"""Comprehensive homepage fix - download all CDN assets and rewrite links."""
import os, re, time, hashlib
from pathlib import Path
import requests
from bs4 import BeautifulSoup

BASE = Path("/Users/kensui/innovaster-static")
INDEX = BASE / "index.html"
ASSETS = BASE / "assets"
CDN_BASE = "https://vhost-hk-s05-cdn.hcwebsite.com/114cc7512acdb6c246325f263e191b62/"

session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

downloaded = {}
stats = {"images": 0, "css": 0, "js": 0}


def download_asset(url: str) -> str:
    """Download a CDN asset, return local path like /assets/xxx.ext."""
    if url in downloaded:
        return downloaded[url]

    # Normalize protocol-relative URL
    if url.startswith("//"):
        full_url = "https:" + url
    elif url.startswith("http"):
        full_url = url
    elif url.startswith("/"):
        # Already local
        downloaded[url] = url
        return url
    else:
        # Relative path - try CDN
        full_url = CDN_BASE + url

    # Try different URL formats
    urls_to_try = [full_url]
    # Strip query params
    base_url = full_url.split("?")[0]
    if base_url != full_url:
        urls_to_try.append(base_url)

    content = None
    for u in urls_to_try:
        try:
            resp = session.get(u, timeout=30)
            if resp.status_code == 200:
                content = resp.content
                break
        except:
            continue

    if content is None:
        print(f"  WARN: Could not download {url}")
        downloaded[url] = url  # Keep original so we don't retry
        return url

    # Determine extension
    ext = os.path.splitext(full_url.split("?")[0])[1].lower()
    if not ext or ext not in ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.webp', '.css', '.js'):
        # Try to detect from content
        if content[:4] == b'\x89PNG':
            ext = '.png'
        elif content[:2] == b'\xff\xd8':
            ext = '.jpeg'
        elif content[:6] in (b'GIF87a', b'GIF89a'):
            ext = '.gif'
        elif b'html' in content[:100].lower():
            ext = '.html'
        else:
            ext = '.bin'

    url_hash = hashlib.md5(full_url.encode()).hexdigest()[:12]
    local_name = f"{url_hash}{ext}"
    local_path = ASSETS / local_name
    local_path.write_bytes(content)

    if ext == '.css':
        stats["css"] += 1
    elif ext == '.js':
        stats["js"] += 1
    else:
        stats["images"] += 1

    result = f"/assets/{local_name}"
    downloaded[url] = result
    return result


def fix_homepage():
    print("── Downloading all CDN assets for homepage... ──")
    html = INDEX.read_text(encoding='utf-8')
    soup = BeautifulSoup(html, 'lxml')

    # --- 1. Fix <img src> and <img data-src> and <img data-lazy> ---
    for tag in soup.find_all('img'):
        for attr in ('src', 'data-src', 'data-lazy'):
            val = tag.get(attr)
            if val and ('vhost-hk-s05-cdn' in val or (not val.startswith('/') and not val.startswith('http') and not val.startswith('data:'))):
                local = download_asset(val)
                tag[attr] = local
                if attr == 'data-lazy':
                    # Also set src for lazy images
                    tag['src'] = local

    # --- 2. Fix <link href> (CSS) ---
    for tag in soup.find_all('link', href=True):
        val = tag['href']
        if 'vhost-hk-s05-cdn' in val:
            local = download_asset(val)
            tag['href'] = local

    # --- 3. Fix <script src> (JS) ---
    for tag in soup.find_all('script', src=True):
        val = tag['src']
        if 'vhost-hk-s05-cdn' in val:
            local = download_asset(val)
            tag['src'] = local

    # --- 4. Fix window.eljson inline JSON data ---
    html_out = str(soup)

    # Find all CDN URLs in JSON data and replace them
    cdn_pattern = re.compile(r'//vhost-hk-s05-cdn\.hcwebsite\.com/114cc7512acdb6c246325f263e191b62/[^"\'\\]+')
    cdn_urls = set(cdn_pattern.findall(html_out))

    for cdn_url in sorted(cdn_urls, key=len, reverse=True):
        local = download_asset(cdn_url)
        html_out = html_out.replace(cdn_url, local)

    # --- 5. Fix relative paths like "res/en/20260226/facotryview_427a2b9c.jpg" ---
    relative_img_pattern = re.compile(r'(data-src|data-lazy|src)=["\'](res/[^"\']+)["\']')
    for match in relative_img_pattern.finditer(html_out):
        attr = match.group(1)
        path = match.group(2)
        full_url = CDN_BASE + path
        local = download_asset(full_url)
        html_out = html_out.replace(f'"{path}"', f'"{local}"')

    # --- 6. Fix product slider "More" buttons (no href) ---
    # These are navigated by JS, but let's check if there are actual buttons
    # The slick-prev/slick-next buttons might work with JS

    # --- 7. Ensure favicon ---
    favicon = soup.find('link', rel='shortcut icon')
    if favicon and favicon.get('href', '').startswith('//'):
        local = download_asset(favicon['href'])
        favicon['href'] = local
        html_out = str(soup)

    INDEX.write_text(html_out, encoding='utf-8')

    print(f"\nDone: {stats['images']} images, {stats['css']} CSS, {stats['js']} JS")
    print(f"Total CDN assets downloaded: {sum(stats.values())}")

    # Verify
    remaining = len(cdn_pattern.findall(INDEX.read_text(encoding='utf-8')))
    print(f"Remaining CDN references: {remaining}")


if __name__ == '__main__':
    fix_homepage()
