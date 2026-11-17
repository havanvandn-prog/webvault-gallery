# -*- coding: utf-8 -*-
import os, sys, json, re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
index_path = os.path.join(BASE_DIR, "index.html")
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "auto_mercedes_metadata.json")
kho_webp = os.path.join(BASE_DIR, "Kho_Anh_Webp")

skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)
from capture_engine import verify_captured_image

approved_domains = [
    'mercedes-danang.com',
    'mercedesvn.vn',
    'giaxemercedes.com.vn',
    'mercedesbenz-automobile.com.vn',
    'mercedes-haxaco.com',
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
websites_data = [w for w in websites_data if w.get("industry") != "landing-page-oto-mercedes"]

# Find max numeric id so we never collide
existing_nums = [int(w["id"]) for w in websites_data if str(w.get("id", "")).isdigit()]
start_id = (max(existing_nums) + 1) if existing_nums else (len(websites_data) + 1)
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
        "industry": "landing-page-oto-mercedes",
        "tag": found.get("tag", "mercedes-cro"),
        "vibe": found.get("vibe", "Chuẩn Chuyển Đổi Google Ads"),
        "vibe_name": found.get("vibe_name", found.get("vibe", "Chuẩn Chuyển Đổi Google Ads")),
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
ind_count = len(matched_items)

print(f"[+] Đã chuẩn bị {ind_count} mẫu Landing Page Mercedes-Benz được duyệt. Tổng cộng {total_count} website trong WebVault.")

# Chèn hoặc cập nhật tab landing-page-oto-mercedes ngay sau noi-that
if 'onclick="setIndustry(\'landing-page-oto-mercedes\'' not in content:
    anchor = """        <li class="nav-item" onclick="setIndustry('noi-that', this)">
          <span>Kiến Trúc & Nội Thất</span>
          <span class="nav-count">7</span>
        </li>"""
    replacement = f"""{anchor}
        <li class="nav-item" onclick="setIndustry('landing-page-oto-mercedes', this)">
          <span>LP Mercedes & Ô Tô</span>
          <span class="nav-count">{ind_count}</span>
        </li>"""
    assert anchor in content, "Không tìm thấy anchor noi-that trong Sidebar!"
    content = content.replace(anchor, replacement, 1)
    print("[+] Đã thêm mục 'LP Mercedes & Ô Tô' vào Sidebar Tier 1!")
else:
    content = re.sub(
        r'<li class="nav-item" onclick="setIndustry\(\'landing-page-oto-mercedes\', this\)">\s*<span>LP Mercedes & Ô Tô</span>\s*<span class="nav-count">\d+</span>\s*</li>',
        f'<li class="nav-item" onclick="setIndustry(\'landing-page-oto-mercedes\', this)">\n          <span>LP Mercedes & Ô Tô</span>\n          <span class="nav-count">{ind_count}</span>\n        </li>',
        content
    )

# Cập nhật countAll
content = re.sub(r'<span class="nav-count" id="countAll">\d+</span>', f'<span class="nav-count" id="countAll">{total_count}</span>', content)

# Cập nhật industryMap
old_map_anchor = "'noi-that': 'Kiến Trúc & Nội Thất (Studio Luxury, Thi Công & Showroom)'"
new_map_section = "'noi-that': 'Kiến Trúc & Nội Thất (Studio Luxury, Thi Công & Showroom)',\n      'landing-page-oto-mercedes': 'Landing Page Mercedes-Benz & Ô Tô (CRO Google Ads)'"
if "'landing-page-oto-mercedes':" not in content:
    assert old_map_anchor in content, "Không tìm thấy old_map_anchor trong industryMap!"
    content = content.replace(old_map_anchor, new_map_section, 1)
    print("[+] Đã thêm 'landing-page-oto-mercedes' vào industryMap!")

# Thay thế WEBSITES_DATA
formatted_json = json.dumps(updated_websites_data, ensure_ascii=False, indent=4)
new_var_declaration = f"const WEBSITES_DATA = {formatted_json};"
pattern = re.compile(r'const WEBSITES_DATA = \[.*?\];', re.DOTALL)
content, count = pattern.subn(lambda m: new_var_declaration, content, count=1)
assert count == 1, "Không thể thay thế WEBSITES_DATA!"

with open(index_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"[+] Đã cập nhật thành công index.html ({total_count} website, trong đó có {ind_count} mẫu LP Mercedes & Ô Tô)!")
