# -*- coding: utf-8 -*-
import sys
import requests
from bs4 import BeautifulSoup
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

urls_to_check = [
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQHdMADlO9zzVw2pV36pq0CI8Qgh6EdifP0z0RuV05NTHp9meXbPhmIrHBnwtZuYb4OZYQybvdNbWlFP62pfFsYMMAOx-rn6sfV-8cRJOxCMAGy0N9xAuQuK7UWh1JE7lH5BUw3LS6wjcdOBULIO-RPRpGGBL7hsQri9I0rd5ivOME-OyOHP6nopGtvv2VJdCobAp3usrIdzSwUUoXLnEuqeUEmw4JJ4LQA1u1FGItbp8U3MTr9Eaki3ulkqCmvhjLmVpRd4IQ==",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQGoSgkZB_Evt_X2d0FcAZG0KNv-UPa86O42t-LecxWDU_KG8GcNq_rRJYrDZ4Ztpr9PVUKlhSXQ0g8bYftVn8ESYUXeH6PN4GvZegRM8YBeKYarnYW6hklfbkgdxH_YlKyMCpeYh6OvPw524WA5QQuvNKdrNkmsdKhxNuk=",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEvnh_0BpL7tnktRwmz_WkkQYXeteBhZBbVkPeBEPQn32YOIu82QXy1zR31yePWiG-NJ57LhzqvQmpagx6Qp4tz0uI2apGbfuuN--dmhZvK5sKncz1ZHPEFngw3Lac6t8OFC9HO91-gUm1lmIa7x_6EfjPEj9jsnEnsJWNWzO4R",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFnD22Zo2hwVq6qDZ0G8q6Pe1cz2axkTfUbxMI_qMq9meIC1yx6GmFtF8Q8XEX4K4fuH0gHWiMa_o-JWH2sQoxax5uCWNr0t_HkD1WySrGvidxshsfPrMLcQBltjnGVpNuRXsNefPYcpU7EyEOXRTdK6COpBHKDlLsGGElTtyZaR3j4-WxBkauOD5BuqoIZNQk-7rbBFXxECwdHrg8dVjdHqc8qVQsNP55QcByg55_P2ZkPDsHR1kzC6Bh_BfnJ4vLcEasNWbY=",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEXe6JO7htczRS9gbKIYrcHKAdBiNYaqX2EHCm5S9hjvLxfd70ea9G-1EqKtiQ2XAeyw4E5NRYQPW9Awi3ZaYbliRao2pCnTAK9Iq75ltc=",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFeHQJGaJ0HFaxMc40r-oEQlxgP9E-y0aADOki4DaiNCE7tA3wNSUr-vO1uJQfyRUevVgksIws8FsrofHHKXmVNcaz3pSHJMyR2N-t4Lm7Aw==" if False else "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFZeHQJGaJ0HFaxMc40r-oEQlxgP9E-y0aADOki4DaiNCE7tA3wNSUr-vO1uJQfyRUevVgksIws8FsrofHHKXmVNcaz3pSHJMyR2N-t4Lm7Aw==",
    "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEOah3DN24dGaA185BsLwe0dbdPxxI_Yc1ysuuNiSC6EyowAX6O-DIuRyxPFxi2soZvCMaSpAqAGL1qGRCt-QQ3p6uc1sUIf4Qv_ypknMw6GgDhsvy2zTnQLQWcfy5272TIj-U=",
    "https://shopfpt.vn/",
    "https://lapmangfpt.ai.vn/",
    "https://fptcenter.com.vn/",
    "https://mangvienthongfpt.vn/",
    "https://fptnet.vn/",
    "https://fpttelecoms.vn/"
]

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36"}

for u in urls_to_check:
    try:
        r = requests.get(u, headers=headers, timeout=10, allow_redirects=True)
        html = r.text
        is_ladi = ("ladipage" in html.lower() or "ladi-section" in html.lower())
        is_elementor_lp = ("elementor" in html.lower())
        s = BeautifulSoup(html, "html.parser")
        nav_links = len(s.select("header a, nav a, .menu a"))
        title = s.title.get_text(strip=True) if s.title else ""
        print(f"[{r.status_code}] {r.url}")
        print(f"    Title: {title[:70]} | LadiPage: {is_ladi} | NavLinks: {nav_links}")
    except Exception as e:
        print(f"[ERR] {u[:60]} -> {e}")
