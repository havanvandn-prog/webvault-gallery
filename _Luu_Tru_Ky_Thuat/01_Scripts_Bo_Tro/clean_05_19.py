import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
import time
from playwright.sync_api import sync_playwright
from test_precision_sticky import capture_smart_clean

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    context = b.new_context(viewport={"width": 1440, "height": 900})
    
    print("Capturing 19_Thang_Long_Event...")
    page = context.new_page()
    page.goto("https://thanglongevent.com/", wait_until="domcontentloaded", timeout=35000)
    time.sleep(2)
    capture_smart_clean(page, "Anh_Chup_Website/19_Thang_Long_Event.png")
    page.close()
    
    print("Capturing 05_Zeit_Media...")
    page = context.new_page()
    page.goto("https://zeitmedia.vn/", wait_until="domcontentloaded", timeout=35000)
    time.sleep(2)
    capture_smart_clean(page, "Anh_Chup_Website/05_Zeit_Media.png")
    page.close()
    
    b.close()
    print("Done cleaning 05 and 19!")
