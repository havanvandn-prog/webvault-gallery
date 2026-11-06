# -*- coding: utf-8 -*-
import sys
import os
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)
from capture_engine import capture_smart_clean, compress_tri_layer, verify_captured_image

ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

sites = [
    ("apollo_edu_vn", "https://apollo.edu.vn/"),
    ("ila_edu_vn", "https://ila.edu.vn/"),
    ("ktdcgroup_vn", "https://ktdcgroup.vn/"),
    ("res_edu_vn", "https://res.edu.vn/"),
    ("aten_edu_vn", "https://aten.edu.vn/")
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for slug, u in sites:
        print(f"\nProcessing {slug} ({u})...")
        context = browser.new_context(user_agent=ua, viewport={"width": 1440, "height": 900})
        page = context.new_page()
        try:
            page.goto(u, timeout=35000, wait_until="domcontentloaded")
            time.sleep(2.0)
            
            # Modal cleanup
            page.evaluate("""() => {
                const sels = [
                    '#maydoAppointmentModal', '.maydo-modal-backdrop',
                    '#hv3-gate', '.hv3-hero-sticky', '.hv3-journey-sticky',
                    '[class*="modal-backdrop"]', '.modal-backdrop',
                    '[id*="popup"]', '[class*="popup"]'
                ];
                sels.forEach(sel => {
                    document.querySelectorAll(sel).forEach(el => el.remove());
                });
            }""")
            
            raw_png = os.path.join(BASE_DIR, "Anh_Chup_Website", f"{slug}.png")
            capture_smart_clean(page, raw_png, viewport_height=900, scroll_delay=0.25)
            compress_tri_layer(raw_png, slug, os.path.join(BASE_DIR, "Kho_Anh_Webp"))
            full_webp = os.path.join(BASE_DIR, "Kho_Anh_Webp", f"{slug}_full.webp")
            valid, msg = verify_captured_image(full_webp)
            print(f"Result {slug}: {'PASS' if valid else 'FAIL'} - {msg}")
        except Exception as e:
            print(f"Error {slug}: {e}")
        finally:
            context.close()
    browser.close()

print("\nFinished checking 5 candidates!")
