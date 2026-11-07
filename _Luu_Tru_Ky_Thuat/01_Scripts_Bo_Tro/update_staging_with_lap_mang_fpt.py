# -*- coding: utf-8 -*-
import json
import os
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
candidates_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "staging_all_candidates.json")
fpt_meta_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "lap_mang_fpt_metadata.json")
build_staging_script = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "01_Scripts_Bo_Tro", "build_multi_staging.py")

# 1. Đọc metadata FPT mới chụp
if not os.path.exists(fpt_meta_file):
    print("[-] Chưa có file lap_mang_fpt_metadata.json!")
    sys.exit(1)

with open(fpt_meta_file, "r", encoding="utf-8") as f:
    fpt_items = json.load(f)

# 2. Đọc staging_all_candidates.json hiện tại
all_candidates = []
if os.path.exists(candidates_file):
    with open(candidates_file, "r", encoding="utf-8") as f:
        all_candidates = json.load(f)

# Loại bỏ các mục cũ của lap-mang-fpt nếu có để tránh trùng lặp
all_candidates = [c for c in all_candidates if c.get("industry") != "lap-mang-fpt"]

# Thêm 20 ứng viên FPT mới
fpt_candidates = []
for d in fpt_items:
    fpt_candidates.append({
        "id": d["id"],
        "industry": d.get("industry", "lap-mang-fpt"),
        "industry_name": d.get("industry_name", "Lắp Mạng FPT (Google Ads)"),
        "name": d["name"],
        "short_name": d.get("short_name", d["name"]),
        "url": d["url"],
        "domain": d["domain"],
        "vibe": d.get("vibe", "Trực quan & Chuẩn chuyển đổi"),
        "location": d["location"],
        "thumb": d.get("thumb") or f"Kho_Anh_Webp/{d['slug']}_thumb.webp",
        "full": d.get("full") or f"Kho_Anh_Webp/{d['slug']}_full.webp",
        "desc": d["desc"]
    })

# Đưa FPT lên đầu
updated_all_candidates = fpt_candidates + all_candidates

with open(candidates_file, "w", encoding="utf-8") as f:
    json.dump(updated_all_candidates, f, ensure_ascii=False, indent=2)

print(f"[+] Đã lưu tổng cộng {len(updated_all_candidates)} ứng viên vào staging_all_candidates.json (trong đó có {len(fpt_candidates)} mẫu Lắp Mạng FPT)!")

# 3. Cập nhật build_multi_staging.py để có tab Lắp Mạng FPT
with open(build_staging_script, "r", encoding="utf-8") as f:
    code = f.read()

# Kiểm tra nếu chưa có tab lap-mang-fpt
tab_html = """      <button class="staging-tab-btn active" data-industry="lap-mang-fpt" onclick="filterStagingTopic('lap-mang-fpt')">
        <span>🌐</span> Lắp Mạng FPT <span class="tab-badge" id="badgeFpt">20</span>
      </button>"""

if 'data-industry="lap-mang-fpt"' not in code:
    # Thay thế nút cafe-va-banh-mi active thành không active và chèn lap-mang-fpt lên trước
    old_target = """      <button class="staging-tab-btn active" data-industry="cafe-va-banh-mi" onclick="filterStagingTopic('cafe-va-banh-mi')">"""
    new_replacement = f"""{tab_html}
      <button class="staging-tab-btn" data-industry="cafe-va-banh-mi" onclick="filterStagingTopic('cafe-va-banh-mi')">"""
    
    if old_target in code:
        code = code.replace(old_target, new_replacement)
    else:
        # Fallback chèn sau Tất Cả Nháp
        old_all = """      <button class="staging-tab-btn" data-industry="all" onclick="filterStagingTopic('all')">
        <span>⚡</span> Tất Cả Nháp <span class="tab-badge" id="badgeAll">121</span>
      </button>"""
        if old_all in code:
            code = code.replace(old_all, f"{old_all}\n{tab_html}")

    # Thêm vào topicMapName
    old_topic_map = """    const topicMapName = {"""
    new_topic_map = """    const topicMapName = {
      'lap-mang-fpt': 'Lắp Đặt Mạng Cáp Quang FPT Telecom (Mẫu Tối Ưu Google Ads & Chuyển Đổi Cao)',"""
    if old_topic_map in code and "'lap-mang-fpt':" not in code:
        code = code.replace(old_topic_map, new_topic_map)

    # Thêm vào badge count
    old_badge = """    if (document.getElementById('badgeAll')) document.getElementById('badgeAll').textContent = CANDIDATES.length;"""
    new_badge = """    if (document.getElementById('badgeAll')) document.getElementById('badgeAll').textContent = CANDIDATES.length;
    if (document.getElementById('badgeFpt')) document.getElementById('badgeFpt').textContent = CANDIDATES.filter(c => c.industry === 'lap-mang-fpt').length;"""
    if old_badge in code and "badgeFpt" not in code:
        code = code.replace(old_badge, new_badge)

    # Cập nhật defaultTopic
    code = code.replace("let currentTopic = 'cafe-va-banh-mi';", "let currentTopic = 'lap-mang-fpt';")
    code = code.replace("const indParam = params.get('industry') || params.get('topic');", "const indParam = params.get('industry') || params.get('topic') || 'lap-mang-fpt';")

    with open(build_staging_script, "w", encoding="utf-8") as f:
        f.write(code)
    print("[+] Đã cập nhật tab và cấu hình cho build_multi_staging.py!")
else:
    print("[i] Tab lap-mang-fpt đã tồn tại trong build_multi_staging.py.")

# 4. Chạy lại build_multi_staging.py để tạo file web_nhap_staging.html hoàn chỉnh
import subprocess
result = subprocess.run([sys.executable, build_staging_script], capture_output=True, text=True, encoding='utf-8')
print("[+] Kết quả build_multi_staging.py:")
print(result.stdout)
if result.stderr:
    print("[-] Lỗi:", result.stderr)

print("[=== HOÀN TẤT ĐỒNG BỘ STAGING CHO LẮP MẠNG FPT! ===]")
