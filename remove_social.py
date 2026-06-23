#!/usr/bin/env python3
"""Remove all Facebook, Twitter, Instagram references from all HTML pages."""
import re
from pathlib import Path
from bs4 import BeautifulSoup, Comment

BASE = Path("/Users/kensui/innovaster-static")

SOCIAL_DOMAINS = ['facebook.com', 'twitter.com', 'instagram.com', 'connect.facebook.net', 'platform.twitter.com']
SOCIAL_CLASSES = ['facebook', 'twitter', 'instagram']


def clean_page(filepath: Path):
    html = filepath.read_text(encoding='utf-8')
    soup = BeautifulSoup(html, 'lxml')
    removed = 0

    # -- 1. Remove <a> links to social media --
    for tag in soup.find_all('a', href=True):
        href = (tag.get('href') or '').lower()
        if any(d in href for d in SOCIAL_DOMAINS):
            # Remove the parent <li> if it's a nav item
            li = tag.find_parent('li')
            if li:
                li.decompose()
                removed += 1
            else:
                tag.decompose()
                removed += 1

    # -- 2. Remove <script> loading social SDKs --
    for tag in soup.find_all('script', src=True):
        try:
            src = (tag.get('src') or '').lower()
            if any(d in src for d in SOCIAL_DOMAINS):
                tag.decompose()
                removed += 1
        except Exception:
            continue

    # -- 3. Remove <iframe> to social media --
    for tag in soup.find_all('iframe', src=True):
        try:
            src = (tag.get('src') or '').lower()
            if any(d in src for d in SOCIAL_DOMAINS):
                tag.decompose()
                removed += 1
        except Exception:
            continue

    # -- 4. Remove <div> with social classes (footer social sections) --
    for tag in soup.find_all('div', class_=True):
        try:
            classes = tag.get('class') or []
            if isinstance(classes, list):
                for cls in classes:
                    if cls.lower() in SOCIAL_CLASSES:
                        tag.decompose()
                        removed += 1
                        break
        except Exception:
            continue

    # -- 5. Remove <li> with social classes --
    for tag in soup.find_all('li', class_=True):
        try:
            classes = tag.get('class') or []
            if isinstance(classes, list):
                for cls in classes:
                    if cls.lower() in SOCIAL_CLASSES:
                        tag.decompose()
                        removed += 1
                        break
        except Exception:
            continue

    # -- 6. Remove social media <blockquote> (Facebook embeds) --
    for tag in soup.find_all('blockquote', cite=True):
        try:
            cite = (tag.get('cite') or '').lower()
            if any(d in cite for d in SOCIAL_DOMAINS):
                parent_div = tag.find_parent('div')
                if parent_div:
                    parent_div.decompose()
                    removed += 1
                else:
                    tag.decompose()
                    removed += 1
        except Exception:
            continue

    # -- 7. Remove <a> with twitter-timeline class --
    for tag in soup.find_all('a', class_=True):
        try:
            classes = tag.get('class') or []
            if isinstance(classes, list):
                if any('twitter' in c.lower() for c in classes):
                    parent_div = tag.find_parent('div')
                    if parent_div:
                        parent_div.decompose()
                        removed += 1
                    else:
                        tag.decompose()
                        removed += 1
        except Exception:
            continue

    # -- 8. Remove <div class="fb-page"> --
    for tag in soup.find_all('div', class_=True):
        try:
            classes = tag.get('class') or []
            if isinstance(classes, list):
                if any('fb-' in c.lower() for c in classes):
                    tag.decompose()
                    removed += 1
        except Exception:
            continue

    # -- 9. Remove any remaining text/links with social URLs in href --
    for tag in soup.find_all(href=True):
        try:
            href = (tag.get('href') or '').lower()
            if any(d in href for d in SOCIAL_DOMAINS):
                tag.decompose()
                removed += 1
        except Exception:
            continue

    # -- 10. Remove commented-out social iframes --
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        if any(d in comment.lower() for d in SOCIAL_DOMAINS):
            comment.extract()
            removed += 1

    if removed > 0:
        filepath.write_text(str(soup), encoding='utf-8')

    return removed


def main():
    print("Removing Facebook/Twitter/Instagram from all pages...\n")
    total = 0
    pages = sorted(BASE.rglob("*.html"))
    for p in pages:
        n = clean_page(p)
        if n > 0:
            rel = str(p.relative_to(BASE))
            print(f"  {rel}: removed {n} refs")
            total += n

    print(f"\nTotal removed: {total} references across {len(pages)} pages")

    # Verify
    remaining = 0
    for p in BASE.rglob("*.html"):
        html = p.read_text(encoding='utf-8').lower()
        for d in SOCIAL_DOMAINS:
            remaining += html.count(d)
    print(f"Remaining references: {remaining}")


if __name__ == '__main__':
    main()
