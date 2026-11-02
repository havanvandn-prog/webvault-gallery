# -*- coding: utf-8 -*-
import os
import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
candidates_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "staging_all_candidates.json")
staging_html = os.path.join(BASE_DIR, "web_nhap_staging.html")

staging_item = {
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

# 1. Cập nhật staging_all_candidates.json
with open(candidates_file, "r", encoding="utf-8") as f:
    candidates = json.load(f)

# Kiểm tra nếu đã có
candidates = [c for c in candidates if c.get("domain") != "hasselblad.com"]
candidates.insert(0, staging_item)

with open(candidates_file, "w", encoding="utf-8") as f:
    json.dump(candidates, f, ensure_ascii=False, indent=2)

print(f"[+] Đã cập nhật staging_all_candidates.json ({len(candidates)} mẫu)")

# 2. Cập nhật web_nhap_staging.html
with open(staging_html, "r", encoding="utf-8") as f:
    content = f.read()

# Cập nhật mảng CANDIDATES trong web_nhap_staging.html
# Tìm khối const CANDIDATES = [...]
pattern = re.compile(r'const CANDIDATES = \[.*?\];\s*(?:const|let|var|function)', re.DOTALL)
m = pattern.search(content)
if m:
    # Thay thế
    formatted_cand = json.dumps(candidates, ensure_ascii=False, indent=2)
    new_decl = f"const CANDIDATES = {formatted_cand};\n\n  "
    content = content[:m.start()] + new_decl + content[m.end() - len(m.group(0).split()[-1]) - 1:]
    print("[+] Đã cập nhật mảng CANDIDATES trong web_nhap_staging.html!")
else:
    print("[-] Không tìm thấy const CANDIDATES trong web_nhap_staging.html!")

# Thêm tab button Máy Chụp Ảnh nếu chưa có
tab_target = '<button class="staging-tab-btn" data-industry="all" onclick="filterStagingTopic(\'all\')">'
new_tab = """<button class="staging-tab-btn" data-industry="ban-may-anh" onclick="filterStagingTopic('ban-may-anh')">
        <span>📷</span> Máy Chụp Ảnh <span class="tab-badge" id="badgeMayAnh">1</span>
      </button>"""

if 'data-industry="ban-may-anh"' not in content:
    # Chèn sau nút Tất Cả Nháp
    end_of_all_btn = content.find('</button>', content.find(tab_target)) + len('</button>')
    content = content[:end_of_all_btn] + '\n      ' + new_tab + content[end_of_all_btn:]
    print("[+] Đã thêm tab 'Máy Chụp Ảnh' vào web_nhap_staging.html!")

# Cập nhật badgeAll
badge_all_match = re.search(r'<span class="tab-badge" id="badgeAll">\d+</span>', content)
if badge_all_match:
    content = content[:badge_all_match.start()] + f'<span class="tab-badge" id="badgeAll">{len(candidates)}</span>' + content[badge_all_match.end():]

with open(staging_html, "w", encoding="utf-8") as f:
    f.write(content)

print("[SUCCESS] Đã cập nhật web_nhap_staging.html thành công!")
