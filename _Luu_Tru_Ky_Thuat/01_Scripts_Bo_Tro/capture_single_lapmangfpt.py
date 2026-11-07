# -*- coding: utf-8 -*-
import os
import sys
import time
import json

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)
from capture_engine import capture_smart_clean, check_for_blank_spaces, compress_tri_layer, verify_captured_image
from playwright.sync_api import sync_playwright

output_dir = os.path.join(BASE_DIR, "Anh_Chup_Website")
kho_webp_dir = os.path.join(BASE_DIR, "Kho_Anh_Webp")
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "lap_mang_fpt_metadata.json")

item = {
    "id": "fpt17",
    "name": "FPT Telecom Toàn Quốc (Lapmangfpt.vn)",
    "short_name": "Lắp Mạng FPT Official",
    "url": "https://lapmangfpt.vn/",
    "domain": "lapmangfpt.vn",
    "slug": "lapmangfpt_vn",
    "industry": "lap-mang-fpt",
    "industry_name": "Lắp Mạng FPT (Google Ads)",
    "category": "High-Traffic Nationwide Official Partner",
    "category_vn": "Kênh Đăng Ký FPT Telecom Trực Tuyến Toàn Quốc",
    "tag": "pricing-comparison",
    "vibe": "Đầy Đủ Tiện Ích & Bảng Giá Khuyến Mãi 2026",
    "location": "Toàn quốc",
    "desc": "Kênh đăng ký trực tuyến toàn quốc với hàng chục ngàn lượt truy cập mỗi tháng. Bố cục bảng giá WiFi 6/WiFi 7 đối xứng, ưu đãi tặng tháng cước thứ 7, miễn phí modem 2 băng tần và danh mục giải pháp Camera an ninh FPT."
}

filename = f"{item['domain']}.png"
filepath = os.path.join(output_dir, filename)
slug = item["slug"]

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
    )
    context = browser.new_context(
        viewport={"width": 1440, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
    page = context.new_page()
    print(f"Đang chụp thay thế {item['name']} -> {item['url']}...")
    page.goto(item['url'], wait_until="domcontentloaded", timeout=40000)
    time.sleep(3)
    res_info = capture_smart_clean(page, filepath)
    size_mb = os.path.getsize(filepath) / (1024 * 1024)
    print(f"Smart clean hoàn tất: {filename} ({res_info[0]}x{res_info[1]}, {size_mb:.2f} MB)")
    browser.close()

thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb = compress_tri_layer(filepath, slug, kho_webp_dir)
full_path = os.path.join(kho_webp_dir, full_name)
ok, audit_msg = verify_captured_image(full_path)
print(f"Đã nén WebP: Thumb {thumb_kb} KB, Full {full_kb} KB, FB {fb_kb} KB | Audit: {audit_msg}")

new_data = {
    **item,
    "image": f"Anh_Chup_Website/{filename}",
    "thumb": f"Kho_Anh_Webp/{thumb_name}",
    "full": f"Kho_Anh_Webp/{full_name}",
    "fb": f"Kho_Anh_Webp/{fb_name}",
    "thumb_kb": thumb_kb,
    "full_kb": full_kb,
    "fb_kb": fb_kb,
    "size_mb": f"{size_mb:.2f} MB",
    "status": "SUCCESS" if ok else "WARN"
}

with open(metadata_file, "r", encoding="utf-8") as f:
    items = json.load(f)

# Cập nhật vị trí fpt17
for i, it in enumerate(items):
    if it.get("id") == "fpt17":
        items[i] = new_data
        break

with open(metadata_file, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

print("[+] Đã cập nhật xong fpt17 vào lap_mang_fpt_metadata.json!")
