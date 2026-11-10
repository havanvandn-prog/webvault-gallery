# -*- coding: utf-8 -*-
import sys, re, time, urllib.parse
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

# 1. Resolve vertexaisearch redirects from search_web results
redirects = [
    # From previous search_web results & latest search_web calls
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQERdfmcwHu8wPlIaaO-x6u2fYo-JILLiveorSGYbErvL2MLfucdY6zw20FDOHrXfADU4AA_Yzt9tGRtkzwYaXUAxoCBJISFpGFNnDjXPYlvyZKgo5VphBKVDtcAhg==",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGpG-0eEY05RWgbuQgjLKTXhmeyl1YASe6PulrwHckAunqRvAJOdryXhvZPCiHNF5jaQmblGLkkeZbkPTgFlBAe1JW_gkkg7sVklx5lAyyyfYf3OoDX27q538bNTXJ5d9VhXNgzvA==",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHcDQ7Q4BfqDr_PkKNofcvDee3LJNAftV9auvNfz-TJrzQ6n-6sgOnjrNRd07WJ7ZsOysjZC38zg9E9qIH29op8mJG0n9CycEDfu3bY0VoprPvO3lnpcV562-Vh5cNi",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF2wurA5TDd15Fpf9H2lF7sUPXd1jbv0_F3-fE8xbupKY8QiQEFdzlq9U5cSHwfj9SaW1x5xwY65uEbJKaI4fDfJwX8RltjdSdPpf4YeCDX6w==",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH3aFFUz6aknxtAxbbp2SRgM6EVncSMzO9rgHeRQpmCMGaNNooN_j9gAgmHYlustC9h2Y-MqCc7QIj7f41SJ2fM7eBgkohXs--WYxfFze6iWrQ==",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFYC_RTiWi5Zc2Uf87SNT6PctafdbwGmIji6tWI8WyK86kTKxUn58oD9A_UP-Zck7HdJ2JDHNk1Kwhvvoi9htoBNGl7kpmxd1_mj_DtrGfom2fF9pt0BHV5VLMwgR1ho7RrImSBYmNiFvh0xjwM-MIYIeYtxOx_yYHt3rmkWtLFwoQDILw3cwWF",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF_I8kXLDKNYDjKu-Hrq3JeCuSk3I4YlkrEY992bvZGLrN1rABrxb932v2cbQcxBB9UmZ06uNeBcEXh6jTnf4IdmfLyZszdV6sEAqvSGhmGTXT5uz7_x9F7fwguHTS1sIXvDuXUYOCdaQ55jxY=",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFnU49KFUD0Ydp2XnM-wLzPrHi0vliUYI583qC-1K49P167t-_lOYuour3bo0ssedZN-zXFg-4iwssBX3lWvVGR6dHVX1g563zx8n2PCc19KCU=",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQENX0kvVtrNrCv-R_JvFMah3ndAqGl4ci1z2igeNT8QAQpLNiJJnPPBYox6TQE6hjBpJBT7iXAJ0u9fEPncPo18OsJUR_EhDwNtv1ejJmAvqPi6aMLlbl63llya5IjYo-DdpOLjw7O5C0DY4ccs5B6o5tz6SXfGy50zLY0HNrnBEKyN0lKOGK7NvR3ureV8N9btnsTG0DjzgltsZIY73USNyU0EG1UTaHLkCMXpCYqb7O3HFzyIHeDLuLbD-nB7idoiPNcYDw==",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHIP9tRrnMNqX4YR-SflXt4lD7nClXs2IFCtwD_b_GV9EEDVO2gWoVy-rbbkWsLV4R7k4TuVlyDoDsj8wHgGqDDYlTkCtndSjYsmnmZTelPtd3pDUqcmPU69Qy9B1Xix6UoXAncYqc6MzuNXq6PZKIyPGzQ4beBox3l3nc=",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGHsNv_Mmb7n17JjoC2Dx4KAmDlYR1pSskC2Ly5fgBu2wOyCv4p720YqK39MgnkLE0k-g6kDFh6VxCx0vdlriEYhGU9Mc1xHZMeoU8vAZDe8X-KYxLC_YAP4965Kj7rcX-BUIE8ZqR0pqipBENToDtesfobeg01PV9bJg=="
]

print("=== 1. Resolving Redirects ===")
for idx, rurl in enumerate(redirects):
    try:
        r = requests.get(rurl, headers=headers, timeout=10, allow_redirects=True)
        print(f"  [{idx}] {r.status_code} -> {r.url}")
    except Exception as e:
        print(f"  [{idx}] ERR -> {e}")

# 2. Check Webflow Telecom & Internet Provider templates marketplace to extract live .webflow.io preview links
print("\n=== 2. Crawling Webflow ISP / Telecom Templates ===")
webflow_template_pages = []
for wf_cat in [
    "https://webflow.com/templates/html/internet-provider-website-templates",
    "https://webflow.com/templates/technologies/telecom-website-templates"
]:
    try:
        r = requests.get(wf_cat, headers=headers, timeout=15)
        s = BeautifulSoup(r.text, "html.parser")
        for a in s.find_all("a", href=True):
            href = a["href"]
            if "/templates/html/" in href and href not in webflow_template_pages and "internet-provider" not in href:
                full = "https://webflow.com" + href if href.startswith("/") else href
                webflow_template_pages.append(full)
    except Exception as e:
        print("WF cat err:", e)

print(f"Found {len(webflow_template_pages)} webflow template pages. Inspecting first 15...")
for tp in webflow_template_pages[:15]:
    try:
        r = requests.get(tp, headers=headers, timeout=10)
        m = re.findall(r'https://[a-z0-9\-]+\.webflow\.io/?', r.text)
        m = [x for x in set(m) if "webflow-templates" not in x and "preview" not in x]
        print(f"  {tp.split('/')[-1]:45s} -> {m[:3]}")
    except Exception as e:
        pass

# 3. Check CocCoc Search for live LP URLs
print("\n=== 3. Searching CocCoc for more live Landing Pages ===")
cc_queries = [
    "khuyến mãi lắp mạng fpt",
    "đăng ký lắp mạng fpt ngay",
    "lắp mạng fpt giá rẻ 2026",
    "đăng ký internet viettel tại nhà",
    "lắp mạng wifi vnpt khuyến mãi",
    "mẫu landing page viễn thông ladipage",
    "site:w.tuybutky.com wifi OR fpt OR internet OR viettel OR camera",
    "site:ldp.page fpt OR internet OR wifi OR viettel",
    "site:ladipage.vn mạng OR wifi OR fpt OR viễn thông"
]

collected_cc = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1440, "height": 900}, user_agent=headers["User-Agent"])
    page = ctx.new_page()
    for q in cc_queries:
        try:
            page.goto("https://coccoc.com/search?query=" + urllib.parse.quote(q), wait_until="load", timeout=20000)
            time.sleep(2.5)
            links = page.evaluate("""() => {
                return Array.from(document.querySelectorAll('a[href^="http"]')).map(a => ({
                    href: a.href,
                    text: (a.innerText || '').replace(/\\s+/g, ' ').trim()
                })).filter(x => !x.href.includes('coccoc.com') && !x.href.includes('yahoo.com') && !x.href.includes('bing.com') && !x.href.includes('google.com') && !x.href.includes('leafletjs') && !x.href.includes('facebook.com'));
            }""")
            print(f"CC '{q}': {len(links)} links")
            seen = set()
            for item in links:
                u = item['href'].split('?')[0] if ('utm_' in item['href'] or 'aff_' in item['href']) else item['href']
                if u not in seen:
                    seen.add(u)
                    print(f"   {u} | {item['text'][:45]}")
                    collected_cc.append(u)
        except Exception as e:
            print(f"CC '{q}' err:", str(e)[:80])
    browser.close()
