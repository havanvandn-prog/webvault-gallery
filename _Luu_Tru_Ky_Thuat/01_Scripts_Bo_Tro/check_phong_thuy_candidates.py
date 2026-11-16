# -*- coding: utf-8 -*-
import os
import sys
import json

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)
from capture_engine import verify_url_health

URLS = [
    # International
    "https://www.dearmodern.com/",
    "https://www.fengshuiconcepts.com.au/",
    "https://www.joeyyap.com/",
    "https://www.wayfengshui.com/",
    "https://www.masterseanchan.com/",
    "https://luminousspaces.com/",
    "https://fengshuidana.com/",
    "https://fengshuiagency.com/",
    "https://energymuse.com/",
    "https://www.wofs.com/",
    "https://redlotusletter.com/",
    "https://www.fengshuiweb.co.uk/",
    "https://thefengshuiinstitute.com/",
    # Vietnam Consulting & Architecture & Astrology
    "https://phongthuyphunggia.com/",
    "https://phongthuydainam.vn/",
    "https://phongthuytamnguyen.com/",
    "https://phongthuyvuong.com/",
    "https://phongthuytuongminh.com/",
    "https://phongthuyhoangtra.vn/",
    "https://phongthuytagia.com/",
    "https://chuyengianguyenngoan.com/",
    "https://thuatphongthuy.vn/",
    "https://nhaxuan.vn/",
    "https://lichngaytot.com/",
    "https://phongthuyso.vn/",
    "https://tuvi.vn/",
    # Vietnam Jewelry, Crystals & Agarwood
    "https://thienmochuong.com/",
    "https://ancarat.com/",
    "https://mixi.vn/",
    "https://liu.com.vn/",
    "https://kaigold.vn/",
    "https://joca.vn/",
    "https://ngoctramhuong.vn/",
    "https://vanhoatramhuong.com/",
    "https://phongthuyankhang.com/",
]

results = []
for u in URLS:
    ok, reason, final_url, title = verify_url_health(u, timeout=12)
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {u} -> {final_url} | {reason} | Title: {title[:70]}")
    results.append({
        "url": u,
        "ok": ok,
        "reason": reason,
        "final_url": final_url,
        "title": title
    })

out_path = os.path.join(os.path.dirname(__file__), "..", "03_Du_Lieu_Tam_Va_Test", "phong_thuy_health_check.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nPassed: {sum(1 for r in results if r['ok'])}/{len(results)}")
