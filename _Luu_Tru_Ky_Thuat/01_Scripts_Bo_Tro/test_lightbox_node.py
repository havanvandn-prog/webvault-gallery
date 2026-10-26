from playwright.sync_api import sync_playwright
import os, time

html_file = os.path.abspath('preview_mau_website_wedding.html').replace('\\', '/')
screenshot_lb = '_Luu_Tru_Ky_Thuat/02_Screenshots_Debug_Va_Khao_Sat/test_wedding_lightbox.png'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('file:///' + html_file, wait_until='load')
    time.sleep(1)
    
    page.click('.card-thumbnail-wrapper')
    time.sleep(0.5)
    
    is_active = page.evaluate("() => document.getElementById('lightboxModal').classList.contains('active')")
    title = page.evaluate("() => document.getElementById('lightboxTitle').innerText")
    img_src = page.evaluate("() => document.getElementById('lightboxImg').src")
    print('Lightbox active:', is_active)
    print('Lightbox title:', title)
    print('Lightbox img src:', img_src)
    
    page.screenshot(path=screenshot_lb)
    print('Captured lightbox to:', screenshot_lb)
    browser.close()
