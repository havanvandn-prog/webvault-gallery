# -*- coding: utf-8 -*-
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

selectors = [
    '.footer-additional', '.fixed-bottom', '.floating-cta',
    '.hotline-phone-ring', '.quick-call-button', '.zalo-chat-widget',
    '.tt-chat-layer', '[class*="chat-layer"]',
    '[class*="popup"]', '[id*="popup"]',
    '[class*="modal"]', '[id*="modal"]',
    '[class*="dialog"]', '[id*="dialog"]',
    '[class*="lightbox"]', '[id*="lightbox"]',
    '[class*="banner-ads"]', '[class*="adv-popup"]',
    '[class*="popup-drawer"]', '[id*="cookie-notice"]', '[class*="overlay-fixed"]',
    '.ast-mobile-popup-drawer', '.ast-mobile-popup-overlay',
    '#introLux', '.introAgency', '[class*="splash-screen"]', '[class*="preloader-overlay"]',
    '[class*="site-intro"]', '[id*="site-intro"]', '[class*="welcome-overlay"]', '[id*="welcome-overlay"]',
    '#hv3-gate', '.hv3-hero-sticky', '.hv3-journey-sticky', '#maydoAppointmentModal', '.maydo-modal-backdrop',
    '.lead-form-popup', '.dialog-container'
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(user_agent=ua, viewport={"width": 1440, "height": 900})
    page = context.new_page()
    page.goto("https://res.edu.vn/", timeout=30000, wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    
    for sel in selectors:
        count = page.evaluate(f"document.querySelectorAll('{sel}').length")
        if count > 0:
            h_before = page.evaluate("document.querySelector('#wrapper').offsetHeight")
            # add style for this selector
            handle = page.add_style_tag(content=f"{sel} {{ display: none !important; }}")
            h_after = page.evaluate("document.querySelector('#wrapper').offsetHeight")
            print(f"Selector '{sel}' (count={count}): {h_before} -> {h_after}")
            # remove the added style
            page.evaluate("() => { let tags = document.querySelectorAll('style'); tags[tags.length-1].remove(); }")
            
    context.close()
    browser.close()
