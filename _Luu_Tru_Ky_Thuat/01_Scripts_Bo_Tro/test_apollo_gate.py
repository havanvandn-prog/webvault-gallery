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
    
    # Hide fixed at y=900
    page.evaluate("window.scrollTo(0, 900)")
    page.wait_for_timeout(200)
    disp900 = page.evaluate("window.getComputedStyle(document.querySelector('#hv3-gate')).display")
    print("At y=900 before hide, hv3-gate display:", disp900)
    
    page.evaluate("document.querySelector('#hv3-gate').style.setProperty('display', 'none', 'important')")
    print("At y=900 after hide, hv3-gate display:", page.evaluate("window.getComputedStyle(document.querySelector('#hv3-gate')).display"))
    
    # Now scroll to 1800
    page.evaluate("window.scrollTo(0, 1800)")
    page.wait_for_timeout(200)
    print("At y=1800, hv3-gate display:", page.evaluate("window.getComputedStyle(document.querySelector('#hv3-gate')).display"))
    
    context.close()
    browser.close()
