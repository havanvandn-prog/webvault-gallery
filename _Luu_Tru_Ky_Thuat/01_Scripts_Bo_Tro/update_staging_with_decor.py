# -*- coding: utf-8 -*-
import json
import re

with open(r'_Luu_Tru_Ky_Thuat\03_Du_Lieu_Tam_Va_Test\decor_metadata.json', 'r', encoding='utf-8') as f:
    decor_items = json.load(f)

with open('web_nhap_staging.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Update candidates in web_nhap_staging.html
staging_candidates = []
for d in decor_items:
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

with open('web_nhap_staging.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("[+] Da cap nhat web_nhap_staging.html voi 20 mau Decor ung vien!")
