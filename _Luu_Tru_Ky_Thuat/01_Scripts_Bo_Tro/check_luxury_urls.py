# -*- coding: utf-8 -*-
import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)
from capture_engine import verify_url_health

candidates = [
    ("XLUXURY (VN)", "https://xluxury.vn/"),
    ("KIM Furniture (VN)", "https://kimfurniture.com/"),
    ("3A Signature (VN)", "https://3asignature.com/"),
    ("AA Corporation (VN)", "https://aacorporation.com/"),
    ("B&B Italia", "https://www.bebitalia.com/en"),
    ("Cassina", "https://www.cassina.com/"),
    ("Flexform", "https://www.flexform.it/en"),
    ("Baxter", "https://www.baxter.it/en/"),
    ("Giorgetti", "https://www.giorgettimeda.com/en"),
    ("Roche Bobois", "https://www.roche-bobois.com/en-US/"),
    ("Kelly Wearstler", "https://www.kellywearstler.com/"),
    ("Axel Vervoordt", "https://www.axelvervoordt.com/"),
    ("Humbert & Poyet", "https://www.humbertpoyet.com/"),
    ("Nicole Hollis", "https://www.nicolehollis.com/"),
    ("Lago Design", "https://www.lago.it/en/"),
    ("Rimadesio", "https://www.rimadesio.it/en/"),
    ("Gilles & Boissier", "https://www.gillesetboissier.com/"),
    ("Beata Heuman", "https://beataheuman.com/"),
]

for name, url in candidates:
    ok, reason, final_url, title = verify_url_health(url, timeout=12)
    print(f"[{'PASS' if ok else 'FAIL'}] {name:24s} | {url:36s} -> {final_url} | {reason} | {title[:45]}")
