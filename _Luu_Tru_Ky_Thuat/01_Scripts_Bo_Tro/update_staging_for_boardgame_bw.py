# -*- coding: utf-8 -*-
import json
import os
import sys
import subprocess

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
cand_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "boardgame_bw_candidates.json")
meta_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "boardgame_bw_metadata.json")
staging_json_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "staging_all_candidates.json")
build_script_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "01_Scripts_Bo_Tro", "build_multi_staging.py")

with open(cand_path, "r", encoding="utf-8") as f:
    cands = json.load(f)

passed = [x for x in cands if x.get("status") == "SUCCESS"]
assert len(passed) == 12, f"Expected 12 passed samples, got {len(passed)}"

with open(meta_path, "w", encoding="utf-8") as f:
    json.dump(passed, f, ensure_ascii=False, indent=2)

with open(staging_json_path, "r", encoding="utf-8") as f:
    existing = json.load(f)

existing_filtered = [item for item in existing if item.get("industry") != "board-game-den-trang"]
merged = passed + existing_filtered

with open(staging_json_path, "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

print(f"[+] Merged 12 board game B&W samples into staging_all_candidates.json (Total: {len(merged)})")

with open(build_script_path, "r", encoding="utf-8") as f:
    text = f.read()

if 'data-industry="board-game-den-trang"' not in text:
    # Remove active class from previous active tab
    text = text.replace(
        '<button class="staging-tab-btn active" data-industry="noi-that-sang-trong"',
        '<button class="staging-tab-btn" data-industry="noi-that-sang-trong"',
        1
    )

    old_tabs = """      <button class="staging-tab-btn" data-industry="all" onclick="filterStagingTopic('all')">
        <span>⚡</span> Tất Cả Nháp <span class="tab-badge" id="badgeAll">"""
    idx_start = text.find(old_tabs)
    assert idx_start != -1, "old_tabs not found"
    idx_end = text.find("</button>", idx_start) + len("</button>")
    old_all_btn = text[idx_start:idx_end]

    new_tabs = f"""      <button class="staging-tab-btn" data-industry="all" onclick="filterStagingTopic('all')">
        <span>⚡</span> Tất Cả Nháp <span class="tab-badge" id="badgeAll">{len(merged)}</span>
      </button>
      <button class="staging-tab-btn active" data-industry="board-game-den-trang" onclick="filterStagingTopic('board-game-den-trang')">
        <span>🎲</span> Board Game Đen Trắng <span class="tab-badge" id="badgeBoardGameBW">{len(passed)}</span>
      </button>"""

    text = text[:idx_start] + new_tabs + text[idx_end:]

    text = text.replace("let currentTopic = 'noi-that-sang-trong';", "let currentTopic = 'board-game-den-trang';", 1)
    text = text.replace(
        "const indParam = params.get('industry') || params.get('topic') || 'noi-that-sang-trong';",
        "const indParam = params.get('industry') || params.get('topic') || 'board-game-den-trang';",
        1
    )

    old_map = "const topicMapName = {"
    new_map = """const topicMapName = {
      'board-game-den-trang': 'Website Board Game Nước Ngoài Phong Cách Đen Trắng (Monochrome Cafe, Bar & Eatery)',"""
    assert old_map in text, "old_map not found"
    text = text.replace(old_map, new_map, 1)

    old_badge = "if (document.getElementById('badgeNoiThatLux'))"
    new_badge = """if (document.getElementById('badgeBoardGameBW')) document.getElementById('badgeBoardGameBW').textContent = CANDIDATES.filter(c => c.industry === 'board-game-den-trang').length;
    if (document.getElementById('badgeNoiThatLux'))"""
    assert old_badge in text, "old_badge not found"
    text = text.replace(old_badge, new_badge, 1)

    with open(build_script_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("[+] Updated build_multi_staging.py with board-game-den-trang tab!")

res = subprocess.run([sys.executable, build_script_path], capture_output=True, text=True, encoding="utf-8")
print("[+] Build output:", res.stdout.strip())
if res.returncode != 0:
    print("[-] Build error:", res.stderr)
    sys.exit(1)
