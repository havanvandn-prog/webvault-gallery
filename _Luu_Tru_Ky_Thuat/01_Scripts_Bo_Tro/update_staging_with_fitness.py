# -*- coding: utf-8 -*-
import json
import os
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
candidates_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "staging_all_candidates.json")
fitness_meta_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "fitness_metadata.json")
build_staging_script = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "01_Scripts_Bo_Tro", "build_multi_staging.py")

# 1. Đọc metadata fitness mới chụp
if not os.path.exists(fitness_meta_file):
    print("[-] Chưa có file fitness_metadata.json!")
    sys.exit(1)

with open(fitness_meta_file, "r", encoding="utf-8") as f:
    fitness_items = json.load(f)

# 2. Đọc staging_all_candidates.json hiện tại
all_candidates = []
if os.path.exists(candidates_file):
    with open(candidates_file, "r", encoding="utf-8") as f:
        all_candidates = json.load(f)

# Loại bỏ các mục cũ của phong-tap-fitness nếu có để tránh trùng lặp
all_candidates = [c for c in all_candidates if c.get("industry") != "phong-tap-fitness"]

# Thêm 20 ứng viên fitness mới
fitness_candidates = []
for d in fitness_items:
    fitness_candidates.append({
        "id": d["id"],
        "industry": d.get("industry", "phong-tap-fitness"),
        "industry_name": d.get("industry_name", "Phòng Tập Fitness & Gym"),
        "name": d["name"],
        "short_name": d.get("short_name", d["name"]),
        "url": d["url"],
        "domain": d["domain"],
        "vibe": d.get("vibe_name", d.get("vibe", "Hiện đại & Năng động")),
        "location": d["location"],
        "thumb": d.get("thumb") or f"Kho_Anh_Webp/{d['slug']}_thumb.webp",
        "full": d.get("full") or f"Kho_Anh_Webp/{d['slug']}_full.webp",
        "desc": d["desc"]
    })

# Đưa fitness lên đầu hoặc gộp
updated_all_candidates = fitness_candidates + all_candidates

with open(candidates_file, "w", encoding="utf-8") as f:
    json.dump(updated_all_candidates, f, ensure_ascii=False, indent=2)

print(f"[+] Đã lưu tổng cộng {len(updated_all_candidates)} ứng viên vào staging_all_candidates.json (trong đó có {len(fitness_candidates)} mẫu Fitness)!")
