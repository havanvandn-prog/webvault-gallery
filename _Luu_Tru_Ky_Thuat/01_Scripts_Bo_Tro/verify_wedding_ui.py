import os
import sys
import time
from playwright.sync_api import sync_playwright

html_file = os.path.abspath("preview_mau_website_wedding.html")
screenshot_out = r"_Luu_Tru_Ky_Thuat\02_Screenshots_Debug_Va_Khao_Sat\test_wedding_preview_desktop.png"
os.makedirs(os.path.dirname(screenshot_out), exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    
    # Catch any console errors
    errors = []
    page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
    
    page.goto(f"file:///{html_file.replace(os.sep, '/')}", wait_until="load")
    time.sleep(1)
    
    card_count = page.evaluate("() => document.querySelectorAll('.website-card').length")
    print(f"Loaded cards: {card_count}")
    
    page.screenshot(path=screenshot_out, full_page=False)
    print(f"Captured preview UI to: {screenshot_out}")
    
    if errors:
        print("Console errors found:", errors)
    else:
        print("Zero console errors! Page rendered cleanly.")
        
    browser.close()
