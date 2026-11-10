# -*- coding: utf-8 -*-
import sys
import re
import time
import urllib.parse
from playwright.sync_api import sync_playwright

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

queries = [
    '"lắp mạng fpt" site:ladipage.vn OR site:ladipage.me OR site:ldp.page OR site:ladi.page',
    '"đăng ký mạng fpt" OR "lắp mạng fpt" "ladipage"',
    '"lắp mạng fpt" inurl:khuyen-mai OR inurl:dang-ky OR inurl:uu-dai OR inurl:landing',
    '"lắp wifi fpt" "bảng giá" site:ladipage.me OR site:ldp.page OR site:ladipage.vn',
    '"lắp đặt mạng fpt" "đăng ký ngay" inurl:ldp OR inurl:km OR inurl:landing',
    '"fpt" "giga" "sky" "meta" site:ladipage.vn OR site:ladipage.me OR site:ldp.page'
]

found_urls = set()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
    page = ctx.new_page()
    for q in queries:
        print(f"\n--- Searching Bing: {q} ---")
        url = "https://www.bing.com/search?q=" + urllib.parse.quote(q) + "&count=30"
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=20000)
            time.sleep(2)
            links = page.evaluate("""() => {
                return Array.from(document.querySelectorAll('li.b_algo h2 a, a.tilk')).map(a => ({
                    href: a.href,
                    text: a.innerText
                }));
            }""")
            for l in links:
                href = l['href']
                if href and href.startswith('http') and 'bing.com' not in href and 'microsoft.com' not in href:
                    print(f"  {href} | {l['text'][:50]}")
                    found_urls.add(href)
        except Exception as e:
            print("Err:", e)
    browser.close()

print(f"\nTotal unique URLs found: {len(found_urls)}")
for u in sorted(found_urls):
    print(u)
