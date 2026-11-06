# -*- coding: utf-8 -*-
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)
from capture_engine import capture_smart_clean, compress_tri_layer, verify_captured_image

ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(user_agent=ua, viewport={"width": 1440, "height": 900})
    page = context.new_page()
    page.goto("https://apollo.edu.vn/", timeout=35000, wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    
    # Unpin sticky hero & remove fixed gate on Apollo
    page.evaluate("""() => {
        document.querySelectorAll('#hv3-gate, #maydoAppointmentModal, .maydo-modal-backdrop').forEach(el => el.remove());
        document.querySelectorAll('.hv3-hero-sticky, .hv3-journey-sticky').forEach(el => {
            el.style.setProperty('position', 'relative', 'important');
            el.style.setProperty('top', 'auto', 'important');
        });
    }""")
    
    raw_png = "Anh_Chup_Website/apollo_edu_vn.png"
    capture_smart_clean(page, raw_png, viewport_height=900, scroll_delay=0.25)
    compress_tri_layer(raw_png, "apollo_edu_vn", "Kho_Anh_Webp")
    valid, msg = verify_captured_image("Kho_Anh_Webp/apollo_edu_vn_full.webp")
    print(f"Apollo test result: {valid} - {msg}")
    
    context.close()
    browser.close()
