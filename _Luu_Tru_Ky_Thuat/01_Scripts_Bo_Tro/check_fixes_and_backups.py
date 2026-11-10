# -*- coding: utf-8 -*-
import os, sys, time
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts")
from capture_engine import verify_url_health, capture_smart_clean, compress_tri_layer, verify_captured_image
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
out_dir = os.path.join(BASE_DIR, "Anh_Chup_Website")
kho_dir = os.path.join(BASE_DIR, "Kho_Anh_Webp")

test_urls = [
    ("lp_zainet_home01", "https://zainet.webflow.io/home-pages/home-01"),
    ("lp_tristate_wifi", "https://tristate-wifi.webflow.io/"),
    ("lp_tuybutky_cam_1495", "https://w.tuybutky.com/735.-camera-se-fpt-1495"),
    ("lp_viettelhcm_vn", "https://www.viettelhochiminh.vn/"),
    ("lp_fpt_play_lp", "https://fpt.vn/truyen-hinh-fpt-play"),
]

print("--- CHECK HEALTH ---")
for slug, url in test_urls:
    ok, msg, final, title = verify_url_health(url)
    print(f"{slug}: {ok} | {msg} | {title[:60]}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    ctx = browser.new_context(
        viewport={"width": 1440, "height": 900},
        ignore_https_errors=True,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
    page = ctx.new_page()

    # Inspect floating pills on fpttelecomvietnam.vn
    print("\n--- INSPECT fpttelecomvietnam.vn floating ---")
    page.goto("https://www.fpttelecomvietnam.vn/", wait_until="domcontentloaded", timeout=30000)
    time.sleep(2)
    res = page.evaluate("""() => {
        window.scrollTo(0, 1500);
        const hits = [];
        document.querySelectorAll('*').forEach(el => {
            const txt = (el.innerText || '').trim();
            if (txt.includes('0977.055.282') && txt.length < 60 && el.children.length <= 4) {
                const s = window.getComputedStyle(el);
                hits.push({id: el.id, cls: el.className, pos: s.position, top: s.top, z: s.zIndex, text: txt});
            }
        });
        return hits.slice(0, 15);
    }""")
    for h in res:
        print(" ", h)

    # Inspect sticky lead bar on fpt.vn/internet-doanh-nghiep
    print("\n--- INSPECT fpt.vn/internet-doanh-nghiep bottom bar ---")
    page.goto("https://fpt.vn/internet-doanh-nghiep", wait_until="domcontentloaded", timeout=30000)
    time.sleep(2)
    res2 = page.evaluate("""() => {
        const hits = [];
        document.querySelectorAll('*').forEach(el => {
            const txt = (el.innerText || '').trim();
            if (txt.includes('Bạn cần hỗ trợ tư vấn sản phẩm') && txt.length < 300) {
                const s = window.getComputedStyle(el);
                hits.push({tag: el.tagName, cls: (el.className || '').slice(0, 80), pos: s.position, bottom: s.bottom, z: s.zIndex});
            }
        });
        return hits;
    }""")
    for h in res2:
        print(" ", h)

    # Capture Zainet Home 01, TriState WiFi, TuyButKy Cam 1495, ViettelHCM, FPT Play
    print("\n--- TEST CAPTURES ---")
    for slug, url in test_urls:
        fp = os.path.join(out_dir, f"{slug}.png")
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        time.sleep(2.5)
        page.evaluate("""() => document.querySelectorAll('.ladi-lazyload').forEach(el => el.classList.remove('ladi-lazyload'))""")
        sz = capture_smart_clean(page, fp, viewport_height=900, scroll_delay=0.22)
        compress_tri_layer(fp, slug, kho_dir)
        ok, amsg = verify_captured_image(os.path.join(kho_dir, f"{slug}_full.webp"))
        print(f"  Captured {slug}: {sz} -> QA: {ok} | {amsg}")

    browser.close()
