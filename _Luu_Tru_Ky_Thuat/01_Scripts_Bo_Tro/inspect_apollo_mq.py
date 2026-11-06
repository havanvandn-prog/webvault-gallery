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
    
    mq_info = page.evaluate("""() => {
        let el = document.querySelector('.mq2-card-right') || document.querySelector('[class*="mq"]');
        let res = [];
        let curr = el;
        while (curr && curr !== document.body) {
            let s = window.getComputedStyle(curr);
            res.push({
                tag: curr.tagName,
                id: curr.id,
                class: curr.className,
                pos: s.position,
                h: curr.offsetHeight,
                top: curr.getBoundingClientRect().top
            });
            curr = curr.parentElement;
        }
        return res;
    }""")
    for item in mq_info:
        print(item)
    context.close()
    browser.close()
