import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    ctx = b.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    print("Navigating to Per-fectiv...")
    page.goto("https://per-fectiv.com/", wait_until="domcontentloaded", timeout=40000)
    time.sleep(3)
    print("Taking test viewport screenshot...")
    page.screenshot(path="_Luu_Tru_Ky_Thuat/03_Du_Lieu_Tam_Va_Test/perfectiv_test.png", timeout=10000)
    print("Screenshot success!")
    ctx.close()
    b.close()
