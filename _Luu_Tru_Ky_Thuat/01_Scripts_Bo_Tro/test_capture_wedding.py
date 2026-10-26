import os
import sys
import time

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)
from capture_engine import capture_smart_clean, check_for_blank_spaces
from playwright.sync_api import sync_playwright

output_dir = "Anh_Chup_Website"
os.makedirs(output_dir, exist_ok=True)

test_sites = [
    {"name": "The Planners", "domain": "theplannersvn.com", "url": "https://theplannersvn.com/"},
    {"name": "GEM Center", "domain": "gemcenter.com.vn", "url": "https://gemcenter.com.vn/"}
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"])
    context = browser.new_context(
        viewport={"width": 1440, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
    page = context.new_page()

    for item in test_sites:
        filename = f"{item['domain']}.png"
        filepath = os.path.join(output_dir, filename)
        print(f"Testing capture for {item['name']} ({item['url']})...", flush=True)
        try:
            page.goto(item['url'], wait_until="domcontentloaded", timeout=45000)
            time.sleep(2)
            size = capture_smart_clean(page, filepath)
            is_blank, reason = check_for_blank_spaces(filepath)
            filesize_mb = os.path.getsize(filepath) / (1024 * 1024)
            print(f"  -> SUCCESS: {filename} | Res: {size[0]}x{size[1]} | Size: {filesize_mb:.2f} MB | Blank check: {reason}", flush=True)
        except Exception as e:
            print(f"  -> ERROR: {e}", flush=True)

    browser.close()
