# -*- coding: utf-8 -*-
import json
import sys
sys.path.append(r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts")
from capture_engine import verify_captured_image

with open(r"_Luu_Tru_Ky_Thuat/03_Du_Lieu_Tam_Va_Test/cafe_banh_mi_metadata.json", "r", encoding="utf-8") as f:
    sites = json.load(f)

print(f"=== AUDIT KIỂM ĐỊNH TOÀN DIỆN {len(sites)} WEBSITE CAFE & BÁNH MÌ ===")
all_pass = True
for idx, s in enumerate(sites, 1):
    slug = s["slug"]
    name = s["name"]
    domain = s["domain"]
    path = f"Kho_Anh_Webp/{slug}_full.webp"
    valid, msg = verify_captured_image(path)
    status = "PASS" if valid else "FAIL"
    if not valid:
        all_pass = False
    print(f"[{idx:02d}/20] {status}: {name} ({domain}) -> {msg}")

print(f"\n===> KẾT QUẢ TỔNG THỂ: {'100% PASS TOÀN DIỆN!' if all_pass else 'CÓ LỖI CẦN SỬA!'}")
