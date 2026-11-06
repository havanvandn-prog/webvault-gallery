# -*- coding: utf-8 -*-
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
candidates_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "staging_all_candidates.json")
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "trung_tam_anh_ngu_metadata.json")
build_staging_script = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "01_Scripts_Bo_Tro", "build_multi_staging.py")

# 1. Đọc metadata mới chụp
if not os.path.exists(metadata_file):
    print("[-] Chưa có file trung_tam_anh_ngu_metadata.json!")
    sys.exit(1)

with open(metadata_file, "r", encoding="utf-8") as f:
    items = json.load(f)

# 2. Đọc staging_all_candidates.json hiện tại
all_candidates = []
if os.path.exists(candidates_file):
    with open(candidates_file, "r", encoding="utf-8") as f:
        all_candidates = json.load(f)

# Loại bỏ các mục cũ của trung-tam-anh-ngu nếu có để tránh trùng lặp
all_candidates = [c for c in all_candidates if c.get("industry") != "trung-tam-anh-ngu"]

# Thêm 20 ứng viên Trung Tâm Anh Ngữ mới
new_candidates = []
for d in items:
    new_candidates.append({
        "id": d["id"],
        "industry": "trung-tam-anh-ngu",
        "industry_name": "Trung Tâm Anh Ngữ",
        "name": d["name"],
        "short_name": d.get("short_name", d["name"]),
        "url": d["url"],
        "domain": d["domain"],
        "vibe": d.get("vibe_name", d.get("vibe", "Hiện Đại & Chuẩn Quốc Tế")),
        "location": d["location"],
        "thumb": d.get("thumb") or f"Kho_Anh_Webp/{d['slug']}_thumb.webp",
        "full": d.get("full") or f"Kho_Anh_Webp/{d['slug']}_full.webp",
        "desc": d["desc"]
    })

# Đưa trung-tam-anh-ngu lên đầu danh sách
updated_all_candidates = new_candidates + all_candidates

with open(candidates_file, "w", encoding="utf-8") as f:
    json.dump(updated_all_candidates, f, ensure_ascii=False, indent=2)

print(f"[+] Đã lưu tổng cộng {len(updated_all_candidates)} ứng viên vào staging_all_candidates.json (trong đó có {len(new_candidates)} mẫu Trung Tâm Anh Ngữ)!")

# 3. Cập nhật build_multi_staging.py
with open(build_staging_script, "r", encoding="utf-8") as f:
    script_content = f.read()

# Kiểm tra nếu chưa có tab trung-tam-anh-ngu
if 'data-industry="trung-tam-anh-ngu"' not in script_content:
    old_nav = """    <div class="staging-tabs-container">
      <button class="staging-tab-btn" data-industry="all" onclick="filterStagingTopic('all')">
        <span>⚡</span> Tất Cả Nháp <span class="tab-badge" id="badgeAll">"""

    # Tìm đoạn nav tab mua-ban-oto-cu hoặc tab đầu tiên
    import re
    # Thay thế phần tab header
    nav_pattern = r'(<div class="staging-tabs-container">\s*<button class="staging-tab-btn"[^>]*onclick="filterStagingTopic\(\'all\'\)">\s*<span>⚡</span> Tất Cả Nháp <span class="tab-badge" id="badgeAll">\d+</span>\s*</button>)'
    
    new_tab_btn = f"""\\1
      <button class="staging-tab-btn active" data-industry="trung-tam-anh-ngu" onclick="filterStagingTopic('trung-tam-anh-ngu')">
        <span>🎓</span> Trung Tâm Anh Ngữ <span class="tab-badge" id="badgeAnhNgu">{len(new_candidates)}</span>
      </button>"""
    
    # Bỏ class active ở các tab khác
    script_content = re.sub(r'<button class="staging-tab-btn active"', '<button class="staging-tab-btn"', script_content)
    script_content = re.sub(nav_pattern, new_tab_btn, script_content)

    # Cập nhật default topic
    script_content = re.sub(
        r"let currentTopic = '[^']+';",
        "let currentTopic = 'trung-tam-anh-ngu';",
        script_content
    )
    
    # Cập nhật danh sách topic
    script_content = script_content.replace(
        "['all', 'mua-ban-oto-cu'",
        "['all', 'trung-tam-anh-ngu', 'mua-ban-oto-cu'"
    )
    if "'trung-tam-anh-ngu'" not in script_content:
        script_content = script_content.replace(
            "['all',",
            "['all', 'trung-tam-anh-ngu',"
        )

    # Cập nhật topicMapName
    old_topic_map = "const topicMapName = {"
    new_topic_map = """const topicMapName = {
      'trung-tam-anh-ngu': 'Trung Tâm Anh Ngữ (Top Chuỗi & Luyện Thi)',"""
    script_content = script_content.replace(old_topic_map, new_topic_map)

    # Cập nhật statTopicName mặc định
    script_content = re.sub(
        r'Chủ đề đang xem: <b id="statTopicName"[^>]*>[^<]+</b>',
        'Chủ đề đang xem: <b id="statTopicName" style="color:#fff;">Trung Tâm Anh Ngữ (Chuẩn Quốc Tế & CRO)</b>',
        script_content
    )

    with open(build_staging_script, "w", encoding="utf-8") as f:
        f.write(script_content)
    print("[+] Đã cập nhật build_multi_staging.py với tab Trung Tâm Anh Ngữ!")
else:
    print("[*] Tab trung-tam-anh-ngu đã tồn tại trong build_multi_staging.py.")

# 4. Chạy build_multi_staging.py để tạo web_nhap_staging.html
import subprocess
result = subprocess.run([sys.executable, build_staging_script], capture_output=True, text=True, encoding="utf-8")
print("[+] Kết quả build staging:", result.stdout)
if result.stderr:
    print("[-] Build stderr:", result.stderr)

print("[+] Hoàn tất tích hợp Trung Tâm Anh Ngữ vào WebVault Staging!")
