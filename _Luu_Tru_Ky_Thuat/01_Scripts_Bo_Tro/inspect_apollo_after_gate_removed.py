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
    
    # Hide hv3-gate
    page.evaluate("document.querySelector('#hv3-gate')?.remove()")
    page.evaluate("window.scrollTo(0, 1800)")
    page.wait_for_timeout(500)
    
    top_els = page.evaluate("""() => {
        let els = document.elementsFromPoint(720, 450);
        return els.map(e => ({
            tag: e.tagName,
            id: e.id,
            class: e.className,
            pos: window.getComputedStyle(e).position,
            text: e.innerText.slice(0, 40)
        }));
    }""")
    print("Elements at (720, 450) when hv3-gate removed:")
    for el in top_els:
        print(el)
        
    context.close()
    browser.close()
