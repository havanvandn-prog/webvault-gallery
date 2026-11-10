# -*- coding: utf-8 -*-
import sys, time
from playwright.sync_api import sync_playwright

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

candidates = [
    # Group 1: LadiPage Vietnam
    ("Ladi FPT Info", "https://www.mangfpt.info.vn/"),
    ("Ladi FPT TelecomVN", "https://www.fpttelecomvietnam.vn/"),
    ("Ladi WiFi 0056", "https://w.tuybutky.com/dich-vu-wifi-0056"),
    ("Ladi FPT HCM 1070", "https://w.tuybutky.com/497.-fpt-wifi-1070"),
    ("Ladi FPT Net 1481", "https://w.tuybutky.com/715.-fpt-internet-1481"),
    ("Ladi FPT PlayBox 1063", "https://w.tuybutky.com/gioi-thieu-fpt-play-box-1063"),
    ("Ladi FPT CamSE 1495", "https://w.tuybutky.com/735.-camera-se-fpt-1495"),
    ("Ladi Viettel Showcase", "https://showcase.ladi.me/64ed9b10f862bd0012aaf304"),
    ("Ladi ViettelCA", "https://viettelca.vn/goi-cuoc-lap-mang-internet-wifi-viettel.html"),

    # Group 2: Dedicated Ads / Official Campaign LPs Vietnam
    ("FPT Official LP", "https://fpt.vn/internet"),
    ("FPT WiFi7 XGS-PON", "https://fpt.vn/internet-wifi-7-xgspon"),
    ("FPTNet 1-Page", "https://fptnet.vn/"),
    ("WiFi24h 1-Page", "https://wifi24h.vn/"),
    ("FPTHotline Ads LP", "https://fpthotline.net/"),
    ("5GVT Viettel LP", "https://5gvt.vn/lap-mang-viettel/"),
    ("VNPT 24h LP", "https://capquangvnpt24h.com/"),
    ("Viettel HCM LP", "https://www.viettelhochiminh.vn/"),
    ("Viettel KhuyenMai", "https://viettelkhuyenmai.vn/"),

    # Group 3: International Webflow / Framer / Elementor Fiber LPs
    ("WF Broadband 128", "https://broadband-and-telecom-128.webflow.io/"),
    ("WF Zainet Fiber", "https://zainet.webflow.io/"),
    ("WF Novos Fiber", "https://novos-fiber.webflow.io/"),
    ("WF Tristate Fiber", "https://tristate-wifi.webflow.io/"),
    ("WF ZaiVOIP", "https://zaivoip.webflow.io/"),
    ("Framer CBN Fiber", "https://wificbnpalembang.framer.website/"),
    ("Framer Stallion Net", "https://stallion.framer.website/"),
    ("Yodden Fiber WP", "https://demo.deverust.com/netlink/template-kit/home/"),
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
    ctx = browser.new_context(
        viewport={"width": 1440, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
    page = ctx.new_page()

    for label, url in candidates:
        try:
            resp = page.goto(url, wait_until="domcontentloaded", timeout=18000)
            time.sleep(2.2)
            status = resp.status if resp else 0
            data = page.evaluate("""() => {
                const title = document.title || '';
                const text = (document.body.innerText || '').replace(/\\s+/g, ' ').trim();
                const h = Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);
                const h1 = (document.querySelector('h1')?.innerText || '').replace(/\\s+/g, ' ').trim();
                const navA = Array.from(document.querySelectorAll('header a, nav a'));
                const topExternalLinks = navA.filter(a => {
                    const href = a.getAttribute('href') || '';
                    return href && !href.startsWith('#') && !href.startsWith('tel:') && !href.startsWith('javascript');
                }).length;
                const imgs = Array.from(document.querySelectorAll('img'));
                const brokenImgs = imgs.filter(i => i.complete && i.naturalWidth === 0).length;
                const forms = document.querySelectorAll('form').length;
                const isLadi = !!document.querySelector('.ladi-section, .ladi-wraper') || document.documentElement.innerHTML.includes('w.ladicdn.com');
                return {title, h, h1, navTotal: navA.length, extNav: topExternalLinks, imgs: imgs.length, brokenImgs, forms, isLadi, snippet: text.slice(0, 120)};
            }""")
            dead = any(k in (data['title'] + data['snippet']).lower() for k in ["ngừng hoạt động", "suspended", "cloudflare", "attention required", "just a moment", "403 forbidden", "404"])
            flag = "FAIL" if (status != 200 or dead or data['h'] < 1200) else "OK"
            print(f"[{flag:4s} {status}] {label:21s} | H={data['h']:5d} | Ladi={str(data['isLadi']):5s} | Nav={data['navTotal']:2d}(ext:{data['extNav']:2d}) | Form={data['forms']:2d} | Imgs={data['imgs']:2d}(bad:{data['brokenImgs']}) | {data['title'][:38]} | H1:{data['h1'][:35]}")
        except Exception as e:
            print(f"[ERR     ] {label:21s} | {url} -> {str(e)[:65]}")

    browser.close()
