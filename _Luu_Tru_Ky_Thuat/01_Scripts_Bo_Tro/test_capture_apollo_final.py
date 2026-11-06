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

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(user_agent=ua, viewport={"width": 1440, "height": 900})
    page = context.new_page()
    page.goto("https://apollo.edu.vn/", timeout=35000, wait_until="domcontentloaded")
    page.wait_for_timeout(2500)
    
    # Apollo unpinning and unlock
    page.evaluate("""() => {
        document.documentElement.classList.remove('hv3-gated');
        document.body.classList.remove('hv3-gated');
        document.querySelector('#hv3-gate')?.remove();
        document.querySelector('#maydoAppointmentModal')?.remove();
        document.querySelectorAll('.maydo-modal-backdrop, .hv3-modal-overlay').forEach(el => el.remove());
        
        // Unpin hero pinned scroll
        const hero = document.querySelector('#hv3-hero');
        if (hero) hero.style.setProperty('height', 'auto', 'important');
        const heroSticky = document.querySelector('.hv3-hero-sticky');
        if (heroSticky) {
            heroSticky.style.setProperty('position', 'relative', 'important');
            heroSticky.style.setProperty('top', '0px', 'important');
        }
        
        // Unpin journey pinned scroll
        const journey = document.querySelector('.hv3-journey');
        if (journey) journey.style.setProperty('height', 'auto', 'important');
        const journeySticky = document.querySelector('.hv3-journey-sticky');
        if (journeySticky) {
            journeySticky.style.setProperty('position', 'relative', 'important');
            journeySticky.style.setProperty('top', '0px', 'important');
        }
    }""")
    
    raw_png = os.path.join(BASE_DIR, "Anh_Chup_Website", "apollo_edu_vn.png")
    capture_smart_clean(page, raw_png, viewport_height=900, scroll_delay=0.22)
    compress_tri_layer(raw_png, "apollo_edu_vn", os.path.join(BASE_DIR, "Kho_Anh_Webp"))
    full_webp = os.path.join(BASE_DIR, "Kho_Anh_Webp", "apollo_edu_vn_full.webp")
    valid, msg = verify_captured_image(full_webp)
    print(f"Final Apollo capture audit: {'PASS' if valid else 'FAIL'} - {msg}")
    
    context.close()
    browser.close()
