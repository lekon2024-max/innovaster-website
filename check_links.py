#!/usr/bin/env python3
"""Check all sitemap URLs with delays and retries."""
import re
import time
import requests
from pathlib import Path

SITEMAP = Path("/Users/kensui/innovaster-static/sitemap.xml")
sitemap = SITEMAP.read_text()
urls = re.findall(r'<loc>https?://innovaster\.cn/([^<]+)</loc>', sitemap)
urls = [f'http://innovaster.cn/{u}' for u in urls]

print(f"Checking {len(urls)} URLs...\n")

ok, failed, errors = [], [], []
session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0"

for i, url in enumerate(urls):
    for attempt in range(3):
        try:
            resp = session.get(url, timeout=30, allow_redirects=True)
            if resp.status_code == 200:
                ok.append(url)
                print(f"  [{i+1:2d}/{len(urls)}] 200 {url.replace('https://innovaster.cn', '')}")
            else:
                failed.append((url, resp.status_code))
                print(f"  [{i+1:2d}/{len(urls)}] {resp.status_code} {url.replace('https://innovaster.cn', '')}")
            break
        except Exception as e:
            if attempt == 2:
                errors.append((url, str(e)))
                print(f"  [{i+1:2d}/{len(urls)}] ERR {url.replace('https://innovaster.cn', '')}: {e}")
            else:
                time.sleep(2)
    time.sleep(0.5)  # Don't hammer the server

print(f"\n{'='*60}")
print(f"Results: {len(ok)} OK, {len(failed)} failed, {len(errors)} errors")
if failed:
    print("\nFailed:")
    for url, code in failed:
        print(f"  {code} {url}")
if errors:
    print("\nErrors:")
    for url, err in errors:
        print(f"  {err[:60]} {url}")
