# -*- coding: utf-8 -*-
import os, sys
from concurrent.futures import ThreadPoolExecutor

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)
from capture_engine import verify_url_health

URLS = [
    # Nhóm 1: Gạch, Đá, Gỗ & Vật liệu hoàn thiện VN
    ("vietceramics", "https://www.vietceramics.com/"),
    ("eurotile", "https://www.eurotile.vn/"),
    ("vicostone", "https://vicostone.com/vi-vn"),
    ("ancuong", "https://ancuong.com/"),
    ("caslaquartz", "https://caslaquartz.com/"),
    ("dongtam", "https://dongtam.com.vn/"),
    ("prime", "https://www.prime.vn/"),
    ("viglaceratiles", "https://viglaceratiles.vn/"),
    ("vinhtuong", "https://vinhtuong.com/"),
    ("kosmos", "https://kosmos.vn/"),
    ("topmatstore", "https://topmatstore.vn/"),
    ("hoasengroup", "https://hoasengroup.vn/"),
    ("hoaphat", "https://www.hoaphat.com.vn/"),
    ("taicera", "https://www.taicera.com/"),
    # Nhóm 2: Cửa, Nhôm kính, Thiết bị vệ sinh & Sơn VN
    ("eurowindow", "https://eurowindow.biz/"),
    ("austdoor", "https://austdoor.com/"),
    ("xingfagroup", "https://xingfagroup.vn/"),
    ("topal", "https://topal.vn/"),
    ("totovn", "https://vn.toto.com/"),
    ("inaxvn", "https://www.inax.com.vn/"),
    ("hafelevn", "https://hafelehome.com.vn/"),
    ("duluxvn", "https://www.dulux.vn/vi"),
    ("jotunvn", "https://www.jotun.com/vn-vi"),
    ("nipponvn", "https://nipponpaint.com.vn/"),
    ("facadesvn", "https://facades.vn/"),
    ("koffmann", "https://koffmann.vn/"),
    # Nhóm 3: Vật liệu kiến trúc, Gạch đá & Cửa Quốc tế
    ("porcelanosa", "https://www.porcelanosa.com/en/"),
    ("cosentino", "https://www.cosentino.com/"),
    ("caesarstone", "https://www.caesarstoneus.com/"),
    ("florim", "https://www.florim.com/en/"),
    ("mutina", "https://www.mutina.it/en/"),
    ("laminam", "https://www.laminam.com/en/"),
    ("marazzi", "https://www.marazzigroup.com/"),
    ("schueco", "https://www.schueco.com/en"),
    ("kohler", "https://www.kohler.com/en"),
    ("hansgrohe", "https://www.hansgrohe.com/"),
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
