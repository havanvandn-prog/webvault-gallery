# -*- coding: utf-8 -*-
import json
import os
import sys
import subprocess

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
cand_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "noi_that_luxury_candidates.json")
meta_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "noi_that_luxury_metadata.json")
staging_json_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "staging_all_candidates.json")
build_script_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "01_Scripts_Bo_Tro", "build_multi_staging.py")
anh_dir = os.path.join(BASE_DIR, "Anh_Chup_Website")
webp_dir = os.path.join(BASE_DIR, "Kho_Anh_Webp")

with open(cand_path, "r", encoding="utf-8") as f:
    all_lux = json.load(f)

drop_slugs = {"noi_that_lux_3asignature", "noi_that_lux_flexform"}
kept = [x for x in all_lux if x["slug"] not in drop_slugs]
assert len(kept) == 10, f"Expected 10 luxury samples, got {len(kept)}"

for i, item in enumerate(kept, 1):
    item["id"] = f"lux{i:02d}"

with open(meta_path, "w", encoding="utf-8") as f:
    json.dump(kept, f, ensure_ascii=False, indent=2)

# Cleanup unused images
for ds in drop_slugs:
    for p in [
        os.path.join(anh_dir, f"{ds}.png"),
        os.path.join(webp_dir, f"{ds}_full.webp"),
        os.path.join(webp_dir, f"{ds}_thumb.webp"),
        os.path.join(webp_dir, f"{ds}_fb.png"),
    ]:
        if os.path.exists(p):
            os.remove(p)
            print(f"  [cleanup] Removed {os.path.basename(p)}")

with open(staging_json_path, "r", encoding="utf-8") as f:
    existing = json.load(f)

existing_filtered = [item for item in existing if item.get("industry") != "noi-that-sang-trong"]
merged = kept + existing_filtered

with open(staging_json_path, "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

print(f"[+] Merged 10 luxury interior samples into staging_all_candidates.json (Total: {len(merged)})")

with open(build_script_path, "r", encoding="utf-8") as f:
    text = f.read()

if 'data-industry="noi-that-sang-trong"' not in text:
    old_tabs = """      <button class="staging-tab-btn" data-industry="all" onclick="filterStagingTopic('all')">
        <span>⚡</span> Tất Cả Nháp <span class="tab-badge" id="badgeAll">281</span>
      </button>
      <button class="staging-tab-btn active" data-industry="noi-that" onclick="filterStagingTopic('noi-that')">"""

    new_tabs = f"""      <button class="staging-tab-btn" data-industry="all" onclick="filterStagingTopic('all')">
        <span>⚡</span> Tất Cả Nháp <span class="tab-badge" id="badgeAll">{len(merged)}</span>
      </button>
      <button class="staging-tab-btn active" data-industry="noi-that-sang-trong" onclick="filterStagingTopic('noi-that-sang-trong')">
        <span>✨</span> Nội Thất Sang Trọng <span class="tab-badge" id="badgeNoiThatLux">{len(kept)}</span>
      </button>
      <button class="staging-tab-btn" data-industry="noi-that" onclick="filterStagingTopic('noi-that')">"""

    assert old_tabs in text, "old_tabs not found"
    text = text.replace(old_tabs, new_tabs, 1)

    text = text.replace("let currentTopic = 'noi-that';", "let currentTopic = 'noi-that-sang-trong';", 1)
    text = text.replace(
        "const indParam = params.get('industry') || params.get('topic') || 'noi-that';",
        "const indParam = params.get('industry') || params.get('topic') || 'noi-that-sang-trong';",
        1
    )

    old_map = "const topicMapName = {"
    new_map = """const topicMapName = {
      'noi-that-sang-trong': 'Nội Thất Phong Cách Sang Trọng (Luxury Editorial, Quiet Luxury & Biệt Thự Thượng Lưu)',"""
    assert old_map in text, "old_map not found"
    text = text.replace(old_map, new_map, 1)

    old_badge = "if (document.getElementById('badgeNoiThat'))"
    new_badge = """if (document.getElementById('badgeNoiThatLux')) document.getElementById('badgeNoiThatLux').textContent = CANDIDATES.filter(c => c.industry === 'noi-that-sang-trong').length;
    if (document.getElementById('badgeNoiThat'))"""
    assert old_badge in text, "old_badge not found"
    text = text.replace(old_badge, new_badge, 1)

    with open(build_script_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("[+] Updated build_multi_staging.py with noi-that-sang-trong tab!")

res = subprocess.run([sys.executable, build_script_path], capture_output=True, text=True, encoding="utf-8")
print("[+] Build output:", res.stdout.strip())
if res.returncode != 0:
    print("[-] Build error:", res.stderr)
    sys.exit(1)
