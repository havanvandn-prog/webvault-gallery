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
    print("Start:", page.evaluate("() => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)"))
    
    # Test super_hydrate parts
    skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
    sys.path.append(skill_path)
    from capture_engine import super_hydrate
    super_hydrate(page)
    print("After super_hydrate:", page.evaluate("() => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)"))
    
    # Test individual elements inside body
    body_children = page.evaluate("""() => {
        return Array.from(document.body.children).map(c => ({tag: c.tagName, id: c.id, class: String(c.className), h: c.offsetHeight, disp: window.getComputedStyle(c).display}));
    }""")
    print("Body children:")
    for c in body_children:
        print(c)
        
    context.close()
    browser.close()
