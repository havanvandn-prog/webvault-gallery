# -*- coding: utf-8 -*-
import json, re, os, sys
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image

def inspect_visual_anomalies():
    with open('web_nhap_staging.html', 'r', encoding='utf-8') as f:
        html = f.read()

    m = re.search(r'const CANDIDATES = (\[.*?\]);', html, re.DOTALL)
    data = json.loads(m.group(1))

    print("=== KIỂM TRA BẤT THƯỜNG TRỰC QUAN 20 MẪU STAGING ===")
    issues = []
    for item in data:
        full_path = item['full']
        if not os.path.exists(full_path):
            issues.append((item['id'], item['short_name'], "File ảnh không tồn tại"))
            continue
        
        im = Image.open(full_path)
        w, h = im.size

        # Check 1: Scaled width (not 1440)
        if w != 1440:
            issues.append((item['id'], item['short_name'], f"Bị méo chiều ngang: {w}px thay vì 1440px (do code resize sai tỷ lệ khi h > 15500)"))

        # Check 2: Ratio check (abnormally short or tall)
        ratio = h / w
        if ratio < 1.0:
            issues.append((item['id'], item['short_name'], f"Ảnh quá ngắn ({w}x{h}, tỷ lệ {ratio:.2f}) - có thể chưa cuộn hết trang"))

        # Check 3: Check GU Decorate domain expired
        if 'gudecorate' in item['url'].lower():
            issues.append((item['id'], item['short_name'], "Tên miền hết hạn (Expired domain for sale)"))

    print(f"Phát hiện {len(issues)} vấn đề:")
    for cid, name, reason in issues:
        print(f"- [{cid}] {name}: {reason}")

if __name__ == '__main__':
    inspect_visual_anomalies()
