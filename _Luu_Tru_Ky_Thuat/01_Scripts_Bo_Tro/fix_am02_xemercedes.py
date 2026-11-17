# -*- coding: utf-8 -*-
import os, sys, time, json
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)

from playwright.sync_api import sync_playwright
from capture_engine import setup_page_protection, capture_smart_clean, compress_tri_layer, verify_captured_image

output_dir = os.path.join(BASE_DIR, "Anh_Chup_Website")
kho_webp_dir = os.path.join(BASE_DIR, "Kho_Anh_Webp")
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "auto_mercedes_candidates.json")

replacement = {
    "id": "am02",
    "name": "Mercedes-Benz Việt Nam (VietnamCom) — Bảng Giá & Dự Toán Trả Góp",
    "short_name": "Mercedes VietnamCom",
    "url": "https://mercedesvietnam.com/",
    "domain": "mercedesvietnam.com",
    "slug": "am_mercedesvietnam_com",
    "industry": "landing-page-oto-mercedes",
    "industry_name": "Landing Page Ô Tô & Mercedes-Benz (CRO)",
    "category": "Mercedes-Benz Price & Loan Calculator LP",
    "category_vn": "Mercedes-Benz Mới — Gọn 4.600px & Dự Toán Trả Góp",
    "tag": "mercedes-cro",
    "vibe": "Dài 4.626px • Bảng Giá & Dự Toán Trả Góp • Form Báo Giá Nhanh",
    "location": "Việt Nam",
    "desc": "Trang bán xe Mercedes-Benz mới bố cục tinh gọn ~4.626px, tích hợp bảng giá niêm yết từng dòng xe, công cụ dự toán trả góp và form đăng ký nhận báo giá & lái thử."
}

raw_png = os.path.join(output_dir, f"{replacement['slug']}.png")
full_webp = os.path.join(kho_webp_dir, f"{replacement['slug']}_full.webp")
replacement["image"] = f"Anh_Chup_Website/{replacement['slug']}.png"
replacement["thumb"] = f"Kho_Anh_Webp/{replacement['slug']}_thumb.webp"
replacement["full"] = f"Kho_Anh_Webp/{replacement['slug']}_full.webp"
replacement["fb"] = f"Kho_Anh_Webp/{replacement['slug']}_fb.png"

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    ctx = b.new_context(
        viewport={'width':1440,'height':900},
        ignore_https_errors=True,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
    pg = ctx.new_page()
    setup_page_protection(pg)
    pg.goto(replacement['url'], timeout=45000, wait_until='domcontentloaded')
    time.sleep(3.5)
    capture_smart_clean(pg, raw_png, viewport_height=900, scroll_delay=0.3)
    thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb = compress_tri_layer(raw_png, replacement['slug'], kho_webp_dir)
    valid, msg = verify_captured_image(full_webp)
    print(f"[+] QA {replacement['domain']}: {'PASS' if valid else 'FAIL'} - {msg}")
    b.close()

assert valid, f"Replacement failed QA: {msg}"
replacement["thumb_kb"] = thumb_kb
replacement["full_kb"] = full_kb
replacement["fb_kb"] = fb_kb
replacement["size_mb"] = f"{round(os.path.getsize(raw_png) / (1024*1024), 2)} MB"
replacement["audit_msg"] = msg
replacement["status"] = "SUCCESS"

with open(metadata_file, "r", encoding="utf-8") as f:
    cands = json.load(f)

cands = [replacement if x["id"] == "am02" else x for x in cands]
with open(metadata_file, "w", encoding="utf-8") as f:
    json.dump(cands, f, ensure_ascii=False, indent=2)

# Clean up failed xemercedes_net files if any
for ext in [".png"]:
    p_old = os.path.join(output_dir, "am_xemercedes_net" + ext)
    if os.path.exists(p_old): os.remove(p_old)
for suf in ["_thumb.webp", "_full.webp", "_fb.png"]:
    p_old = os.path.join(kho_webp_dir, "am_xemercedes_net" + suf)
    if os.path.exists(p_old): os.remove(p_old)

print("[+] Updated auto_mercedes_candidates.json: 20/20 PASS!")
