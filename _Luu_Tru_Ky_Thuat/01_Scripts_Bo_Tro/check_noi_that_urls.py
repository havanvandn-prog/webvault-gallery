# -*- coding: utf-8 -*-
import os
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)
from capture_engine import verify_url_health

candidates = [
    # Nhóm 1: Thiết kế & Thi công Nội thất Cao cấp / Luxury & Studio Việt Nam
    ("Thái Công Interior Design", "https://thaicong.com/"),
    ("Nội Thất Đồng Gia", "https://donggia.vn/"),
    ("EuroStyle Luxury Interiors", "https://eurostyle.com.vn/"),
    ("Byzan Interior", "https://byzan.vn/"),
    ("House Design", "https://thehousedesign.vn/"),
    ("Decox Design", "https://decoxdesign.com/"),
    ("Nội Thất Kenli", "https://noithatkenli.vn/"),
    ("AA Corporation", "https://aacorporation.com/"),

    # Nhóm 2: Doanh nghiệp Thiết kế Thi công Nội thất Top SEO & Quy mô lớn Việt Nam
    ("XHome Việt Nam", "https://xhome.com.vn/"),
    ("Nội Thất MoreHome", "https://thietkenoithat.com/"),
    ("MoreHome Official", "https://morehome.vn/"),
    ("S.Housing", "https://s-housing.vn/"),
    ("Nội Thất Mạnh Hệ", "https://noithatmanhhe.vn/"),
    ("Nội Thất Tứ Gia", "https://noithattugia.com/"),
    ("Flexfit", "https://flexfit.vn/"),
    ("Gỗ An Cường", "https://www.ancuong.com/"),

    # Nhóm 3: Showroom & Thương mại điện tử Đồ nội thất hiện đại Việt Nam
    ("Nội Thất Nhà Xinh", "https://nhaxinh.com/"),
    ("Nội Thất MOHO", "https://moho.com.vn/"),
    ("Make My Home", "https://makemyhomevn.com/"),
    ("BEYOURs Nội Thất", "https://beyours.vn/"),
    ("JYSK Việt Nam", "https://jysk.vn/"),
    ("Baya Việt Nam", "https://baya.vn/"),
    ("Phố Xinh", "https://phoxinh.com.vn/"),
    ("DERGO Việt Nam", "https://dergo.vn/"),
    ("ErgoLife", "https://ergolife.vn/"),
    ("SMA Furniture", "https://smafurniture.com/"),

    # Nhóm 4: Studio & Thương hiệu Nội thất Đẳng cấp Quốc tế (UI/UX Chuẩn Mực)
    ("BoConcept", "https://www.boconcept.com/vi-vn/"),
    ("Herman Miller", "https://www.hermanmiller.com/"),
    ("Minotti", "https://www.minotti.com/en"),
    ("Poliform", "https://www.poliform.it/en/"),
    ("Molteni&C", "https://www.molteni.it/en/"),
    ("Vincent Van Duysen", "https://vincentvanduysen.com/"),
    ("Kelly Wearstler", "https://www.kellywearstler.com/"),
    ("HAY", "https://www.hay.com/"),
]

print(f"Checking {len(candidates)} candidate URLs...\n")
for name, url in candidates:
    ok, reason, final_url, title = verify_url_health(url, timeout=12)
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name:30s} | {url:38s} -> {final_url} | {reason} | Title: {title[:50]}")
