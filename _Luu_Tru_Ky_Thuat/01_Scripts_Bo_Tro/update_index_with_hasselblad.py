# -*- coding: utf-8 -*-
import os
import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
index_path = os.path.join(BASE_DIR, "index.html")
kho_webp = os.path.join(BASE_DIR, "Kho_Anh_Webp")
metadata_dir = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test")

# 1. Tạo file metadata cho ngành Bán Máy Chụp Ảnh
metadata_file = os.path.join(metadata_dir, "ban_may_anh_metadata.json")
may_anh_item = {
    "id": "mayanh01",
    "name": "Hasselblad",
    "short_name": "Hasselblad",
    "url": "https://www.hasselblad.com/",
    "domain": "hasselblad.com",
    "slug": "hasselblad_com",
    "industry": "ban-may-anh",
    "category": "Medium Format & Luxury Cameras",
    "category_vn": "Máy Ảnh Medium Format & Xa Xỉ",
    "tag": "may-anh-medium-format",
    "vibe": "nordic-minimalist-luxury",
    "vibe_name": "Đẳng cấp, Tinh giản & Nghệ thuật Thụy Điển",
    "location": "Thụy Điển / Toàn cầu",
    "desc": "Thương hiệu máy ảnh Medium Format huyền thoại của Thụy Điển với hơn 80 năm di sản quang học đỉnh cao. Website mang phong cách tối giản Scandinavian đặc trưng, phô diễn trọn vẹn chất lượng ảnh 100MP, tái sinh màu sắc tự nhiên HNCS và hệ sinh thái máy ảnh chuyên nghiệp.",
    "image": "Anh_Chup_Website/hasselblad.com.png",
    "thumb": "Kho_Anh_Webp/hasselblad_com_thumb.webp",
    "full": "Kho_Anh_Webp/hasselblad_com_full.webp",
    "fb": "Kho_Anh_Webp/hasselblad_com_fb.png",
    "thumb_kb": 62.5,
    "full_kb": 310.2,
    "fb_kb": 1120.6,
    "status": "SUCCESS"
}

with open(metadata_file, "w", encoding="utf-8") as f:
    json.dump([may_anh_item], f, ensure_ascii=False, indent=2)
print(f"[+] Đã ghi metadata: {metadata_file}")

# 2. Đọc index.html
with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

# Trích xuất WEBSITES_DATA hiện tại
m = re.search(r'const WEBSITES_DATA = (\[.*?\]);', content, re.DOTALL)
if not m:
    print("[-] Không tìm thấy WEBSITES_DATA trong index.html!")
    sys.exit(1)

websites_data = json.loads(m.group(1))

# Kiểm tra xem Hasselblad đã có chưa
existing = next((w for w in websites_data if "hasselblad.com" in w.get("url", "") or w.get("domain") == "hasselblad.com"), None)
if existing:
    print("[*] Hasselblad đã có trong WEBSITES_DATA, tiến hành cập nhật...")
    websites_data = [w for w in websites_data if w.get("domain") != "hasselblad.com"]

new_id = f"{len(websites_data) + 1:02d}"

new_entry = {
    "id": new_id,
    "name": "Hasselblad",
    "short_name": "Hasselblad",
    "url": "https://www.hasselblad.com/",
    "domain": "hasselblad.com",
    "industry": "ban-may-anh",
    "tag": "may-anh-medium-format",
    "vibe": "nordic-minimalist-luxury",
    "vibe_name": "Đẳng cấp, Tinh giản & Nghệ thuật Thụy Điển",
    "location": "Thụy Điển / Toàn cầu",
    "desc": "Thương hiệu máy ảnh Medium Format huyền thoại của Thụy Điển với hơn 80 năm di sản quang học đỉnh cao. Website mang phong cách tối giản Scandinavian đặc trưng, phô diễn trọn vẹn chất lượng ảnh 100MP, tái tạo màu sắc chân thực HNCS và trải nghiệm thị giác ấn tượng.",
    "thumb": "Kho_Anh_Webp/hasselblad_com_thumb.webp",
    "full": "Kho_Anh_Webp/hasselblad_com_full.webp",
    "fb": "Kho_Anh_Webp/hasselblad_com_fb.png",
    "thumb_kb": 62.5,
    "full_kb": 310.2,
    "fb_kb": 1120.6
}

websites_data.append(new_entry)
total_count = len(websites_data)
may_anh_count = len([w for w in websites_data if w.get("industry") == "ban-may-anh"])

print(f"[+] Tổng số website sau khi nạp: {total_count} (Ngành Máy Chụp Ảnh: {may_anh_count})")

# 3. Cập nhật Sidebar Tier 1 trong index.html
old_nav_target = """        <li class="nav-item" onclick="setIndustry('mua-ban-oto-cu', this)">
          <span>Mua Bán Xe Ô Tô Cũ</span>
          <span class="nav-count">7</span>
        </li>"""

may_anh_nav = f"""        <li class="nav-item" onclick="setIndustry('mua-ban-oto-cu', this)">
          <span>Mua Bán Xe Ô Tô Cũ</span>
          <span class="nav-count">7</span>
        </li>
        <li class="nav-item" onclick="setIndustry('ban-may-anh', this)">
          <span>Máy Chụp Ảnh & Nhiếp Ảnh</span>
          <span class="nav-count">{may_anh_count}</span>
        </li>"""

if "onclick=\"setIndustry('ban-may-anh'" not in content:
    content = content.replace(old_nav_target, may_anh_nav)
    print("[+] Đã chèn tab 'Máy Chụp Ảnh & Nhiếp Ảnh' vào Sidebar!")
else:
    content = re.sub(
        r'<li class="nav-item" onclick="setIndustry\(\'ban-may-anh\', this\)">\s*<span>Máy Chụp Ảnh & Nhiếp Ảnh</span>\s*<span class="nav-count">\d+</span>\s*</li>',
        f'<li class="nav-item" onclick="setIndustry(\'ban-may-anh\', this)">\n          <span>Máy Chụp Ảnh & Nhiếp Ảnh</span>\n          <span class="nav-count">{may_anh_count}</span>\n        </li>',
        content
    )

# 4. Cập nhật countAll
content = re.sub(r'<span class="nav-count" id="countAll">\d+</span>', f'<span class="nav-count" id="countAll">{total_count}</span>', content)

# 5. Cập nhật industryMap trong JavaScript
old_ind_map = """    const industryMap = {
      'all': 'Tất Cả Mẫu Tuyển Chọn',
      'su-kien': 'Sự Kiện & Activation',
      'decor-su-kien': 'Trang Trí & Decor Tiệc',
      'du-lich': 'Du Lịch & Tour Tuyến',
      'du-hoc-dinh-cu-my': 'Du Học & Định Cư Mỹ (Google Ads & CRO)',
      'mua-ban-oto-cu': 'Mua Bán Xe Ô Tô Cũ & Xe Lướt (Google Ads & CRO)'
    };"""

new_ind_map = """    const industryMap = {
      'all': 'Tất Cả Mẫu Tuyển Chọn',
      'su-kien': 'Sự Kiện & Activation',
      'decor-su-kien': 'Trang Trí & Decor Tiệc',
      'du-lich': 'Du Lịch & Tour Tuyến',
      'du-hoc-dinh-cu-my': 'Du Học & Định Cư Mỹ (Google Ads & CRO)',
      'mua-ban-oto-cu': 'Mua Bán Xe Ô Tô Cũ & Xe Lướt (Google Ads & CRO)',
      'ban-may-anh': 'Máy Chụp Ảnh & Thiết Bị Nhiếp Ảnh'
    };"""

if old_ind_map in content:
    content = content.replace(old_ind_map, new_ind_map)
    print("[+] Đã cập nhật industryMap trong JavaScript!")
elif "'ban-may-anh'" not in content:
    # thay thế nếu có dạng khác
    content = re.sub(
        r"('mua-ban-oto-cu': '[^']+')\s*\n\s*\};",
        r"\1,\n      'ban-may-anh': 'Máy Chụp Ảnh & Thiết Bị Nhiếp Ảnh'\n    };",
        content
    )
    print("[+] Đã bổ sung 'ban-may-anh' vào industryMap qua regex!")

# 6. Thay thế khối WEBSITES_DATA
formatted_json = json.dumps(websites_data, ensure_ascii=False, indent=4)
new_var_declaration = f"const WEBSITES_DATA = {formatted_json};"
pattern = re.compile(r'const WEBSITES_DATA = \[.*?\];', re.DOTALL)
content, count = pattern.subn(lambda m: new_var_declaration, content, count=1)

if count == 1:
    print("[+] Đã cập nhật const WEBSITES_DATA thành công!")
else:
    print("[-] Lỗi: Không thể thay thế WEBSITES_DATA!")
    sys.exit(1)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(content)

print("[SUCCESS] Đã nạp thành công Hasselblad vào index.html!")
