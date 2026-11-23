# -*- coding: utf-8 -*-
import json, os, sys, subprocess

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
pool_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "xay_dung_pool_audit.json")
meta_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "xay_dung_metadata.json")
staging_json_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "staging_all_candidates.json")
build_script_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "01_Scripts_Bo_Tro", "build_multi_staging.py")
anh_dir = os.path.join(BASE_DIR, "Anh_Chup_Website")
webp_dir = os.path.join(BASE_DIR, "Kho_Anh_Webp")

SELECTED_SLUGS = [
    # Nhóm 1: Tổng Thầu & Tập Đoàn Xây Dựng Hàng Đầu Việt Nam (7)
    "xd_coteccons",
    "xd_newtecons",
    "xd_centralcons",
    "xd_unicons",
    "xd_solenc",
    "xd_fecon",
    "xd_dinco",
    # Nhóm 2: Xây Nhà Trọn Gói, Biệt Thự & Thiết Kế Thi Công Việt Nam (7)
    "xd_sbshouse",
    "xd_akisa",
    "xd_betaviet",
    "xd_neohouse",
    "xd_nhattin",
    "xd_greenhn",
    "xd_ancu",
    # Nhóm 3: Kết Cấu Thép Công Nghiệp & Tổng Thầu Quốc Tế Chuẩn UI/UX (6)
    "xd_atad",
    "xd_bmbsteel",
    "xd_suffolk",
    "xd_bechtel",
    "xd_skanska",
    "xd_olsonkundig",
]

with open(pool_path, "r", encoding="utf-8") as f:
    pool_data = json.load(f)

by_slug = {x["slug"]: x for x in pool_data if x.get("status") == "SUCCESS"}

curated = []
for idx, slug in enumerate(SELECTED_SLUGS, 1):
    assert slug in by_slug, f"Missing slug in pool: {slug}"
    item = dict(by_slug[slug])
    item["id"] = f"xd{idx:02d}"
    curated.append(item)

assert len(curated) == 20, f"Expected 20 curated items, got {len(curated)}"

# Dọn sạch ảnh của các mẫu không được chọn
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

existing_filtered = [item for item in existing if item.get("industry") != "xay-dung"]
merged = curated + existing_filtered

with open(staging_json_path, "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

print(f"[+] Merged 20 Xay Dung samples into staging_all_candidates.json (Total: {len(merged)})")

with open(build_script_path, "r", encoding="utf-8") as f:
    text = f.read()

# Bỏ active ở các tab cũ
text = text.replace('<button class="staging-tab-btn active"', '<button class="staging-tab-btn"')

if 'data-industry="xay-dung"' not in text:
    old_tabs = '      <button class="staging-tab-btn" data-industry="all" onclick="filterStagingTopic(\'all\')">'
    idx_start = text.find(old_tabs)
    assert idx_start != -1, "old_tabs not found"
    idx_end = text.find("</button>", idx_start) + len("</button>")

    new_tabs = f"""      <button class="staging-tab-btn" data-industry="all" onclick="filterStagingTopic('all')">
        <span>⚡</span> Tất Cả Nháp <span class="tab-badge" id="badgeAll">{len(merged)}</span>
      </button>
      <button class="staging-tab-btn active" data-industry="xay-dung" onclick="filterStagingTopic('xay-dung')">
        <span>🏗️</span> Mảng Xây Dựng <span class="tab-badge" id="badgeXayDung">{len(curated)}</span>
      </button>"""

    text = text[:idx_start] + new_tabs + text[idx_end:]

    import re
    text = re.sub(r"let currentTopic = '[^']+';", "let currentTopic = 'xay-dung';", text, count=1)
    text = re.sub(
        r"const indParam = params\.get\('industry'\) \|\| params\.get\('topic'\) \|\| '[^']+';",
        "const indParam = params.get('industry') || params.get('topic') || 'xay-dung';",
        text,
        count=1
    )

    old_map = "const topicMapName = {"
    new_map = """const topicMapName = {
      'xay-dung': 'Mảng Xây Dựng (Tổng Thầu VN, Xây Nhà Trọn Gói, Kết Cấu Thép & Tổng Thầu Quốc Tế)',"""
    assert old_map in text, "old_map not found"
    text = text.replace(old_map, new_map, 1)

    old_badge = "if (document.getElementById('badgeAll')) document.getElementById('badgeAll').textContent = CANDIDATES.length;"
    new_badge = old_badge + "\n    if (document.getElementById('badgeXayDung')) document.getElementById('badgeXayDung').textContent = CANDIDATES.filter(c => c.industry === 'xay-dung').length;"
    assert old_badge in text, "old_badge not found"
    text = text.replace(old_badge, new_badge, 1)
else:
    text = text.replace('<button class="staging-tab-btn" data-industry="xay-dung"', '<button class="staging-tab-btn active" data-industry="xay-dung"', 1)

with open(build_script_path, "w", encoding="utf-8") as f:
    f.write(text)

print("[+] Updated build_multi_staging.py with xay-dung tab.")
res = subprocess.run([sys.executable, build_script_path], capture_output=True, text=True, encoding="utf-8")
print(res.stdout)
if res.returncode != 0:
    print(res.stderr)
    sys.exit(res.returncode)
print("[+] Successfully rebuilt web_nhap_staging.html!")
