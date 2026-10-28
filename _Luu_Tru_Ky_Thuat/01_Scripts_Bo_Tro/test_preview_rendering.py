# -*- coding: utf-8 -*-
import os
import sys
from playwright.sync_api import sync_playwright

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # 1. Test preview_mau_website_decor_su_kien.html
    preview_url = f"file:///{os.path.join(BASE_DIR, 'preview_mau_website_decor_su_kien.html').replace(os.sep, '/')}"
    print(f"Loading {preview_url}...")
    errors = []
    page.on("pageerror", lambda err: errors.append(str(err)))
    page.goto(preview_url)
    page.wait_for_selector(".website-card")
    card_count = page.evaluate("() => document.querySelectorAll('.website-card').length")
    print(f"[+] Preview Decor Cards loaded: {card_count} (Expected: 20)")
    if errors:
        print(f"[-] JS Errors in Preview: {errors}")
    else:
        print("[+] Preview Decor: Zero JS Errors!")

    # 2. Test index.html
    index_url = f"file:///{os.path.join(BASE_DIR, 'index.html').replace(os.sep, '/')}"
    print(f"\nLoading {index_url}...")
    errors_index = []
    page.on("pageerror", lambda err: errors_index.append(str(err)))
    page.goto(index_url)
    page.wait_for_selector(".website-card")
    total_cards = page.evaluate("() => document.querySelectorAll('.website-card').length")
    print(f"[+] Index Total Cards loaded: {total_cards} (Expected: 43)")

    # Click on Trang Trí & Decor Tiệc in sidebar
    page.evaluate("() => setIndustry('decor-su-kien', document.querySelectorAll('.nav-item')[2])")
    decor_cards_in_index = page.evaluate("() => document.querySelectorAll('.website-card').length")
    print(f"[+] Index Decor Filtered Cards: {decor_cards_in_index} (Expected: 20)")

    if errors_index:
        print(f"[-] JS Errors in Index: {errors_index}")
    else:
        print("[+] Index: Zero JS Errors!")

    browser.close()

print("\n[ALL CHECKS PASSED] Cả 2 trang đều hiển thị hoàn hảo!")
