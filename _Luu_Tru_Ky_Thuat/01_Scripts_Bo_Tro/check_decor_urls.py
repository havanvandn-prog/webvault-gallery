import urllib.request
import ssl
import json
import socket
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

candidates = [
    {"name": "Bliss Weddings & Events", "url": "https://www.blissvn.com/", "domain": "blissvn.com"},
    {"name": "7799 Wedding Storyteller", "url": "https://7799wedding.vn/", "domain": "7799wedding.vn"},
    {"name": "Lutèce Wedding & Party Design", "url": "https://lutece.vn/", "domain": "lutece.vn"},
    {"name": "Phi Điệp Wedding & Event Decor", "url": "https://phidiepwedding.com/", "domain": "phidiepwedding.com"},
    {"name": "AZ Party", "url": "https://azparty.vn/", "domain": "azparty.vn"},
    {"name": "Party Design VN", "url": "https://partydesign.vn/", "domain": "partydesign.vn"},
    {"name": "Vua Trang Trí Event", "url": "https://vuatrangtri.vn/", "domain": "vuatrangtri.vn"},
    {"name": "GU Decorate", "url": "https://gudecorate.com/", "domain": "gudecorate.com"},
    {"name": "Hoàng Luân Event", "url": "https://hoangluanevent.com/", "domain": "hoangluanevent.com"},
    {"name": "Lucky Balloons", "url": "https://bongbaysukien.com/", "domain": "bongbaysukien.com"},
    {"name": "Sinh Nhật 5 Sao", "url": "https://sinhnhat5sao.com/", "domain": "sinhnhat5sao.com"},
    {"name": "Angeline Birthday & Event", "url": "https://angeline.vn/", "domain": "angeline.vn"},
    {"name": "Cát Decor Đà Nẵng", "url": "https://trangtrisinhnhatdanang.com/", "domain": "trangtrisinhnhatdanang.com"},
    {"name": "Oha Decor", "url": "https://ohadecor.com/", "domain": "ohadecor.com"},
    {"name": "Palamun Event", "url": "https://palamunevent.com/", "domain": "palamunevent.com"},
    {"name": "Will Event", "url": "https://willevent.vn/", "domain": "willevent.vn"},
    {"name": "Cyber Show", "url": "https://cybershow.vn/", "domain": "cybershow.vn"},
    {"name": "Perfect Media", "url": "https://tochucsukienperfect.com/", "domain": "tochucsukienperfect.com"},
    {"name": "HoaBinh Events", "url": "https://hoabinhevents.com/", "domain": "hoabinhevents.com"},
    {"name": "Venus Decor Hà Nội", "url": "https://venusdecor.vn/", "domain": "venusdecor.vn"},
    {"name": "Chill Decor", "url": "https://chilldecor.net/", "domain": "chilldecor.net"},
    {"name": "Shop Babystyle", "url": "https://sinhnhatchobe.vn/", "domain": "sinhnhatchobe.vn"},
    {"name": "D2 Events Đà Nẵng", "url": "https://d2events.com/", "domain": "d2events.com"},
    {"name": "Anh Đức Wedding & Decor", "url": "https://anhducwedding.com/", "domain": "anhducwedding.com"},
]

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

results = []
for c in candidates:
    url = c["url"]
    status = "ERROR"
    code = 0
    err_msg = ""
    try:
        req = urllib.request.Request(
            url, 
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        )
        with urllib.request.urlopen(req, timeout=8, context=ctx) as response:
            code = response.getcode()
            status = "OK" if code == 200 else f"HTTP {code}"
    except Exception as e:
        err_msg = str(e)
    
    print(f"[{status}] {code} - {c['name']} ({url}) {err_msg}")
    results.append({**c, "status": status, "code": code, "error": err_msg})

with open(r"_Luu_Tru_Ky_Thuat\03_Du_Lieu_Tam_Va_Test\decor_check_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
