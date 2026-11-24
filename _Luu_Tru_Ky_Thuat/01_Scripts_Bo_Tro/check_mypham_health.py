# -*- coding: utf-8 -*-
import os, sys
from concurrent.futures import ThreadPoolExecutor

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)
from capture_engine import verify_url_health

URLS = [
    # Nhóm 1: Mỹ phẩm & Skincare Việt Nam
    ("cocoon", "https://cocoonvietnam.com/"),
    ("comem", "https://comem.vn/"),
    ("hasaki", "https://hasaki.vn/"),
    ("thegioiskinfood", "https://thegioiskinfood.com/"),
    ("beautybox", "https://beautybox.com.vn/"),
    ("guardian", "https://www.guardian.com.vn/"),
    ("lemonade", "https://www.lemonade.vn/"),
    ("ofelia", "https://ofelia.vn/"),
    ("moicosmetics", "https://moicosmetics.vn/"),
    ("paulaschoicevn", "https://paulaschoice.vn/"),
    ("larocheposayvn", "https://www.larocheposay.vn/"),
    ("innisfreevn", "https://www.innisfree.vn/"),
    # Nhóm 2: Thực phẩm chức năng, Vitamin & Nhà thuốc VN
    ("longchau", "https://nhathuoclongchau.com.vn/"),
    ("pharmacity", "https://www.pharmacity.vn/"),
    ("ankhang", "https://www.nhathuocankhang.com/"),
    ("dhcvietnam", "https://dhcvietnam.com.vn/"),
    ("doppelherz", "https://doppelherz.vn/"),
    ("blackmoresvn", "https://www.blackmores.com.vn/"),
    ("ecogreen", "https://ecogreen.com.vn/"),
    ("traphaco", "https://traphaco.com.vn/"),
    ("wheystore", "https://www.wheystore.vn/"),
    ("hector", "https://dongtrunghathaohector.com/"),
    # Nhóm 3: D2C Mỹ phẩm & TPCN Quốc tế chuẩn UI/UX
    ("glossier", "https://www.glossier.com/"),
    ("rhodeskin", "https://www.rhodeskin.com/"),
    ("summerfridays", "https://summerfridays.com/"),
    ("theordinary", "https://theordinary.com/en-us"),
    ("rarebeauty", "https://www.rarebeauty.com/"),
    ("drunkelephant", "https://www.drunkelephant.com/"),
    ("laneigeus", "https://us.laneige.com/"),
    ("seed", "https://seed.com/"),
    ("ritual", "https://ritual.com/"),
    ("drinkag1", "https://drinkag1.com/"),
    ("humnutrition", "https://www.humnutrition.com/"),
    ("moonjuice", "https://moonjuice.com/"),
    ("aesop", "https://www.aesop.com/us/"),
    ("glowrecipe", "https://www.glowrecipe.com/"),
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
