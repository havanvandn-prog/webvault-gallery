import sys
import urllib.request
import ssl
import json
import socket

sys.stdout.reconfigure(encoding='utf-8')

# Context ignoring ssl cert errors if any
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

candidates = [
    # Nhóm 1: Luxury & Xa Xỉ
    {"id": "dh01", "name": "Gia Bảo Luxury", "url": "https://giabaoluxury.com/"},
    {"id": "dh02", "name": "Boss Luxury Watch", "url": "https://bossluxurywatch.vn/"},
    {"id": "dh03", "name": "Empire Luxury", "url": "https://empireluxury.vn/"},
    {"id": "dh04", "name": "Authentic Luxury", "url": "https://authenticluxury.vn/"},
    {"id": "dh05", "name": "24Kara Authentic Watches", "url": "https://24kara.com/"},
    {"id": "dh06", "name": "Tam Sơn Luxury", "url": "https://tamsonvn.com/"},
    
    # Nhóm 2: Chuỗi Bán Lẻ Hàng Đầu & Top SEO VN
    {"id": "dh07", "name": "Đồng Hồ Hải Triều", "url": "https://donghohaitrieu.com/"},
    {"id": "dh08", "name": "Galle Watch", "url": "https://galle.vn/"},
    {"id": "dh09", "name": "Xwatch Chính Hãng", "url": "https://xwatch.vn/"},
    {"id": "dh10", "name": "Đồng Hồ Duy Anh", "url": "https://donghoduyanh.com/"},
    {"id": "dh11", "name": "Đồng Hồ Tân Tân", "url": "https://donghotantan.vn/"},
    {"id": "dh12", "name": "Đăng Quang Watch", "url": "https://www.dangquangwatch.vn/"},
    {"id": "dh13", "name": "Luxshopping", "url": "https://luxshopping.vn/"},
    {"id": "dh14", "name": "Thế Giới Thời Gian", "url": "https://thegioithoigian.vn/"},
    
    # Nhóm 3: Thương hiệu Thời Trang / DTC Tối Giản
    {"id": "dh15", "name": "Curnon Watch", "url": "https://curnonwatch.com/"},
    {"id": "dh16", "name": "ViWat Watch", "url": "https://viwat.vn/"},
    
    # Nhóm 4: Quốc Tế & Benchmark Trải Nghiệm Thượng Lưu
    {"id": "dh17", "name": "Hodinkee", "url": "https://www.hodinkee.com/"},
    {"id": "dh18", "name": "The 1916 Company", "url": "https://www.the1916company.com/"},
    {"id": "dh19", "name": "Chrono24", "url": "https://www.chrono24.com/"},
    {"id": "dh20", "name": "The Hour Glass", "url": "https://www.thehourglass.com/"}
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

results = []
for c in candidates:
    req = urllib.request.Request(c['url'], headers=headers)
    status = "FAIL"
    code = 0
    err_msg = ""
    try:
        with urllib.request.urlopen(req, timeout=10, context=ctx) as response:
            code = response.getcode()
            status = "OK" if code == 200 else f"HTTP {code}"
    except Exception as e:
        err_msg = str(e)
    print(f"[{status}] {c['id']} - {c['name']} ({c['url']}) -> Code: {code} {err_msg}")
    results.append({
        "id": c["id"],
        "name": c["name"],
        "url": c["url"],
        "status": status,
        "code": code,
        "error": err_msg
    })

with open('_Luu_Tru_Ky_Thuat/03_Du_Lieu_Tam_Va_Test/check_watch_urls_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
