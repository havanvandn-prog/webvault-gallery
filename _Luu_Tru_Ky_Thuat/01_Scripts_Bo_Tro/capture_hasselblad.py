# -*- coding: utf-8 -*-
import os
import sys
import time

sys.path.append(r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts")
from playwright.sync_api import sync_playwright
from capture_engine import setup_page_protection, super_hydrate, capture_smart_clean, compress_tri_layer, verify_captured_image

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
anh_chup_dir = os.path.join(BASE_DIR, "Anh_Chup_Website")
kho_webp_dir = os.path.join(BASE_DIR, "Kho_Anh_Webp")
os.makedirs(anh_chup_dir, exist_ok=True)
os.makedirs(kho_webp_dir, exist_ok=True)

url = "https://www.hasselblad.com/"
slug = "hasselblad_com"
raw_png = os.path.join(anh_chup_dir, "hasselblad.com.png")

print(f"[+] Đang khởi chạy Playwright để khảo sát & chụp: {url}")

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--disable-web-security", "--no-sandbox", "--disable-setuid-sandbox"]
    )
    context = browser.new_context(
        viewport={"width": 1440, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        device_scale_factor=1,
    )
    page = context.new_page()
    setup_page_protection(page)

    try:
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
    except Exception as e:
        print(f"[-] Goto warning: {e}")

    time.sleep(3)

    # Đóng banner cookie / consent nếu có
    try:
        cookie_selectors = [
            "#onetrust-accept-btn-handler",
            "button#onetrust-accept-btn-handler",
            "button:has-text('Accept All')",
            "button:has-text('Accept Cookies')",
            "button:has-text('Agree')",
            "button:has-text('I Agree')",
            ".cookie-banner button",
            "[aria-label*='Accept']"
        ]
        for sel in cookie_selectors:
            btn = page.query_selector(sel)
            if btn and btn.is_visible():
                print(f"[+] Tìm thấy cookie button: {sel}, đang bấm...")
                btn.click()
                time.sleep(1)
                break
    except Exception as e:
        print(f"[-] Cookie close error: {e}")

    # Chụp ảnh thông minh
    print("[+] Bắt đầu capture_smart_clean...")
    size = capture_smart_clean(page, raw_png, viewport_height=900, scroll_delay=0.2)
    print(f"[+] Đã chụp xong ảnh gốc: {raw_png} ({size[0]}x{size[1]})")

    browser.close()

# Nén WebP 3 tầng
print("[+] Bắt đầu nén 3 tầng WebP...")
thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb = compress_tri_layer(raw_png, slug, kho_webp_dir)
print(f"[+] Đã nén WebP thành công:")
print(f"    - Full: {full_name} ({full_kb} KB)")
print(f"    - Thumb: {thumb_name} ({thumb_kb} KB)")
print(f"    - FB Card: {fb_name} ({fb_kb} KB)")

# Cổng kiểm định chất lượng ảnh (Post-Capture QA)
full_webp_path = os.path.join(kho_webp_dir, full_name)
is_valid, reason = verify_captured_image(full_webp_path)
print(f"[+] Kết quả kiểm định QA: is_valid={is_valid}, reason={reason}")

if not is_valid:
    print(f"[-] Cảnh báo: Ảnh chưa đạt chuẩn: {reason}")
    sys.exit(1)
else:
    print(f"[SUCCESS] Ảnh hoàn toàn đạt chuẩn 100%!")
