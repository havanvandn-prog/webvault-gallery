# -*- coding: utf-8 -*-
import os, sys, json, re

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
candidates_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "staging_all_candidates.json")
builder_script = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "01_Scripts_Bo_Tro", "build_multi_staging.py")

# 1. Update staging_all_candidates.json
with open(candidates_file, "r", encoding="utf-8") as f:
    candidates = json.load(f)

hasselblad_candidate = {
    "id": "mayanh01",
    "industry": "ban-may-anh",
    "industry_name": "Máy Chụp Ảnh & Thiết Bị Nhiếp Ảnh",
    "name": "Hasselblad",
    "short_name": "Hasselblad",
    "url": "https://www.hasselblad.com/",
    "domain": "hasselblad.com",
    "vibe": "Đẳng cấp, Tinh giản & Nghệ thuật Thụy Điển",
    "location": "Thụy Điển / Toàn cầu",
    "thumb": "Kho_Anh_Webp/hasselblad_com_thumb.webp",
    "full": "Kho_Anh_Webp/hasselblad_com_full.webp",
    "desc": "Thương hiệu máy ảnh Medium Format huyền thoại của Thụy Điển với hơn 80 năm di sản quang học đỉnh cao. Website mang phong cách tối giản Scandinavian đặc trưng, phô diễn trọn vẹn chất lượng ảnh 100MP, tái tạo màu sắc chân thực HNCS và trải nghiệm thị giác ấn tượng."
}

candidates = [c for c in candidates if c.get("domain") != "hasselblad.com"]
candidates.insert(0, hasselblad_candidate)

with open(candidates_file, "w", encoding="utf-8") as f:
    json.dump(candidates, f, ensure_ascii=False, indent=2)

print(f"[+] Đã cập nhật staging_all_candidates.json: {len(candidates)} mẫu")

# 2. Update build_multi_staging.py
with open(builder_script, "r", encoding="utf-8") as f:
    code = f.read()

# Tab HTML
tab_btn = """      <button class="staging-tab-btn" data-industry="ban-may-anh" onclick="filterStagingTopic('ban-may-anh')">
        <span>📷</span> Máy Chụp Ảnh <span class="tab-badge" id="badgeMayAnh">1</span>
      </button>"""

if 'data-industry="ban-may-anh"' not in code:
    code = code.replace(
        """      <button class="staging-tab-btn" data-industry="all" onclick="filterStagingTopic('all')">
        <span>⚡</span> Tất Cả Nháp <span class="tab-badge" id="badgeAll">120</span>
      </button>""",
        """      <button class="staging-tab-btn" data-industry="all" onclick="filterStagingTopic('all')">
        <span>⚡</span> Tất Cả Nháp <span class="tab-badge" id="badgeAll">121</span>
      </button>\n""" + tab_btn
    )

# initTopicFromUrl
code = code.replace(
    "['all', 'mua-ban-oto-cu'",
    "['all', 'ban-may-anh', 'mua-ban-oto-cu'"
)

# topicMapName
if "'ban-may-anh':" not in code:
    code = code.replace(
        """    const topicMapName = {
      'all': 'Tất Cả Nháp Chờ Duyệt',""",
        """    const topicMapName = {
      'all': 'Tất Cả Nháp Chờ Duyệt',
      'ban-may-anh': 'Máy Chụp Ảnh & Thiết Bị Nhiếp Ảnh (Google Ads & CRO)',"""
    )

# badge
if "badgeMayAnh" not in code:
    code = code.replace(
        "if (document.getElementById('badgeOtoCu'))",
        "if (document.getElementById('badgeMayAnh')) document.getElementById('badgeMayAnh').textContent = CANDIDATES.filter(c => c.industry === 'ban-may-anh').length;\n    if (document.getElementById('badgeOtoCu'))"
    )

with open(builder_script, "w", encoding="utf-8") as f:
    f.write(code)

print("[+] Đã cập nhật build_multi_staging.py!")
