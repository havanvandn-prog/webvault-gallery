# -*- coding: utf-8 -*-
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(user_agent=ua, viewport={"width": 1440, "height": 900})
    page = context.new_page()
    page.goto("https://res.edu.vn/", timeout=30000, wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    
    res = page.evaluate("""() => {
        let els = document.querySelectorAll('[class*="modal"], [id*="modal"], [class*="popup"], [id*="popup"], [class*="dialog"], [id*="dialog"]');
        return Array.from(els).map(e => ({tag: e.tagName, id: e.id, class: String(e.className), h: e.offsetHeight, w: e.offsetWidth}));
    }""")
    print("Matched elements in res.edu.vn:")
    for item in res:
        print(item)
        
    context.close()
    browser.close()
