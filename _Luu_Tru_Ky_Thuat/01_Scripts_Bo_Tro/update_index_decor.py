# -*- coding: utf-8 -*-
import os
import sys
import json

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
index_path = os.path.join(BASE_DIR, "index.html")
decor_meta_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "decor_metadata.json")

with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

with open(decor_meta_path, "r", encoding="utf-8") as f:
    decor_items = json.load(f)

content_norm = content.replace("\r\n", "\n")

# 1. Update Top Header Actions
old_header_link = """      <div class="header-actions">
        <a href="web_nhap_staging.html" class="btn btn-secondary">"""

new_header_link = """      <div class="header-actions">
        <a href="preview_mau_website_decor_su_kien.html" class="btn btn-secondary" style="border-color: #d97706; color: #fbbf24;">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
          Bộ Mẫu Decor Tiệc
        </a>

        <a href="preview_mau_website_du_lich.html" class="btn btn-secondary" style="border-color: #0284c7; color: #38bdf8;">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"></polygon></svg>
          Bộ Mẫu Du Lịch
        </a>

        <a href="web_nhap_staging.html" class="btn btn-secondary">"""

if old_header_link in content_norm:
    content_norm = content_norm.replace(old_header_link, new_header_link)
    print("[+] Da them link Bo Mau Decor Tiec & Du Lich vao Top Header!")
else:
    print("[-] Khong tim thay old_header_link trong index.html!")

# 2. Format decor items as JS objects for WEBSITES_DATA
decor_js_list = []
start_id = 24
for i, d in enumerate(decor_items):
    cur_id = f"{start_id + i:02d}"
    decor_js_list.append(f"""    {{
        "id": "{cur_id}",
        "name": "{d['name']}",
        "short_name": "{d.get('short_name', d['name'])}",
        "url": "{d['url']}",
        "domain": "{d['domain']}",
        "industry": "decor-su-kien",
        "tag": "{d.get('tag', 'balloon-backdrop')}",
        "vibe": "{d.get('vibe', 'creative-art')}",
        "vibe_name": "{d.get('vibe_name', 'Hiện đại & Sáng tạo')}",
        "location": "{d['location']}",
        "desc": "{d['desc']}",
        "thumb": "{d['thumb']}",
        "full": "{d['full']}",
        "fb": "{d['fb']}",
        "thumb_kb": {d.get('thumb_kb', 0)},
        "full_kb": {d.get('full_kb', 0)},
        "fb_kb": {d.get('fb_kb', 0)}
    }}""")

decor_joined_js = ",\n" + ",\n".join(decor_js_list) + "\n];"

old_closing = """        "thumb_kb": 262.6,
        "full_kb": 1047.3,
        "fb_kb": 1964.1
    }
];"""

if old_closing in content_norm:
    replacement = """        "thumb_kb": 262.6,
        "full_kb": 1047.3,
        "fb_kb": 1964.1
    }""" + decor_joined_js
    content_norm = content_norm.replace(old_closing, replacement)
    print("[+] Da nap thanh cong 20 website decor vao WEBSITES_DATA trong index.html!")
else:
    print("[-] Khong tim thay old_closing trong index.html!")

with open(index_path, "w", encoding="utf-8") as f:
    f.write(content_norm)

print("[SUCCESS] Hoan tat cap nhat index.html!")
