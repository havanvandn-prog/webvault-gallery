# -*- coding: utf-8 -*-
import json, re, os, sys
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image

def audit_candidates():
    with open('web_nhap_staging.html', 'r', encoding='utf-8') as f:
        html = f.read()

    m = re.search(r'const CANDIDATES = (\[.*?\]);', html, re.DOTALL)
    if not m:
        print("No CANDIDATES found")
        return []
    
    data = json.loads(m.group(1))
    print(f"=== CANDIDATES IN STAGING ({len(data)} items) ===")
    for item in data:
        thumb_path = item.get('thumb', '')
        full_path = item.get('full', '')
        thumb_exists = os.path.exists(thumb_path)
        full_exists = os.path.exists(full_path)
        thumb_size = os.path.getsize(thumb_path) if thumb_exists else 0
        full_size = os.path.getsize(full_path) if full_exists else 0
        
        # Check image dimensions
        full_dim = "N/A"
        if full_exists:
            try:
                im = Image.open(full_path)
                full_dim = f"{im.size[0]}x{im.size[1]}"
            except Exception as e:
                full_dim = f"Error: {e}"

        print(f"[{item['id']}] {item['short_name']} | URL: {item['url']}")
        print(f"     Thumb: {thumb_exists} ({thumb_size//1024} KB) | Full: {full_exists} ({full_size//1024} KB, {full_dim})")
    return data

if __name__ == '__main__':
    audit_candidates()
