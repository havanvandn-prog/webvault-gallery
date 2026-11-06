# -*- coding: utf-8 -*-
import os
import sys
import time
sys.path.append(r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts")
from capture_engine import capture_smart_clean, compress_tri_layer, verify_captured_image
from playwright.sync_api import sync_playwright

sites = [
    {
        "domain": "cotdienquan.com",
        "slug": "cotdienquan_com",
        "url": "https://cotdienquan.com/"
    },
    {
        "domain": "taobanhmicafe.com",
        "slug": "taobanhmicafe_com",
        "url": "https://taobanhmicafe.com/"
    },
    {
        "domain": "localbread.vn",
        "slug": "localbread_vn",
        "url": "https://localbread.vn/"
    }
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for s in sites:
        domain = s["domain"]
        slug = s["slug"]
        url = s["url"]
        print(f"Processing {domain}...")
        context = browser.new_context(viewport={"width": 1440, "height": 900}, ignore_https_errors=True)
        page = context.new_page()
        try:
            page.goto(url, timeout=45000, wait_until="networkidle" if "localbread" in url else "domcontentloaded")
            time.sleep(3.5 if "localbread" in url else 1.5)
            raw_png = os.path.join("Anh_Chup_Website", f"{domain}.png")
            capture_smart_clean(page, raw_png, viewport_height=900, scroll_delay=0.20)
            res = compress_tri_layer(raw_png, slug, "Kho_Anh_Webp")
            full_webp = os.path.join("Kho_Anh_Webp", f"{slug}_full.webp")
            valid, msg = verify_captured_image(full_webp)
            print(f"  -> QA {domain}: {'PASS' if valid else 'FAIL'} - {msg}")
        except Exception as e:
            print(f"  [-] Error on {domain}: {e}")
        finally:
            context.close()
    browser.close()

print("[+] Done capturing remaining 3 sites!")
