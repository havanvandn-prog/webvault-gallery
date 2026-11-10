# -*- coding: utf-8 -*-
import sys, re, time
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

redirects_to_resolve = [
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEnmqKtu5fG9fG1bWqowCFgx1D98u1sXFBrP3zU0dPQVIFY0EUNisot7DGtCIkh2aCEv82dA4PEr04ewwFmXDR9f_iBj8z5BJu0EggxnP88pxDMNU3Jzf8YGYTJyoSfZOTirt9sxQZG-W3i8Yp0vUrKDkSuCHMJY9Q_fHy4hIeGsQKKiDFq4ZddxwyrXOHYThMC2xTDOLPkQriogwpOSf5AukiyCYt6bERLlHI5icsDhWAIre0b83Vtm1YKRfHRCuxHrguNRX4=",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHdgfx8nQoXMZyEOvM9jy0RN5Mb9uA3T9VXKXNAS7qDZMrelZVzLJnL5QWeoTFyN3k_A6DoOHn2vet34U2hH_EoykxUBrk0S2Fnk1jrBlNyDgj4QJXbPH5jZ2Rrpi49qzr-WPkMbV1WpVyghtNkbl9B7C8wIIHB-NAnP1jZHFe3jUkAZf_tUQq16LSEd2hcExlfeWGpZrbrGAGWt8VjHLHowDw97P7gD1iq",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHwlgCy6amEOWrJhJ_HMG9XlPEeirYjExXiniD3YN0eEaYUEeOC8xXHeZWEdRZoqjTn8CcFLX-QPdDB_mo9jtkcsepDqGmrvtTM0zbVRVvZiC_hXJDu1q1F3gZV1h9rgtO0qx1dxKeP0qJmWrZ17YC2LPasrwSk5_MMEJWlyhh08vuYIDw=",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHTsRoQ7SGrT6nFVSuTyVJ5ne-yiuOACYQB7OagoMOTRsr61aZR-u1aQPMHZEQnxlbBT3RTB0JJTjg0o47F2Z6q5uF_NOAWaKRV4D-BvmHMtMxVYtxdNn7WTtUTuGN49H4fMcr2-DezjBgcklRoBT4hcN7K9ftOKzbX6ij8iX4W3VjrTNE=",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEYfgGJXQeqcbyUNcFMLFcxo9DoydbibhZuCr4CHzYcJYYWYYID2PpDd8vBuks-O1eGLdIfh04RCtl5blYxKFQ180gO3WuO3RqyaZSqdt3qzs9oC8nJvO0hHDuuxIaExA==",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHTC2-6AP64rwomE_3CusNvBvSdkqA56w2mLlA6OFRDa2Cm6D8oc6aY4B0rQCNW1HX0xVfzHv5I40wSw4bDhJP0HHUmxkjaOBmYqPiM7b9UHfMVeX3OWmzU86BLUCM=",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQG8a-_UKC4_BeRknKt7DBIDx6xaDD_sQygerSKpPAiZi1yVQLv3Afz_nXIIcVAdkkx5clwUI8uTf73PPxuKDGSPBj2yfiBz5103lfa3CMPuBPukzC0R28Kva7ClPZCBASb583ihgSVxcagh",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFFU6fshtj2_umoKllo4Eb_ON2SSBYaLFHZInaDH1bfnCqSocripeqGsr-oEVexJHhhdYNccpIh50DwcyLRht4I0JRNX8UDfH4q8CAW7hnkLKASV6vQHQsnb1gkezkRpfZ1SqQ3O1NxrcYPZnCMMt4BZaXE3ZPMCItspIMSnWGeDOq_dg2WLl9kgmQP2eF0ZFJDj-XvdU_57PaX6Q49osdVPDu7",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE7tHYFIBgMUNCWYuMu8bQlY6RVHhW-c0F0xekOGoeH0EIxOIYQZMn43ICrx9bnjJIa9wCBksZ138VzV8X7P9_WoEz7CxQ_Oqz1pqjeVs4hBwy6nvgtB0HVp2fGnvWZppdpSEUTjov-yOAFtEXBNwSVg1fVlSzvKrss_4mYeFZ-YmPDop8PDOmWxg==",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEVRrsJdNNFiWp-T-8LSncef1LG-m-26e3Oick3hlA2-BbIJv-h9CXxhJmDo0uiJ1_IL3GReVqpx7qCbZoZarPs5PprT7GuAkeeVpheJrSJacByjAvZA85zVZYNvrk_",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFVvQi0-HpV9-ARTuEuk3BRl3Pg2X6TViW_y9L0MyHAEvA2dwTQsE0jgPuPY3zsXdZopm7aB-lOXsaSzmXqeNUVmu9dGj2vfIRYvkTDZZENH86Wt1PUkLKiyhe86K6kAuBmFlP3l_M1hLpZiJuTzS40M2yJJCeJcFEGv4dTXyRVmxP38I02o6QMUNur8ZI="
]

print("=== 1. Resolved Redirects ===")
resolved_pages = []
for i, u in enumerate(redirects_to_resolve):
    try:
        r = requests.get(u, headers=headers, timeout=10, allow_redirects=True)
        print(f"  [{i}] {r.status_code} -> {r.url}")
        resolved_pages.append(r.url)
    except Exception as e:
        print(f"  [{i}] ERR -> {e}")

# 2. Extract NVA Internet/Wifi/Camera category + individual product live demos
print("\n=== 2. Crawling nguyenvietanh.net Internet/Wifi/Camera ===")
nva_urls = [
    "https://nguyenvietanh.net/mau-theme-landing-page-internet-wifi-camera/",
    "https://nguyenvietanh.net/mau-theme-landing-page-internet-wifi-camera/page/2/"
]
nva_products = set()
for nu in nva_urls:
    try:
        r = requests.get(nu, headers=headers, timeout=12)
        if r.status_code == 200:
            s = BeautifulSoup(r.text, "html.parser")
            for a in s.select("a"):
                h = a.get("href", "")
                if "w.tuybutky.com" in h:
                    print("  Direct tuybutky:", h)
                elif "/mau-" in h or "/theme-" in h or "product" in h or "internet" in h or "wifi" in h or "fpt" in h or "viettel" in h or "vnpt" in h:
                    if "nguyenvietanh.net" in h and "#" not in h and "mau-theme-landing-page" not in h:
                        nva_products.add(h)
    except Exception as e:
        print("NVA err:", e)

print(f"Found {len(nva_products)} NVA product pages. Checking inside...")
tuybutky_demos = set()
for npage in sorted(nva_products):
    try:
        r = requests.get(npage, headers=headers, timeout=10)
        links = re.findall(r'https?://w\.tuybutky\.com/[a-zA-Z0-9\-\._]+', r.text)
        for l in set(links):
            print(f"  {npage.split('/')[-2][:35]:35s} -> {l}")
            tuybutky_demos.add(l)
    except Exception:
        pass

# 3. Extract live demos from simplepage, redxmedia, creatives, webflow template pages
print("\n=== 3. Checking Webflow & Theme Demos via Playwright ===")
check_pages = [
    "https://webflow.com/templates/html/internet-provider-128-business-website-template",
    "https://webflow.com/templates/technologies/telecom-website-templates",
    "https://webflow.com/templates/html/internet-provider-website-templates",
    "https://redxmedia.net/product/mau-website-lap-dat-mang-internet-fpt/",
    "https://simplepage.vn/blog/mau-landing-page-cong-nghe-dien-tu-dep-mat-tai-simple-page/"
] + [u for u in resolved_pages if any(k in u for k in ["creativemox", "themeplace", "deverust", "aedevstudio", "stylelib", "guywp", "marketplace.ladipage.vn"])]

discovered_demos = set()
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1440, "height": 900}, user_agent=headers["User-Agent"])
    page = ctx.new_page()
    for url in check_pages:
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=15000)
            time.sleep(2)
            found = page.evaluate("""() => {
                const res = [];
                document.querySelectorAll('a[href], iframe[src]').forEach(el => {
                    const u = el.href || el.src || '';
                    const txt = (el.innerText || '').trim().slice(0, 40);
                    if (u.includes('.webflow.io') || u.includes('showcase.ladi.me') || u.includes('tuybutky.com') || u.includes('simplepage') || txt.toLowerCase().includes('demo') || txt.toLowerCase().includes('preview') || txt.toLowerCase().includes('xem') || txt.toLowerCase().includes('view site')) {
                        res.push(u + ' | ' + txt);
                    }
                });
                return Array.from(new Set(res)).slice(0, 30);
            }""")
            print(f"\n[PAGE] {url[:80]}")
            for fitem in found:
                print("   ->", fitem)
                u_only = fitem.split(" | ")[0]
                if u_only.startswith("http"):
                    discovered_demos.add(u_only)
        except Exception as e:
            print(f"[ERR] {url[:60]} -> {str(e)[:60]}")
    browser.close()
