# -*- coding: utf-8 -*-
import sys
import time
import urllib.parse
from playwright.sync_api import sync_playwright

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(
        viewport={"width": 1440, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
    page = ctx.new_page()

    # 1. Check LadiPage Marketplace Theme Demo URL
    print("=== 1. Inspecting LadiPage Marketplace FPT Theme ===")
    try:
        page.goto("https://marketplace.ladipage.vn/theme/lap-dat-fpt-internet-camera-fpt-wifi-theme-mau-landing-page-dich-vu-mang-nva1481-65ba0be5a0ca77001246d1d7", wait_until="networkidle", timeout=25000)
        time.sleep(2)
        links = page.evaluate("""() => {
            const iframes = Array.from(document.querySelectorAll('iframe')).map(i => i.src);
            const anchors = Array.from(document.querySelectorAll('a')).map(a => ({href: a.href, text: a.innerText}));
            return {iframes, anchors: anchors.filter(a => a.href.includes('preview') || a.href.includes('demo') || a.href.includes('ladipage') || a.text.toLowerCase().includes('xem'))};
        }""")
        print("Iframes:", links['iframes'])
        print("Anchors:", links['anchors'][:10])
    except Exception as e:
        print("Err LadiPage theme:", e)

    # 2. Search LadiPage Marketplace catalog
    print("\n=== 2. Searching LadiPage Marketplace ===")
    for kw in ["fpt", "internet", "wifi", "mạng", "viễn thông", "viettel", "camera"]:
        try:
            url = f"https://marketplace.ladipage.vn/?search={urllib.parse.quote(kw)}"
            page.goto(url, wait_until="networkidle", timeout=20000)
            time.sleep(2)
            # Check if there is a search input on the page
            cards = page.evaluate("""() => {
                return Array.from(document.querySelectorAll('a[href*="/theme/"]')).map(a => ({
                    href: a.href,
                    text: a.innerText.replace(/\\s+/g, ' ').trim()
                })).slice(0, 12);
            }""")
            print(f"Keyword '{kw}': {len(cards)} theme links")
            for c in cards[:6]:
                print("  ", c['href'], "|", c['text'][:50])
        except Exception as e:
            print(f"Err search {kw}:", e)

    # 3. Check nguyenvietanh.net demo links
    print("\n=== 3. Checking nguyenvietanh.net ===")
    try:
        page.goto("https://nguyenvietanh.net/mau-theme-landing-page-internet-wifi-camera/", wait_until="domcontentloaded", timeout=20000)
        time.sleep(2)
        links = page.evaluate("""() => {
            return Array.from(document.querySelectorAll('a')).map(a => ({href: a.href, text: a.innerText.trim()}))
                .filter(a => a.href.includes('demo') || a.href.includes('xem') || a.text.toLowerCase().includes('demo') || a.text.toLowerCase().includes('xem'));
        }""")
        print("NguyenVietAnh links:", links[:10])
    except Exception as e:
        print("Err nguyenvietanh:", e)

    # 4. Check fptnet.vn
    print("\n=== 4. Checking fptnet.vn ===")
    try:
        page.goto("https://fptnet.vn/", wait_until="domcontentloaded", timeout=20000)
        time.sleep(2)
        info = page.evaluate("""() => ({
            title: document.title,
            h1: document.querySelector('h1')?.innerText,
            height: document.body.scrollHeight,
            forms: document.querySelectorAll('form').length
        })""")
        print("fptnet.vn:", info)
    except Exception as e:
        print("Err fptnet:", e)

    # 5. Check Webflow made-in-webflow/internet
    print("\n=== 5. Checking Webflow Made in Webflow Internet ===")
    try:
        page.goto("https://webflow.com/made-in-webflow/internet", wait_until="domcontentloaded", timeout=20000)
        time.sleep(2)
        wf_links = page.evaluate("""() => {
            return Array.from(document.querySelectorAll('a[href*="/made-in-webflow/website/"]')).map(a => ({
                href: a.href,
                text: a.innerText.replace(/\\s+/g, ' ').trim()
            })).slice(0, 15);
        }""")
        print(f"Webflow internet items: {len(wf_links)}")
        for w in wf_links[:10]:
            print("  ", w['href'], "|", w['text'][:50])
    except Exception as e:
        print("Err webflow:", e)

    # 6. Check CocCoc Search for FPT landing pages
    print("\n=== 6. Checking CocCoc Search ===")
    for q in ['"lắp mạng fpt" ladipage', 'lắp mạng fpt khuyến mãi', 'đăng ký wifi fpt']:
        try:
            page.goto("https://coccoc.com/search?query=" + urllib.parse.quote(q), wait_until="domcontentloaded", timeout=20000)
            time.sleep(3)
            res = page.evaluate("""() => {
                return Array.from(document.querySelectorAll('a[href^="http"]')).map(a => a.href)
                    .filter(h => !h.includes('coccoc.com') && !h.includes('google.com'))
                    .slice(0, 15);
            }""")
            print(f"CocCoc '{q}': {len(res)} links")
            for r in res[:8]:
                print("  ", r)
        except Exception as e:
            print("Err coccoc:", e)

    browser.close()
