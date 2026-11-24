# -*- coding: utf-8 -*-
import json, os, sys, subprocess

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
pool_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "spa_pool_audit.json")
meta_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "spa_metadata.json")
staging_json_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "staging_all_candidates.json")
build_script_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "01_Scripts_Bo_Tro", "build_multi_staging.py")
anh_dir = os.path.join(BASE_DIR, "Anh_Chup_Website")
webp_dir = os.path.join(BASE_DIR, "Kho_Anh_Webp")

SELECTED_20 = [
    # Nhóm 1: Bệnh Viện Thẩm Mỹ & Clinic Da Liễu VN (9)
    "spa_rohtoaohal",
    "spa_ruco",
    "spa_o2skin",
    "spa_pensilia",
    "spa_lavender",
    "spa_saigonsmile",
    "spa_luxclinic",
    "spa_thucuc",
    "spa_kangnam",
    # Nhóm 2: Day Spa, Dưỡng Sinh & Massage Thư Giãn VN (3)
    "spa_sentaithu",
    "spa_herbalspa",
    "spa_charmspa",
    # Nhóm 3: Luxury Spa, MedSpa & Facial Bar Quốc Tế Chuẩn UI/UX (8)
    "spa_everbody",
    "spa_heydayskincare",
    "spa_glowbar",
    "spa_silvermirror",
    "spa_formulafig",
    "spa_bathhouse",
    "spa_burkewilliams",
    "spa_canyonranch",
]

with open(pool_path, "r", encoding="utf-8") as f:
    pool = json.load(f)

by_slug = {x["slug"]: x for x in pool if x.get("status") == "SUCCESS"}

selected_items = []
for idx, slug in enumerate(SELECTED_20, 1):
    assert slug in by_slug, f"Missing slug: {slug}"
    item = dict(by_slug[slug])
    item["id"] = f"sp{idx:02d}"
    raw_png = os.path.join(anh_dir, f"{slug}.png")
    full_webp = os.path.join(webp_dir, f"{slug}_full.webp")
    thumb_webp = os.path.join(webp_dir, f"{slug}_thumb.webp")
    fb_png = os.path.join(webp_dir, f"{slug}_fb.png")
    for p_req in [raw_png, full_webp, thumb_webp, fb_png]:
        assert os.path.exists(p_req), f"Missing asset file: {p_req}"
    item["thumb_kb"] = round(os.path.getsize(thumb_webp) / 1024, 1)
    item["full_kb"] = round(os.path.getsize(full_webp) / 1024, 1)
    item["fb_kb"] = round(os.path.getsize(fb_png) / 1024, 1)
    item["size_mb"] = f"{round(os.path.getsize(raw_png) / (1024*1024), 2)} MB"
    selected_items.append(item)

assert len(selected_items) == 20, f"Expected 20 items, got {len(selected_items)}"

unused_slugs = set(by_slug.keys()) - set(SELECTED_20)
removed = 0
for uslug in unused_slugs:
    for fp in [
        os.path.join(anh_dir, f"{uslug}.png"),
        os.path.join(webp_dir, f"{uslug}_full.webp"),
        os.path.join(webp_dir, f"{uslug}_thumb.webp"),
        os.path.join(webp_dir, f"{uslug}_fb.png"),
    ]:
        if os.path.exists(fp):
            os.remove(fp)
            removed += 1
print(f"[+] Cleaned {removed} files from {len(unused_slugs)} rejected candidates: {sorted(unused_slugs)}")

with open(meta_path, "w", encoding="utf-8") as f:
    json.dump(selected_items, f, ensure_ascii=False, indent=2)

with open(staging_json_path, "r", encoding="utf-8") as f:
    existing = json.load(f)

existing_filtered = [x for x in existing if x.get("industry") != "spa-tham-my-vien"]
merged = selected_items + existing_filtered

with open(staging_json_path, "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

print(f"[+] Merged 20 spa-tham-my-vien samples into staging_all_candidates.json (Total: {len(merged)})")

res = subprocess.run([sys.executable, build_script_path], capture_output=True, text=True, encoding="utf-8")
print(res.stdout)
if res.returncode != 0:
    print(res.stderr)
    sys.exit(res.returncode)
print("[+] Successfully rebuilt web_nhap_staging.html!")
