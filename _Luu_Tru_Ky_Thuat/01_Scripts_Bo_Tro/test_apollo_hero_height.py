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
    
    hero_h = page.evaluate("document.querySelector('#hv3-hero').offsetHeight")
    sticky_h = page.evaluate("document.querySelector('.hv3-hero-sticky').offsetHeight")
    print(f"Apollo #hv3-hero height: {hero_h}, sticky height: {sticky_h}")
    
    # Test setting height auto and position relative
    page.evaluate("""() => {
        document.documentElement.classList.remove('hv3-gated');
        document.querySelector('#hv3-gate')?.remove();
        let hero = document.querySelector('#hv3-hero');
        if (hero) hero.style.setProperty('height', 'auto', 'important');
        let sticky = document.querySelector('.hv3-hero-sticky');
        if (sticky) {
            sticky.style.setProperty('position', 'relative', 'important');
            sticky.style.setProperty('top', '0px', 'important');
        }
    }""")
    print("After unpinning:")
    print("New hero height:", page.evaluate("document.querySelector('#hv3-hero').offsetHeight"))
    print("Total body scrollHeight:", page.evaluate("document.body.scrollHeight"))
    
    context.close()
    browser.close()
