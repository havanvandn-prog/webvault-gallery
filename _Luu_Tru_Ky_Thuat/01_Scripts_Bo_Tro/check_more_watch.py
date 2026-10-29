import sys
import urllib.request
import ssl

sys.stdout.reconfigure(encoding='utf-8')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

candidates = [
    {"name": "WatchStore", "url": "https://www.watchstore.vn/"},
    {"name": "Đồng Hồ Chính Hãng", "url": "https://donghochinhhang.com/"},
    {"name": "Đồng Hồ Thụy Sỹ", "url": "https://donghothuysy.vn/"},
    {"name": "Cititime Mall", "url": "https://cititime.com.vn/"},
    {"name": "Kỳ Lân Luxury", "url": "https://kylanluxury.com/"},
    {"name": "Tudor Watch VN", "url": "https://www.tudorwatch.com/vi"},
    {"name": "Vua Hàng Hiệu (Đồng Hồ)", "url": "https://vuahanghieu.com/dong-ho"},
    {"name": "S&S Group", "url": "https://ssgroup.net/"},
    {"name": "Duy Anh Watch", "url": "https://donghoduyanh.com/"},
    {"name": "Hải Triều (Browser UA)", "url": "https://donghohaitrieu.com/"}
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

for c in candidates:
    req = urllib.request.Request(c['url'], headers=headers)
    status = "FAIL"
    code = 0
    err = ""
    try:
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            code = resp.getcode()
            status = "OK" if code == 200 else str(code)
    except Exception as e:
        err = str(e)
    print(f"[{status}] {c['name']} ({c['url']}) -> {code} {err}")
