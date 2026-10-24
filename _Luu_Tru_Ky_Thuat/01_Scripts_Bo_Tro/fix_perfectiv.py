import os
import sys
import time
from io import BytesIO
from PIL import Image

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Import from capture_all_into_folder
from capture_all_into_folder import capture_smart_clean

from playwright.sync_api import sync_playwright

output_path = r"D:\AI Agent\Website\Tìm mẫu website\Anh_Chup_Website\02_Per_fectiv.png"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    ctx = b.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    print("Navigating to Per-fectiv...")
    page.goto("https://per-fectiv.com/", wait_until="domcontentloaded", timeout=45000)
    print("Waiting 4s for GSAP/React preloader to finish and DOM to expand...")
    time.sleep(4)
    h = page.evaluate("() => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
    print(f"Verified height before capture: {h}px")
    w, h_final = capture_smart_clean(page, output_path)
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"Successfully captured Per-fectiv: {w}x{h_final} px ({size_mb:.2f} MB)")
    ctx.close()
    b.close()
