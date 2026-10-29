import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

test_urls = [
    "https://www.dangquangwatch.vn/",
    "https://donghothanhphat.vn/",
    "https://topwatch.vn/",
    "https://frostofthecapital.com/",
    "https://frostofficial.com/",
    "https://www.thehourglass.com/"
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    for u in test_urls:
        try:
            resp = page.goto(u, timeout=15000, wait_until="domcontentloaded")
            print(f"[STATUS {resp.status}] {u} -> Title: {page.title()}")
        except Exception as e:
            print(f"[FAIL] {u} -> {e}")
    browser.close()
