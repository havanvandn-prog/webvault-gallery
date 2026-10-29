# -*- coding: utf-8 -*-
import requests, re, sys
sys.stdout.reconfigure(encoding='utf-8')

candidates = [
    ("The Planners", "https://theplannersvn.com/"),
    ("Meraki Wedding Planner", "https://merakiweddingplanner.com/"),
    ("Jeju Wedding", "https://jeju.vn/"),
    ("Bling Bling Decor", "https://blingbling.vn/"),
    ("Bong Bay Vang", "https://bongbayvang.com/")
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}

for name, url in candidates:
    try:
        r = requests.get(url, headers=headers, timeout=8, allow_redirects=True)
        title = ''
        tm = re.search(r'<title>(.*?)</title>', r.text, re.IGNORECASE | re.DOTALL)
        if tm:
            title = tm.group(1).strip()
        print(f"[OK] {name} -> {r.url} (HTTP {r.status_code})")
        print(f"     Title: {title[:70]}")
    except Exception as e:
        print(f"[ERR] {name} -> {url}: {e}")
