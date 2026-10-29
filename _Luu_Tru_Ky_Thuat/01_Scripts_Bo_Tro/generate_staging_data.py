# -*- coding: utf-8 -*-
import json, os, sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# 1. Bán đồng hồ
with open(os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "dong_ho_metadata.json"), "r", encoding="utf-8") as f:
    dong_ho_raw = json.load(f)

dong_ho_list = []
for d in dong_ho_raw:
    slug = d.get("slug") or d["domain"].replace(".", "_")
    dong_ho_list.append({
        "id": d["id"],
        "industry": "ban-dong-ho",
        "industry_name": "Bán Đồng Hồ",
        "name": d["name"],
        "short_name": d.get("short_name", d["name"]),
        "url": d["url"],
        "domain": d["domain"],
        "vibe": d.get("vibe_name", d.get("vibe", "Hiện đại")),
        "location": d["location"],
        "thumb": d.get("thumb") or f"Kho_Anh_Webp/{slug}_thumb.webp",
        "full": d.get("full") or f"Kho_Anh_Webp/{slug}_full.webp",
        "desc": d["desc"]
    })

# 2. Decor sự kiện
with open(os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "decor_metadata.json"), "r", encoding="utf-8") as f:
    decor_raw = json.load(f)

decor_list = []
for d in decor_raw:
    slug = d.get("slug") or d["domain"].replace(".", "_")
    decor_list.append({
        "id": d["id"],
        "industry": "decor-su-kien",
        "industry_name": "Decor Sự Kiện",
        "name": d["name"],
        "short_name": d.get("short_name", d["name"]),
        "url": d["url"],
        "domain": d["domain"],
        "vibe": d.get("vibe_name", d.get("vibe", "Hiện đại")),
        "location": d["location"],
        "thumb": d.get("thumb") or f"Kho_Anh_Webp/{slug}_thumb.webp",
        "full": d.get("full") or f"Kho_Anh_Webp/{slug}_full.webp",
        "desc": d["desc"]
    })

# 3. Tiệc cưới & Wedding
with open(os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "wedding_metadata.json"), "r", encoding="utf-8") as f:
    wedding_raw = json.load(f)

wedding_list = []
for idx, d in enumerate(wedding_raw, start=1):
    slug = d["domain"].replace(".", "_")
    wid = f"wd{idx:02d}"
    wedding_list.append({
        "id": wid,
        "industry": "tiec-cuoi",
        "industry_name": "Tiệc Cưới & Wedding",
        "name": d["name"],
        "short_name": d.get("name").split("—")[0].strip(),
        "url": d["url"],
        "domain": d["domain"],
        "vibe": d.get("category_vn", "Tiệc cưới sang trọng"),
        "location": d.get("location", "Toàn quốc"),
        "thumb": f"Kho_Anh_Webp/{slug}_thumb.webp",
        "full": f"Kho_Anh_Webp/{slug}_full.webp",
        "desc": d["desc"]
    })

all_candidates = dong_ho_list + decor_list + wedding_list

print(f"Bán đồng hồ: {len(dong_ho_list)}")
print(f"Decor sự kiện: {len(decor_list)}")
print(f"Tiệc cưới: {len(wedding_list)}")
print(f"Tổng cộng ứng viên nháp: {len(all_candidates)}")

# Lưu database nháp tổng hợp
output_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "staging_all_candidates.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(all_candidates, f, ensure_ascii=False, indent=2)

print("Đã lưu vào staging_all_candidates.json")
