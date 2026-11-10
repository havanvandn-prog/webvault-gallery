# -*- coding: utf-8 -*-
import sys
import time
import urllib.parse
from playwright.sync_api import sync_playwright

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

coccoc_queries = [
    "lắp mạng fpt",
    "đăng ký lắp mạng fpt",
    "lắp mạng fpt hà nội",
    "lắp mạng fpt tphcm",
    "tổng đài lắp mạng fpt",
    "lắp wifi fpt",
    "đăng ký internet fpt",
    "lắp mạng fpt giá rẻ",
    "landing page lắp mạng fpt",
    "lắp mạng internet viettel vnpt fpt"
]

all_links = set()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(
        viewport={"width": 1440, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
    page = ctx.new_page()

    for q in coccoc_queries:
        print(f"\n=== CocCoc Query: {q} ===")
        try:
            page.goto("https://coccoc.com/search?query=" + urllib.parse.quote(q), wait_until="domcontentloaded", timeout=20000)
            time.sleep(3)
            # Scroll down to load all organic results too
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1.5)
            links = page.evaluate("""() => {
                return Array.from(document.querySelectorAll('a[href^="http"]')).map(a => {
                    let href = a.href;
                    return {href, text: a.innerText.replace(/\\s+/g, ' ').trim()};
                }).filter(x => !x.href.includes('coccoc.com') && !x.href.includes('yahoo.com') && !x.href.includes('bing.com') && !x.href.includes('google.com') && !x.href.includes('youtube.com') && !x.href.includes('facebook.com'));
            }""")
            seen_in_q = set()
            for l in links:
                clean_url = l['href'].split('?')[0] if ('utm_source' in l['href'] or 'aff_sid' in l['href']) else l['href']
                if clean_url not in seen_in_q:
                    seen_in_q.add(clean_url)
                    all_links.add(clean_url)
                    print(f"  {clean_url} | {l['text'][:45]}")
        except Exception as e:
            print("  Err:", e)

    # Check Google Ads Transparency or Theme pages on nguyenvietanh.net for wifi/fpt/internet/mang
    print("\n=== Checking nguyenvietanh.net search ===")
    for kw in ["fpt", "wifi", "internet", "mạng", "viettel", "vnpt"]:
        try:
            page.goto(f"https://nguyenvietanh.net/?s={urllib.parse.quote(kw)}&post_type=product", wait_until="domcontentloaded", timeout=15000)
            time.sleep(1.5)
            prods = page.evaluate("""() => Array.from(document.querySelectorAll('a[href*="/mau-theme-"], a[href*="/san-pham/"], .product a')).map(a => a.href)""")
            for pr in set(prods):
                print("  NVA:", pr)
        except Exception as e:
            pass

    # Also check Google.com.vn directly via Playwright
    print("\n=== Checking Google.com.vn ===")
    for q in ['"lắp mạng fpt" site:ladipage.vn OR site:ldp.page OR site:ladipage.me', '"lắp mạng fpt" "đăng ký ngay" inurl:khuyen-mai']:
        try:
            page.goto("https://www.google.com/search?q=" + urllib.parse.quote(q) + "&hl=vi&num=20", wait_until="domcontentloaded", timeout=15000)
            time.sleep(2.5)
            glinks = page.evaluate("""() => Array.from(document.querySelectorAll('#search a[href^="http"]')).map(a => a.href).filter(h => !h.includes('google.com'))""")
            print(f"Google '{q}': {len(glinks)} links")
            for gl in glinks[:15]:
                print("  ", gl)
                all_links.add(gl)
        except Exception as e:
            print("  Google err:", e)

    browser.close()

print(f"\n=== TOTAL UNIQUE URLS: {len(all_links)} ===")
for u in sorted(all_links):
    print(u)
