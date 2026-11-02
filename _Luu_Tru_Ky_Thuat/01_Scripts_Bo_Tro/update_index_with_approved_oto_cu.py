# -*- coding: utf-8 -*-
import os
import sys
import json
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
index_path = os.path.join(BASE_DIR, "index.html")
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "mua_ban_oto_cu_metadata.json")
kho_webp = os.path.join(BASE_DIR, "Kho_Anh_Webp")

# 7 website người dùng đã duyệt
approved_domains = [
    'carpla.vn',
    'vucar.vn',
    'thegioixeduc.vn',
    'sieuthiotosaigon.vn',
    'chootoso1hanoi.com',
    'xeluottoantrung.com',
    'sieuthiotoluot.vn'
]

with open(metadata_file, "r", encoding="utf-8") as f:
    all_metadata = json.load(f)

with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Trích xuất WEBSITES_DATA hiện tại
m = re.search(r'const WEBSITES_DATA = (\[.*?\]);', content, re.DOTALL)
if not m:
    print("[-] Không tìm thấy WEBSITES_DATA trong index.html!")
    sys.exit(1)

websites_data = json.loads(m.group(1))

# Loại bỏ các mục mua-ban-oto-cu cũ nếu có
websites_data = [w for w in websites_data if w.get("industry") != "mua-ban-oto-cu"]

start_id = len(websites_data) + 1

# Tạo 7 đối tượng mới
matched_items = []
for d in approved_domains:
    found = next((item for item in all_metadata if d in item['url'] or d in item['domain']), None)
    if not found:
        print(f"[-] Cảnh báo: Không tìm thấy domain {d}")
        continue

    slug = found['slug']
    thumb_path = os.path.join(kho_webp, f"{slug}_thumb.webp")
    full_path = os.path.join(kho_webp, f"{slug}_full.webp")
    fb_path = os.path.join(kho_webp, f"{slug}_fb.png")

    thumb_kb = round(os.path.getsize(thumb_path) / 1024, 1) if os.path.exists(thumb_path) else 150.0
    full_kb = round(os.path.getsize(full_path) / 1024, 1) if os.path.exists(full_path) else 750.0
    fb_kb = round(os.path.getsize(fb_path) / 1024, 1) if os.path.exists(fb_path) else 1200.0

    current_id_str = f"{start_id:02d}"
    start_id += 1

    matched_items.append({
        "id": current_id_str,
        "name": found["name"],
        "short_name": found.get("short_name", found["name"]),
        "url": found["url"],
        "domain": found["domain"],
        "industry": "mua-ban-oto-cu",
        "tag": found.get("tag", "oto-cu"),
        "vibe": found.get("vibe", "corporate"),
        "vibe_name": found.get("vibe_name", "Uy tín & Tối ưu chuyển đổi"),
        "location": found["location"],
        "desc": found["desc"],
        "thumb": f"Kho_Anh_Webp/{slug}_thumb.webp",
        "full": f"Kho_Anh_Webp/{slug}_full.webp",
        "fb": f"Kho_Anh_Webp/{slug}_fb.png",
        "thumb_kb": thumb_kb,
        "full_kb": full_kb,
        "fb_kb": fb_kb
    })

updated_websites_data = websites_data + matched_items
total_count = len(updated_websites_data)
oto_cu_count = len(matched_items)

print(f"[+] Đã chuẩn bị {oto_cu_count} mẫu xe ô tô cũ được duyệt. Tổng cộng {total_count} website trong WebVault.")

# 2. Cập nhật Sidebar Tier 1
old_sidebar_section = """        <li class="nav-item" onclick="setIndustry('du-hoc-dinh-cu-my', this)">
          <span>Du Học & Định Cư Mỹ</span>
          <span class="nav-count">12</span>
        </li>"""

new_sidebar_section = f"""        <li class="nav-item" onclick="setIndustry('du-hoc-dinh-cu-my', this)">
          <span>Du Học & Định Cư Mỹ</span>
          <span class="nav-count">12</span>
        </li>
        <li class="nav-item" onclick="setIndustry('mua-ban-oto-cu', this)">
          <span>Mua Bán Xe Ô Tô Cũ</span>
          <span class="nav-count">{oto_cu_count}</span>
        </li>"""

if 'onclick="setIndustry(\'mua-ban-oto-cu\'' not in content:
    content = content.replace(old_sidebar_section, new_sidebar_section)
    print("[+] Đã thêm tab 'Mua Bán Xe Ô Tô Cũ' vào Sidebar!")
else:
    # Cập nhật số đếm nếu tab đã tồn tại
    content = re.sub(
        r'<li class="nav-item" onclick="setIndustry\(\'mua-ban-oto-cu\', this\)">\s*<span>Mua Bán Xe Ô Tô Cũ</span>\s*<span class="nav-count">\d+</span>\s*</li>',
        f'<li class="nav-item" onclick="setIndustry(\'mua-ban-oto-cu\', this)">\n          <span>Mua Bán Xe Ô Tô Cũ</span>\n          <span class="nav-count">{oto_cu_count}</span>\n        </li>',
        content
    )

# 3. Cập nhật countAll
content = re.sub(r'<span class="nav-count" id="countAll">\d+</span>', f'<span class="nav-count" id="countAll">{total_count}</span>', content)

# 4. Cập nhật industryMap trong JavaScript
old_industry_map = """    const industryMap = {
      'all': 'Tất Cả Mẫu Tuyển Chọn',
      'su-kien': 'Sự Kiện & Activation',
      'decor-su-kien': 'Trang Trí & Decor Tiệc',
      'du-lich': 'Du Lịch & Tour Tuyến',
      'du-hoc-dinh-cu-my': 'Du Học & Định Cư Mỹ (Google Ads & CRO)'
    };"""

new_industry_map = """    const industryMap = {
      'all': 'Tất Cả Mẫu Tuyển Chọn',
      'su-kien': 'Sự Kiện & Activation',
      'decor-su-kien': 'Trang Trí & Decor Tiệc',
      'du-lich': 'Du Lịch & Tour Tuyến',
      'du-hoc-dinh-cu-my': 'Du Học & Định Cư Mỹ (Google Ads & CRO)',
      'mua-ban-oto-cu': 'Mua Bán Xe Ô Tô Cũ & Xe Lướt (Google Ads & CRO)'
    };"""

content = content.replace(old_industry_map, new_industry_map)

# 5. Thay thế chính xác khối const WEBSITES_DATA = [...] bằng re.sub
formatted_json = json.dumps(updated_websites_data, ensure_ascii=False, indent=4)
new_var_declaration = f"const WEBSITES_DATA = {formatted_json};"

pattern = re.compile(r'const WEBSITES_DATA = \[.*?\];', re.DOTALL)
content, count = pattern.subn(lambda m: new_var_declaration, content, count=1)

if count == 1:
    print("[+] Đã thay thế thành công khối const WEBSITES_DATA bằng re.subn!")
else:
    print("[-] Lỗi: Không thể thay thế khối WEBSITES_DATA!")
    sys.exit(1)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"[+] Đã nạp thành công {oto_cu_count} mẫu được duyệt vào index.html!")
