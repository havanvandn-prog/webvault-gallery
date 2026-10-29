# -*- coding: utf-8 -*-
"""
WebVault Sync Handler — Tự động nạp mẫu được duyệt vào index.html & đẩy lên GitHub Pages
"""
import os
import sys
import json
import re
import subprocess

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

def sync_approved_items_to_hub(approved_items, industry_slug="decor-su-kien", industry_name="Trang Trí & Decor Tiệc"):
    index_path = os.path.join(BASE_DIR, "index.html")
    if not os.path.exists(index_path):
        return {"success": False, "error": "Không tìm thấy file index.html"}

    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Trích xuất WEBSITES_DATA hiện tại
    m = re.search(r'const WEBSITES_DATA = (\[.*?\]);', html, re.DOTALL)
    if not m:
        return {"success": False, "error": "Không tìm thấy WEBSITES_DATA trong index.html"}

    try:
        websites_data = json.loads(m.group(1))
    except Exception as e:
        return {"success": False, "error": f"Lỗi đọc WEBSITES_DATA: {e}"}

    # 2. Hợp nhất các mẫu mới (tránh trùng lặp theo domain)
    existing_domains = {w['domain'] for w in websites_data}
    added_count = 0

    for item in approved_items:
        if item['domain'] not in existing_domains:
            # Gán ngành nghề chuẩn
            item['industry'] = industry_slug
            if 'thumb_kb' not in item:
                thumb_p = os.path.join(BASE_DIR, item.get('thumb', ''))
                item['thumb_kb'] = round(os.path.getsize(thumb_p) / 1024, 1) if os.path.exists(thumb_p) else 150.0
            if 'full_kb' not in item:
                full_p = os.path.join(BASE_DIR, item.get('full', ''))
                item['full_kb'] = round(os.path.getsize(full_p) / 1024, 1) if os.path.exists(full_p) else 800.0

            websites_data.append(item)
            existing_domains.add(item['domain'])
            added_count += 1

    # 3. Đánh số lại ID từ 01, 02... hoặc giữ nguyên
    for idx, w in enumerate(websites_data, start=1):
        w['id'] = str(idx).padStart(2, '0') if hasattr(str(idx), 'padStart') else f"{idx:02d}"

    total_count = len(websites_data)
    industry_count = len([w for w in websites_data if w.get('industry') == industry_slug])

    # 4. Ghi lại WEBSITES_DATA vào index.html
    new_json_str = json.dumps(websites_data, ensure_ascii=False, indent=4)
    html = html[:m.start(1)] + new_json_str + html[m.end(1):]

    # 5. Cập nhật Sidebar: countAll và Chuyên mục mới
    html = re.sub(r'<span class="nav-count" id="countAll">\d+</span>',
                  f'<span class="nav-count" id="countAll">{total_count}</span>', html)

    # Kiểm tra xem chuyên mục ngành đã có trong sidebar chưa
    nav_pattern = f"onclick=\"setIndustry\\('{industry_slug}', this\\)\""
    if nav_pattern not in html:
        # Chèn chuyên mục mới ngay dưới chuyên mục du lịch
        insert_marker = '<li class="nav-item" onclick="setIndustry(\'du-lich\', this)">'
        new_nav_item = f'''<li class="nav-item" onclick="setIndustry('{industry_slug}', this)">
          <span>{industry_name}</span>
          <span class="nav-count">{industry_count}</span>
        </li>
        '''
        if insert_marker in html:
            pos = html.find(insert_marker)
            # Tìm thẻ đóng </li>
            pos_end = html.find('</li>', pos) + 5
            html = html[:pos_end] + '\n        ' + new_nav_item + html[pos_end:]
    else:
        # Cập nhật số đếm chuyên mục đó
        cat_regex = rf'(<li class="nav-item" onclick="setIndustry\(\'{industry_slug}\', this\)">\s*<span>.*?</span>\s*<span class="nav-count">)(\d+)(</span>)'
        html = re.sub(cat_regex, rf'\g<1>{industry_count}\g<3>', html)

    # Ghi file index.html
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html)

    # 6. Chạy lệnh Git để đồng bộ lên GitHub Pages
    try:
        subprocess.run(["git", "add", "index.html", "Kho_Anh_Webp/", "_Luu_Tru_Ky_Thuat/"], cwd=BASE_DIR, check=True)
        subprocess.run(["git", "commit", "-m", f"feat(webvault): auto-sync {added_count} approved {industry_slug} samples via 1-click system"], cwd=BASE_DIR, check=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=BASE_DIR, check=True)
        git_synced = True
    except Exception as e:
        print(f"Git push notice: {e}")
        git_synced = False

    return {
        "success": True,
        "added_count": added_count,
        "total_count": total_count,
        "industry_count": industry_count,
        "git_synced": git_synced,
        "redirect_url": f"index.html?industry={industry_slug}"
    }

if __name__ == '__main__':
    # Test import
    print("Sync handler module loaded OK")
