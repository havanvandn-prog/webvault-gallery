# -*- coding: utf-8 -*-
import os, sys, time, json
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts")
from capture_engine import setup_page_protection, capture_smart_clean, compress_tri_layer, verify_captured_image
from playwright.sync_api import sync_playwright

meta_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "boardgame_bw_candidates.json")
with open(meta_path, "r", encoding="utf-8") as f:
    cands = json.load(f)

site = next(x for x in cands if x["id"] == "bg05")
raw_png = os.path.join(BASE_DIR, "Anh_Chup_Website", f"{site['slug']}.png")
kho_webp_dir = os.path.join(BASE_DIR, "Kho_Anh_Webp")
full_webp = os.path.join(kho_webp_dir, f"{site['slug']}_full.webp")

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    ctx = b.new_context(viewport={"width": 1440, "height": 900}, ignore_https_errors=True,
                        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    pg = ctx.new_page()
    setup_page_protection(pg)
    pg.goto(site["url"], timeout=45000, wait_until="domcontentloaded")
    time.sleep(3.5)
    pg.evaluate("""() => {
        document.querySelectorAll('button, a').forEach(el => {
            const t = (el.innerText || '').trim().toLowerCase();
            if (['ok', 'accept', 'accept all'].includes(t)) { try { el.click(); } catch(e) {} }
        });
    }""")
    time.sleep(0.8)
    capture_smart_clean(pg, raw_png, viewport_height=900, scroll_delay=0.3)
    thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb = compress_tri_layer(raw_png, site["slug"], kho_webp_dir)
    valid, msg = verify_captured_image(full_webp)
    print(f"bg05 QA: {'PASS' if valid else 'FAIL'} - {msg}")
    site["thumb_kb"] = thumb_kb
    site["full_kb"] = full_kb
    site["fb_kb"] = fb_kb
    site["size_mb"] = f"{round(os.path.getsize(raw_png) / (1024*1024), 2)} MB"
    site["audit_msg"] = msg
    site["status"] = "SUCCESS" if valid else "FAIL"
    ctx.close()
    b.close()

with open(meta_path, "w", encoding="utf-8") as f:
    json.dump(cands, f, ensure_ascii=False, indent=2)
