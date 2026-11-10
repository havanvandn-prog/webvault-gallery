# -*- coding: utf-8 -*-
import json
import os
import re
import sys
import time
import requests
from bs4 import BeautifulSoup

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
meta_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "lap_mang_fpt_metadata.json")

with open(meta_file, "r", encoding="utf-8") as f:
    items = json.load(f)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

results = []

for it in items:
    url = it["url"]
    domain = it["domain"]
    t0 = time.time()
    try:
        r = requests.get(url, headers=headers, timeout=12)
        ttfb = round(time.time() - t0, 2)
        html = r.text
        soup = BeautifulSoup(html, "html.parser")
        
        forms = soup.find_all("form")
        # Count visible-like inputs inside forms (exclude hidden, submit)
        form_details = []
        for fm in forms:
            inputs = [inp for inp in fm.find_all(["input", "select", "textarea"]) if inp.get("type") not in ["hidden", "submit", "button"]]
            if len(inputs) > 0:
                form_details.append(len(inputs))
        
        tel_links = len(soup.find_all("a", href=re.compile(r"^tel:", re.I)))
        zalo_links = len(soup.find_all("a", href=re.compile(r"zalo\.me|chat\.zalo", re.I)))
        
        text = soup.get_text(" ", strip=True).lower()
        has_giga_sky_meta = all(k in text for k in ["giga", "sky", "meta"])
        has_wifi6 = "wifi 6" in text or "wi-fi 6" in text
        has_price = len(re.findall(r"\d{3}[\.,]000\s*[đd]|k/tháng|/tháng", text))
        has_faq = "câu hỏi thường gặp" in text or "thắc mắc" in text or "faq" in text
        has_process = "quy trình" in text or "bước 1" in text
        has_promo = "khuyến mãi" in text or "ưu đãi" in text or "tặng" in text
        has_table = len(soup.find_all("table"))
        
        # Check viewport meta for mobile
        vp = soup.find("meta", attrs={"name": re.compile("viewport", re.I)})
        mobile_ready = vp is not None
        
        # Get image height from Anh_Chup_Website if available
        from PIL import Image
        img_path = os.path.join(BASE_DIR, it["image"])
        img_h = 0
        if os.path.exists(img_path):
            with Image.open(img_path) as im:
                img_h = im.size[1]
        
        results.append({
            "id": it["id"],
            "domain": domain,
            "name": it["name"],
            "ttfb_s": ttfb,
            "html_kb": round(len(html) / 1024, 1),
            "img_h": img_h,
            "lead_forms": len(form_details),
            "min_form_fields": min(form_details) if form_details else 0,
            "tel_links": tel_links,
            "zalo_links": zalo_links,
            "price_mentions": has_price,
            "has_giga_sky_meta": has_giga_sky_meta,
            "has_wifi6": has_wifi6,
            "tables": has_table,
            "has_faq": has_faq,
            "has_process": has_process,
            "mobile_ready": mobile_ready,
            "status": r.status_code
        })
        print(f"[OK] {domain:26s} | TTFB: {ttfb:4.2f}s | H: {img_h:5d}px | Forms: {len(form_details)} (min {min(form_details) if form_details else 0}f) | Tel: {tel_links:2d} | Zalo: {zalo_links:2d} | PriceMentions: {has_price:2d} | Tables: {has_table}")
    except Exception as e:
        print(f"[ERR] {domain}: {e}")

out_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "fpt_cro_audit.json")
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print("Saved audit to", out_file)
