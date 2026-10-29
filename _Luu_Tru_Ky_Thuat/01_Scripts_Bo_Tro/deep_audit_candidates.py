# -*- coding: utf-8 -*-
import json, re, os, sys, requests
sys.stdout.reconfigure(encoding='utf-8')
from PIL import Image

def audit_urls_and_images():
    with open('web_nhap_staging.html', 'r', encoding='utf-8') as f:
        html = f.read()

    m = re.search(r'const CANDIDATES = (\[.*?\]);', html, re.DOTALL)
    data = json.loads(m.group(1))

    print("=== KIỂM TRA TOÀN DIỆN 20 MẪU STAGING ===")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    for item in data:
        url = item['url']
        full_path = item['full']
        
        # 1. Check HTTP Status & Title
        status = 'Error'
        final_url = url
        title = ''
        try:
            r = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
            status = r.status_code
            final_url = r.url
            tm = re.search(r'<title>(.*?)</title>', r.text, re.IGNORECASE | re.DOTALL)
            if tm:
                title = tm.group(1).strip()[:60]
        except Exception as e:
            status = str(e)[:30]

        # 2. Check Image Dimensions & Aspect Ratio
        im_info = "No image"
        if os.path.exists(full_path):
            im = Image.open(full_path)
            w, h = im.size
            im_info = f"{w}x{h}"
            
        print(f"[{item['id']}] {item['short_name']}")
        print(f"  URL: {url} -> {final_url} (HTTP {status})")
        print(f"  Title: {title}")
        print(f"  Image: {full_path} ({im_info})")
        
        # Warning flags
        flags = []
        if 'expired' in title.lower() or 'domain' in title.lower() or 'for sale' in title.lower():
            flags.append("🚨 EXPIRED DOMAIN / FOR SALE")
        if status != 200:
            flags.append(f"🚨 HTTP {status}")
        if im_info.startswith("1064") or im_info.startswith("1311") or im_info.startswith("1415"):
            flags.append("⚠️ WIDTH NOT 1440px (SCALED DOWN)")
        if flags:
            print("  ==> " + " | ".join(flags))
        print("-" * 60)

if __name__ == '__main__':
    audit_urls_and_images()
