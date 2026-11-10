# -*- coding: utf-8 -*-
import sys
import requests
from bs4 import BeautifulSoup
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

candidates = [
    "https://www.mangfpt.info.vn/",
    "https://w.tuybutky.com/dich-vu-wifi-0056",
    "https://w.tuybutky.com/gioi-thieu-fpt-play-box-1063",
    "https://w.tuybutky.com/497.-fpt-wifi-1070",
    "https://w.tuybutky.com/715.-fpt-internet-1481",
    "https://w.tuybutky.com/735.-camera-se-fpt-1495",
    "https://fptnet.vn/",
    "https://www.cskh1900.com/internet2",
    "https://www.tongdaihotro.vn/",
    "https://fpthotline.net/",
    "https://fptel.com.vn/dang-ky-lap-mang-fpt/",
    "http://dichvufpttelecom.com/lap-mang-fpt/",
    "https://5gvt.vn/lap-mang-viettel/",
    "https://viettelvietnam.com/",
    "https://netviettel.vn/",
    "https://viettelkhuyenmai.vn/",
    "https://viettelhochiminh.vn/",
    "https://viettels.vn/",
    "https://mangvnpt.com.vn/",
    "https://capquangvnpt24h.com/",
    "https://fptcenter.com.vn/",
    "https://shopfpt.vn/",
    "https://mangvienthongfpt.vn/",
    "https://zainet.webflow.io/",
    "https://novos-fiber.webflow.io/",
    "https://lapmangfpt.vip/",
    "https://lapdatmangfpt.vn/",
    "https://fptconnect.vn/"
]

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36"}

for u in candidates:
    try:
        r = requests.get(u, headers=headers, timeout=10, allow_redirects=True)
        html = r.text
        lower_html = html.lower()
        if "ngừng hoạt động" in lower_html or "suspended" in lower_html or "không tồn tại" in lower_html and len(html) < 5000:
            print(f"[DEAD] {u} -> Suspended/Stopped")
            continue
        s = BeautifulSoup(html, "html.parser")
        title = s.title.get_text(strip=True) if s.title else ""
        is_ladi = ("ladi-section" in lower_html or "ladipage" in lower_html or "w.ladicdn.com" in lower_html)
        is_elementor_canvas = ("elementor-template-canvas" in lower_html)
        nav_links = len(s.select("header a, nav a, .menu a, .navbar a"))
        forms = len([fm for fm in s.find_all("form") if len([i for i in fm.find_all(["input","select","textarea"]) if i.get("type") not in ["hidden","submit","button"]]) > 0])
        tel_links = len(s.find_all("a", href=re.compile(r"^tel:", re.I)))
        print(f"[{r.status_code}] {r.url:52s} | Ladi: {str(is_ladi):5s} | Canvas: {str(is_elementor_canvas):5s} | Nav: {nav_links:2d} | Forms: {forms} | Tel: {tel_links:2d} | {title[:40]}")
    except Exception as e:
        print(f"[ERR] {u} -> {str(e)[:60]}")
