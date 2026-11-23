# -*- coding: utf-8 -*-
import json, os, sys, subprocess

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
meta1_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "xay_dung_metadata.json")
pool2_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "xay_dung_batch2_pool_audit.json")
meta2_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "xay_dung_batch2_metadata.json")
staging_json_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "staging_all_candidates.json")
build_script_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "01_Scripts_Bo_Tro", "build_multi_staging.py")
anh_dir = os.path.join(BASE_DIR, "Anh_Chup_Website")
webp_dir = os.path.join(BASE_DIR, "Kho_Anh_Webp")

SELECTED_BATCH2 = [
    # Nhóm 1: Tổng Thầu, Hạ Tầng & Kết Cấu Thép Việt Nam (8)
    "xd_hoabinh",
    "xd_cc1",
    "xd_viteccons",
    "xd_anphong",
    "xd_daidung",
    "xd_searefico",
    "xd_hailong",
    "xd_pebsteel",
    # Nhóm 2: Thiết Kế & Thi Công Xây Nhà Trọn Gói Việt Nam (6)
    "xd_xhome",
    "xd_vinavic",
    "xd_laco",
    "xd_vietquang",
    "xd_kienanvinh",
    "xd_minhbao",
    # Nhóm 3: Tổng Thầu & Xây Dựng Quốc Tế Chuẩn UI/UX (6)
    "xd_turner",
    "xd_pcl",
    "xd_mortenson",
    "xd_lendlease",
    "xd_swinerton",
    "xd_henselphelps",
]

with open(meta1_path, "r", encoding="utf-8") as f:
    batch1 = json.load(f)

with open(pool2_path, "r", encoding="utf-8") as f:
    pool2 = json.load(f)

by_slug2 = {x["slug"]: x for x in pool2 if x.get("status") == "SUCCESS"}

batch2 = []
for idx, slug in enumerate(SELECTED_BATCH2, 1):
    assert slug in by_slug2, f"Missing slug in pool2: {slug}"
    item = dict(by_slug2[slug])
    item["id"] = f"xd{20+idx:02d}"
    batch2.append(item)

assert len(batch2) == 20, f"Expected 20 batch2 items, got {len(batch2)}"

unused_slugs = set(by_slug2.keys()) - set(SELECTED_BATCH2)
removed_files = 0
for uslug in unused_slugs:
    for fp in [
        os.path.join(anh_dir, f"{uslug}.png"),
        os.path.join(webp_dir, f"{uslug}_full.webp"),
        os.path.join(webp_dir, f"{uslug}_thumb.webp"),
        os.path.join(webp_dir, f"{uslug}_fb.png"),
    ]:
        if os.path.exists(fp):
            os.remove(fp)
            removed_files += 1
print(f"[+] Cleaned {removed_files} unused capture files from {len(unused_slugs)} rejected batch-2 candidates.")

with open(meta2_path, "w", encoding="utf-8") as f:
    json.dump(batch2, f, ensure_ascii=False, indent=2)

all_xd = batch1 + batch2
assert len(all_xd) == 40, f"Expected 40 total xay-dung items, got {len(all_xd)}"

with open(staging_json_path, "r", encoding="utf-8") as f:
    existing = json.load(f)

existing_filtered = [item for item in existing if item.get("industry") != "xay-dung"]
merged = all_xd + existing_filtered

with open(staging_json_path, "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

print(f"[+] Merged 40 Xay Dung samples into staging_all_candidates.json (Total: {len(merged)})")

res = subprocess.run([sys.executable, build_script_path], capture_output=True, text=True, encoding="utf-8")
print(res.stdout)
if res.returncode != 0:
    print(res.stderr)
    sys.exit(res.returncode)
print("[+] Successfully rebuilt web_nhap_staging.html with 40 construction samples!")
