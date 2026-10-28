# -*- coding: utf-8 -*-
import os
import sys
import time
import json
from io import BytesIO
from PIL import Image

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)
from capture_engine import capture_smart_clean, check_for_blank_spaces
from playwright.sync_api import sync_playwright

output_dir = os.path.join(BASE_DIR, "Anh_Chup_Website")
kho_webp_dir = os.path.join(BASE_DIR, "Kho_Anh_Webp")
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "decor_metadata.json")

item = {
    "id": "dc16",
    "name": "D2 Events Đà Nẵng — Tổ Chức & Decor Sự Kiện",
    "short_name": "D2 Events",
    "url": "https://d2events.com/",
    "domain": "d2events.com",
    "slug": "d2events_com",
    "industry": "decor-su-kien",
    "category": "Balloon & Backdrop Styling",
    "category_vn": "Decor Sự Kiện & Tiệc Gala Miền Trung",
    "tag": "balloon-backdrop",
    "vibe": "corporate",
    "vibe_name": "Chuyên nghiệp & Uy tín",
    "location": "Đà Nẵng & Miền Trung",
    "desc": "Công ty tổ chức và decor sự kiện chuyên nghiệp tại Đà Nẵng. Cung cấp trọn gói backdrop chụp hình, sân khấu gala dinner, decor tiệc tất niên và trang trí thôi nôi sinh nhật uy tín."
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
    print(f"Đang chụp {item['name']} -> {item['url']}...")
    try:
        page.goto(item['url'], wait_until="domcontentloaded", timeout=35000)
        time.sleep(2)
        res_info = capture_smart_clean(page, filepath)
        is_blank, reason = check_for_blank_spaces(filepath)
        size_mb = os.path.getsize(filepath) / (1024 * 1024)
        print(f"Smart clean thành công: {res_info[0]}x{res_info[1]}, {size_mb:.2f} MB, Blank: {reason}")
    except Exception as e:
        print(f"Fallback fullpage: {e}")
        page.goto(item['url'], wait_until="load", timeout=30000)
        time.sleep(2)
        page.screenshot(path=filepath, full_page=True)
    browser.close()

# Tri-layer compress
thumb_name = f"{slug}_thumb.webp"
full_name = f"{slug}_full.webp"
fb_name = f"{slug}_fb.png"
thumb_path = os.path.join(kho_webp_dir, thumb_name)
full_path = os.path.join(kho_webp_dir, full_name)
fb_path = os.path.join(kho_webp_dir, fb_name)

with Image.open(filepath) as im:
    im_rgb = im.convert("RGB")
    w, h = im_rgb.size
    if h > 15500:
        scale = 15500.0 / h
        new_w = int(w * scale)
        im_full = im_rgb.resize((new_w, 15500), Image.Resampling.LANCZOS)
    else:
        im_full = im_rgb
    im_full.save(full_path, "WEBP", quality=80, method=4)

    new_w = 600
    new_h = int(h * (new_w / w))
    if new_h > 15500:
        new_h = 15500
    im_thumb = im_rgb.resize((new_w, new_h), Image.Resampling.LANCZOS)
    im_thumb.save(thumb_path, "WEBP", quality=75, method=4)

    slice_h = min(h, int(w * 16 / 9))
    crop = im_rgb.crop((0, 0, w, slice_h))
    im_fb = crop.resize((1080, 1920), Image.Resampling.LANCZOS)
    im_fb.save(fb_path, format="PNG", optimize=True)

thumb_kb = round(os.path.getsize(thumb_path) / 1024, 1)
full_kb = round(os.path.getsize(full_path) / 1024, 1)
fb_kb = round(os.path.getsize(fb_path) / 1024, 1)

item_data = {
    **item,
    "image": f"Anh_Chup_Website/{filename}",
    "thumb": f"Kho_Anh_Webp/{thumb_name}",
    "full": f"Kho_Anh_Webp/{full_name}",
    "fb": f"Kho_Anh_Webp/{fb_name}",
    "thumb_kb": thumb_kb,
    "full_kb": full_kb,
    "fb_kb": fb_kb,
    "size_mb": f"{os.path.getsize(filepath)/(1024*1024):.2f} MB",
    "status": "SUCCESS"
}

# Update decor_metadata.json
with open(metadata_file, "r", encoding="utf-8") as f:
    meta = json.load(f)

for i, m in enumerate(meta):
    if m["id"] == "dc16":
        meta[i] = item_data
        break

with open(metadata_file, "w", encoding="utf-8") as f:
    json.dump(meta, f, ensure_ascii=False, indent=2)

print(f"[SUCCESS] Đã cập nhật dc16 thành công: {item_data['name']}")
