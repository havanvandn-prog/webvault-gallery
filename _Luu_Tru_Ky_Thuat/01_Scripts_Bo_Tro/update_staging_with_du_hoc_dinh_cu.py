# -*- coding: utf-8 -*-
import json
import os
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
candidates_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "staging_all_candidates.json")
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "du_hoc_dinh_cu_metadata.json")
build_staging_script = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "01_Scripts_Bo_Tro", "build_multi_staging.py")

# 1. Đọc metadata mới chụp
if not os.path.exists(metadata_file):
    print("[-] Chưa có file du_hoc_dinh_cu_metadata.json!")
    sys.exit(1)

with open(metadata_file, "r", encoding="utf-8") as f:
    items = json.load(f)

# 2. Đọc staging_all_candidates.json hiện tại
all_candidates = []
if os.path.exists(candidates_file):
    with open(candidates_file, "r", encoding="utf-8") as f:
        all_candidates = json.load(f)

# Loại bỏ các mục cũ của du-hoc-dinh-cu-my nếu có để tránh trùng lặp
all_candidates = [c for c in all_candidates if c.get("industry") != "du-hoc-dinh-cu-my"]

# Thêm 20 ứng viên du học & định cư mới
new_candidates = []
for d in items:
    new_candidates.append({
        "id": d["id"],
        "industry": d.get("industry", "du-hoc-dinh-cu-my"),
        "industry_name": d.get("industry_name", "Du Học & Định Cư Mỹ"),
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

# Đưa du-hoc-dinh-cu-my lên đầu danh sách
updated_all_candidates = new_candidates + all_candidates

with open(candidates_file, "w", encoding="utf-8") as f:
    json.dump(updated_all_candidates, f, ensure_ascii=False, indent=2)

print(f"[+] Đã lưu tổng cộng {len(updated_all_candidates)} ứng viên vào staging_all_candidates.json (trong đó có {len(new_candidates)} mẫu Du Học & Định Cư Mỹ)!")

# 3. Cập nhật build_multi_staging.py
with open(build_staging_script, "r", encoding="utf-8") as f:
    script_content = f.read()

# Kiểm tra nếu chưa có tab du-hoc-dinh-cu-my
if 'data-industry="du-hoc-dinh-cu-my"' not in script_content:
    old_nav = """    <div class="staging-tabs-container">
      <button class="staging-tab-btn" data-industry="all" onclick="filterStagingTopic('all')">
        <span>⚡</span> Tất Cả Nháp <span class="tab-badge" id="badgeAll">80</span>
      </button>
      <button class="staging-tab-btn active" data-industry="phong-tap-fitness" onclick="filterStagingTopic('phong-tap-fitness')">"""

    new_nav = """    <div class="staging-tabs-container">
      <button class="staging-tab-btn" data-industry="all" onclick="filterStagingTopic('all')">
        <span>⚡</span> Tất Cả Nháp <span class="tab-badge" id="badgeAll">100</span>
      </button>
      <button class="staging-tab-btn active" data-industry="du-hoc-dinh-cu-my" onclick="filterStagingTopic('du-hoc-dinh-cu-my')">
        <span>🎓</span> Du Học & Định Cư Mỹ <span class="tab-badge" id="badgeDuHocDinhCu">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="phong-tap-fitness" onclick="filterStagingTopic('phong-tap-fitness')">"""

    script_content = script_content.replace(old_nav, new_nav)

    # Cập nhật default topic
    script_content = script_content.replace(
        "let currentTopic = 'phong-tap-fitness';",
        "let currentTopic = 'du-hoc-dinh-cu-my';"
    )
    script_content = script_content.replace(
        "['all', 'phong-tap-fitness', 'ban-dong-ho', 'decor-su-kien', 'tiec-cuoi']",
        "['all', 'du-hoc-dinh-cu-my', 'phong-tap-fitness', 'ban-dong-ho', 'decor-su-kien', 'tiec-cuoi']"
    )

    # Cập nhật counter text
    script_content = script_content.replace(
        """Chủ đề đang xem: <b id="statTopicName" style="color:#fff;">Phòng Tập Fitness & Gym</b>""",
        """Chủ đề đang xem: <b id="statTopicName" style="color:#fff;">Du Học & Định Cư Mỹ (Google Ads & CRO)</b>"""
    )

    # Cập nhật topicMapName
    old_topic_map = """    const topicMapName = {
      'all': 'Tất Cả Nháp Chờ Duyệt',
      'phong-tap-fitness': 'Phòng Tập Fitness & Gym',"""

    new_topic_map = """    const topicMapName = {
      'all': 'Tất Cả Nháp Chờ Duyệt',
      'du-hoc-dinh-cu-my': 'Du Học & Định Cư Mỹ (Google Ads & CRO)',
      'phong-tap-fitness': 'Phòng Tập Fitness & Gym',"""

    script_content = script_content.replace(old_topic_map, new_topic_map)

    # Cập nhật badge
    old_badges = """    if (document.getElementById('badgeAll')) document.getElementById('badgeAll').textContent = CANDIDATES.length;
    if (document.getElementById('badgeFitness')) document.getElementById('badgeFitness').textContent = CANDIDATES.filter(c => c.industry === 'phong-tap-fitness').length;"""

    new_badges = """    if (document.getElementById('badgeAll')) document.getElementById('badgeAll').textContent = CANDIDATES.length;
    if (document.getElementById('badgeDuHocDinhCu')) document.getElementById('badgeDuHocDinhCu').textContent = CANDIDATES.filter(c => c.industry === 'du-hoc-dinh-cu-my').length;
    if (document.getElementById('badgeFitness')) document.getElementById('badgeFitness').textContent = CANDIDATES.filter(c => c.industry === 'phong-tap-fitness').length;"""

    script_content = script_content.replace(old_badges, new_badges)

    with open(build_staging_script, "w", encoding="utf-8") as f:
        f.write(script_content)
    print("[+] Đã cập nhật build_multi_staging.py thành công!")
else:
    print("[*] build_multi_staging.py đã có sẵn tab du-hoc-dinh-cu-my.")

# 4. Chạy build_multi_staging.py để render web_nhap_staging.html
os.system(f'python "{build_staging_script}"')
print("[+] Đã render lại web_nhap_staging.html hoàn tất!")
