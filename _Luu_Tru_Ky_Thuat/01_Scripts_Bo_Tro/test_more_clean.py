import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
import time
from playwright.sync_api import sync_playwright
from test_smart_sticky import capture_smart_clean

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page(viewport={"width": 1440, "height": 900})
    
    print("Testing Zeit Media clean capture...")
    page.goto("https://zeitmedia.vn/", wait_until="domcontentloaded", timeout=35000)
    time.sleep(2)
    capture_smart_clean(page, "Anh_Chup_Website/05_Zeit_Media_clean.png")
    
    print("\nTesting Thang Long Event clean capture...")
    page.goto("https://thanglongevent.com/", wait_until="domcontentloaded", timeout=35000)
    time.sleep(2)
    capture_smart_clean(page, "Anh_Chup_Website/19_Thang_Long_Event_clean.png")
    
    b.close()
