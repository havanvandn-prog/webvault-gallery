# -*- coding: utf-8 -*-
import json
import pathlib

base = pathlib.Path(r"d:\AI Agent\Website\Tìm mẫu website")
meta = json.loads((base / "_Luu_Tru_Ky_Thuat/03_Du_Lieu_Tam_Va_Test/logistics_xnk_approved.json").read_text(encoding="utf-8"))
idx_path = base / "index.html"
html = idx_path.read_text(encoding="utf-8")

# 1. Update countAll
old_count = '<span class="nav-count" id="countAll">63</span>'
new_count = '<span class="nav-count" id="countAll">74</span>'
assert old_count in html, "countAll not found"
html = html.replace(old_count, new_count, 1)

# 2. Add sidebar item after xay-dung
target_li = """        <li class="nav-item" onclick="setIndustry('xay-dung', this)">
          <span>Xây Dựng & Tổng Thầu</span>
          <span class="nav-count">2</span>
        </li>"""
new_li = target_li + """
        <li class="nav-item" onclick="setIndustry('logistics-xnk', this)">
          <span>Logistics & Xuất Nhập Khẩu</span>
          <span class="nav-count">11</span>
        </li>"""
assert target_li in html, "target_li not found"
html = html.replace(target_li, new_li, 1)

# 3. Append 11 items to WEBSITES_DATA
clean_items = []
for item in meta:
    clean_items.append({
        "id": item["id"],
        "name": item["name"],
        "short_name": item["short_name"],
        "url": item["url"],
        "domain": item["domain"],
        "industry": item["industry"],
        "tag": item["tag"],
        "vibe": item["vibe"],
        "vibe_name": item["vibe_name"],
        "location": item["location"],
        "desc": item["desc"],
        "thumb": item["thumb"],
        "full": item["full"],
        "fb": item["fb"],
        "thumb_kb": item["thumb_kb"],
        "full_kb": item["full_kb"],
        "fb_kb": item["fb_kb"],
    })

items_str = ",\n".join("    " + json.dumps(it, ensure_ascii=False, indent=4).replace("\n", "\n    ") for it in clean_items)
end_marker = "\n];\n\n  // STATE MANAGEMENT"
assert end_marker in html, "end_marker not found"
html = html.replace(end_marker, ",\n" + items_str + end_marker, 1)

# 4. Update industryMap
map_target = "'xay-dung': 'Xây Dựng & Tổng Thầu (Tổng Thầu VN & Thiết Kế Thi Công)'"
assert map_target in html, "map_target not found"
html = html.replace(
    map_target,
    map_target + ",\n      'logistics-xnk': 'Logistics & Xuất Nhập Khẩu (Vận Tải, Kho Vận & Xuất Khẩu Quốc Tế)'",
    1,
)

# 5. Update SHORT_INDUSTRY_LABELS
short_target = "'xay-dung': 'Xây dựng'"
assert short_target in html, "short_target not found"
html = html.replace(short_target, short_target + ",\n    'logistics-xnk': 'Logistics & XNK'", 1)

idx_path.write_text(html, encoding="utf-8")
print(f"Successfully updated index.html! Total items added: {len(clean_items)}")
