# -*- coding: utf-8 -*-
import os, sys
from concurrent.futures import ThreadPoolExecutor

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)
from capture_engine import verify_url_health

URLS = [
    # Nhóm 1: Bệnh viện Thẩm mỹ, Clinic Da liễu & Chuỗi TMV VN
    ("rohtoaohal", "https://rohtoaohalclinic.com.vn/"),
    ("ruco", "https://rucointernational.vn/"),
    ("pensilia", "https://pensilia.com/"),
    ("lavender", "https://www.lavenderbychang.com/"),
    ("kangnam", "https://benhvienthammykangnam.vn/"),
    ("thucuc", "https://thammythucuc.vn/"),
    ("ngocdung", "https://thammyvienngocdung.com/"),
    ("seoulcenter", "https://seoulcenter.vn/"),
    ("gangwhoo", "https://benhvienthammygangwhoo.vn/"),
    ("o2skin", "https://o2skin.vn/"),
    ("saigonsmile", "https://saigonsmilespa.com.vn/"),
    ("luxclinic", "https://luxclinic.vn/"),
    ("laratio", "https://laratio.vn/"),
    ("aura", "https://thammyaura.vn/"),
    # Nhóm 2: Day Spa, Dưỡng Sinh & Boutique Spa VN
    ("laspa", "https://laspas.vn/"),
    ("mebuki", "https://mebukispa.com/"),
    ("sentaithu", "https://sentaithu.com.vn/"),
    ("herbalspa", "https://herbalspa.vn/"),
    ("charmspa", "https://charmspagrand.com/"),
    ("anspa", "https://anspadanang.vn/"),
    ("lapothiquaire", "https://lapothiquaire.com/"),
    ("mochuong", "https://mochuongspa.vn/"),
    ("catmocspa", "https://catmocspa.vn/"),
    # Nhóm 3: Luxury Spa, MedSpa & Skincare Clinic Quốc Tế Chuẩn UI/UX
    ("heydayskincare", "https://www.heydayskincare.com/"),
    ("skinlaundry", "https://www.skinlaundry.com/"),
    ("everbody", "https://everbody.com/"),
    ("silvermirror", "https://silvermirror.com/"),
    ("glowbar", "https://www.glowbar.com/"),
    ("formulafig", "https://formulafig.com/"),
    ("bathhouse", "https://www.abathhouse.com/"),
    ("beaire", "https://beaire.com/en"),
    ("burkewilliams", "https://www.burkewilliams.com/"),
    ("upkeepmedspa", "https://www.upkeepmedspa.com/"),
    ("studiomd", "https://www.studiomd.com/"),
    ("canyonranch", "https://www.canyonranch.com/"),
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
