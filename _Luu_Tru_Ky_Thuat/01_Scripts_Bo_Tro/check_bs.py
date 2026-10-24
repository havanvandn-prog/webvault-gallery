import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto("https://bsgroup.com.vn/", wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(3000)
    print("Page Title:", page.title())
    text = page.inner_text("body")
    print("Body text snippet:\n", text[:300])
    # check if there's any loading overlay
    elements = page.query_selector_all("div")
    print(f"Total div elements: {len(elements)}")
    page.screenshot(path="Anh_Chup_Website/04_BS_Group_debug.png", full_page=True)
    browser.close()
