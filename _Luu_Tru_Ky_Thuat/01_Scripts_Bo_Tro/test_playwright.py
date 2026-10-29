import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

urls = [
    "https://donghohaitrieu.com/",
    "https://curnonwatch.com/",
    "https://giabaoluxury.com/",
    "https://galle.vn/"
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    for u in urls:
        try:
            resp = page.goto(u, timeout=15000, wait_until="domcontentloaded")
            print(f"[PLAYWRIGHT] {u} -> Status: {resp.status}, Title: {page.title()[:40]}")
        except Exception as e:
            print(f"[PLAYWRIGHT FAIL] {u} -> {e}")
    browser.close()
