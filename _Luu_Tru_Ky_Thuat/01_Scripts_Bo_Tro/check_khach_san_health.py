# -*- coding: utf-8 -*-
import os, sys, json

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)

from capture_engine import verify_url_health

urls = [
    ("ks01", "Mia Saigon", "https://www.miasaigon.com/"),
    ("ks02", "Peridot Grand Hanoi", "https://peridotgrandhotel.com/"),
    ("ks03", "Sofitel Metropole Hanoi", "https://www.sofitel-legend-metropole-hanoi.com/"),
    ("ks04", "Caravelle Saigon", "https://www.caravellesaigon.com/"),
    ("ks05", "The Reverie Saigon", "https://www.thereveriesaigon.com/"),
    ("ks06", "Hotel des Arts Saigon", "https://www.hoteldesartssaigon.com/"),
    ("ks07", "Hotel de la Coupole Sapa", "https://hoteldelacoupole.com/"),
    ("ks08", "Mai House Saigon", "https://maihouse.com/saigon/"),
    ("ks09", "Silverland Hotels", "https://silverlandhotels.com/"),
    ("ks10", "Capella Hanoi", "https://capellahotels.com/en/capella-hanoi"),
    ("ks11", "Zannier Bai San Ho", "https://www.zannierhotels.com/baisanho/en/"),
    ("ks12", "Regent Phu Quoc", "https://phuquoc.regenthotels.com/"),
    ("ks13", "Azerai Resorts", "https://azerai.com/"),
    ("ks14", "An Lam Retreats", "https://anlam.com/"),
    ("ks15", "The Anam", "https://theanam.com/"),
    ("ks16", "Wink Hotels", "https://wink-hotels.com/"),
    ("ks17", "Fusion Hotel Group", "https://fusionhotelgroup.com/"),
    ("ks18", "Silk Path Hotels", "https://silkpathhotel.com/"),
    ("ks19", "La Siesta Hotels", "https://lasiestahotels.com/"),
    ("ks20", "P'apiu Resort", "https://papiu.vn/"),
    ("ks21", "Topas Ecolodge", "https://topasecolodge.com/"),
    ("ks22", "Aman Resorts", "https://www.aman.com/"),
    ("ks23", "Six Senses", "https://www.sixsenses.com/"),
    ("ks24", "Rosewood Hotels", "https://www.rosewoodhotels.com/"),
    ("ks25", "Ett Hem Stockholm", "https://www.etthem.se/"),
    ("ks26", "Our Habitas", "https://www.ourhabitas.com/"),
    ("ks27", "Constance Hotels", "https://www.constancehotels.com/en/"),
    ("ks28", "7132 Hotel", "https://7132.com/en"),
    ("ks29", "Badrutt's Palace", "https://badruttspalace.com/"),
    ("ks30", "Ace Hotel", "https://www.acehotel.com/"),
    ("ks31", "Le Barn Hotel", "https://lebarnhotel.com/en/"),
]

results = []
for cid, name, url in urls:
    ok, reason, final_url, title = verify_url_health(url, timeout=12)
    print(f"{cid} | {'OK  ' if ok else 'FAIL'} | {name:26s} | {final_url} | {reason}")
    results.append({"id": cid, "name": name, "url": url, "ok": ok, "final_url": final_url, "reason": reason, "title": title})

out_path = r"d:\AI Agent\Website\Tìm mẫu website\_Luu_Tru_Ky_Thuat\03_Du_Lieu_Tam_Va_Test\khach_san_health_check.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
