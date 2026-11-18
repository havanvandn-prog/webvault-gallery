# -*- coding: utf-8 -*-
import json, os, sys, subprocess

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
cand_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "anhngu_dep_candidates.json")
meta_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "anhngu_dep_metadata.json")
staging_json_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "staging_all_candidates.json")
build_script_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "01_Scripts_Bo_Tro", "build_multi_staging.py")

with open(cand_path, "r", encoding="utf-8") as f:
    cands = json.load(f)

passed = [x for x in cands if x.get("status") == "SUCCESS"]
assert len(passed) == 20, f"Expected 20 passed samples, got {len(passed)}"

with open(meta_path, "w", encoding="utf-8") as f:
    json.dump(passed, f, ensure_ascii=False, indent=2)

with open(staging_json_path, "r", encoding="utf-8") as f:
    existing = json.load(f)

existing_filtered = [item for item in existing if item.get("industry") != "trung-tam-tieng-anh-dep"]
merged = passed + existing_filtered

with open(staging_json_path, "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

print(f"[+] Merged 20 English Center (Beautiful Layout) samples into staging_all_candidates.json (Total: {len(merged)})")

with open(build_script_path, "r", encoding="utf-8") as f:
    text = f.read()

if 'data-industry="trung-tam-tieng-anh-dep"' not in text:
    text = text.replace(
        '<button class="staging-tab-btn active" data-industry="khach-san"',
        '<button class="staging-tab-btn" data-industry="khach-san"',
        1
    )

    old_tabs = """      <button class="staging-tab-btn" data-industry="all" onclick="filterStagingTopic('all')">
        <span>⚡</span> Tất Cả Nháp <span class="tab-badge" id="badgeAll">"""
    idx_start = text.find(old_tabs)
    assert idx_start != -1, "old_tabs not found"
    idx_end = text.find("</button>", idx_start) + len("</button>")

    new_tabs = f"""      <button class="staging-tab-btn" data-industry="all" onclick="filterStagingTopic('all')">
        <span>⚡</span> Tất Cả Nháp <span class="tab-badge" id="badgeAll">{len(merged)}</span>
      </button>
      <button class="staging-tab-btn active" data-industry="trung-tam-tieng-anh-dep" onclick="filterStagingTopic('trung-tam-tieng-anh-dep')">
        <span>🏫</span> Tiếng Anh (Bố Cục Đẹp) <span class="tab-badge" id="badgeAnhNguDep">{len(passed)}</span>
      </button>"""

    text = text[:idx_start] + new_tabs + text[idx_end:]

    text = text.replace("let currentTopic = 'khach-san';", "let currentTopic = 'trung-tam-tieng-anh-dep';", 1)
    text = text.replace(
        "const indParam = params.get('industry') || params.get('topic') || 'khach-san';",
        "const indParam = params.get('industry') || params.get('topic') || 'trung-tam-tieng-anh-dep';",
        1
    )

    old_map = "const topicMapName = {"
    new_map = """const topicMapName = {
      'trung-tam-tieng-anh-dep': 'Trung Tâm Tiếng Anh Bố Cục Đẹp (Quốc Tế Editorial, EdTech & Trung Tâm Hiện Đại)',"""
    assert old_map in text, "old_map not found"
    text = text.replace(old_map, new_map, 1)

    old_badge = "if (document.getElementById('badgeKhachSan'))"
    new_badge = """if (document.getElementById('badgeAnhNguDep')) document.getElementById('badgeAnhNguDep').textContent = CANDIDATES.filter(c => c.industry === 'trung-tam-tieng-anh-dep').length;
    if (document.getElementById('badgeKhachSan'))"""
    assert old_badge in text, "old_badge not found"
    text = text.replace(old_badge, new_badge, 1)

    with open(build_script_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("[+] Updated build_multi_staging.py with trung-tam-tieng-anh-dep tab!")

res = subprocess.run([sys.executable, build_script_path], capture_output=True, text=True, encoding="utf-8")
print("[+] Build output:", res.stdout.strip())
if res.returncode != 0:
    print("[-] Build error:", res.stderr)
    sys.exit(1)
