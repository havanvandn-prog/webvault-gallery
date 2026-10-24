import os
import sys
import time
from io import BytesIO
from PIL import Image

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)
from capture_engine import capture_smart_clean

from playwright.sync_api import sync_playwright

output_path = r"D:\AI Agent\Website\Tìm mẫu website\Anh_Chup_Website\05_Zeit_Media.png"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    ctx = b.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()
    print("Navigating to Zeit Media...")
    page.goto("https://zeitmedia.vn/", wait_until="domcontentloaded", timeout=45000)
    time.sleep(3)
    w, h = capture_smart_clean(page, output_path)
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"Successfully captured Zeit Media: {w}x{h} px ({size_mb:.2f} MB)")
    ctx.close()
    b.close()
