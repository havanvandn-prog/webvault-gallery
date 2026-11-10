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
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36"
}

redirects = [
    ("fpttelecomvietnam", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFRxAAqfmiy95xribXDdn0Zi5zyEyKwxJkCk4nR51VZ82zpmWweXlFLOq-N1T1sAtCsV9mqa_BCjuQB7AH14lVSys4aEeU1ssFgXndoZcrN9LVJlIGvVRo="),
    ("viettelca", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFfJaWW3Pynd1w-SaVEVbk3HucLDfdb_i3snRHaNczP67QW3UvrTfoN6w1keKaqBYolsnZghPZMeEwFg8m3IOruJcVMJEiPGpoaD4eWyUBFadp0DL5an5jKOsjjpX13FCDDerBr1K7m4hB_xkAFJxMhXL7UAPnE8w=="),
    ("vnpt", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFoSIQ8sYJlT0s9i_NWny4Ais624iiVgxLV1fnlNfE50gUETbfSfeP1K4W1VryCE7WvIOUwE6xyDUEOunOiWet8159MstvJHpnpt_NRNy4FsN4nOeSoNCM5B_cSrSUUxAwMhwe9TEgxS21KBBl8VwQk2Prc-ELF-DoQVRd_cAexfoU6mMlmYrTegtmaQTO-mrGk30kMtdyBlxl4kbz_sZYYmdo="),
    ("vnpthcmc", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQE-1qlLunuDAe7Zhh2AKcjg48R-STbIdMIAc9IWIOM9CxAXr2Zd2QXcIpvs_2HnjmWA3T_Bjd3F8AO8TG2v8z87A4i49TPz9EYPjOfxBMrrj3m-cOVq3siKOu3aP2gky5mhpzUguMgsoZUUDQYXmTVZy9p1KXymK_7Y1EAYiokBGqKimQs1bPcXEUi6nFdY8q_N15hEWxEG63JG41z8rfLk09FaMgu7c5gacPqAU7Af-NU="),
    ("vnpt-tayninh", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF5dcDm1HDRaVBJj2wyel_khbQ3EFmcihoOnmBi1BupjyR9GGwUhuehb75CyhJTLAQ3otfURxVM5ssJrvJ2Cc3RxhrM6fPiqysp3njXqjxCq2PWt-GUWYKFwiZdJjpxKLa62nAjFZKEhAMC6EVK"),
    ("18001166", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQH9kz_nc5GhyAroCs9tPmNP1jTZ9sIOq-tqLLj8CphzAgVi8-RVJW6bz4i9O_zG6UyhWvwL3qMVMlQ4A-NegAWoZsfKb4bNHacCFtfyk4QXbudo5A1YqbOu3-VOnZM52glKhI-WV_0M0S1RbdhLorYCZj0bqXk9TrQz-cDiSS4jTixkzYpcJWJavEHYF5CsSX1lBLKkIbPlKKzd_2oV9ZhtdLl0eZRW"),
    ("lapwifivnpt", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGbpAodZmiJ7cNwROUCmoBhouo0OqKbRg6E6HWQ6u-Duc2Pa6UIokC5K4JA0JwwZCSDtZr7NlTWInDKa01NqCn1gm-4k6NoSo4adiRXMdlKn6qekzQmP_6QhahBFTh7VU5r6PytRchik412pgU2w8BcSoqNRCkL_sQ="),
    ("ladimkt_viettel1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHL9Yd1V_ySyeyjPcQDhymOAYMEt7HJqoKoR5CZptFcEr13Vml3ycaBDP-5mAbWm2-I03-aWb_LK3MppblGWX3jGvrOIEFbAwoEjeUMk-tuOKYItBnSuTvZPLWn4boSSRM5qd1-wgLckPDtanfuXV0poiBv5ldVCc0EAUIXFDNCTFdgPBM="),
    ("ladimkt_viettel2", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGrugip3KdoBmY7qh2x78quSuBIddJLBSqTPe-A_hbJaJ26a8D25uNlE-f2IiTzxyFofzF1O42KqB5JtEp8NXGk3SZRL5gFtKrxVMksEZUrE4sJ9lfhfUF5u6xKJgfIFP6TSXdY8wKoIOlABakTa5V3q05qacQZXT6RMVQ07jbqj_n5fBawCy6Y0F8wSlbVzXYBAj08LnegZ10MxYt66qqhEA2lOhmtGEYOJfzhdX9wcV0WMzztApjMd4QGT6zLNfTy"),
    ("themewp1", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFTGDkeCV8jynW3qqf4SVUKG2walw48GSgpB3wrByjJoTfWQhCHAm_eL9rbWkqnZQx60hMVto76GuTgyRHECgnV94ooeigKjive1CJgB5OUhyYg3ZJu4kGXogsLNzAFUOAO-SmytoMabge-XjI="),
    ("themewp3", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEfw6Z88yTI4WNjGYlU5BdxGHssYtt7dQW75Bnhax1gfy18LUbD9BNONAX1dMNbWaOzzqqfI9bt6nngVDYXGfykNXYqvpTWZlez0SDGuSCGtsYhpmEjLcMRGUdH7tll5Spo3P956bbgeAzgsZNXlfWPK2s="),
    ("themewp4", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF03YR33RJWcCdRZvKx4KxYF8lZACiE-8kTch2hEbBO5Rtg78pGr8m1u1QkOb1gQbjVL_SOc-UPCisui45ZSJomLBKkwpQVE_0CHtyMoYEZa3adai6gfy7j_8Beocw2I6Uy92JfhIt-KaqneGdVPuuO10y1tiY="),
    ("themewp5", "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQF_PZv4rF-aACHtcS0feBrnnLARPbscswB-nhwwJeIXzL2QnjmxM9mf3Jjwizr3zhJgs_qGT9he37P-iaV_TvTC4h47Mb2UmLymfYCSGz8u_taym-zb0tulFwTPLvND4cqfonDsJt3VHmKgGRmRsyXX9YzFdVlWxVICzbxxWHn-7RcURaX20_E="),
]

direct_urls = [
    "https://fpt.webmau.dev/",
    "https://www.mangfpt.info.vn/",
    "https://fptnet.vn/",
    "https://w.tuybutky.com/dich-vu-wifi-0056",
    "https://w.tuybutky.com/gioi-thieu-fpt-play-box-1063",
    "https://w.tuybutky.com/497.-fpt-wifi-1070",
    "https://w.tuybutky.com/715.-fpt-internet-1481",
    "https://w.tuybutky.com/735.-camera-se-fpt-1495",
]

print("=== Resolving Redirects ===")
for lbl, rurl in redirects:
    try:
        r = requests.get(rurl, headers=headers, timeout=10, allow_redirects=True)
        print(f"  {lbl:20s} -> [{r.status_code}] {r.url}")
        if r.status_code == 200:
            if "marketplace.ladipage.vn/theme/" in r.url:
                m = re.search(r'-([a-f0-9]{24})$', r.url)
                if m:
                    sc = f"https://showcase.ladi.me/{m.group(1)}"
                    print(f"     -> Extracted showcase: {sc}")
                    direct_urls.append(sc)
            elif "themewp.vn" in r.url:
                s = BeautifulSoup(r.text, "html.parser")
                for a in s.select("a[href*='demo'], a[href*='webmau'], a"):
                    href = a.get("href", "")
                    txt = (a.get_text() or "").lower()
                    if any(k in txt for k in ["xem thử", "demo", "xem trước"]) and href.startswith("http"):
                        print(f"     -> Extracted themewp demo: {href}")
                        direct_urls.append(href)
            else:
                direct_urls.append(r.url)
    except Exception as e:
        print(f"  {lbl:20s} -> ERR: {str(e)[:60]}")

print("\n=== Auditing via Requests + BeautifulSoup ===")
for u in dict.fromkeys(direct_urls):
    try:
        r = requests.get(u, headers=headers, timeout=10, allow_redirects=True)
        html = r.text
        lower = html.lower()
        if any(k in lower for k in ["ngừng hoạt động", "suspended"]) and len(html) < 25000:
            print(f"[DEAD] {u}")
            continue
        s = BeautifulSoup(html, "html.parser")
        title = s.title.get_text(strip=True) if s.title else ""
        is_ladi = ("ladi-section" in lower or "w.ladicdn.com" in lower or "ladipage" in lower)
        nav_links = len(s.select("header a, nav a, .menu a, .navbar a"))
        forms = len([fm for fm in s.find_all("form") if len([i for i in fm.find_all(["input","select","textarea"]) if i.get("type") not in ["hidden","submit","button"]]) > 0])
        tel = len(s.find_all("a", href=re.compile(r"^tel:", re.I)))
        print(f"[{r.status_code}] {r.url:58s} | Ladi:{str(is_ladi):5s} | Nav:{nav_links:2d} | Forms:{forms} | Tel:{tel:2d} | {title[:45]}")
    except Exception as e:
        print(f"[ERR] {u} -> {str(e)[:60]}")
