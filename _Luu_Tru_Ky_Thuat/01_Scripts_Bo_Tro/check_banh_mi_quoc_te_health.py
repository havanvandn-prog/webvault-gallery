# -*- coding: utf-8 -*-
import os, sys, json

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)

from capture_engine import verify_url_health

urls = [
    ("bm01", "Bánh Mì Kêu (London)", "https://banhmikeu.co.uk/"),
    ("bm02", "Bánh NYC", "https://www.banhny.com/"),
    ("bm03", "Bánh Shop House (NYC)", "https://www.banhshophouse.com/"),
    ("bm04", "Bun Mee (SF & NYC)", "https://bunmee.co/"),
    ("bm05", "Bánh Anh Em (Seattle)", "https://www.banhanhem.com/"),
    ("bm06", "BAMMI (Melbourne)", "https://bammivietnam.com.au/"),
    ("bm07", "Banh Mi Bao (Sydney)", "https://banhmibao.com.au/"),
    ("bm08", "The Banh Mi House (AU)", "https://thebanhmihouse.com.au/"),
    ("bm09", "Roll'd Vietnamese (AU)", "https://rolld.com.au/"),
    ("bm10", "Luke's Bánh Mì (Melbourne)", "https://www.lukesbanhmi.au/"),
    ("bm11", "Banh Mi Factory (Brisbane)", "https://banhmifactory.com.au/"),
    ("bm12", "Bun Banh Mi (Perth)", "https://bunbanhmi.com.au/"),
    ("bm13", "Mister Banh Mi (Perth)", "https://misterbanhmi.com.au/"),
    ("bm14", "Bánh Mì Oï! (Paris)", "https://www.banhmioi.fr/"),
    ("bm15", "Banemi (Paris)", "https://www.banemi.fr/"),
    ("bm16", "An Banh Mi (Berlin)", "https://anbanhmi.de/"),
    ("bm17", "Banh Mi 73 (Berlin)", "https://www.banhmi73.de/"),
    ("bm18", "Banh Mi Boys (Toronto)", "https://banhmiboys.com/"),
    ("bm19", "Lamhan Banh Mi (Toronto)", "https://www.lamhanbanhmi.com/"),
    ("bm20", "Bánh Mì Xin Chào (Tokyo)", "https://banhmixinchao.co.jp/"),
    ("bm21", "Nonette Banh Mi (Paris)", "https://nonettebanhmi.com/"),
    ("bm22", "Joo Chiat Caphe (Singapore)", "https://joochiatcaphe.com/"),
    ("bm23", "The Viet Roti (Singapore)", "https://thevietroti.com/"),
    ("bm24", "Paris Banh Mi (USA)", "https://www.parisbanhmi.com/"),
    ("bm25", "Banh Mi Kitchen", "https://banhmikitchen.ph/"),
    ("bm26", "Lee's Sandwiches (USA)", "https://leesandwiches.com/"),
    ("bm27", "Banh Mi & Ti (USA)", "https://www.banhmiandti.com/"),
    ("bm28", "Num Pang (NYC)", "https://eatnumpang.com/"),
    ("bm29", "Saigon Sisters (Chicago)", "https://www.saigonsisters.com/"),
    ("bm30", "Cafe Bunn Mi (SF)", "https://bunnmi.com/"),
    ("bm31", "Mr. Banh Mi (Brooklyn)", "https://mrbanhminyc.com/"),
    ("bm32", "Ba Le Sandwiches (Chicago)", "https://www.balesandwiches.com/"),
    ("bm33", "Bánh Mì Ông Mười (Chicago)", "https://banhmiongmuoi.com/"),
    ("bm34", "Lotus Banh Mi (Chicago)", "https://lotusbanhmi.com/"),
    ("bm35", "The Best Baguette (Portland)", "https://www.thebestbaguette.com/"),
    ("bm36", "Bánh Mì & Bottles (Denver)", "https://www.banhmibottles.com/"),
    ("bm37", "Bánh Mì Mẹ Ỉn (Saigon)", "https://banhmi.mein.vn/"),
    ("bm38", "Vietnom Local Eatery (DN/HA)", "https://vietnom.kitchen/"),
    ("bm39", "Bami Bread (VN)", "https://bamibread.com/"),
    ("bm40", "Anan Saigon (VN)", "https://www.anansaigon.com/"),
    ("bm41", "Banh Mi King (Amsterdam)", "https://banhmiking.nl/"),
    ("bm42", "Destination Roll (AU)", "https://destinationroll.co/"),
]

results = []
for cid, name, url in urls:
    ok, reason, final_url, title = verify_url_health(url, timeout=12)
    print(f"{cid} | {'OK  ' if ok else 'FAIL'} | {name:28s} | {final_url} | {reason}")
    results.append({"id": cid, "name": name, "url": url, "ok": ok, "final_url": final_url, "reason": reason, "title": title})

out_path = r"d:\AI Agent\Website\Tìm mẫu website\_Luu_Tru_Ky_Thuat\03_Du_Lieu_Tam_Va_Test\banh_mi_quoc_te_health_check.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
