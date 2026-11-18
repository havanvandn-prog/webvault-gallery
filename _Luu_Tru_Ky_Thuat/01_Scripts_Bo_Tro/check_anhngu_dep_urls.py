# -*- coding: utf-8 -*-
import os, sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)
from capture_engine import verify_url_health

urls = [
    # EdTech & Online English
    "https://prepedu.com/vi",
    "https://vn.elsaspeak.com/",
    "https://www.speak.com/",
    "https://www.lingoda.com/en/",
    "https://www.cambly.com/",
    "https://www.ringleplus.com/en",
    "https://www.novakidschool.com/",
    "https://www.busuu.com/",
    "https://www.fluentu.com/",
    # International English Schools
    "https://www.ecenglish.com/",
    "https://www.kaplaninternational.com/",
    "https://www.ef.com/wwen/",
    "https://www.bsceducation.com/",
    "https://www.oxfordinternationalenglish.com/",
    "https://www.bayswater.ac/",
    "https://www.wimbledon-school.ac.uk/",
    "https://www.staffordhouse.com/",
    "https://www.kingseducation.com/",
    "https://www.berlitz.com/",
    # Vietnam Modern English Centers (not in trung-tam-anh-ngu)
    "https://talkfirst.vn/",
    "https://www.britishcouncil.vn/",
    "https://simpleenglish.com.vn/",
    "https://summit.edu.vn/",
    "https://monkey.edu.vn/",
    "https://kynaenglish.vn/",
    "https://axcela.vn/",
    "https://eiv.edu.vn/",
]

for u in urls:
    ok, reason, final_url, title = verify_url_health(u, timeout=12)
    print(f"[{'PASS' if ok else 'FAIL'}] {u} -> {final_url} | {reason} | {title[:60]}")
