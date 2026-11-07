# -*- coding: utf-8 -*-
import os
import sys
import json
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
index_path = os.path.join(BASE_DIR, "index.html")
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "cafe_banh_mi_metadata.json")
kho_webp = os.path.join(BASE_DIR, "Kho_Anh_Webp")

# 5 website người dùng đã duyệt
approved_domains = [
    'dropincafe.com.vn',
    'banhmigac.com',
    'banconghanoi.com',
    'taobanhmicafe.com',
    'banhmihuynhhoa.vn'
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

# Loại bỏ các mục cafe-va-banh-mi cũ nếu có
websites_data = [w for w in websites_data if w.get("industry") != "cafe-va-banh-mi"]

start_id = len(websites_data) + 1

# Tạo 5 đối tượng mới
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
        "industry": "cafe-va-banh-mi",
        "tag": found.get("tag", "cafe-banh-mi"),
        "vibe": found.get("vibe", "Hiện Đại & Trực Quan"),
        "vibe_name": found.get("vibe_name", found.get("vibe", "Hiện Đại & Trực Quan")),
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
cafe_count = len(matched_items)

print(f"[+] Đã chuẩn bị {cafe_count} mẫu Cafe & Bánh Mì được duyệt. Tổng cộng {total_count} website trong WebVault.")

# 2. Cập nhật Sidebar Tier 1
old_sidebar_anchor = """        <li class="nav-item" onclick="setIndustry('ban-may-anh', this)">
          <span>Máy Chụp Ảnh & Nhiếp Ảnh</span>
          <span class="nav-count">1</span>
        </li>"""

new_sidebar_section = f"""        <li class="nav-item" onclick="setIndustry('ban-may-anh', this)">
          <span>Máy Chụp Ảnh & Nhiếp Ảnh</span>
          <span class="nav-count">1</span>
        </li>
        <li class="nav-item" onclick="setIndustry('cafe-va-banh-mi', this)">
          <span>Cafe & Bánh Mì (F&B)</span>
          <span class="nav-count">{cafe_count}</span>
        </li>"""

if 'onclick="setIndustry(\'cafe-va-banh-mi\'' not in content:
    content = content.replace(old_sidebar_anchor, new_sidebar_section)
    print("[+] Đã thêm tab 'Cafe & Bánh Mì (F&B)' vào Sidebar!")
else:
    # Cập nhật số đếm nếu tab đã tồn tại
    content = re.sub(
        r'<li class="nav-item" onclick="setIndustry\(\'cafe-va-banh-mi\', this\)">\s*<span>Cafe & Bánh Mì \(F&B\)</span>\s*<span class="nav-count">\d+</span>\s*</li>',
        f'<li class="nav-item" onclick="setIndustry(\'cafe-va-banh-mi\', this)">\n          <span>Cafe & Bánh Mì (F&B)</span>\n          <span class="nav-count">{cafe_count}</span>\n        </li>',
        content
    )

# 3. Cập nhật countAll
content = re.sub(r'<span class="nav-count" id="countAll">\d+</span>', f'<span class="nav-count" id="countAll">{total_count}</span>', content)

# 4. Cập nhật industryMap trong JavaScript
old_industry_map_anchor = "'ban-may-anh': 'Máy Chụp Ảnh & Thiết Bị Nhiếp Ảnh'"
new_industry_map_section = "'ban-may-anh': 'Máy Chụp Ảnh & Thiết Bị Nhiếp Ảnh',\n      'cafe-va-banh-mi': 'Cafe & Bánh Mì (Menu & Quán F&B Chuẩn Hà Nội)'"

if "'cafe-va-banh-mi'" not in content:
    content = content.replace(old_industry_map_anchor, new_industry_map_section)
    print("[+] Đã thêm 'cafe-va-banh-mi' vào industryMap!")

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

print(f"[+] Đã nạp thành công {cafe_count} mẫu Cafe & Bánh Mì được duyệt vào index.html!")
