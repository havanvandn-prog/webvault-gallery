# -*- coding: utf-8 -*-
import os, sys
from concurrent.futures import ThreadPoolExecutor

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)
from capture_engine import verify_url_health

URLS = [
    # Nhóm 1: Bệnh viện tư nhân & Phòng khám đa khoa lớn VN
    ("vinmec", "https://www.vinmec.com/vie/"),
    ("tamanh", "https://tamanhhospital.vn/"),
    ("hongngoc", "https://hongngochospital.vn/"),
    ("thucucmed", "https://benhvienthucuc.vn/"),
    ("medlatec", "https://medlatec.vn/"),
    ("careplus", "https://careplusvn.com/vi/"),
    ("victoria", "https://www.victoriavn.com/"),
    ("fvhospital", "https://www.fvhospital.com/"),
    ("hoanmy", "https://hoanmy.com/"),
    ("bernard", "https://bernard.vn/"),
    ("diag", "https://diag.vn/"),
    ("fmp", "https://www.vietnammedicalpractice.com/"),
    ("rafflesvn", "https://rafflesmedical.vn/"),
    # Nhóm 2: Phòng khám chuyên khoa (Xương khớp, Mắt, Nhi, Đặt lịch) VN
    ("accvn", "https://acc.vn/"),
    ("iccare", "https://iccare.com.vn/"),
    ("matsaigon", "https://www.matsaigon.com/"),
    ("matvietnga", "https://matvietnga.com/"),
    ("hethong315", "https://www.hethong315.com/"),
    ("bookingcare", "https://bookingcare.vn/"),
    ("medpro", "https://medpro.vn/"),
    ("hellobacsi", "https://hellobacsi.com/"),
    ("yhoccotruyen", "https://www.vienyduochocdantoc.org.vn/"),
    # Nhóm 3: Phòng khám hiện đại & Y tế Quốc tế chuẩn UI/UX
    ("onemedical", "https://www.onemedical.com/"),
    ("parsleyhealth", "https://www.parsleyhealth.com/"),
    ("asktia", "https://asktia.com/"),
    ("carbonhealth", "https://carbonhealth.com/"),
    ("springfertility", "https://springfertility.com/"),
    ("kindbody", "https://kindbody.com/"),
    ("mayoclinic", "https://www.mayoclinic.org/"),
    ("cleveland", "https://my.clevelandclinic.org/"),
    ("headway", "https://headway.co/"),
    ("nuffield", "https://www.nuffieldhealth.com/"),
    ("mountelizabeth", "https://www.mountelizabeth.com.sg/"),
    ("zocdoc", "https://www.zocdoc.com/"),
    ("onewelbeck", "https://onewelbeck.com/"),
]

def check_one(item):
    slug, url = item
    ok, reason, final_url, title = verify_url_health(url, timeout=12)
    return (slug, url, ok, reason, final_url, title[:65])

with ThreadPoolExecutor(max_workers=10) as ex:
    results = list(ex.map(check_one, URLS))

for slug, url, ok, reason, final_url, title in results:
    status = "OK  " if ok else "FAIL"
    print(f"[{status}] {slug:16s} | {url:42s} | {reason[:35]:35s} | {title}")
