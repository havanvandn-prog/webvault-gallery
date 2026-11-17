# -*- coding: utf-8 -*-
import os, sys, time, json

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)

from capture_engine import setup_page_protection, capture_smart_clean, compress_tri_layer, verify_captured_image
from playwright.sync_api import sync_playwright

output_dir = os.path.join(BASE_DIR, "Anh_Chup_Website")
kho_webp_dir = os.path.join(BASE_DIR, "Kho_Anh_Webp")

backups = [
    {"slug": "noi_that_baya", "url": "https://baya.vn/", "domain": "baya.vn"},
    {"slug": "noi_that_dergo", "url": "https://dergo.vn/", "domain": "dergo.vn"},
    {"slug": "noi_that_molteni", "url": "https://www.molteni.it/en/", "domain": "molteni.it"},
    {"slug": "noi_that_hay", "url": "https://www.hay.com/", "domain": "hay.com"},
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for b in backups:
        print(f"\nTesting {b['domain']} ({b['url']})...")
        raw_png = os.path.join(output_dir, f"{b['slug']}.png")
        full_webp = os.path.join(kho_webp_dir, f"{b['slug']}_full.webp")
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            ignore_https_errors=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        setup_page_protection(page)
        try:
            page.goto(b['url'], timeout=45000, wait_until="domcontentloaded")
            time.sleep(3.0)
            page.evaluate("""() => {
                ['button[aria-label*="Close" i]', 'button[aria-label*="accept" i]', '.onetrust-close-btn-handler', '#onetrust-accept-btn-handler', '.cookie-accept', '.btn-close-popup', '.popup-close', '.close-modal', '#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll'].forEach(sel => {
                    document.querySelectorAll(sel).forEach(btn => { try { btn.click(); } catch(e) {} });
                });
            }""")
            time.sleep(0.5)
            capture_smart_clean(page, raw_png, viewport_height=900, scroll_delay=0.25)
            thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb = compress_tri_layer(raw_png, b['slug'], kho_webp_dir)
            valid, msg = verify_captured_image(full_webp)
            print(f"  -> {b['domain']}: {'PASS' if valid else 'FAIL'} | {msg} | thumb={thumb_kb}KB, full={full_kb}KB, fb={fb_kb}KB")
        except Exception as e:
            print(f"  -> {b['domain']}: ERROR - {e}")
        finally:
            context.close()
    browser.close()
