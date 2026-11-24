# -*- coding: utf-8 -*-
import os, sys
from concurrent.futures import ThreadPoolExecutor

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)
from capture_engine import verify_url_health

URLS = [
    # Nhóm 1: Chuỗi Nha Khoa & Bệnh Viện RHM Lớn VN
    ("nhakhoakim", "https://nhakhoakim.com/"),
    ("parkway", "https://nhakhoaparkway.com/"),
    ("elitedental", "https://elitedental.com.vn/"),
    ("nhakhoaparis", "https://nhakhoaparis.vn/"),
    ("drcare", "https://drcareimplant.com/"),
    ("ident", "https://nhakhoaident.com/"),
    ("lacvietintech", "https://lacvietintech.vn/"),
    ("peace", "https://nhakhoapeace.vn/"),
    ("updental", "https://updental.vn/"),
    ("nhantam", "https://nhakhoanhantam.com/"),
    ("worldwide", "https://benhvienworldwide.vn/"),
    ("trongrangsg", "https://nhakhoatrongrang.com/"),
    # Nhóm 2: Nha Khoa Thẩm Mỹ, Niềng Răng & Boutique VN
    ("jetdentist", "https://jetdentist.vn/"),
    ("westcoast", "https://westcoastinternational.com/"),
    ("thuyduc", "https://nhakhoathuyduc.com.vn/"),
    ("vidental", "https://vidental.vn/"),
    ("myauris", "https://myauris.vn/"),
    ("vietphap", "https://nhakhoaquoctevietphap.vn/"),
    ("nhakhoaiway", "https://nhakhoaiway.com/"),
    ("nhakhoavietuc", "https://nhakhoavietuc.com/"),
    ("sydneydental", "https://nhakhoasydney.vn/"),
    ("starlight", "https://starlightdental.net/"),
    # Nhóm 3: Nha Khoa Thẩm Mỹ & Boutique Quốc Tế Chuẩn UI/UX
    ("tend", "https://www.hellotend.com/"),
    ("grandstreet", "https://www.grandstreetdental.com/"),
    ("apaaesthetic", "https://apaaesthetic.com/"),
    ("premierarts", "https://www.premierartsdental.com/"),
    ("swishdental", "https://www.swishdental.com/"),
    ("studiodental", "https://www.studiodental.com/"),
    ("thesmilist", "https://www.thesmilist.com/"),
    ("dentalboutique", "https://www.dentalboutique.com.au/"),
    ("mintdentistry", "https://mintdentistry.com/"),
    ("villagedental", "https://www.villagedentaldtc.com/"),
    ("harleystreet", "https://www.harleystreetdentalstudio.com/"),
    ("209nycdental", "https://www.209nycdental.com/"),
    ("wallyhealth", "https://www.wallyhealth.com/"),
]

def check_one(item):
    slug, url = item
    ok, reason, final_url, title = verify_url_health(url, timeout=12)
    return (slug, url, ok, reason, final_url, title[:65])

with ThreadPoolExecutor(max_workers=10) as ex:
    results = list(ex.map(check_one, URLS))

for slug, url, ok, reason, final_url, title in results:
    status = "OK  " if ok else "FAIL"
    print(f"[{status}] {slug:16s} | {url:40s} | {reason[:35]:35s} | {title}")
