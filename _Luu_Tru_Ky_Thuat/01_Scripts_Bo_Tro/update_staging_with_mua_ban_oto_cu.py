# -*- coding: utf-8 -*-
import json
import os
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
candidates_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "staging_all_candidates.json")
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "mua_ban_oto_cu_metadata.json")
build_staging_script = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "01_Scripts_Bo_Tro", "build_multi_staging.py")

# 1. Đọc metadata mới chụp
if not os.path.exists(metadata_file):
    print("[-] Chưa có file mua_ban_oto_cu_metadata.json!")
    sys.exit(1)

with open(metadata_file, "r", encoding="utf-8") as f:
    items = json.load(f)

# 2. Đọc staging_all_candidates.json hiện tại
all_candidates = []
if os.path.exists(candidates_file):
    with open(candidates_file, "r", encoding="utf-8") as f:
        all_candidates = json.load(f)

# Loại bỏ các mục cũ của mua-ban-oto-cu nếu có để tránh trùng lặp
all_candidates = [c for c in all_candidates if c.get("industry") != "mua-ban-oto-cu"]

# Thêm 20 ứng viên Mua Bán Xe Ô Tô Cũ mới
new_candidates = []
for d in items:
    new_candidates.append({
        "id": d["id"],
        "industry": d.get("industry", "mua-ban-oto-cu"),
        "industry_name": d.get("industry_name", "Mua Bán Xe Ô Tô Cũ"),
        "name": d["name"],
        "short_name": d.get("short_name", d["name"]),
        "url": d["url"],
        "domain": d["domain"],
        "vibe": d.get("vibe_name", d.get("vibe", "Uy tín & Tối ưu chuyển đổi")),
        "location": d["location"],
        "thumb": d.get("thumb") or f"Kho_Anh_Webp/{d['slug']}_thumb.webp",
        "full": d.get("full") or f"Kho_Anh_Webp/{d['slug']}_full.webp",
        "desc": d["desc"]
    })

# Đưa mua-ban-oto-cu lên đầu danh sách
updated_all_candidates = new_candidates + all_candidates

with open(candidates_file, "w", encoding="utf-8") as f:
    json.dump(updated_all_candidates, f, ensure_ascii=False, indent=2)

print(f"[+] Đã lưu tổng cộng {len(updated_all_candidates)} ứng viên vào staging_all_candidates.json (trong đó có {len(new_candidates)} mẫu Mua Bán Xe Ô Tô Cũ)!")

# 3. Cập nhật build_multi_staging.py
with open(build_staging_script, "r", encoding="utf-8") as f:
    script_content = f.read()

# Kiểm tra nếu chưa có tab mua-ban-oto-cu
if 'data-industry="mua-ban-oto-cu"' not in script_content:
    old_nav = """    <div class="staging-tabs-container">
      <button class="staging-tab-btn" data-industry="all" onclick="filterStagingTopic('all')">
        <span>⚡</span> Tất Cả Nháp <span class="tab-badge" id="badgeAll">100</span>
      </button>
      <button class="staging-tab-btn active" data-industry="du-hoc-dinh-cu-my" onclick="filterStagingTopic('du-hoc-dinh-cu-my')">"""

    new_nav = f"""    <div class="staging-tabs-container">
      <button class="staging-tab-btn" data-industry="all" onclick="filterStagingTopic('all')">
        <span>⚡</span> Tất Cả Nháp <span class="tab-badge" id="badgeAll">{len(updated_all_candidates)}</span>
      </button>
      <button class="staging-tab-btn active" data-industry="mua-ban-oto-cu" onclick="filterStagingTopic('mua-ban-oto-cu')">
        <span>🚗</span> Mua Bán Xe Ô Tô Cũ <span class="tab-badge" id="badgeOtoCu">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="du-hoc-dinh-cu-my" onclick="filterStagingTopic('du-hoc-dinh-cu-my')">"""

    script_content = script_content.replace(old_nav, new_nav)

    # Cập nhật default topic
    script_content = script_content.replace(
        "let currentTopic = 'du-hoc-dinh-cu-my';",
        "let currentTopic = 'mua-ban-oto-cu';"
    )
    script_content = script_content.replace(
        "['all', 'du-hoc-dinh-cu-my', 'phong-tap-fitness', 'ban-dong-ho', 'decor-su-kien', 'tiec-cuoi']",
        "['all', 'mua-ban-oto-cu', 'du-hoc-dinh-cu-my', 'phong-tap-fitness', 'ban-dong-ho', 'decor-su-kien', 'tiec-cuoi']"
    )

    # Cập nhật counter text
    script_content = script_content.replace(
        """Chủ đề đang xem: <b id="statTopicName" style="color:#fff;">Du Học & Định Cư Mỹ (Google Ads & CRO)</b>""",
        """Chủ đề đang xem: <b id="statTopicName" style="color:#fff;">Mua Bán Xe Ô Tô Cũ (Google Ads & CRO)</b>"""
    )

    # Cập nhật topicMapName
    old_topic_map = """    const topicMapName = {
      'all': 'Tất Cả Nháp Chờ Duyệt',
      'du-hoc-dinh-cu-my': 'Du Học & Định Cư Mỹ',"""

    new_topic_map = """    const topicMapName = {
      'all': 'Tất Cả Nháp Chờ Duyệt',
      'mua-ban-oto-cu': 'Mua Bán Xe Ô Tô Cũ',
      'du-hoc-dinh-cu-my': 'Du Học & Định Cư Mỹ',"""

    script_content = script_content.replace(old_topic_map, new_topic_map)

    # Cập nhật badge trong JS
    old_badges = """    if (document.getElementById('badgeDuHocDinhCu')) document.getElementById('badgeDuHocDinhCu').textContent = CANDIDATES.filter(c => c.industry === 'du-hoc-dinh-cu-my').length;"""
    new_badges = """    if (document.getElementById('badgeOtoCu')) document.getElementById('badgeOtoCu').textContent = CANDIDATES.filter(c => c.industry === 'mua-ban-oto-cu').length;
    if (document.getElementById('badgeDuHocDinhCu')) document.getElementById('badgeDuHocDinhCu').textContent = CANDIDATES.filter(c => c.industry === 'du-hoc-dinh-cu-my').length;"""
    script_content = script_content.replace(old_badges, new_badges)

    with open(build_staging_script, "w", encoding="utf-8") as f:
        f.write(script_content)
    print("[+] Đã cập nhật xong build_multi_staging.py!")
else:
    print("[i] build_multi_staging.py đã có tab mua-ban-oto-cu.")

# 4. Chạy build_multi_staging.py để biên dịch ra web_nhap_staging.html
print("[*] Đang biên dịch web_nhap_staging.html...")
import subprocess
res = subprocess.run([sys.executable, build_staging_script], capture_output=True, text=True, encoding="utf-8")
print(res.stdout)
if res.stderr:
    print("Stderr:", res.stderr)

print("[+] Hoàn tất tích hợp Mua Bán Xe Ô Tô Cũ vào Staging!")
