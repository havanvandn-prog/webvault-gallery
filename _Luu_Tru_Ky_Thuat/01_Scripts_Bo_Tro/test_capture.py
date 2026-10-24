import os
import sys
import time
from playwright.sync_api import sync_playwright

output_dir = "Anh_Chup_Website"
os.makedirs(output_dir, exist_ok=True)

test_sites = [
    {"id": "01", "name": "Square Experiential", "url": "https://square-vn.com/"},
    {"id": "02", "name": "Per-fectiv", "url": "https://per-fectiv.com/"},
    {"id": "03", "name": "Le Bros", "url": "https://lebros.vn/"}
]

def auto_scroll(page):
    try:
        # Scroll down in increments to trigger lazy-load
        viewport_height = page.viewport_size['height'] if page.viewport_size else 900
        total_height = page.evaluate("() => document.body.scrollHeight")
        current_scroll = 0
        while current_scroll < min(total_height, 15000):
            current_scroll += 800
            page.evaluate(f"window.scrollTo(0, {current_scroll});")
            time.sleep(0.2)
        # Scroll back to top
        page.evaluate("window.scrollTo(0, 0);")
        time.sleep(0.5)
    except Exception as e:
        print(f"Scroll warning: {e}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox"])
    context = browser.new_context(
        viewport={"width": 1440, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    page = context.new_page()

    for item in test_sites:
        filename = f"{item['id']}_{item['name'].replace(' ', '_')}.png"
        filepath = os.path.join(output_dir, filename)
        print(f"Navigating to {item['name']}: {item['url']}...")
        try:
            page.goto(item['url'], wait_until="domcontentloaded", timeout=30000)
            time.sleep(2)
            auto_scroll(page)
            page.screenshot(path=filepath, full_page=True)
            size_kb = os.path.getsize(filepath) / 1024
            print(f"SUCCESS: {filepath} ({size_kb:.1f} KB)")
        except Exception as e:
            print(f"ERROR capturing {item['name']}: {e}")

    browser.close()
