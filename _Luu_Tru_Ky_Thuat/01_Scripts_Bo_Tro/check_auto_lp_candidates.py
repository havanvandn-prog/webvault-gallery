# -*- coding: utf-8 -*-
import os, sys, json, re, concurrent.futures

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)

import requests
from bs4 import BeautifulSoup
from capture_engine import verify_url_health

URLS = [
    # Mercedes-Benz VN (priority)
    ("Mercedes-Benz Việt Nam (Chính thức)", "https://www.mercedes-benz.com.vn/"),
    ("Mercedes Vietnam Star", "https://mercedes-vietnamstar.vn/"),
    ("Mercedes Vietnam Star (com.vn)", "https://mercedes-vietnamstar.com.vn/"),
    ("Mercedes An Du (hanoi.vn)", "https://mercedesbenz.hanoi.vn/"),
    ("Mercedes Haxaco", "https://mercedes-haxaco.com/"),
    ("Mercedes Láng Hạ (Haxaco)", "https://langha-mercedes.com.vn/"),
    ("Mercedes-Benz Láng Hạ", "https://mercedesbenzlangha.com.vn/"),
    ("Mercedes-Benz An Du (com.vn)", "https://mercedesbenz-andu.com.vn/"),
    ("An Du Mercedes", "https://andu-mercedes.com/"),
    ("Mercedes Phú Mỹ Hưng", "https://mercedesphumyhung.com.vn/"),
    ("Mercedes Đà Nẵng (com.vn)", "https://mercedes-danang.com.vn/"),
    ("Mercedes Đà Nẵng", "https://mercedes-danang.com/"),
    ("Mercedes Automobile", "https://mercedesbenz-automobile.com.vn/"),
    ("Mercedes-Automobile VN", "https://mercedes-automobile.vn/"),
    ("Kha Mercedes", "https://khamercedes.vn/"),
    ("Giá Xe Mercedes (com.vn)", "https://giaxemercedes.com.vn/"),
    ("Giá Xe Mercedes (vn)", "https://giaxemercedes.vn/"),
    ("Mercedes Vietnam Org", "https://mercedes-vietnam.org/"),
    ("Mercedes Vietnam VN", "https://mercedesvietnam.vn/"),
    ("Mercedes Vietnam Com", "https://mercedesvietnam.com/"),
    ("Mercedes-Benz VN", "https://mercedes-benz-vn.com/"),
    ("Mercedes-Benz Hà Nội (com.vn)", "https://mercedes-benz-hanoi.com.vn/"),
    ("Mercedes Hà Nội (com.vn)", "https://mercedeshanoi.com.vn/"),
    ("Mercedess-Benz VN", "https://mercedess-benz.vn/"),
    ("Mercedes Car VN", "https://mercedes-car.com.vn/"),
    ("Mercedes Star VN", "https://mercedesstar.vn/"),
    ("Mercedes VN (mercedesvn.vn)", "https://mercedesvn.vn/"),
    ("Mercedes Hà Nội (mercedes-hanoi.com.vn)", "https://mercedes-hanoi.com.vn/"),
    ("Xe Mercedes Net", "https://xemercedes.net/"),
    ("Xe Mercedes VN", "https://xemercedes.vn/"),
    ("Haxaco Corp", "https://haxaco.com.vn/"),
    ("Mercedes Vietnam Star (mercedesvietnamstar.vn)", "https://mercedesvietnamstar.vn/"),
    # Other luxury & high-converting VN auto landing pages
    ("Lexus Center Sài Gòn", "https://lexuscentersaigon.com/"),
    ("Lexus Saigon Center", "https://lexussaigoncenter.vn/"),
    ("Lexus Hà Nội", "https://lexus-hanoi.vn/"),
    ("Volvo Car Vietnam", "https://volvocars.vn/"),
    ("Volvo Vietnam", "https://volvovietnam.vn/"),
    ("Volvo Car Hà Nội", "https://volvocarhanoi.vn/"),
    ("Volvo Hà Nội", "https://volvo-hanoi.vn/"),
    ("BMW Miền Bắc", "https://bmwmienbac.com.vn/"),
    ("BMW Việt Nam", "https://bmwvietnam.vn/"),
    ("Audi Hồ Chí Minh", "https://audi-hcmc.vn/"),
    ("VinFast Sài Gòn", "https://vinfast-saigon.com.vn/"),
    ("VinFast TP.HCM", "https://vinfast-tphcm.vn/"),
    ("VinFast Ô Tô Miền Nam", "https://vinfastotomiennam.com/"),
    ("VinFast VN", "https://vinfast-vn.vn/"),
    ("VinFast Hà Nội", "https://vinfasthanoi.net/"),
    ("VinFast Việt Nam", "https://vinfastvietnam.com.vn/"),
    ("Sài Gòn Ford", "https://saigonford.com.vn/"),
    ("Gia Định Ford", "https://giadinhford.com.vn/"),
    ("Dana Ford Đà Nẵng", "https://danaford.com.vn/"),
]

def inspect_url(item):
    name, url = item
    healthy, reason, final_url, title = verify_url_health(url, timeout=12)
    if not healthy:
        return {"name": name, "url": url, "healthy": False, "reason": reason}
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
        r = requests.get(final_url, headers=headers, timeout=12, allow_redirects=True)
        r.encoding = r.apparent_encoding or 'utf-8'
        html = r.text
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text(" ", strip=True).lower()
        forms = len(soup.find_all('form'))
        inputs = len(soup.find_all(['input', 'select', 'textarea']))
        tel_links = len(soup.select('a[href^="tel:"]'))
        zalo_links = len([a for a in soup.find_all('a', href=True) if 'zalo.me' in a['href'].lower()])
        is_ladipage = ('ladipage' in html.lower()) or ('ldi-' in html.lower())
        is_wp = ('wp-content' in html.lower())
        
        cro_keywords = ['báo giá', 'lăn bánh', 'lái thử', 'trả góp', 'ưu đãi', 'khuyến mãi', 'đặt cọc', 'liên hệ ngay', 'tư vấn']
        matched_kws = [kw for kw in cro_keywords if kw in text]
        
        # Check nav link count to distinguish pure Landing Page vs large portal
        nav_links = len(soup.select('header a, nav a'))
        
        # Score CRO readiness
        cro_score = len(matched_kws) * 10 + min(forms, 3) * 15 + min(tel_links, 2) * 10 + (10 if zalo_links else 0) + (15 if is_ladipage else 0)
        
        return {
            "name": name,
            "url": url,
            "final_url": r.url,
            "healthy": True,
            "title": (soup.title.string.strip() if soup.title and soup.title.string else title)[:100],
            "forms": forms,
            "inputs": inputs,
            "tel": tel_links,
            "zalo": zalo_links,
            "nav_links": nav_links,
            "is_ladipage": is_ladipage,
            "is_wp": is_wp,
            "matched_kws": matched_kws,
            "cro_score": cro_score,
            "html_len": len(html)
        }
    except Exception as e:
        return {"name": name, "url": url, "healthy": False, "reason": f"Inspect error: {str(e)[:60]}"}

results = []
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
    for res in ex.map(inspect_url, URLS):
        results.append(res)

healthy_list = [r for r in results if r.get("healthy")]
failed_list = [r for r in results if not r.get("healthy")]

healthy_list.sort(key=lambda x: x.get("cro_score", 0), reverse=True)

print(f"=== HEALTHY: {len(healthy_list)} | FAILED: {len(failed_list)} ===\n")
print("--- TOP HEALTHY CANDIDATES (SORTED BY CRO SCORE) ---")
for i, r in enumerate(healthy_list, 1):
    tech = "LadiPage" if r['is_ladipage'] else ("WordPress" if r['is_wp'] else "Custom/CMS")
    print(f"{i:02d}. [{r['cro_score']:3d}] {r['name']} | {r['final_url']} | {tech} | Forms:{r['forms']} Inputs:{r['inputs']} Tel:{r['tel']} Zalo:{r['zalo']} Nav:{r['nav_links']} | KWs:{len(r['matched_kws'])} ({', '.join(r['matched_kws'][:5])})")

print("\n--- FAILED ---")
for r in failed_list:
    print(f"  X {r['name']} ({r['url']}): {r['reason']}")

out_path = os.path.join(os.path.dirname(__file__), "..", "03_Du_Lieu_Tam_Va_Test", "auto_lp_health_check.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump({"healthy": healthy_list, "failed": failed_list}, f, ensure_ascii=False, indent=2)
print(f"\nSaved to {out_path}")
