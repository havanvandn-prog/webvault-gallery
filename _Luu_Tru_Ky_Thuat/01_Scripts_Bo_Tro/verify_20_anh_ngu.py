# -*- coding: utf-8 -*-
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)
from capture_engine import verify_captured_image

metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "trung_tam_anh_ngu_metadata.json")
with open(metadata_file, "r", encoding="utf-8") as f:
    websites = json.load(f)

pass_count = 0
fail_count = 0

print(f"=== KIỂM ĐỊNH TOÀN DIỆN {len(websites)} ẢNH WEBP TRUNG TÂM ANH NGỮ ===")
for site in websites:
    slug = site["slug"]
    full_path = os.path.join(BASE_DIR, "Kho_Anh_Webp", f"{slug}_full.webp")
    thumb_path = os.path.join(BASE_DIR, "Kho_Anh_Webp", f"{slug}_thumb.webp")
    fb_path = os.path.join(BASE_DIR, "Kho_Anh_Webp", f"{slug}_fb.png")
    
    valid, msg = verify_captured_image(full_path)
    has_thumb = os.path.exists(thumb_path)
    has_fb = os.path.exists(fb_path)
    
    status = "PASS" if (valid and has_thumb and has_fb) else "FAIL"
    if status == "PASS":
        pass_count += 1
    else:
        fail_count += 1
    print(f"[{status}] {site['name']} ({site['domain']}): {msg}")

print(f"\nTỔNG KẾT: PASS: {pass_count}/{len(websites)} | FAIL: {fail_count}/{len(websites)}")
