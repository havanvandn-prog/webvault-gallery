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

    # 1. Test normal load
    base_url = f"file:///{os.path.join(BASE_DIR, 'index.html').replace(os.sep, '/')}"
    page.goto(base_url)
    page.wait_for_selector(".website-card")
    total = page.evaluate("() => document.querySelectorAll('.website-card').length")
    heading = page.evaluate("() => document.getElementById('viewHeading').textContent")
    print(f"[TEST 1] Normal Load -> Cards: {total}, Heading: '{heading}'")
    assert total == 43, f"Expected 43, got {total}"

    # 2. Test deep link ?industry=decor-su-kien
    decor_url = f"{base_url}?industry=decor-su-kien"
    page.goto(decor_url)
    page.wait_for_selector(".website-card")
    decor_count = page.evaluate("() => document.querySelectorAll('.website-card').length")
    decor_heading = page.evaluate("() => document.getElementById('viewHeading').textContent")
    active_nav_text = page.evaluate("() => document.querySelector('.nav-item.active span').textContent")
    print(f"[TEST 2] Deep Link ?industry=decor-su-kien -> Cards: {decor_count}, Heading: '{decor_heading}', Active Nav: '{active_nav_text}'")
    assert decor_count == 20, f"Expected 20, got {decor_count}"
    assert "Trang Trí & Decor Tiệc" in decor_heading
    assert "Trang Trí & Decor Tiệc" in active_nav_text

    # 3. Test clicking industry dynamically
    page.evaluate("() => setIndustry('du-lich', document.querySelectorAll('.nav-item')[3])")
    travel_count = page.evaluate("() => document.querySelectorAll('.website-card').length")
    travel_heading = page.evaluate("() => document.getElementById('viewHeading').textContent")
    print(f"[TEST 3] Dynamic Click Du Lich -> Cards: {travel_count}, Heading: '{travel_heading}'")
    assert travel_count == 3, f"Expected 3, got {travel_count}"

    browser.close()

print("\n[ALL TESTS PASSED] Tích hợp Single Hub và Deep Linking hoạt động hoàn hảo 100%!")
