#!/usr/bin/env python3
"""Fix remaining issues in the static site."""

import re
from pathlib import Path
from bs4 import BeautifulSoup
import requests

OUTPUT_DIR = Path("/Users/kensui/innovaster-static")

def fix_index_page():
    """Re-download the English homepage."""
    print("── Fixing index.html (was Spanish, need English)... ──")
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        resp = requests.get("https://www.innovaster-tech.com/", headers=headers, timeout=30)
        if resp.status_code == 200:
            html = resp.text
            # Apply same transformations
            html = html.replace("www.innovaster-tech.com", "innovaster.cn")
            html = html.replace("innovaster-tech.com", "innovaster.cn")
            html = html.replace("info@innovaster-tech.com", "info@innovaster.cn")
            html = html.replace("Powered by HiCheng", "")
            html = html.replace('action="/index.php?c=cart"', 'action="mailto:info@innovaster.cn?subject=Product%20Inquiry"')
            html = re.sub(r'action=["\']/index\.php[^"\']*["\']', 'action="mailto:info@innovaster.cn?subject=Contact%20Form"', html)

            # Remove vacuum fryer references
            soup = BeautifulSoup(html, 'lxml')
            for tag in soup.find_all('a', href=True):
                try:
                    href = tag.get('href')
                    if href and 'vacuum' in href.lower():
                        li = tag.find_parent('li')
                        if li:
                            li.decompose()
                        else:
                            tag.decompose()
                except:
                    continue
            html = str(soup)

            (OUTPUT_DIR / "index.html").write_text(html, encoding='utf-8')
            lang_match = re.search(r'<html[^>]*lang="([^"]*)"', html)
            print(f"  Saved English index.html (lang={lang_match.group(1) if lang_match else 'N/A'})")
        else:
            print(f"  WARNING: Got status {resp.status_code}")
    except Exception as e:
        print(f"  ERROR: {e}")

def fix_success_stories():
    """Remove vacuum fryer content from success-stories.html."""
    print("\n── Fixing success-stories.html... ──")
    path = OUTPUT_DIR / "success-stories.html"
    if not path.exists():
        return
    html = path.read_text(encoding='utf-8')
    soup = BeautifulSoup(html, 'lxml')

    # Find vacuum fryer related items and remove their parent containers
    for tag in soup.find_all(['h3', 'h2', 'h4', 'p', 'img']):
        try:
            text = tag.get_text().lower()
        except:
            continue
        if 'vacuum fry' in text or 'vacuum frying' in text:
            # Find parent article/card container
            parent = tag.find_parent(['div', 'li', 'article', 'section'])
            if parent:
                # Go up to find the item card
                for cls in parent.get('class', []):
                    if any(kw in cls.lower() for kw in ['item', 'card', 'post', 'story', 'case']):
                        parent.decompose()
                        print("  Removed vacuum fryer success story card")
                        break
                else:
                    # If we can't find a card, try grandparent
                    grandparent = parent.find_parent(['div', 'li', 'article'])
                    if grandparent:
                        grandparent.decompose()
                        print("  Removed vacuum fryer content block")
                        break

    path.write_text(str(soup), encoding='utf-8')
    print("  Done")

def verify_clean():
    """Final verification."""
    print("\n── Final verification... ──")
    issues = []
    for path in sorted(OUTPUT_DIR.rglob("*.html")):
        try:
            html = path.read_text(encoding='utf-8')
        except:
            continue
        rel = str(path.relative_to(OUTPUT_DIR))

        if 'innovaster-tech.com' in html:
            issues.append(f"  OLD DOMAIN in: {rel}")

        if 'vacuum fryer' in html.lower() or 'vacuum frying' in html.lower():
            issues.append(f"  VACUUM FRYER in: {rel}")

        if 'vacuum-fry' in html.lower():
            issues.append(f"  VACUUM LINK in: {rel}")

    if issues:
        print("⚠️  Remaining issues:")
        for i in issues:
            print(i)
    else:
        print("✅ All clean! No remaining issues.")

    # Count pages
    pages = [p for p in OUTPUT_DIR.rglob("*.html") if 'assets' not in str(p)]
    print(f"\n  Total HTML pages: {len(pages)}")

def main():
    fix_index_page()
    fix_success_stories()
    verify_clean()

if __name__ == '__main__':
    main()
