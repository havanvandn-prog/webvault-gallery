# -*- coding: utf-8 -*-
import os, sys, json
from concurrent.futures import ThreadPoolExecutor

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)
from capture_engine import verify_url_health

URLS = [
    # Nhóm 1: Sàn & Môi giới nhà đất VN
    ("onehousing", "https://onehousing.vn/"),
    ("nhatot", "https://www.nhatot.com/"),
    ("homedy", "https://homedy.com/"),
    ("mogi", "https://mogi.vn/"),
    ("meeyland", "https://meeyland.com/"),
    ("bds123", "https://bds123.vn/"),
    ("rever", "https://rever.vn/"),
    ("cenhomes", "https://cenhomes.vn/"),
    ("greenhouse", "https://greenhouseagency.vn/"),
    ("dotproperty", "https://www.dotproperty.com.vn/"),
    ("batdongsan", "https://batdongsan.com.vn/"),
    ("guland", "https://guland.vn/"),
    # Nhóm 2: Cho thuê căn hộ & nhà ở VN
    ("jhouse", "https://jhouse.vn/"),
    ("cityhouse", "https://cityhouseapartment.com/"),
    ("cityapartment", "https://cityapartment.vn/"),
    ("saigonluxury", "https://saigonluxury.com.vn/"),
    ("hoozing", "https://hoozing.com/"),
    ("thuecanho123", "https://thuecanho123.com/"),
    ("phongtro123", "https://phongtro123.com/"),
    ("chothuenha", "https://chothuenha.com.vn/"),
    ("toanhuyhoang", "https://toanhuyhoang.com/"),
    ("housingvn", "https://housing.vn/"),
    ("savillsvn", "https://www.savills.com.vn/"),
    ("moso", "https://moso.vn/"),
    ("sumouhousing", "https://sumouhousing.com/"),
    ("cvr", "https://cvr.com.vn/"),
    ("honeycomb", "https://honeycomb.vn/"),
    # Nhóm 3: Quốc tế chuẩn UI/UX
    ("compass", "https://www.compass.com/"),
    ("blueground", "https://www.theblueground.com/"),
    ("theagency", "https://www.theagencyre.com/"),
    ("sothebys", "https://www.sothebysrealty.com/eng"),
    ("knightfrank", "https://www.knightfrank.com/"),
    ("corcoran", "https://www.corcoran.com/"),
    ("elliman", "https://www.elliman.com/"),
    ("housinganywhere", "https://housinganywhere.com/"),
    ("domainau", "https://www.domain.com.au/"),
    ("engelvoelkers", "https://www.engelvoelkers.com/en/"),
    ("savillsglobal", "https://www.savills.com/"),
]

def check_one(item):
    slug, url = item
    ok, reason, final_url, title = verify_url_health(url, timeout=12)
    return (slug, url, ok, reason, final_url, title[:65])

with ThreadPoolExecutor(max_workers=10) as ex:
    results = list(ex.map(check_one, URLS))

for slug, url, ok, reason, final_url, title in results:
    status = "OK  " if ok else "FAIL"
    print(f"[{status}] {slug:16s} | {url:38s} | {reason[:35]:35s} | {title}")
