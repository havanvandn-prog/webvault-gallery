# -*- coding: utf-8 -*-
import sys
import os
import requests

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)
from capture_engine import verify_url_health

urls = [
    "https://fpt.vn/vi/khach-hang-ca-nhan/internet-fpt",
    "https://mangfpt.vn/",
    "https://lapmangfpt.vip/",
    "https://fpttelecom.net.vn/",
    "https://fpt-vn.vn/",
    "https://fpthanoi.com.vn/",
    "https://hcmfpt.vn/",
    "https://fptinternet.vn/",
    "https://fptconnect.vn/",
    "https://capquangfpt.net.vn/",
    "https://tongdaifpt.com.vn/",
    "https://dangkywifi.com.vn/",
    "https://fptsale.vn/",
    "https://fptwifi.com.vn/",
    "https://lapdatmangfpt.vn/",
    "https://vienthongfpttelecom.vn/",
    "https://lapmangfptdanang.com.vn/",
    "https://fptbienhoa.vn/",
    "https://fpt-vietnam.com/",
    "https://lapmangfpt-toanquoc.com.vn/",
    "https://fpttelecomvietnam.com.vn/",
    "https://capquangfpt.vn/",
    "https://hanoifpt.vn/",
    "https://fpt365.vn/",
    "https://lapmangfpt.vn/"
]

print(f"Bắt đầu kiểm tra {len(urls)} URLs...")
passed = []
failed = []

for u in urls:
    ok, reason, final_u, title = verify_url_health(u, timeout=12)
    if ok:
        print(f"[OK] {u} -> Title: {title[:50]}...")
        passed.append({"url": u, "final_url": final_u, "title": title})
    else:
        print(f"[FAIL] {u} -> Reason: {reason}")
        failed.append({"url": u, "reason": reason})

print(f"\nTổng kết: {len(passed)} PASS, {len(failed)} FAIL.")
