#!/usr/bin/env python3
"""Re-fetch original homepage with minimal transformations - preserve exact HTML structure."""
import re, hashlib, os
from pathlib import Path
import requests

BASE = Path("/Users/kensui/innovaster-static")
ASSETS = BASE / "assets"

session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

downloaded = {}

def download_cdn(url: str) -> str:
    """Download CDN asset and return local path."""
    if url in downloaded:
        return downloaded[url]

    full_url = "https:" + url if url.startswith("//") else url
    try:
        resp = session.get(full_url, timeout=30)
        if resp.status_code != 200:
            downloaded[url] = url
            return url
        content = resp.content
    except:
        downloaded[url] = url
        return url

    ext = os.path.splitext(full_url.split("?")[0])[1].lower()
    if not ext:
        if content[:4] == b'\x89PNG': ext = '.png'
        elif content[:2] == b'\xff\xd8': ext = '.jpeg'
        else: ext = '.bin'

    name = hashlib.md5(full_url.encode()).hexdigest()[:12] + ext
    (ASSETS / name).write_bytes(content)
    result = f"/assets/{name}"
    downloaded[url] = result
    return result


def main():
    print("Fetching original homepage...")
    resp = session.get("https://www.innovaster-tech.com/", timeout=30)
    html = resp.text

    # --- Apply ONLY essential string replacements ---
    replacements = [
        ("www.innovaster-tech.com", "innovaster.cn"),
        ("innovaster-tech.com", "innovaster.cn"),
        ("es.innovaster-tech.com", "innovaster.cn"),
        ("info@innovaster-tech.com", "ken@innovaster-tech.com"),
        ("Powered by HiCheng", ""),
        ('href="index.php?c=cart"', 'href="mailto:ken@innovaster-tech.com?subject=Product%20Inquiry"'),
        ("href='/index.php?c=cart'", "href='mailto:ken@innovaster-tech.com?subject=Product%20Inquiry'"),
    ]
    for old, new in replacements:
        html = html.replace(old, new)

    # Replace all CDN URLs with local versions
    # Match protocol-relative and absolute CDN URLs
    cdn_pattern = re.compile(r'//vhost-hk-s05-cdn\.hcwebsite\.com/[^"\'<>\s]+')
    for match in set(cdn_pattern.findall(html)):
        local = download_cdn(match)
        html = html.replace(match, local)

    # Remove vacuum fryer from eljson (keep the original page structure intact)
    # The vacuum fryer entry is a JSON entry: ,[{"url":"/vacuum-fryer.html"...}]
    vacuum_pattern = re.compile(r',\[{"url":"/vacuum-fryer\.html"[^]]*}\]')
    html = vacuum_pattern.sub('', html)

    # Remove Facebook/Twitter/Instagram social elements (but keep structure)
    # Remove social <li> items
    for cls in ['facebook', 'twitter', 'instagram']:
        html = re.sub(r'<li class="' + cls + r'">\s*<a[^>]*></a>\s*</li>', '', html)

    # Remove social footer divs
    for cls in ['facebook', 'twitter', 'instagram']:
        # Remove entire div with social class, including nested content
        html = re.sub(
            r'<div class="' + cls + r'">.*?</div>\s*</div>\s*</div>',
            '</div></div>',
            html,
            flags=re.DOTALL
        )

    # Fix form actions
    html = re.sub(r'action="[^"]*index\.php[^"]*"', 'action="mailto:ken@innovaster-tech.com?subject=Contact%20Form"', html)

    # Save
    (BASE / "index.html").write_text(html, encoding='utf-8')
    print(f"Saved index.html ({len(html)} bytes)")
    print(f"Assets downloaded: {len(downloaded)}")
    print(f"CDN refs remaining: {len(cdn_pattern.findall(html))}")


if __name__ == '__main__':
    main()
