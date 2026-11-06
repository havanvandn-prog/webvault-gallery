# -*- coding: utf-8 -*-
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(user_agent=ua, viewport={"width": 1440, "height": 900})
    page = context.new_page()
    page.goto("https://apollo.edu.vn/", timeout=30000, wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    
    # Check what scroll triggers or sticky containers exist
    info = page.evaluate("""() => {
        let res = [];
        document.querySelectorAll('.hv3-hero-sticky, #hv3-gate, .hv3-journey-sticky').forEach(el => {
            res.push({
                tag: el.tagName,
                id: el.id,
                class: el.className,
                style: el.getAttribute('style') || '',
                computed_pos: window.getComputedStyle(el).position
            });
        });
        return res;
    }""")
    print("Apollo sticky containers:", info)
    
    context.close()
    browser.close()
