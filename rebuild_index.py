#!/usr/bin/env python3
"""Rebuild index.html from original - exact structure, all fixes applied at once."""
import re, hashlib, os, requests
from pathlib import Path
from bs4 import BeautifulSoup

BASE = Path("/Users/kensui/innovaster-static")
ASSETS = BASE / "assets"
session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0"
downloaded = {}

def dl(url):
    if url in downloaded: return downloaded[url]
    full = "https:" + url if url.startswith("//") else url
    try:
        r = session.get(full, timeout=30)
        if r.status_code != 200: downloaded[url] = url; return url
        c = r.content
    except:
        downloaded[url] = url; return url
    ext = os.path.splitext(full.split("?")[0])[1].lower() or ".jpeg"
    name = hashlib.md5(full.encode()).hexdigest()[:12] + ext
    p = ASSETS / name
    if not p.exists(): p.write_bytes(c)
    res = f"/assets/{name}"; downloaded[url] = res
    return res


def main():
    print("Fetching original homepage...")
    resp = session.get("https://www.innovaster-tech.com/", timeout=30)
    orig_html = resp.text
    soup = BeautifulSoup(orig_html, "lxml")

    # --- 1. Remove vacuum fryer ONLY ---
    # Product-nav: remove <li> containing vacuum fryer link
    pn = soup.find("div", class_="product-nav")
    if pn:
        for li in pn.find("ul").find_all("li", recursive=False):
            a = li.find("a")
            if a and "vacuum" in (a.get("href") or "").lower():
                li.decompose()
                print("Removed vacuum fryer from product-nav")

    # Sort/tab bar: remove vacuum fryer <li>
    sort_div = soup.find("div", class_="sort")
    if sort_div:
        for li in sort_div.find("ul").find_all("li", recursive=False):
            a = li.find("a")
            if a and "vacuum" in (a.get("href") or "").lower():
                li.decompose()
                print("Removed vacuum fryer from sort tabs")

    # Customer case: remove vacuum frying machine card
    for div in soup.find_all("div", class_="item"):
        img = div.find("img")
        if img and "vacuum" in (img.get("alt") or "").lower():
            parent = div.find_parent("div")
            if parent and parent.parent:
                parent.decompose()
                print("Removed vacuum fryer customer case card")

    # Mobile/secondary nav: remove vacuum links
    for a in soup.find_all("a", href=True):
        href = (a.get("href") or "").lower()
        if "vacuum" in href:
            li = a.find_parent("li")
            if li and li.find_parent("div", class_="product-nav") is None:
                li.decompose()
                print(f"Removed vacuum fryer mobile nav link: {href}")

    # --- 2. Replace domains ---
    html = str(soup)
    html = html.replace("www.innovaster-tech.com", "innovaster.cn")
    html = html.replace("innovaster-tech.com", "innovaster.cn")
    html = html.replace("es.innovaster-tech.com", "innovaster.cn")
    html = html.replace("info@innovaster-tech.com", "ken@innovaster-tech.com")
    html = html.replace("Powered by HiCheng", "")

    # --- 3. Download and replace ALL CDN references ---
    cdn_pattern = re.compile(r'//vhost-hk-s05-cdn\.hcwebsite\.com/[^"\'<>\s]+')
    for url in set(cdn_pattern.findall(html)):
        local = dl(url)
        html = html.replace(url, local)
    print(f"CDN assets: {len(downloaded)}")

    # --- 4. Fix cart ---
    html = html.replace('href="/index.php?c=cart"', 'href="mailto:ken@innovaster-tech.com?subject=Product%20Inquiry"')

    # --- 5. Fix forms ---
    html = re.sub(r'action="/index\.php[^"]*"', 'action="mailto:ken@innovaster-tech.com?subject=Contact%20Form"', html)

    # --- 6. Remove social media (but keep linkedin/youtube) ---
    for cls in ["facebook", "twitter", "instagram"]:
        # Header social icons
        html = re.sub(r'<li class="' + cls + r'">\s*<a[^>]*></a>\s*</li>', '', html)
    # Footer social blocks
    html = re.sub(r'<div class="facebook">.*?</div>\s*</div>\s*</div>', '</div></div>', html, flags=re.DOTALL)
    html = re.sub(r'<div class="twitter">.*?</div>\s*</div>\s*</div>', '</div></div>', html, flags=re.DOTALL)
    html = re.sub(r'<div class="instagram">.*?</div>\s*</div>\s*</div>', '</div></div>', html, flags=re.DOTALL)

    # Remove JS SDK script tags
    html = re.sub(r'<script[^>]*connect\.facebook\.net[^>]*></script>', '', html)
    html = re.sub(r'<script[^>]*platform\.twitter\.com[^>]*></script>', '', html)
    html = re.sub(r'<script[^>]*instagram\.com[^>]*></script>', '', html)

    # Save
    out = BASE / "index.html"
    out.write_text(html, encoding="utf-8")
    print(f"Saved: {len(html)} bytes")

    # Verify
    v = BeautifulSoup(html, "lxml")
    v_pn = v.find("div", class_="product-nav")
    items = v_pn.find("ul").find_all("li", recursive=False) if v_pn else []
    print(f"Product-nav items: {len(items)}")
    for li in items:
        a = li.find("a")
        print(f"  - {a.get_text(strip=True) if a else '???'}")
    remaining_cdn = len(cdn_pattern.findall(html))
    remaining_vac = html.lower().count("vacuum-fryer") + html.lower().count("vacuum fryer")
    print(f"CDN refs: {remaining_cdn}")
    print(f"Vacuum product refs: {remaining_vac}")
    print(f"Social refs: {html.lower().count('facebook.com') + html.lower().count('twitter.com') + html.lower().count('instagram.com')}")


if __name__ == "__main__":
    main()
