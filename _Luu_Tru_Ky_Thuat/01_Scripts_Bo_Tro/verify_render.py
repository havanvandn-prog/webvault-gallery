# -*- coding: utf-8 -*-
import os, sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

index_file = "file:///" + os.path.join(BASE_DIR, "index.html").replace("\\", "/")
staging_file = "file:///" + os.path.join(BASE_DIR, "web_nhap_staging.html").replace("\\", "/")

errors = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    # 1. Test index.html
    page = browser.new_page()
    page.on("pageerror", lambda err: errors.append(f"[index.html JS Error] {err}"))
    page.goto(index_file + "?industry=ban-may-anh", wait_until="load")
    page.wait_for_timeout(1000)
    
    cards = page.query_selector_all(".website-card")
    print(f"[index.html] URL: {page.url}")
    print(f"[index.html] Thẻ hiển thị khi lọc ban-may-anh: {len(cards)}")
    hassel_el = page.query_selector("text=Hasselblad")
    print(f"[index.html] Tìm thấy Hasselblad: {hassel_el is not None}")

    # 2. Test web_nhap_staging.html
    page2 = browser.new_page()
    page2.on("pageerror", lambda err: errors.append(f"[web_nhap_staging.html JS Error] {err}"))
    page2.goto(staging_file + "?industry=ban-may-anh", wait_until="load")
    page2.wait_for_timeout(1000)
    
    staging_cards = page2.query_selector_all(".staging-card")
    print(f"[staging] URL: {page2.url}")
    print(f"[staging] Thẻ hiển thị khi lọc ban-may-anh: {len(staging_cards)}")
    hassel_el2 = page2.query_selector("text=Hasselblad")
    print(f"[staging] Tìm thấy Hasselblad: {hassel_el2 is not None}")

    browser.close()

if errors:
    print("[-] Cảnh báo lỗi JavaScript:")
    for e in errors:
        print("   ", e)
    sys.exit(1)
else:
    print("[SUCCESS] Hoàn toàn không có lỗi JavaScript trên cả 2 trang!")
