# -*- coding: utf-8 -*-
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

for target_url, slug in [("https://res.edu.vn/", "res"), ("https://aten.edu.vn/", "aten"), ("https://apollo.edu.vn/", "apollo")]:
    print(f"\n--- Checking fixed elements on {slug} ({target_url}) ---")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=ua, viewport={"width": 1440, "height": 900})
        page = context.new_page()
        page.goto(target_url, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_timeout(2000)
        
        info = page.evaluate("""() => {
            let res = [];
            document.querySelectorAll('*').forEach(el => {
                const s = window.getComputedStyle(el);
                if (s.position === 'fixed' || s.position === 'sticky') {
                    const r = el.getBoundingClientRect();
                    res.push({
                        tag: el.tagName,
                        id: el.id,
                        class: String(el.className).slice(0, 50),
                        pos: s.position,
                        zIndex: s.zIndex,
                        w: Math.round(r.width),
                        h: Math.round(r.height),
                        top: Math.round(r.top),
                        bottom: Math.round(r.bottom)
                    });
                }
            });
            return res;
        }""")
        for item in info:
            print(item)
        context.close()
        browser.close()
