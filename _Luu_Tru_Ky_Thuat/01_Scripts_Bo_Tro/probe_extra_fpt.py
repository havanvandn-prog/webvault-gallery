# -*- coding: utf-8 -*-
import os, sys, time, requests
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts")
from capture_engine import compress_tri_layer, verify_captured_image, setup_page_protection, super_hydrate
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
out_dir = os.path.join(BASE_DIR, "Anh_Chup_Website")
kho_dir = os.path.join(BASE_DIR, "Kho_Anh_Webp")

for u in ['https://wififptlapdat.com/', 'https://vn-fpt.com/', 'https://fpt-telecom.com.vn/']:
    try:
        r = requests.get(u, timeout=8, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36'})
        print(u, r.status_code, 'LADI' if 'ladipage' in r.text.lower() else 'WP/OTHER', 'len=', len(r.text))
    except Exception as e:
        print(u, "ERR:", str(e)[:80])

# Clean full_page capture of fpt.vn/internet-wifi-7-xgspon (expand FAQ cleanly without overlap) + test any live LadiPage
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    ctx = browser.new_context(
        viewport={"width": 1440, "height": 900},
        ignore_https_errors=True,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
    page = ctx.new_page()
    setup_page_protection(page)
    page.goto("https://fpt.vn/internet-wifi-7-xgspon", wait_until="domcontentloaded", timeout=35000)
    time.sleep(2.5)
    page.add_style_tag(content="html, body { scroll-behavior: auto !important; } * { transition: none !important; }")
    super_hydrate(page)
    h = page.evaluate("() => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
    y = 0
    while y < h:
        page.evaluate(f"() => {{ window.scrollTo(0, {y}); document.documentElement.scrollTop = {y}; }}")
        time.sleep(0.2)
        y += 600
        h = page.evaluate("() => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
    page.evaluate("() => { window.scrollTo(0, 0); document.documentElement.scrollTop = 0; }")
    time.sleep(0.5)
    page.evaluate("""() => {
        document.querySelectorAll('*').forEach(el => {
            const s = window.getComputedStyle(el);
            if (s.position === 'fixed' || s.position === 'sticky') {
                const r = el.getBoundingClientRect();
                if (r.top <= 60 && r.height <= 160 && el.tagName !== 'BODY') {
                    el.style.setProperty('position', 'relative', 'important');
                } else {
                    el.style.setProperty('display', 'none', 'important');
                }
            }
        });
    }""")
    time.sleep(0.3)
    fp = os.path.join(out_dir, "lp_fpt_wifi7_xgspon.png")
    page.screenshot(path=fp, full_page=True)
    compress_tri_layer(fp, "lp_fpt_wifi7_xgspon", kho_dir)
    ok_i, amsg = verify_captured_image(os.path.join(kho_dir, "lp_fpt_wifi7_xgspon_full.webp"))
    print("Re-captured lp_fpt_wifi7_xgspon:", ok_i, amsg)
    browser.close()
