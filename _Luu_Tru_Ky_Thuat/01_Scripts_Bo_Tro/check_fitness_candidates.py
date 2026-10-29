# -*- coding: utf-8 -*-
import sys
import os

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)
from capture_engine import verify_url_health

candidates = [
    # Nhóm 1: Đại Gia 5 Sao & Tổ Hợp Thể Hình Thượng Lưu (Việt Nam)
    ("California Fitness & Yoga", "https://cali.vn/", "Cali"),
    ("CITIGYM", "https://citigym.com.vn/", "Citigym"),
    ("Elite Fitness", "https://elitefitness.com.vn/", "Elite Fitness"),
    ("Diamond Fitness Center", "https://diamondfitness.vn/", "Diamond Fitness"),
    ("The A Fitness", "https://thea.com.vn/", "The A"),
    
    # Nhóm 2: Chuỗi Tiện Lợi 24/7 & Đại Chúng Hiện Đại
    ("The New Gym", "https://thenewgym.vn/", "The New Gym"),
    ("Anytime Fitness Vietnam", "https://anytimefitness.vn/", "Anytime Fitness"),
    ("Unity Fitness", "https://unityfitness.vn/", "Unity Fitness"),
    
    # Nhóm 3: Chuyên Sâu, EMS, Võ Thuật & Boutique Studio
    ("25 FIT - EMS Training", "https://25fit.vn/", "25 FIT"),
    ("GymHaus Boutique Fitness", "https://gymhausvietnam.com/", "GymHaus"),
    ("Swequity Ultimate Fitness", "https://swequity.vn/", "Swequity"),
    ("Kickfit Sports", "https://kickfit-sports.com/", "Kickfit Sports"),
    ("HD Fitness Đà Nẵng", "https://hdfitness.vn/", "HD Fitness"),
    ("Curves Vietnam", "https://curvesvietnam.com.vn/", "Curves Vietnam"),
    ("Gym One", "https://gymone.vn/", "Gym One"),
    ("Advance Fitness", "https://advancegym.com.vn/", "Advance Fitness"),
    ("Fit365", "https://fit365.vn/", "Fit365"),
    ("Level Fitness & Yoga", "https://levelfyc.com/", "Level Fitness"),
    ("Elite Pilates", "https://elitepilates.vn/", "Elite Pilates"),
    ("Pilates Station", "https://pilatesstation.vn/", "Pilates Station"),

    # Nhóm 4: Biểu Tượng Fitness Quốc Tế (UI/UX Đỉnh Cao Thế Giới)
    ("Equinox", "https://www.equinox.com/", "Equinox"),
    ("Third Space London", "https://www.thirdspace.london/", "Third Space"),
    ("Barry's Bootcamp", "https://www.barrys.com/", "Barry's"),
    ("F45 Training", "https://f45training.com/", "F45 Training")
]

print(f"Bắt đầu kiểm tra {len(candidates)} ứng viên...")
healthy_list = []
for name, url, short in candidates:
    ok, reason, final_url, title = verify_url_health(url, timeout=12)
    status_icon = "✅" if ok else "❌"
    print(f"{status_icon} [{name}] ({url}) -> {reason} | Title: {title[:40]}")
    if ok:
        healthy_list.append((name, url, short, final_url, title))

print(f"\n=> Tổng số website hợp lệ: {len(healthy_list)} / {len(candidates)}")
