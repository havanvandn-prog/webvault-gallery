# -*- coding: utf-8 -*-
import json
import os
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
pt_meta_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "phong_thuy_metadata.json")
staging_json_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "staging_all_candidates.json")
build_script_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "01_Scripts_Bo_Tro", "build_multi_staging.py")

with open(pt_meta_path, "r", encoding="utf-8") as f:
    pt_data = json.load(f)

with open(staging_json_path, "r", encoding="utf-8") as f:
    existing = json.load(f)

# Loại bỏ bản cũ của phong-thuy nếu chạy lại
existing_filtered = [item for item in existing if item.get("industry") != "phong-thuy"]
merged = pt_data + existing_filtered

with open(staging_json_path, "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

print(f"[+] Đã gộp {len(pt_data)} mẫu Phong thủy vào staging_all_candidates.json (Tổng: {len(merged)} mẫu)")

# Cập nhật build_multi_staging.py
with open(build_script_path, "r", encoding="utf-8") as f:
    text = f.read()

if 'data-industry="phong-thuy"' not in text:
    # 1. Cập nhật Tabs & chuyển active sang phong-thuy
    old_tabs = """      <button class="staging-tab-btn" data-industry="all" onclick="filterStagingTopic('all')">
        <span>⚡</span> Tất Cả Nháp <span class="tab-badge" id="badgeAll">241</span>
      </button>
      <button class="staging-tab-btn active" data-industry="phong-kham-thu-y" onclick="filterStagingTopic('phong-kham-thu-y')">"""

    new_tabs = f"""      <button class="staging-tab-btn" data-industry="all" onclick="filterStagingTopic('all')">
        <span>⚡</span> Tất Cả Nháp <span class="tab-badge" id="badgeAll">{len(merged)}</span>
      </button>
      <button class="staging-tab-btn active" data-industry="phong-thuy" onclick="filterStagingTopic('phong-thuy')">
        <span>☯️</span> Phong Thủy <span class="tab-badge" id="badgePhongThuy">{len(pt_data)}</span>
      </button>
      <button class="staging-tab-btn" data-industry="phong-kham-thu-y" onclick="filterStagingTopic('phong-kham-thu-y')">"""

    assert old_tabs in text, "Không tìm thấy old_tabs trong build_multi_staging.py"
    text = text.replace(old_tabs, new_tabs, 1)

    # 2. Cập nhật default topic
    old_topic = "let currentTopic = 'phong-kham-thu-y';"
    new_topic = "let currentTopic = 'phong-thuy';"
    assert old_topic in text, "Không tìm thấy old_topic"
    text = text.replace(old_topic, new_topic, 1)

    old_param = "const indParam = params.get('industry') || params.get('topic') || 'phong-kham-thu-y';"
    new_param = "const indParam = params.get('industry') || params.get('topic') || 'phong-thuy';"
    assert old_param in text, "Không tìm thấy old_param"
    text = text.replace(old_param, new_param, 1)

    # 3. Cập nhật topicMapName
    old_map = "const topicMapName = {"
    new_map = """const topicMapName = {
      'phong-thuy': 'Phong Thủy, Kiến Trúc Tâm Linh & Vật Phẩm Đá Quý (Quốc Tế & Top SEO Việt Nam)',"""
    assert old_map in text, "Không tìm thấy old_map"
    text = text.replace(old_map, new_map, 1)

    # 4. Cập nhật badgePhongThuy
    old_badge = "if (document.getElementById('badgeThuY'))"
    new_badge = """if (document.getElementById('badgePhongThuy')) document.getElementById('badgePhongThuy').textContent = CANDIDATES.filter(c => c.industry === 'phong-thuy').length;
    if (document.getElementById('badgeThuY'))"""
    assert old_badge in text, "Không tìm thấy old_badge"
    text = text.replace(old_badge, new_badge, 1)

    with open(build_script_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("[+] Đã cập nhật build_multi_staging.py thành công!")
else:
    print("[i] build_multi_staging.py đã có tab phong-thuy từ trước.")
