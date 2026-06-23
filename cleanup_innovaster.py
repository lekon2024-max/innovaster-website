#!/usr/bin/env python3
"""
Post-crawl cleanup for innovaster-static - ROBUST VERSION.
"""

import os, re, shutil, traceback
from pathlib import Path
from bs4 import BeautifulSoup

OUTPUT_DIR = Path("/Users/kensui/innovaster-static")
ASSETS_DIR = OUTPUT_DIR / "assets"

VACUUM_FRYER_FILES = [
    "product/vacuum-fryer.html", "product/vacuum-fryer-machine.html",
    "product/industrial-vacuum-fryer.html", "product/automatic-vacuum-fryer.html",
    "vacuum-fryer.html", "industrial-vacuum-frying-machine.html",
    "sweet-corn-in-vacuum-package-process-flow.html",
    "congrats-on-new-launch-of-innovaster-vacuum-fryer.html",
]
VACUUM_FRYER_DIRS = [
    "product/vacuum-fryer", "product/vacuum-fryer-machine",
    "product/industrial-vacuum-fryer", "product/automatic-vacuum-fryer",
]
VACUUM_KEYWORDS = ["vacuum-fryer", "vacuum-frying", "vacuum-fry", "vacuum fryer"]

stats = {"deleted_files": 0, "deleted_dirs": 0, "modified_files": 0, "vacuum_refs_removed": 0}


def safe_get_text(el):
    """Safely get text from a BeautifulSoup element."""
    try:
        return el.get_text(strip=True) if el else ""
    except:
        return ""


def delete_vacuum_content():
    """Delete vacuum fryer files."""
    print("── Deleting vacuum fryer files... ──")
    for f in VACUUM_FRYER_FILES:
        p = OUTPUT_DIR / f
        if p.exists():
            p.unlink()
            print(f"  DEL: {f}")
            stats["deleted_files"] += 1
    for d in VACUUM_FRYER_DIRS:
        p = OUTPUT_DIR / d
        if p.exists() and p.is_dir():
            shutil.rmtree(p)
            print(f"  DEL DIR: {d}")
            stats["deleted_dirs"] += 1
    for p in list(OUTPUT_DIR.rglob("*")):
        if p.is_file() and any(kw in p.name.lower() for kw in VACUUM_KEYWORDS):
            print(f"  DEL (kw): {p.relative_to(OUTPUT_DIR)}")
            p.unlink()
            stats["deleted_files"] += 1


def clean_pagination():
    """Remove page2, page3 etc."""
    print("\n── Cleaning pagination... ──")
    for p in sorted(OUTPUT_DIR.rglob("page[2-9]*.html")):
        print(f"  DEL: {p.relative_to(OUTPUT_DIR)}")
        p.unlink()
        stats["deleted_files"] += 1
    # Also remove any page1.html that's just a duplicate of the parent
    for p in sorted(OUTPUT_DIR.rglob("page1.html")):
        parent = p.parent / "index.html" if p.parent.name.startswith("page") else p.parent.with_suffix(".html")
        # If parent doesn't exist as index, this page1 is just a duplicate
        if not parent.exists():
            # Check if parent dir has meaningful content
            pass  # Keep it
        else:
            # Remove duplicate
            print(f"  DEL (dup): {p.relative_to(OUTPUT_DIR)}")
            p.unlink()
            stats["deleted_files"] += 1
    # Remove empty page dirs
    for p in sorted(OUTPUT_DIR.rglob("page*"), reverse=True):
        if p.is_dir():
            try:
                remaining = list(p.iterdir())
                if not remaining:
                    p.rmdir()
                    print(f"  DEL DIR: {p.relative_to(OUTPUT_DIR)}")
                    stats["deleted_dirs"] += 1
            except OSError:
                pass


def process_html_file(filepath: Path):
    """Process a single HTML file: remove vacuum refs, replace domains, fix dynamic stuff."""
    try:
        html = filepath.read_text(encoding='utf-8')
    except Exception:
        return False

    original = html
    soup = BeautifulSoup(html, 'lxml')

    # -- 1. Remove vacuum fryer nav items --
    for tag in soup.find_all('a', href=True):
        try:
            href_val = tag.get('href')
            if href_val is None:
                continue
            href = href_val.lower()
        except Exception:
            continue
        if any(kw in href for kw in VACUUM_KEYWORDS):
            li = tag.find_parent('li')
            if li is not None:
                li.decompose()
                stats["vacuum_refs_removed"] += 1
            else:
                tag.decompose()
                stats["vacuum_refs_removed"] += 1

    # -- 2. Remove vacuum fryer sections/divs by class --
    for tag in soup.find_all(True):
        if tag is None or tag.name is None:
            continue
        try:
            css_class = tag.get('class')
            if css_class and isinstance(css_class, list):
                classes_str = ' '.join(css_class).lower()
                if any(kw in classes_str for kw in VACUUM_KEYWORDS):
                    tag.decompose()
                    stats["vacuum_refs_removed"] += 1
        except Exception:
            continue

    # -- 3. Replace domain references in text --
    html = str(soup)

    domain_replacements = [
        ("www.innovaster-tech.com", "innovaster.cn"),
        ("innovaster-tech.com", "innovaster.cn"),
        ("es.innovaster-tech.com", "innovaster.cn"),
        ("info@innovaster-tech.com", "info@innovaster.cn"),
    ]
    for old, new in domain_replacements:
        html = html.replace(old, new)

    # -- 4. Fix cart/inquiry links --
    html = html.replace('href="index.php?c=cart"', 'href="mailto:info@innovaster.cn?subject=Product%20Inquiry"')
    html = html.replace("href='/index.php?c=cart'", "href='mailto:info@innovaster.cn?subject=Product%20Inquiry'")
    html = html.replace("href=\"/index.php?c=cart\"", "href=\"mailto:info@innovaster.cn?subject=Product%20Inquiry\"")

    # -- 5. Replace form actions --
    html = re.sub(r'action=["\']/index\.php[^"\']*["\']', 'action="mailto:info@innovaster.cn?subject=Contact%20Form"', html)
    html = re.sub(r'action=["\']\?c=cart["\']', 'action="mailto:info@innovaster.cn?subject=Inquiry"', html)

    # -- 6. Remove "Powered by HiCheng" or replace --
    html = html.replace("Powered by HiCheng", "")

    # Write back
    if html != original:
        filepath.write_text(html, encoding='utf-8')
        return True
    return False


def process_all_html():
    """Process all HTML files."""
    print("\n── Processing HTML files... ──")
    html_files = list(OUTPUT_DIR.rglob("*.html"))
    print(f"  Found {len(html_files)} HTML files")

    for filepath in sorted(html_files):
        try:
            changed = process_html_file(filepath)
            if changed:
                stats["modified_files"] += 1
        except Exception:
            rel = filepath.relative_to(OUTPUT_DIR)
            print(f"  ERROR: {rel}")
            traceback.print_exc()

    print(f"  Modified {stats['modified_files']} files")


def process_assets():
    """Process CSS/JS assets to replace domain references."""
    print("\n── Processing assets... ──")
    if not ASSETS_DIR.exists():
        print("  No assets directory")
        return
    for filepath in ASSETS_DIR.rglob("*"):
        if filepath.is_file() and filepath.suffix in ('.css', '.js', '.svg'):
            try:
                content = filepath.read_text(encoding='utf-8')
                new_content = content.replace("innovaster-tech.com", "innovaster.cn")
                if new_content != content:
                    filepath.write_text(new_content, encoding='utf-8')
                    stats["modified_files"] += 1
            except Exception:
                pass


def generate_sitemap():
    """Generate sitemap.xml for innovaster.cn."""
    print("\n── Generating sitemap.xml... ──")
    urls = set()
    for p in sorted(OUTPUT_DIR.rglob("*.html")):
        rel = str(p.relative_to(OUTPUT_DIR))
        # Skip pagination, assets dir, junk
        if any(x in rel for x in ['page2', 'page3', 'page1/', 'assets/', '/229', '/438']):
            continue
        urls.add(f"https://innovaster.cn/{rel}")

    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for url in sorted(urls):
        sitemap += f"  <url><loc>{url}</loc></url>\n"
    sitemap += '</urlset>\n'
    (OUTPUT_DIR / 'sitemap.xml').write_text(sitemap, encoding='utf-8')
    print(f"  {len(urls)} URLs in sitemap")

    robots = "User-agent: *\nAllow: /\nSitemap: https://innovaster.cn/sitemap.xml\n"
    (OUTPUT_DIR / 'robots.txt').write_text(robots, encoding='utf-8')
    print("  robots.txt created")


def main():
    print("=" * 60)
    print("Innovaster Static Site Cleanup")
    print("=" * 60)

    delete_vacuum_content()
    clean_pagination()
    process_all_html()
    process_assets()
    generate_sitemap()

    print("\n" + "=" * 60)
    print("CLEANUP COMPLETE")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    print(f"  Total files in output:")
    for d in sorted(OUTPUT_DIR.rglob("*")):
        if d.is_file():
            print(f"    {d.relative_to(OUTPUT_DIR)}")
    print("=" * 60)


if __name__ == '__main__':
    main()
