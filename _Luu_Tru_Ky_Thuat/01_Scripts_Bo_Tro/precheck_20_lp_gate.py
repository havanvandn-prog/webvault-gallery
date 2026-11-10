# -*- coding: utf-8 -*-
import os, sys, json, time
from playwright.sync_api import sync_playwright

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts")
from capture_engine import verify_url_health

with open(os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "staging_all_candidates.json"), "r", encoding="utf-8") as f:
    existing = json.load(f)
id_prefixes = sorted(set(c["id"][:3] for c in existing))
industries = sorted(set(c["industry"] for c in existing))
print("Existing ID prefixes:", id_prefixes)
print("Existing industries:", industries)

test_urls = [
    "https://www.mangfpt.info.vn/",
    "https://www.fpttelecomvietnam.vn/",
    "https://w.tuybutky.com/dich-vu-wifi-0056",
    "https://w.tuybutky.com/497.-fpt-wifi-1070",
    "https://w.tuybutky.com/715.-fpt-internet-1481",
    "https://w.tuybutky.com/gioi-thieu-fpt-play-box-1063",
    "https://showcase.ladi.me/64ed9b10f862bd0012aaf304",
    "https://viettelca.vn/goi-cuoc-lap-mang-internet-wifi-viettel.html",
    "https://fpt.vn/internet",
    "https://fpt.vn/internet-wifi-7-xgspon",
    "https://fpt.vn/internet-doanh-nghiep",
    "https://fpt.vn/truyen-hinh-fpt-play",
    "https://fptnet.vn/",
    "https://fpthotline.net/",
    "https://5gvt.vn/lap-mang-viettel/",
    "https://www.viettelhochiminh.vn/",
    "https://opnet.framer.website/",
    "https://wificbnpalembang.framer.website/",
    "https://stallion.framer.website/",
    "https://zainet.webflow.io/",
    "https://novos-fiber.webflow.io/",
    "https://broadband-and-telecom-128.webflow.io/",
    "https://tristate-wifi.webflow.io/",
    "https://zaivoip.webflow.io/",
    "https://w.tuybutky.com/735.-camera-se-fpt-1495"
]

print("\n=== 1. Running Pre-Capture Health Gate (verify_url_health) ===")
for u in test_urls:
    ok, reason, final_url, title = verify_url_health(u, timeout=10)
    print(f"[{'PASS' if ok else 'FAIL'}] {u:62s} | {reason} | {title[:35]}")

print("\n=== 2. Playwright check on Opnet + FPT doanh nghiep + FPT Play ===")
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--no-sandbox"])
    ctx = b.new_context(viewport={"width": 1440, "height": 900}, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36")
    pg = ctx.new_page()
    for u in ["https://opnet.framer.website/", "https://fpt.vn/internet-doanh-nghiep", "https://fpt.vn/truyen-hinh-fpt-play"]:
        resp = pg.goto(u, wait_until="domcontentloaded", timeout=15000)
        time.sleep(2.5)
        d = pg.evaluate("() => ({h: document.body.scrollHeight, title: document.title, nav: document.querySelectorAll('header a, nav a').length, badImgs: Array.from(document.querySelectorAll('img')).filter(i=>i.complete && i.naturalWidth===0).length, text: document.body.innerText.replace(/\\s+/g,' ').slice(0,140)})")
        print(f"[{resp.status}] {u:42s} | H={d['h']} | Nav={d['nav']} | BadImg={d['badImgs']} | {d['title'][:40]} | {d['text'][:90]}")
    b.close()
