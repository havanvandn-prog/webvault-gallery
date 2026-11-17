# -*- coding: utf-8 -*-
import os
import sys
import json
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
index_path = os.path.join(BASE_DIR, "index.html")
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "noi_that_metadata.json")
kho_webp = os.path.join(BASE_DIR, "Kho_Anh_Webp")

skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)
from capture_engine import verify_captured_image

approved_domains = [
    'donggia.vn',
    'byzan.vn',
    'noithatmanhhe.vn',
    'noithattugia.com',
    'beyours.vn',
    'minotti.com',
    'poliform.it',
]

with open(metadata_file, "r", encoding="utf-8") as f:
    all_metadata = json.load(f)

with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

m = re.search(r'const WEBSITES_DATA = (\[.*?\]);', content, re.DOTALL)
if not m:
    print("[-] Không tìm thấy WEBSITES_DATA trong index.html!")
    sys.exit(1)

websites_data = json.loads(m.group(1))
websites_data = [w for w in websites_data if w.get("industry") != "noi-that"]

start_id = len(websites_data) + 1
matched_items = []

for d in approved_domains:
    found = next((item for item in all_metadata if item['domain'] == d or d in item['url']), None)
    if not found:
        print(f"[-] Lỗi: Không tìm thấy domain {d}")
        sys.exit(1)

    slug = found['slug']
    thumb_path = os.path.join(kho_webp, f"{slug}_thumb.webp")
    full_path = os.path.join(kho_webp, f"{slug}_full.webp")
    fb_path = os.path.join(kho_webp, f"{slug}_fb.png")

    valid, msg = verify_captured_image(full_path)
    if not valid:
        print(f"[-] Ảnh không đạt QA cho {d}: {msg}")
        sys.exit(1)

    thumb_kb = round(os.path.getsize(thumb_path) / 1024, 1)
    full_kb = round(os.path.getsize(full_path) / 1024, 1)
    fb_kb = round(os.path.getsize(fb_path) / 1024, 1)

    current_id_str = f"{start_id:02d}"
    start_id += 1

    matched_items.append({
        "id": current_id_str,
        "name": found["name"],
        "short_name": found.get("short_name", found["name"]),
        "url": found["url"],
        "domain": found["domain"],
        "industry": "noi-that",
        "tag": found.get("tag", "noi-that"),
        "vibe": found.get("vibe", "Hiện Đại & Sang Trọng"),
        "vibe_name": found.get("vibe_name", found.get("vibe", "Hiện Đại & Sang Trọng")),
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
nt_count = len(matched_items)

print(f"[+] Đã chuẩn bị {nt_count} mẫu Kiến Trúc & Nội Thất được duyệt. Tổng cộng {total_count} website trong WebVault.")

# Xóa placeholder "Kiến Trúc & Nội Thất" (Sắp có) nếu còn
placeholder_pattern = re.compile(
    r'\s*<li class="nav-item" style="opacity: 0\.45; cursor: not-allowed;" title="Sắp nạp dữ liệu">\s*<span>Kiến Trúc & Nội Thất</span>\s*<span class="nav-count">Sắp có</span>\s*</li>',
    re.MULTILINE
)
content = placeholder_pattern.sub("", content)

# Chèn hoặc cập nhật tab noi-that ngay sau cafe-va-banh-mi
if 'onclick="setIndustry(\'noi-that\'' not in content:
    anchor = """        <li class="nav-item" onclick="setIndustry('cafe-va-banh-mi', this)">
          <span>Cafe & Bánh Mì (F&B)</span>
          <span class="nav-count">5</span>
        </li>"""
    replacement = f"""{anchor}
        <li class="nav-item" onclick="setIndustry('noi-that', this)">
          <span>Kiến Trúc & Nội Thất</span>
          <span class="nav-count">{nt_count}</span>
        </li>"""
    assert anchor in content, "Không tìm thấy anchor cafe-va-banh-mi trong Sidebar!"
    content = content.replace(anchor, replacement, 1)
    print("[+] Đã thêm mục 'Kiến Trúc & Nội Thất' vào Sidebar Tier 1!")
else:
    content = re.sub(
        r'<li class="nav-item" onclick="setIndustry\(\'noi-that\', this\)">\s*<span>Kiến Trúc & Nội Thất</span>\s*<span class="nav-count">\d+</span>\s*</li>',
        f'<li class="nav-item" onclick="setIndustry(\'noi-that\', this)">\n          <span>Kiến Trúc & Nội Thất</span>\n          <span class="nav-count">{nt_count}</span>\n        </li>',
        content
    )

# Cập nhật countAll
content = re.sub(r'<span class="nav-count" id="countAll">\d+</span>', f'<span class="nav-count" id="countAll">{total_count}</span>', content)

# Cập nhật industryMap
old_map_anchor = "'cafe-va-banh-mi': 'Cafe & Bánh Mì (Menu & Quán F&B Chuẩn Hà Nội)'"
new_map_section = "'cafe-va-banh-mi': 'Cafe & Bánh Mì (Menu & Quán F&B Chuẩn Hà Nội)',\n      'noi-that': 'Kiến Trúc & Nội Thất (Studio Luxury, Thi Công & Showroom)'"
if "'noi-that':" not in content:
    assert old_map_anchor in content, "Không tìm thấy old_map_anchor trong industryMap!"
    content = content.replace(old_map_anchor, new_map_section, 1)
    print("[+] Đã thêm 'noi-that' vào industryMap!")

# Thay thế WEBSITES_DATA
formatted_json = json.dumps(updated_websites_data, ensure_ascii=False, indent=4)
new_var_declaration = f"const WEBSITES_DATA = {formatted_json};"
pattern = re.compile(r'const WEBSITES_DATA = \[.*?\];', re.DOTALL)
content, count = pattern.subn(lambda m: new_var_declaration, content, count=1)
assert count == 1, "Không thể thay thế WEBSITES_DATA!"

with open(index_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"[+] Đã cập nhật thành công index.html ({total_count} website, trong đó có {nt_count} mẫu Nội Thất)!")
