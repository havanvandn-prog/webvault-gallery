# -*- coding: utf-8 -*-
import os
import sys
import time
from io import BytesIO
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)
from capture_engine import capture_smart_clean, compress_tri_layer, verify_captured_image
from playwright.sync_api import sync_playwright

ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

test_sites = [
    ("ila_edu_vn", "https://ila.edu.vn/"),
    ("apollo_edu_vn", "https://apollo.edu.vn/"),
    ("dolenglish_vn", "https://www.dolenglish.vn/"),
    ("res_edu_vn", "https://res.edu.vn/"),
    ("ktdcgroup_vn", "https://ktdcgroup.vn/"),
    ("aten_edu_vn", "https://aten.edu.vn/")
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    for slug, url in test_sites:
        print(f"\n--- Testing fix for: {slug} ({url}) ---")
        context = browser.new_context(user_agent=ua, viewport={"width": 1440, "height": 900})
        page = context.new_page()
        
        try:
            page.goto(url, timeout=40000, wait_until="domcontentloaded")
            time.sleep(2.5)
            
            # Custom DOM cleanup for known pesky modals
            page.evaluate("""() => {
                const selectors = [
                    '#maydoAppointmentModal', '.maydo-modal-backdrop',
                    '#hv3-gate', '.hv3-hero-sticky', '.hv3-journey-sticky',
                    '[class*="modal-backdrop"]', '.modal-backdrop',
                    '[id*="popup-banner"]', '[class*="popup-banner"]',
                    '.lead-form-popup', '.dialog-container'
                ];
                selectors.forEach(sel => {
                    document.querySelectorAll(sel).forEach(el => el.remove());
                });
            }""")
            
            raw_png = os.path.join(BASE_DIR, "Anh_Chup_Website", f"{slug}.png")
            capture_smart_clean(page, raw_png, viewport_height=900, scroll_delay=0.25)
            
            if os.path.exists(raw_png) and os.path.getsize(raw_png) > 0:
                compress_tri_layer(raw_png, slug, os.path.join(BASE_DIR, "Kho_Anh_Webp"))
                full_webp = os.path.join(BASE_DIR, "Kho_Anh_Webp", f"{slug}_full.webp")
                valid, msg = verify_captured_image(full_webp)
                print(f"Result for {slug}: {'PASS' if valid else 'FAIL'} - {msg}")
            else:
                print(f"Failed to capture raw png for {slug}")
        except Exception as e:
            print(f"Error on {slug}: {e}")
        finally:
            context.close()
            
    browser.close()
