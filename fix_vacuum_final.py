#!/usr/bin/env python3
"""Final cleanup of vacuum fryer references — more aggressive approach."""
import re, json
from pathlib import Path
from bs4 import BeautifulSoup

OUTPUT_DIR = Path("/Users/kensui/innovaster-static")


def clean_index():
    """Remove vacuum fryer from index.html."""
    print("── Cleaning index.html... ──")
    path = OUTPUT_DIR / "index.html"
    html = path.read_text(encoding='utf-8')

    # 1. Remove the vacuum fryer nav link
    soup = BeautifulSoup(html, 'lxml')
    for tag in soup.find_all('a'):
        try:
            if tag.get_text(strip=True).lower() == 'vacuum fryer':
                li = tag.find_parent('li')
                if li:
                    li.decompose()
                    print("  Removed vacuum fryer nav <li>")
                else:
                    tag.decompose()
                    print("  Removed vacuum fryer nav <a>")
        except:
            continue

    # 2. Remove vacuum fryer from the window.eljson JSON block
    html = str(soup)
    # The JSON block contains product data; find and remove vacuum fryer entry
    pattern = r'\{"url":"/vacuum-fryer\.html","img":"[^"]+","name1":"Vacuum Fryer Machine","name2":"[^"]*"\}'
    match = re.search(pattern, html)
    if match:
        # Remove with surrounding comma handling
        entry = match.group(0)
        # Try removing with preceding comma
        html = html.replace(',' + entry, '')
        # Try removing with trailing comma
        html = html.replace(entry + ',', '')
        # Try removing standalone
        html = html.replace(entry, '')
        print("  Removed vacuum fryer from JSON data")

    # 3. Remove success story cards about vacuum frying
    soup = BeautifulSoup(html, 'lxml')
    for tag in soup.find_all(['h3', 'p', 'span']):
        try:
            text = tag.get_text().lower()
        except:
            continue
        if 'vacuum fry' in text or 'vacuum frying' in text:
            # Walk up to find a card-like container
            parent = tag
            for _ in range(5):
                parent = parent.parent
                if parent is None:
                    break
                if parent.name in ('li', 'article', 'section'):
                    parent.decompose()
                    print(f"  Removed success story <{parent.name}>")
                    break
                # Also check for div with class containing 'item' or 'card'
                try:
                    classes = parent.get('class')
                    if classes and isinstance(classes, list):
                        if any('item' in c.lower() or 'card' in c.lower() or 'post' in c.lower() or 'story' in c.lower() for c in classes):
                            parent.decompose()
                            print(f"  Removed card <div class=\"{' '.join(classes)}\">")
                            break
                except:
                    pass

    path.write_text(str(soup), encoding='utf-8')
    print("  index.html cleaned")


def clean_success_stories():
    """Remove vacuum fryer from success-stories.html."""
    print("\n── Cleaning success-stories.html... ──")
    path = OUTPUT_DIR / "success-stories.html"
    html = path.read_text(encoding='utf-8')
    soup = BeautifulSoup(html, 'lxml')

    # Find any element mentioning vacuum frying and remove its ancestor card
    done = set()
    for tag in soup.find_all(text=re.compile(r'vacuum\s*fry', re.I)):
        parent = tag.parent
        if parent is None:
            continue
        # Walk up to find a card/container (up to 6 levels)
        current = parent
        for _ in range(6):
            if current is None or current in done:
                break
            try:
                if current.name in ('li', 'article', 'section', 'tr'):
                    current.decompose()
                    done.add(current)
                    print(f"  Removed <{current.name}>")
                    break
                classes = current.get('class')
                if classes and isinstance(classes, list):
                    cls_str = ' '.join(classes).lower()
                    if any(kw in cls_str for kw in ('item', 'card', 'post', 'story', 'case', 'grid', 'col')):
                        current.decompose()
                        done.add(current)
                        print(f"  Removed <{current.name} class=\"{' '.join(classes)}\">")
                        break
            except:
                pass
            current = current.parent

    # Fallback: also search by img alt text
    for tag in soup.find_all('img', alt=re.compile(r'vacuum\s*fry', re.I)):
        current = tag
        for _ in range(5):
            current = current.parent if current else None
            if current is None:
                break
            try:
                classes = current.get('class')
                if classes and isinstance(classes, list):
                    if any(kw in ' '.join(classes).lower() for kw in ('item', 'card', 'post', 'story', 'case', 'col', 'grid')):
                        current.decompose()
                        print(f"  Fallback removed <{current.name}>")
                        break
            except:
                pass

    path.write_text(str(soup), encoding='utf-8')
    print("  success-stories.html cleaned")


def verify():
    """Final check."""
    print("\n── Verification... ──")
    for path in sorted(OUTPUT_DIR.rglob("*.html")):
        try:
            html = path.read_text(encoding='utf-8')
        except:
            continue
        rel = str(path.relative_to(OUTPUT_DIR))
        lower = html.lower()
        if 'vacuum fryer' in lower or 'vacuum frying' in lower:
            print(f"  ⚠️  VACUUM FRYER still in: {rel}")
        if 'vacuum-fry' in lower:
            # Only check non-asset paths
            if '/vacuum-fry' in lower or 'vacuum-fryer.html' in lower:
                print(f"  ⚠️  VACUUM LINK in: {rel}")

    # Count remaining
    count = 0
    for p in OUTPUT_DIR.rglob("*.html"):
        if 'assets' not in str(p):
            h = p.read_text(encoding='utf-8').lower()
            if 'vacuum fry' in h or 'vacuum-fry' in h:
                count += 1
    if count == 0:
        print("  ✅ No vacuum fryer references remain!")
    else:
        print(f"  ⚠️  {count} files still have references")


if __name__ == '__main__':
    clean_index()
    clean_success_stories()
    verify()
