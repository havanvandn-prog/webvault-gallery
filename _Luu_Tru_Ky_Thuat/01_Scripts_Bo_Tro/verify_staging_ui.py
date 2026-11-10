# -*- coding: utf-8 -*-
import os, sys, time, threading, http.server, socketserver
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
os.chdir(BASE_DIR)

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

srv = socketserver.TCPServer(("127.0.0.1", 0), QuietHandler)
port = srv.server_address[1]
t = threading.Thread(target=srv.serve_forever, daemon=True)
t.start()

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))

    pg.goto(f"http://127.0.0.1:{port}/web_nhap_staging.html?industry=landing-page-lap-mang", wait_until="networkidle")
    time.sleep(0.5)
    c_lp = pg.locator(".staging-card").count()
    b_all = pg.locator("#badgeAll").inner_text()
    b_lp = pg.locator("#badgeLpLapMang").inner_text()
    b_fpt = pg.locator("#badgeFpt").inner_text()
    b_cf = pg.locator("#badgeCafeBanhMi").inner_text()

    pg.evaluate("() => document.querySelectorAll('img').forEach(i => i.loading='eager')")
    time.sleep(1.5)
    bad = pg.evaluate("""() => Array.from(document.querySelectorAll('.card-thumb-img')).filter(i => !i.complete || i.naturalWidth === 0).map(i => i.src)""")

    # Test lightbox on LPF01
    pg.locator(".card-thumbnail-box").first.click()
    time.sleep(0.6)
    lb_idx = pg.locator("#lbIndex").inner_text()
    lb_w = pg.evaluate("() => document.getElementById('lbImage').naturalWidth")
    lb_h = pg.evaluate("() => document.getElementById('lbImage').naturalHeight")

    # Test switching to lap-mang-fpt URL param (previous bug check!)
    pg.goto(f"http://127.0.0.1:{port}/web_nhap_staging.html?industry=lap-mang-fpt", wait_until="networkidle")
    time.sleep(0.5)
    c_fpt = pg.locator(".staging-card").count()
    topic_fpt = pg.locator("#statTopicName").inner_text()

    print(f"LP cards: {c_lp} | FPT cards: {c_fpt}")
    print(f"Badges (All/LP/FPT/Cafe): {b_all}/{b_lp}/{b_fpt}/{b_cf}")
    print(f"Bad thumb images: {bad}")
    print(f"Lightbox LPF01: {lb_idx} | {lb_w}x{lb_h}")
    print(f"FPT topic header: {topic_fpt}")
    print(f"JS errors: {errs}")
    assert c_lp == 20 and c_fpt == 20 and b_all == "201" and len(bad) == 0 and lb_w == 1440 and len(errs) == 0, "Verification FAILED!"
    print("[PASS] ALL STAGING VERIFICATIONS PASSED!")
    b.close()

srv.shutdown()
