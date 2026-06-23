#!/usr/bin/env python3
"""Add data-i18n attributes to homepage HTML elements."""
import re
from pathlib import Path
from bs4 import BeautifulSoup

BASE = Path('/Users/kensui/innovaster-static')

# Mapping of text content → i18n key for the homepage
# These are exact or partial matches
TEXT_TO_KEY = {
    # Navigation
    "Retorts/Autoclaves": "nav.retorts",
    "Water Spray Retorts": "nav.water_spray",
    "Water Immersion Retorts": "nav.water_immersion",
    "Steam Retorts": "nav.steam",
    "Steam-Air Retorts": "nav.steam_air",
    "Rotary Retorts": "nav.rotary",
    "Water Cascade Retorts": "nav.water_cascade",
    "Pilot Retorts": "nav.pilot",
    "Retort Accessories": "nav.accessories",
    "Shuttle And Loading/Unloading Machine ": "nav.shuttle",
    "Semi Automatic Loader Unloader  ": "nav.semi_auto",
    "Retort Shuttle": "nav.shuttle_rgv",
    "Full Automatic Loader Unloader": "nav.full_auto",
    "Solutions": "nav.solutions",
    "Service": "nav.service",
    "Blog": "nav.news",
    "Contact Us": "nav.contact",
    "About Us": "nav.about_us",
    "Who We Are": "nav.who_we_are",
    "Missions & Values": "nav.missions",
    "Production Facilities": "nav.facilities",
    "What We Do": "nav.what_we_do",
    "New Products": "nav.product_new",
    "Success Stories": "nav.success",
    "Services": "nav.services_menu",
    "Thermal Validation": "nav.thermal_validation",
    "Training & Technical Support": "nav.training",
    "Spare Parts": "nav.spare_parts",

    # Product Categories
    "Product Categories": "pc.title",

    # Solutions
    "Find The Solution You Need": "solutions.title",
    "READY TO EAT/DRINK": "solutions.ready_eat",
    "CANNED FISH SOLUTIONS": "solutions.canned_fish",
    "CANNED MEAT": "solutions.canned_meat",
    "PET FOOD": "solutions.pet_food",
    "BABY FOOD": "solutions.baby_food",
    "CANNED VEGETABLES": "solutions.canned_veg",

    # About
    "Profile": "about.profile",
    "About Innovaster": "about.title",
    "Read more": "about.readmore",

    # Customer Case
    "Customer Case": "case.title",

    # Why Choose Us
    "Why Choose Us": "why.title",
    "Design And Construction": "why.design_title",
    "Innovaster Certifications": "why.cert_title",
    "Safety": "why.safety_title",
    "Training & Customer Care Service": "why.training_title",
    "Technical Support": "why.tech_title",
    "Delivery On Time": "why.delivery_title",

    # FAQ
    "FAQ": "faq.title",

    # Blog
    "Insights & News": "blog.title",

    # Newsletter
    "Subscribe to Our Newsletter": "newsletter.title",
    "Enter Your Email Here...": "newsletter.placeholder",
    "SUBMIT": "newsletter.submit",

    # Search
    "START TYPING AND PRESS ENTER TO SEARCH": "search.prompt",

    # Footer
    "Products": "footer.products",
    "Quick Links": "footer.quick_links",
    "CONTACT US": "footer.contact_us",
    "Online Message": "footer.message",
    "Subscribe": "footer.subscribe",
    "Copyrights © 2018 InnovaSter. All rights reserved.": "footer.copyright",
    "In-Container Sterilization Solutions": "footer.tagline",

    # Mobile nav
    "Home": "common.home",
    "Contact": "common.contact",
}


def apply_to_homepage():
    path = BASE / 'index.html'
    html = path.read_text()
    soup = BeautifulSoup(html, 'lxml')

    applied = 0

    # Find text elements and match against TEXT_TO_KEY
    for tag in soup.find_all(['a', 'b', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'span', 'button', 'div']):
        text = tag.get_text(strip=True)
        if not text or len(text) < 2:
            continue

        # Check exact match
        if text in TEXT_TO_KEY:
            key = TEXT_TO_KEY[text]
            if not tag.get('data-i18n'):
                tag['data-i18n'] = key
                applied += 1
                continue

    # Also match long descriptions (use first 30 chars to match)
    long_texts = {
        "Innovaster has been dedicated to retorts manufacturing and process optimization": "why.design_desc",
        "Innovaster guarantees quality products in accordance": "why.cert_desc",
        "To us, safety is quality.": "why.safety_desc",
        "We provide training in our factory and at customers' site": "why.training_desc",
        "Technical assistance on installation and site commissioning": "why.tech_desc",
        "Innovaster products are designed, built, and tested": "why.delivery_desc",
    }

    for tag in soup.find_all(['p', 'div']):
        text = tag.get_text(strip=True)
        for prefix, key in long_texts.items():
            if text.startswith(prefix) and not tag.get('data-i18n'):
                tag['data-i18n'] = key
                applied += 1
                break

    path.write_text(str(soup), encoding='utf-8')
    print(f'Applied {applied} data-i18n attributes to homepage')

    # Also add data-i18n to common elements on ALL pages (nav, footer)
    apply_to_all_pages()


def apply_to_all_pages():
    """Add data-i18n to common elements across all pages."""
    common_keys = {
        "Retorts/Autoclaves": "nav.retorts",
        "Shuttle And Loading/Unloading Machine ": "nav.shuttle",
        "About Us": "nav.about_us",
        "Who We Are": "nav.who_we_are",
        "Missions & Values": "nav.missions",
        "Production Facilities": "nav.facilities",
        "What We Do": "nav.what_we_do",
        "Solutions": "nav.solutions",
        "Service": "nav.service",
        "Blog": "nav.news",
        "Contact Us": "nav.contact",
        "New Products": "nav.product_new",
        "Success Stories": "nav.success",
        "Products": "footer.products",
        "Quick Links": "footer.quick_links",
    }

    count = 0
    for fp in BASE.rglob('*.html'):
        if 'assets' in str(fp) or fp.name == 'index.html':
            continue
        try:
            html = fp.read_text()
        except:
            continue
        soup = BeautifulSoup(html, 'lxml')
        changed = False
        for tag in soup.find_all(['a', 'b', 'h1', 'h2', 'h3', 'p', 'span']):
            text = tag.get_text(strip=True)
            if text in common_keys and not tag.get('data-i18n'):
                tag['data-i18n'] = common_keys[text]
                changed = True

        if changed:
            fp.write_text(str(soup), encoding='utf-8')
            count += 1

    print(f'Applied common i18n to {count} other pages')


if __name__ == '__main__':
    apply_to_homepage()
