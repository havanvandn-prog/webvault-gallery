# -*- coding: utf-8 -*-
import sys
import time
import urllib.parse
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

found_candidates = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(
        viewport={"width": 1440, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
    page = ctx.new_page()

    # 1. Search Yahoo Vietnam for LadiPages & Landing Pages
    yahoo_queries = [
        '"lắp mạng fpt" site:ladipage.vn OR site:ladipage.me OR site:ldp.page',
        '"lắp mạng fpt" "ladipage"',
        '"lắp mạng fpt" "khuyến mãi" inurl:khuyen-mai',
        '"đăng ký mạng fpt" inurl:dang-ky',
        '"lắp mạng viettel" "ladipage"',
        '"lắp mạng vnpt" "ladipage"',
        '"mẫu landing page" "lắp mạng" OR "internet" OR "wifi"'
    ]
    print("=== 1. Searching Yahoo Vietnam ===")
    for q in yahoo_queries:
        try:
            page.goto("https://vn.search.yahoo.com/search?p=" + urllib.parse.quote(q), wait_until="domcontentloaded", timeout=15000)
            time.sleep(2)
            links = page.evaluate("""() => {
                return Array.from(document.querySelectorAll('#web ol li a[href^="http"]')).map(a => ({
                    href: a.href,
                    text: a.innerText.replace(/\\s+/g, ' ').trim()
                })).filter(x => !x.href.includes('yahoo.com') && !x.href.includes('bing.com'));
            }""")
            print(f"Yahoo '{q}': {len(links)} links")
            for l in links[:10]:
                # Decode yahoo RU redirect if needed
                href = l['href']
                if 'r.search.yahoo.com' in href and '/RU=' in href:
                    import re
                    m = re.search(r'/RU=([^/]+)/', href)
                    if m:
                        href = urllib.parse.unquote(m.group(1))
                print("  ", href, "|", l['text'][:45])
                found_candidates.append(href)
        except Exception as e:
            print("Yahoo err:", e)

    # 2. Search CocCoc for Viettel, VNPT, FPT sub-pages
    print("\n=== 2. Searching CocCoc for Viettel/VNPT/Internet LPs ===")
    for q in ["lắp mạng viettel", "lắp mạng vnpt", "đăng ký internet vnpt", "đăng ký cáp quang fpt", "lắp wifi gia đình fpt"]:
        try:
            page.goto("https://coccoc.com/search?query=" + urllib.parse.quote(q), wait_until="domcontentloaded", timeout=15000)
            time.sleep(2.5)
            links = page.evaluate("""() => Array.from(document.querySelectorAll('a[href^="http"]')).map(a => a.href).filter(h => !h.includes('coccoc.com') && !h.includes('yahoo.com') && !h.includes('bing.com') && !h.includes('google.com') && !h.includes('leafletjs'))""")
            seen = set()
            for l in links:
                cu = l.split('?')[0] if 'utm_' in l or 'aff_sid' in l else l
                if cu not in seen:
                    seen.add(cu)
                    print("  CC:", cu)
                    found_candidates.append(cu)
        except Exception as e:
            print("CC err:", e)

    # 3. Search nguyenvietanh.net for more w.tuybutky.com demos
    print("\n=== 3. Checking nguyenvietanh.net categories ===")
    for path in ["/danh-muc/cong-nghe/", "/danh-muc/dich-vu/", "/?s=wifi&post_type=product", "/?s=internet&post_type=product", "/?s=viettel&post_type=product", "/?s=vnpt&post_type=product", "/?s=fpt&post_type=product", "/?s=camera&post_type=product"]:
        try:
            page.goto("https://nguyenvietanh.net" + path, wait_until="domcontentloaded", timeout=15000)
            time.sleep(1.5)
            links = page.evaluate("""() => Array.from(document.querySelectorAll('a[href*="tuybutky"], .product a, h2 a, .woocommerce-LoopProduct-link')).map(a => a.href)""")
            for l in set(links):
                if "nguyenvietanh.net" in l or "tuybutky.com" in l:
                    print("  NVA link:", l)
                    found_candidates.append(l)
        except Exception as e:
            pass

    browser.close()

print(f"\n=== DONE: {len(set(found_candidates))} unique links collected ===")
