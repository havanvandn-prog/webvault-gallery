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
    
    # Remove hv3-gated
    page.evaluate("""() => {
        document.documentElement.classList.remove('hv3-gated');
        document.body.classList.remove('hv3-gated');
    }""")
    
    main_vis = page.evaluate("window.getComputedStyle(document.querySelector('main.main')).visibility")
    print("main.main visibility after removing hv3-gated:", main_vis)
    print("Body scroll height after removing hv3-gated:", page.evaluate("document.body.scrollHeight"))
    
    context.close()
    browser.close()
