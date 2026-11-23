# -*- coding: utf-8 -*-
import os, sys, json

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

SKILL_SCRIPTS = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.insert(0, SKILL_SCRIPTS)
from capture_engine import verify_url_health

CANDIDATES = [
    # Nhóm 1: Tổng Thầu & Tập Đoàn Xây Dựng Hàng Đầu Việt Nam
    ("xd_coteccons", "Coteccons", "https://www.coteccons.vn/", "tong-thau-vn"),
    ("xd_ricons", "Ricons", "https://www.ricons.vn/", "tong-thau-vn"),
    ("xd_newtecons", "Newtecons", "https://newtecons.vn/", "tong-thau-vn"),
    ("xd_centralcons", "Central Construction", "https://www.centralcons.vn/", "tong-thau-vn"),
    ("xd_unicons", "Unicons", "https://unicons.vn/", "tong-thau-vn"),
    ("xd_solenc", "SOL E&C", "https://solenc.vn/", "tong-thau-vn"),
    ("xd_hoabinh", "Hòa Bình Construction (HBC)", "https://hbcg.vn/", "tong-thau-vn"),
    ("xd_deltagroup", "Delta Group", "https://deltagroup.vn/", "tong-thau-vn"),
    ("xd_fecon", "FECON", "https://fecon.com.vn/", "tong-thau-vn"),
    ("xd_phuchung", "Phục Hưng Holdings", "https://phuchung.com.vn/", "tong-thau-vn"),
    ("xd_dinco", "Dinco E&C", "https://dinco.com.vn/", "tong-thau-vn"),

    # Nhóm 2: Xây Nhà Trọn Gói, Biệt Thự & Thiết Kế Thi Công (VN)
    ("xd_sbshouse", "SBS House", "https://sbshouse.vn/", "xay-nha-tron-goi"),
    ("xd_akisa", "Kiến Trúc Akisa", "https://akisa.vn/", "xay-nha-tron-goi"),
    ("xd_betaviet", "Betaviet Group", "https://betaviet.vn/", "xay-nha-tron-goi"),
    ("xd_neohouse", "NeoHouse", "https://neohouse.vn/", "xay-nha-tron-goi"),
    ("xd_nhattin", "Xây Dựng Nhất Tín", "https://xaydungnhattin.com/", "xay-nha-tron-goi"),
    ("xd_kienanvinh", "Kiến An Vinh", "https://kienanvinh.vn/", "xay-nha-tron-goi"),
    ("xd_greenhn", "GreenHN", "https://greenhn.vn/", "xay-nha-tron-goi"),
    ("xd_ancu", "Xây Dựng An Cư", "https://xaydungancu.com.vn/", "xay-nha-tron-goi"),
    ("xd_minhbao", "Xây Dựng Minh Bảo", "https://minhbao.vn/", "xay-nha-tron-goi"),

    # Nhóm 3: Kết Cấu Thép Công Nghiệp & Tổng Thầu Quốc Tế Chuẩn UI/UX
    ("xd_atad", "ATAD Steel Structure", "https://atad.vn/", "cong-nghiep-quoc-te"),
    ("xd_bmbsteel", "BMB Steel", "https://bmbsteel.com.vn/", "cong-nghiep-quoc-te"),
    ("xd_suffolk", "Suffolk Construction", "https://www.suffolk.com/", "cong-nghiep-quoc-te"),
    ("xd_turner", "Turner Construction", "https://www.turnerconstruction.com/", "cong-nghiep-quoc-te"),
    ("xd_bechtel", "Bechtel", "https://www.bechtel.com/", "cong-nghiep-quoc-te"),
    ("xd_skanska", "Skanska Group", "https://group.skanska.com/", "cong-nghiep-quoc-te"),
    ("xd_clark", "Clark Construction", "https://www.clarkconstruction.com/", "cong-nghiep-quoc-te"),
    ("xd_olsonkundig", "Olson Kundig", "https://olsonkundig.com/", "cong-nghiep-quoc-te"),
]

results = []
passed = 0
for slug, name, url, group in CANDIDATES:
    ok, reason, final_url, title = verify_url_health(url, timeout=12)
    status = "OK" if ok else "FAIL"
    if ok:
        passed += 1
    print(f"[{status}] {slug:16s} | {name:28s} | {reason} | {final_url}")
    results.append({
        "slug": slug,
        "name": name,
        "url": url,
        "final_url": final_url,
        "group": group,
        "healthy": ok,
        "reason": reason,
        "title": title[:120] if title else ""
    })

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "03_Du_Lieu_Tam_Va_Test", "xay_dung_health.json"))
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nTOTAL HEALTHY: {passed}/{len(CANDIDATES)}")
