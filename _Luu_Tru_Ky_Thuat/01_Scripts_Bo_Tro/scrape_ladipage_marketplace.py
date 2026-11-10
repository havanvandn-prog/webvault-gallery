# -*- coding: utf-8 -*-
import sys, time, json, re
from playwright.sync_api import sync_playwright
import requests

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

# 1. Inspect showcase & demo URLs directly for title/text/nav/suspension
direct_check = [
    "https://lp-fiber.vercel.app/",
    "https://wificbnpalembang.framer.website/",
    "https://stallion.framer.website/",
    "https://redxmedia.net/preview/2502",
    "https://showcase.ladi.me/64ed9b10f862bd0012aaf304",
    "https://showcase.ladi.me/648b32090188320011648a54",
    "https://www.tongdaitructuyen.vn/vienthongcardinallapinternet",
    "https://www.cskh1900.com/internet2",
    "https://www.tongdaihotro.vn/",
    "https://fpthotline.net/",
    "https://5gvt.vn/lap-mang-viettel/",
    "https://www.viettelhochiminh.vn/",
    "https://viettelkhuyenmai.vn/",
    "https://capquangvnpt24h.com/",
    "https://fptnet.vn/",
    "https://www.mangfpt.info.vn/"
]

print("=== 1. Playwright Visual/Text Audit of Key Candidates ===")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1440, "height": 900}, user_agent=headers["User-Agent"])
    page = ctx.new_page()

    for url in direct_check:
        try:
            resp = page.goto(url, wait_until="domcontentloaded", timeout=15000)
            time.sleep(2)
            info = page.evaluate("""() => {
                const text = (document.body.innerText || '').replace(/\\s+/g, ' ').trim();
                const title = document.title || '';
                const navLinks = document.querySelectorAll('header a, nav a, .menu a, .navbar a').length;
                const forms = document.querySelectorAll('form').length;
                const h = Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);
                const iframes = Array.from(document.querySelectorAll('iframe')).map(f => f.src);
                const visibleLinks = Array.from(document.querySelectorAll('header a, nav a')).map(a => (a.innerText || '').trim()).filter(Boolean).slice(0, 10);
                return {title, navLinks, forms, h, iframes, visibleLinks, snippet: text.slice(0, 180)};
            }""")
            status = resp.status if resp else 0
            dead_flag = any(k in (info['snippet'] + info['title']).lower() for k in ["ngừng hoạt động", "suspended", "không tồn tại", "404"])
            print(f"[{status}] {'DEAD' if dead_flag else 'LIVE'} | {url}")
            print(f"    Title: {info['title'][:65]} | H={info['h']}px | Nav={info['navLinks']} {info['visibleLinks'][:5]} | Forms={info['forms']}")
            if info['iframes']:
                print(f"    Iframes: {info['iframes'][:3]}")
            print(f"    Text: {info['snippet'][:140]}")
        except Exception as e:
            print(f"[ERR] {url} -> {str(e)[:70]}")

    # 2. Search marketplace.ladipage.vn via Playwright
    print("\n=== 2. Crawling LadiPage Marketplace ===")
    ladi_theme_urls = set()
    for term in ["fpt", "wifi", "internet", "viettel", "vnpt", "mạng", "cáp quang"]:
        try:
            search_url = f"https://marketplace.ladipage.vn/search?q={term}"
            page.goto(search_url, wait_until="networkidle", timeout=15000)
            time.sleep(2)
            links = page.evaluate("""() => Array.from(document.querySelectorAll('a[href*="/theme/"]')).map(a => ({href: a.href, text: (a.innerText||'').replace(/\\s+/g,' ').trim()}))""")
            print(f"Search '{term}': {len(links)} theme links")
            for l in links:
                print(f"   {l['href']} | {l['text'][:50]}")
                ladi_theme_urls.add(l['href'])
        except Exception as e:
            print(f"Search '{term}' err:", str(e)[:60])

    # Also check NVA profile on LadiPage Marketplace
    try:
        page.goto("https://marketplace.ladipage.vn/profileId/5e51ff6161a254079fc6d2ed", wait_until="networkidle", timeout=15000)
        time.sleep(2)
        links = page.evaluate("""() => Array.from(document.querySelectorAll('a[href*="/theme/"]')).map(a => ({href: a.href, text: (a.innerText||'').replace(/\\s+/g,' ').trim()})).filter(x => /wifi|internet|fpt|viettel|vnpt|mạng|camera/i.test(x.text + x.href))""")
        print(f"NVA profile internet themes: {len(links)}")
        for l in links:
            print("  ", l['href'], "|", l['text'][:50])
            ladi_theme_urls.add(l['href'])
    except Exception as e:
        print("NVA profile err:", str(e)[:60])

    browser.close()
