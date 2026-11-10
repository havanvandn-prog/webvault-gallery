# -*- coding: utf-8 -*-
import os, sys, time
sys.stdout.reconfigure(encoding='utf-8')
sys.path.append(r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts")
from capture_engine import verify_url_health, capture_smart_clean, super_hydrate, setup_page_protection, compress_tri_layer, verify_captured_image
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
out_dir = os.path.join(BASE_DIR, "Anh_Chup_Website")
kho_dir = os.path.join(BASE_DIR, "Kho_Anh_Webp")

# Test candidates + full_page fix on fpt.vn & fpttelecomvietnam.vn
targets = [
    ("lp_zainet_v1", "https://zainet.webflow.io/home-pages/home-v1"),
    ("lp_dangkywifivnpt", "https://dangkywifivnpt.io.vn/"),
    ("lp_fpt_doanh_nghiep", "https://fpt.vn/internet-doanh-nghiep"),
    ("lp_fpt_play_lp", "https://fpt.vn/truyen-hinh-fpt-play"),
    ("lp_fpttelecomvietnam_vn", "https://www.fpttelecomvietnam.vn/"),
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    for slug, url in targets:
        ok_h, msg_h, _, ttl = verify_url_health(url)
        print(f"\n[{slug}] health={ok_h} ({msg_h}) title={ttl[:50]}")
        ctx = browser.new_context(
            viewport={"width": 1440, "height": 900},
            ignore_https_errors=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = ctx.new_page()
        setup_page_protection(page)
        page.goto(url, wait_until="domcontentloaded", timeout=35000)
        time.sleep(2.5)
        page.evaluate("""() => {
            document.querySelectorAll('.ladi-lazyload').forEach(el => el.classList.remove('ladi-lazyload'));
        }""")
        page.add_style_tag(content="html, body { scroll-behavior: auto !important; }")
        fp = os.path.join(out_dir, f"{slug}.png")

        # Scroll down and back to hydrate everything
        super_hydrate(page)
        h = page.evaluate("() => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
        y = 0
        while y < h:
            page.evaluate(f"() => {{ window.scrollTo(0, {y}); document.documentElement.scrollTop = {y}; }}")
            time.sleep(0.2)
            y += 600
            h = page.evaluate("() => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
        page.evaluate("() => { window.scrollTo(0, 0); document.documentElement.scrollTop = 0; }")
        time.sleep(0.8)

        # Hide floating fixed/sticky elements cleanly (keep header if top < 80 & height < 140 by switching fixed->relative or hiding bottom widgets)
        page.evaluate("""() => {
            document.querySelectorAll('*').forEach(el => {
                const s = window.getComputedStyle(el);
                if (s.position === 'fixed' || s.position === 'sticky') {
                    const r = el.getBoundingClientRect();
                    if (r.top <= 60 && r.height <= 160 && el.tagName !== 'BODY') {
                        // header bar - leave at top or static so it doesn't follow full_page screenshot
                        el.style.setProperty('position', 'relative', 'important');
                    } else {
                        el.style.setProperty('display', 'none', 'important');
                    }
                }
            });
        }""")
        time.sleep(0.3)
        page.screenshot(path=fp, full_page=True)
        compress_tri_layer(fp, slug, kho_dir)
        ok_i, amsg = verify_captured_image(os.path.join(kho_dir, f"{slug}_full.webp"))
        print(f"  Full-page screenshot -> QA: {ok_i} | {amsg}")
        ctx.close()
    browser.close()
