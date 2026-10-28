# -*- coding: utf-8 -*-
import json
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Revert WEBSITES_DATA: keep only items with id <= "23"
m = re.search(r'const WEBSITES_DATA = (\[[\s\S]*?\]);', content)
if m:
    data = json.loads(m.group(1))
    print(f"Original items in index.html: {len(data)}")
    
    # Filter to only approved previous items (id <= 23, i.e. su-kien and du-lich)
    approved_items = [item for item in data if int(item['id']) <= 23]
    print(f"Rolling back to approved items: {len(approved_items)}")
    
    new_data_js = "const WEBSITES_DATA = " + json.dumps(approved_items, ensure_ascii=False, indent=4) + ";"
    content = content[:m.start(0)] + new_data_js + content[m.end(0):]

# 2. Revert Tier 1 Sidebar: remove decor-su-kien
tier1_decor = """        <li class="nav-item" onclick="setIndustry('decor-su-kien', this)">
          <span>Trang Trí & Decor Tiệc</span>
          <span class="nav-count">20</span>
        </li>
"""
content = content.replace(tier1_decor, "")

# 3. Update countAll and heading in static HTML
content = content.replace('<span class="nav-count" id="countAll">43</span>', '<span class="nav-count" id="countAll">23</span>')
content = content.replace('Tất Cả Mẫu Tuyển Chọn (43 Website)', 'Tất Cả Mẫu Tuyển Chọn (23 Website)')
content = content.replace('Hiển thị: <b>43/43</b>', 'Hiển thị: <b>23/23</b>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("[+] Da rollback index.html ve 23 mau cu (20 Su Kien + 3 Du Lich)!")
