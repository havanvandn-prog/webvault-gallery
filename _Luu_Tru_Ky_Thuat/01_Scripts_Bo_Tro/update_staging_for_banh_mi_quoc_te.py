# -*- coding: utf-8 -*-
import json, os, sys, subprocess

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
pool_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "banh_mi_quoc_te_pool_audit.json")
meta_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "banh_mi_quoc_te_metadata.json")
staging_json_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "staging_all_candidates.json")
build_script_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "01_Scripts_Bo_Tro", "build_multi_staging.py")
anh_dir = os.path.join(BASE_DIR, "Anh_Chup_Website")
webp_dir = os.path.join(BASE_DIR, "Kho_Anh_Webp")

SELECTED_SLUGS = [
    # Nhóm 1: Tiệm Bánh Mì & Ẩm Thực Việt Phục Vụ Khách Quốc Tế Tại Việt Nam (3)
    "bmqt_mein_saigon",
    "bmqt_vietnom_kitchen",
    "bmqt_anan_saigon",
    # Nhóm 2: Tiệm Bánh Mì Boutique Tại Châu Âu, Úc & Châu Á (11)
    "bmqt_nonette_paris",
    "bmqt_banemi_paris",
    "bmqt_an_banh_mi_berlin",
    "bmqt_banhmi_king_nl",
    "bmqt_destination_roll",
    "bmqt_rolld_au",
    "bmqt_lukes_banhmi",
    "bmqt_banh_mi_bao_sydney",
    "bmqt_the_banh_mi_house",
    "bmqt_the_viet_roti",
    "bmqt_banh_mi_kitchen",
    # Nhóm 3: Thương Hiệu Bánh Mì Đương Đại Tại Mỹ (6)
    "bmqt_bun_mee_sf",
    "bmqt_bale_chicago",
    "bmqt_banh_mi_and_ti",
    "bmqt_mr_banh_mi_nyc",
    "bmqt_lotus_banhmi",
    "bmqt_paris_banh_mi_usa",
]

with open(pool_path, "r", encoding="utf-8") as f:
    pool_data = json.load(f)

by_slug = {x["slug"]: x for x in pool_data if x.get("status") == "SUCCESS"}

curated = []
for idx, slug in enumerate(SELECTED_SLUGS, 1):
    assert slug in by_slug, f"Missing slug in pool: {slug}"
    item = dict(by_slug[slug])
    item["id"] = f"bmqt{idx:02d}"
    curated.append(item)

assert len(curated) == 20, f"Expected 20 curated items, got {len(curated)}"

# Dọn sạch ảnh của các mẫu không được chọn (hoặc bị Cloudflare block)
unused_slugs = set(by_slug.keys()) - set(SELECTED_SLUGS)
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
print(f"[+] Cleaned {removed_files} unused capture files from {len(unused_slugs)} rejected candidates.")

with open(meta_path, "w", encoding="utf-8") as f:
    json.dump(curated, f, ensure_ascii=False, indent=2)

with open(staging_json_path, "r", encoding="utf-8") as f:
    existing = json.load(f)

existing_filtered = [item for item in existing if item.get("industry") != "banh-mi-quoc-te"]
merged = curated + existing_filtered

with open(staging_json_path, "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

print(f"[+] Merged 20 Banh Mi Quoc Te samples into staging_all_candidates.json (Total: {len(merged)})")

with open(build_script_path, "r", encoding="utf-8") as f:
    text = f.read()

if 'data-industry="banh-mi-quoc-te"' not in text:
    text = text.replace(
        '<button class="staging-tab-btn active" data-industry="khach-san"',
        '<button class="staging-tab-btn" data-industry="khach-san"',
        1
    )

    old_tabs = '      <button class="staging-tab-btn" data-industry="all" onclick="filterStagingTopic(\'all\')">'
    idx_start = text.find(old_tabs)
    assert idx_start != -1, "old_tabs not found"
    idx_end = text.find("</button>", idx_start) + len("</button>")

    new_tabs = f"""      <button class="staging-tab-btn" data-industry="all" onclick="filterStagingTopic('all')">
        <span>⚡</span> Tất Cả Nháp <span class="tab-badge" id="badgeAll">{len(merged)}</span>
      </button>
      <button class="staging-tab-btn active" data-industry="banh-mi-quoc-te" onclick="filterStagingTopic('banh-mi-quoc-te')">
        <span>🥖</span> Bánh Mì Quốc Tế <span class="tab-badge" id="badgeBanhMiQuocTe">{len(curated)}</span>
      </button>"""

    text = text[:idx_start] + new_tabs + text[idx_end:]

    text = text.replace("let currentTopic = 'khach-san';", "let currentTopic = 'banh-mi-quoc-te';", 1)
    text = text.replace(
        "const indParam = params.get('industry') || params.get('topic') || 'khach-san';",
        "const indParam = params.get('industry') || params.get('topic') || 'banh-mi-quoc-te';",
        1
    )

    old_map = "const topicMapName = {"
    new_map = """const topicMapName = {
      'banh-mi-quoc-te': 'Tiệm Bánh Mì Cho Người Nước Ngoài (Boutique VN, Châu Âu, Úc & Mỹ)',"""
    assert old_map in text, "old_map not found"
    text = text.replace(old_map, new_map, 1)

    old_badge = "if (document.getElementById('badgeKhachSan'))"
    new_badge = """if (document.getElementById('badgeBanhMiQuocTe')) document.getElementById('badgeBanhMiQuocTe').textContent = CANDIDATES.filter(c => c.industry === 'banh-mi-quoc-te').length;
    if (document.getElementById('badgeKhachSan'))"""
    assert old_badge in text, "old_badge not found"
    text = text.replace(old_badge, new_badge, 1)

    with open(build_script_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("[+] Updated build_multi_staging.py with banh-mi-quoc-te tab!")

res = subprocess.run([sys.executable, build_script_path], capture_output=True, text=True, encoding="utf-8")
print("[+] Build output:", res.stdout.strip())
if res.returncode != 0:
    print("[-] Build error:", res.stderr)
    sys.exit(1)
