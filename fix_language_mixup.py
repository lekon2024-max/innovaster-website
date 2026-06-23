#!/usr/bin/env python3
"""Re-fetch English versions of pages that were overwritten by Spanish."""
import re
from pathlib import Path
from bs4 import BeautifulSoup
import requests

OUTPUT_DIR = Path("/Users/kensui/innovaster-static")
EN_BASE = "https://www.innovaster-tech.com"

# Spanish pages that need English replacement
# URL path → local file path
PAGES_TO_FIX = [
    ("/who-we-are.html", "who-we-are.html"),
    ("/product/rotary-retorts1.html", "product/rotary-retorts1.html"),
    ("/product/pilot-retorts1.html", "product/pilot-retorts1.html"),
    ("/product/shuttle-and-loading-unloading-machine.html", "product/shuttle-and-loading-unloading-machine.html"),
    ("/product/steam-retorts.html", "product/steam-retorts.html"),
    ("/product/water-immersion-retorts.html", "product/water-immersion-retorts.html"),
    ("/product/steam-air-retorts.html", "product/steam-air-retorts.html"),
    ("/product/retort-loader-unloader.html", "product/retort-loader-unloader.html"),
    ("/product/retort-shuttle1.html", "product/retort-shuttle1.html"),
    ("/product/retorts-autoclaves.html", "product/retorts-autoclaves.html"),
    ("/product/water-spray-retorts.html", "product/water-spray-retorts.html"),
]

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept-Language": "en-US,en;q=0.9",
})


def fetch_english_page(url_path: str):
    """Fetch a page from the English site."""
    url = EN_BASE + url_path
    print(f"  Fetching: {url}")
    try:
        resp = session.get(url, timeout=30)
        if resp.status_code == 200:
            return resp.text
        else:
            print(f"    WARNING: HTTP {resp.status_code}")
            return None
    except Exception as e:
        print(f"    ERROR: {e}")
        return None


def process_html(html: str) -> str:
    """Apply same transformations as the crawled pages."""
    # Replace domains
    html = html.replace("www.innovaster-tech.com", "innovaster.cn")
    html = html.replace("innovaster-tech.com", "innovaster.cn")
    html = html.replace("es.innovaster-tech.com", "innovaster.cn")
    html = html.replace("info@innovaster-tech.com", "ken@innovaster-tech.com")
    html = html.replace("info@innovaster.cn", "ken@innovaster-tech.com")
    html = html.replace("Powered by HiCheng", "")

    # Fix cart/inquiry links
    html = html.replace('href="index.php?c=cart"', 'href="mailto:ken@innovaster-tech.com?subject=Product%20Inquiry"')
    html = html.replace("href='/index.php?c=cart'", "href='mailto:ken@innovaster-tech.com?subject=Product%20Inquiry'")
    html = html.replace('href="/index.php?c=cart"', 'href="mailto:ken@innovaster-tech.com?subject=Product%20Inquiry"')

    # Fix form actions
    html = re.sub(r'action=["\']/index\.php[^"\']*["\']', 'action="mailto:ken@innovaster-tech.com?subject=Contact%20Form"', html)

    # Fix logo to use English version
    html = html.replace('c29c40869fc8.png', 'd8bc0781bf1e.png')

    # Remove vacuum fryer references
    soup = BeautifulSoup(html, 'lxml')
    for tag in soup.find_all('a', href=True):
        try:
            href = (tag.get('href') or '').lower()
            if 'vacuum' in href:
                li = tag.find_parent('li')
                if li:
                    li.decompose()
                else:
                    tag.decompose()
        except:
            continue
    html = str(soup)

    return html


def main():
    print("=" * 60)
    print("Fixing language mix-up: ES → EN")
    print("=" * 60)

    fixed = 0
    for url_path, local_path in PAGES_TO_FIX:
        en_html = fetch_english_page(url_path)
        if en_html is None:
            continue

        en_html = process_html(en_html)

        filepath = OUTPUT_DIR / local_path
        filepath.write_text(en_html, encoding='utf-8')
        lang = re.search(r'<html[^>]*lang="([^"]*)"', en_html)
        print(f"    Saved: {local_path} (lang={lang.group(1) if lang else 'N/A'})")
        fixed += 1

    print(f"\nFixed {fixed}/{len(PAGES_TO_FIX)} pages")

    # Verify
    print("\n── Verification ──")
    remaining_es = []
    for path in sorted(OUTPUT_DIR.rglob("*.html")):
        try:
            html = path.read_text(encoding='utf-8')
            if 'lang="es"' in html:
                remaining_es.append(str(path.relative_to(OUTPUT_DIR)))
        except:
            pass

    if remaining_es:
        print(f"⚠️  {len(remaining_es)} Spanish pages remaining:")
        for p in remaining_es:
            print(f"     {p}")
    else:
        print("✅ All pages are now English!")


if __name__ == '__main__':
    main()
