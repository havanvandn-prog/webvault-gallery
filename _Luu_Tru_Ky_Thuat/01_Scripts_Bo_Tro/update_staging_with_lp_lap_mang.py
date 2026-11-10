# -*- coding: utf-8 -*-
import json
import os
import subprocess
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
candidates_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "staging_all_candidates.json")
lp_meta_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "landing_page_lap_mang_metadata.json")
build_staging_script = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "01_Scripts_Bo_Tro", "build_multi_staging.py")

# 1. Đọc metadata Landing Page Lắp Mạng mới chụp
if not os.path.exists(lp_meta_file):
    print("[-] Chưa có file landing_page_lap_mang_metadata.json!")
    sys.exit(1)

with open(lp_meta_file, "r", encoding="utf-8") as f:
    lp_items = json.load(f)

# 2. Đọc staging_all_candidates.json hiện tại và ghép dữ liệu không trùng lặp
all_candidates = []
if os.path.exists(candidates_file):
    with open(candidates_file, "r", encoding="utf-8") as f:
        all_candidates = json.load(f)

all_candidates = [c for c in all_candidates if c.get("industry") != "landing-page-lap-mang"]

lp_candidates = []
for d in lp_items:
    lp_candidates.append({
        "id": d["id"],
        "industry": d.get("industry", "landing-page-lap-mang"),
        "industry_name": d.get("industry_name", "Landing Page Lắp Mạng"),
        "name": d["name"],
        "short_name": d.get("short_name", d["name"]),
        "url": d["url"],
        "domain": d["domain"],
        "vibe": d.get("vibe", "1-Page Chuẩn Chuyển Đổi"),
        "location": d["location"],
        "thumb": d.get("thumb") or f"Kho_Anh_Webp/{d['slug']}_thumb.webp",
        "full": d.get("full") or f"Kho_Anh_Webp/{d['slug']}_full.webp",
        "desc": d["desc"]
    })

updated_all_candidates = lp_candidates + all_candidates

with open(candidates_file, "w", encoding="utf-8") as f:
    json.dump(updated_all_candidates, f, ensure_ascii=False, indent=2)

print(f"[+] Đã cập nhật staging_all_candidates.json: {len(updated_all_candidates)} mẫu (trong đó {len(lp_candidates)} Landing Page Lắp Mạng).")

# 3. Cập nhật build_multi_staging.py (thêm tab Landing Page Lắp Mạng + sửa bug URL/Badge)
with open(build_staging_script, "r", encoding="utf-8") as f:
    code = f.read().replace("\r\n", "\n")

# 3a. Thêm tab Landing Page Lắp Mạng lên đầu (active) & bỏ active tab Lắp Mạng FPT
lp_tab_html = """      <button class="staging-tab-btn active" data-industry="landing-page-lap-mang" onclick="filterStagingTopic('landing-page-lap-mang')">
        <span>🎯</span> Landing Page Lắp Mạng <span class="tab-badge" id="badgeLpLapMang">20</span>
      </button>"""

if 'data-industry="landing-page-lap-mang"' not in code:
    old_fpt_tab = """      <button class="staging-tab-btn active" data-industry="lap-mang-fpt" onclick="filterStagingTopic('lap-mang-fpt')">"""
    new_fpt_tab = f"""{lp_tab_html}
      <button class="staging-tab-btn" data-industry="lap-mang-fpt" onclick="filterStagingTopic('lap-mang-fpt')">"""
    assert old_fpt_tab in code, "Không tìm thấy tab lap-mang-fpt active trong build_multi_staging.py"
    code = code.replace(old_fpt_tab, new_fpt_tab, 1)

# Cập nhật badgeAll ban đầu & fallback header topic text
code = code.replace('<span class="tab-badge" id="badgeAll">121</span>', f'<span class="tab-badge" id="badgeAll">{len(updated_all_candidates)}</span>')
code = code.replace(
    'Chủ đề đang xem: <b id="statTopicName" style="color:#fff;">Cafe & Bánh Mì (Menu & Quán F&B Chuẩn Hà Nội)</b>',
    'Chủ đề đang xem: <b id="statTopicName" style="color:#fff;">Landing Page Lắp Đặt Mạng Internet & FPT (1-Page Chuẩn Chuyển Đổi Google Ads)</b>'
)

# 3b. Sửa currentTopic & initTopicFromUrl để nhận mọi tab động từ DOM
old_init_block = """  let currentTopic = 'lap-mang-fpt';

  function initTopicFromUrl() {
    const params = new URLSearchParams(window.location.search);
    const indParam = params.get('industry') || params.get('topic') || 'lap-mang-fpt';
    if (indParam && ['all', 'ban-may-anh', 'mua-ban-oto-cu', 'du-hoc-dinh-cu-my', 'phong-tap-fitness', 'ban-dong-ho', 'decor-su-kien', 'tiec-cuoi'].includes(indParam)) {
      currentTopic = indParam;
    }
  }"""

new_init_block = """  let currentTopic = 'landing-page-lap-mang';

  function initTopicFromUrl() {
    const params = new URLSearchParams(window.location.search);
    const indParam = params.get('industry') || params.get('topic') || 'landing-page-lap-mang';
    const validTopics = Array.from(document.querySelectorAll('.staging-tab-btn')).map(btn => btn.dataset.industry);
    if (indParam && validTopics.includes(indParam)) {
      currentTopic = indParam;
    }
  }"""

if old_init_block in code:
    code = code.replace(old_init_block, new_init_block, 1)

# 3c. Hiển thị subpath thay vì chỉ domain trên card browser bar để phân biệt nhiều LP cùng domain (fpt.vn, w.tuybutky.com)
old_pill_line = """          <a href="${item.url}" target="_blank" class="browser-url-pill">https://${item.domain}/</a>"""
new_pill_line = """          <a href="${item.url}" target="_blank" class="browser-url-pill" title="${item.url}">${(item.url || '').replace(/^https?:\\/\\//, '') || item.domain}</a>"""
if old_pill_line in code:
    code = code.replace(old_pill_line, new_pill_line, 1)

code = code.replace("${item.industry_name || 'Đồng Hồ'}", "${item.industry_name || 'Mẫu Web'}")

# 3d. Cập nhật topicMapName
old_topic_map = """    const topicMapName = {
      'lap-mang-fpt': 'Lắp Đặt Mạng Cáp Quang FPT Telecom (Mẫu Tối Ưu Google Ads & Chuyển Đổi Cao)',"""
new_topic_map = """    const topicMapName = {
      'landing-page-lap-mang': 'Landing Page Lắp Đặt Mạng Internet & FPT (1-Page Chuẩn Chuyển Đổi Google Ads)',
      'lap-mang-fpt': 'Lắp Đặt Mạng Cáp Quang FPT Telecom (Mẫu Tối Ưu Google Ads & Chuyển Đổi Cao)',
      'mua-ban-oto-cu': 'Mua Bán Xe Ô Tô Cũ',"""
if "'landing-page-lap-mang':" not in code and old_topic_map in code:
    code = code.replace(old_topic_map, new_topic_map, 1)

# 3e. Cập nhật toàn bộ badge count động theo CANDIDATES
old_badges_block = """    if (document.getElementById('badgeAll')) document.getElementById('badgeAll').textContent = CANDIDATES.length;
    if (document.getElementById('badgeOtoCu')) document.getElementById('badgeOtoCu').textContent = CANDIDATES.filter(c => c.industry === 'mua-ban-oto-cu').length;
    if (document.getElementById('badgeDuHocDinhCu')) document.getElementById('badgeDuHocDinhCu').textContent = CANDIDATES.filter(c => c.industry === 'du-hoc-dinh-cu-my').length;
    if (document.getElementById('badgeFitness')) document.getElementById('badgeFitness').textContent = CANDIDATES.filter(c => c.industry === 'phong-tap-fitness').length;
    if (document.getElementById('badgeDongHo')) document.getElementById('badgeDongHo').textContent = CANDIDATES.filter(c => c.industry === 'ban-dong-ho').length;
    if (document.getElementById('badgeDecor')) document.getElementById('badgeDecor').textContent = CANDIDATES.filter(c => c.industry === 'decor-su-kien').length;
    if (document.getElementById('badgeWedding')) document.getElementById('badgeWedding').textContent = CANDIDATES.filter(c => c.industry === 'tiec-cuoi').length;"""

new_badges_block = """    if (document.getElementById('badgeAll')) document.getElementById('badgeAll').textContent = CANDIDATES.length;
    if (document.getElementById('badgeLpLapMang')) document.getElementById('badgeLpLapMang').textContent = CANDIDATES.filter(c => c.industry === 'landing-page-lap-mang').length;
    if (document.getElementById('badgeFpt')) document.getElementById('badgeFpt').textContent = CANDIDATES.filter(c => c.industry === 'lap-mang-fpt').length;
    if (document.getElementById('badgeCafeBanhMi')) document.getElementById('badgeCafeBanhMi').textContent = CANDIDATES.filter(c => c.industry === 'cafe-va-banh-mi').length;
    if (document.getElementById('badgeAnhNgu')) document.getElementById('badgeAnhNgu').textContent = CANDIDATES.filter(c => c.industry === 'trung-tam-anh-ngu').length;
    if (document.getElementById('badgeMayAnh')) document.getElementById('badgeMayAnh').textContent = CANDIDATES.filter(c => c.industry === 'ban-may-anh').length;
    if (document.getElementById('badgeOtoCu')) document.getElementById('badgeOtoCu').textContent = CANDIDATES.filter(c => c.industry === 'mua-ban-oto-cu').length;
    if (document.getElementById('badgeDuHocDinhCu')) document.getElementById('badgeDuHocDinhCu').textContent = CANDIDATES.filter(c => c.industry === 'du-hoc-dinh-cu-my').length;
    if (document.getElementById('badgeFitness')) document.getElementById('badgeFitness').textContent = CANDIDATES.filter(c => c.industry === 'phong-tap-fitness').length;
    if (document.getElementById('badgeDongHo')) document.getElementById('badgeDongHo').textContent = CANDIDATES.filter(c => c.industry === 'ban-dong-ho').length;
    if (document.getElementById('badgeDecor')) document.getElementById('badgeDecor').textContent = CANDIDATES.filter(c => c.industry === 'decor-su-kien').length;
    if (document.getElementById('badgeWedding')) document.getElementById('badgeWedding').textContent = CANDIDATES.filter(c => c.industry === 'tiec-cuoi').length;"""

if old_badges_block in code:
    code = code.replace(old_badges_block, new_badges_block, 1)

with open(build_staging_script, "w", encoding="utf-8") as f:
    f.write(code)

print("[+] Đã cập nhật build_multi_staging.py thành công!")

# 4. Chạy lại build_multi_staging.py
result = subprocess.run([sys.executable, build_staging_script], capture_output=True, text=True, encoding="utf-8")
print("[+] Kết quả build_multi_staging.py:")
print(result.stdout)
if result.stderr:
    print("[-] Lỗi:", result.stderr)
if result.returncode != 0:
    sys.exit(result.returncode)
