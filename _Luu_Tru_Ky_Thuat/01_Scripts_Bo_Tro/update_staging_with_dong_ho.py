# -*- coding: utf-8 -*-
import json
import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

metadata_path = r'_Luu_Tru_Ky_Thuat\03_Du_Lieu_Tam_Va_Test\dong_ho_metadata.json'
staging_path = 'web_nhap_staging.html'

if not os.path.exists(metadata_path):
    print("Metadata file does not exist yet.")
    exit(1)

with open(metadata_path, 'r', encoding='utf-8') as f:
    items = json.load(f)

with open(staging_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Update candidates in web_nhap_staging.html
staging_candidates = []
for d in items:
    staging_candidates.append({
        "id": d["id"],
        "name": d["name"],
        "short_name": d.get("short_name", d["name"]),
        "url": d["url"],
        "domain": d["domain"],
        "vibe": d.get("vibe_name", d.get("vibe", "Hiện đại")),
        "location": d["location"],
        "thumb": d.get("thumb") or f"Kho_Anh_Webp/{d['slug']}_thumb.webp",
        "full": d.get("full") or f"Kho_Anh_Webp/{d['slug']}_full.webp",
        "desc": d["desc"]
    })

js_candidates = "const CANDIDATES = " + json.dumps(staging_candidates, ensure_ascii=False, indent=2) + ";"

content = re.sub(r'const CANDIDATES = \[[\s\S]*?\];', js_candidates, content)

# Update title / sub-header text
content = re.sub(
    r'<title>.*?</title>',
    '<title>Trạm Kiểm Duyệt Mẫu Website (WebVault Staging) — Ngành Bán Đồng Hồ</title>',
    content
)
content = re.sub(
    r'<h1>.*?</h1>',
    '<h1>Trạm Thẩm Định Mẫu Website — Ngành Bán Đồng Hồ (20 Mẫu)</h1>',
    content
)
content = re.sub(
    r'<p>Xem lướt từng mẫu.*?</p>',
    '<p>Khảo sát 20 website bán đồng hồ chính hãng & xa xỉ hàng đầu. Nhấp xem ảnh full và chọn Giữ lại/Bỏ qua.</p>',
    content
)

with open(staging_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"[+] Đã nạp thành công {len(staging_candidates)} mẫu Đồng Hồ vào web_nhap_staging.html!")
