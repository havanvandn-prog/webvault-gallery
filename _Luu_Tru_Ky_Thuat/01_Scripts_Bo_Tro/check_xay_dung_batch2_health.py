# -*- coding: utf-8 -*-
import os, sys, json

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

SKILL_SCRIPTS = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.insert(0, SKILL_SCRIPTS)
from capture_engine import verify_url_health

CANDIDATES = [
    # Nhóm 1: Tổng Thầu & Hạ Tầng Công Nghiệp Việt Nam (Đợt 2)
    ("xd_hoabinh", "Hòa Bình Construction (HBC)", "https://hbcg.vn/", "tong-thau-vn"),
    ("xd_cc1", "CC1 — Tổng Công Ty Xây Dựng Số 1", "https://www.cc1.vn/", "tong-thau-vn"),
    ("xd_vinaconex", "Vinaconex", "https://www.vinaconex.com.vn/", "tong-thau-vn"),
    ("xd_viteccons", "Viteccons", "https://www.viteccons.vn/", "tong-thau-vn"),
    ("xd_anphong", "An Phong Construction", "https://www.anphong.vn/", "tong-thau-vn"),
    ("xd_daidung", "Đại Dũng Group (DDC)", "https://daidung.com/", "tong-thau-vn"),
    ("xd_searefico", "Searefico", "https://searefico.com/", "tong-thau-vn"),
    ("xd_hailong", "Hải Long Construction", "https://hailongjsc.vn/", "tong-thau-vn"),
    ("xd_pebsteel", "Pebsteel Vietnam", "https://pebsteel.com/vi", "tong-thau-vn"),
    ("xd_zamilsteel", "Zamil Steel Vietnam", "https://www.zamilsteel.com.vn/", "tong-thau-vn"),

    # Nhóm 2: Thiết Kế & Thi Công Xây Nhà Trọn Gói Việt Nam (Đợt 2)
    ("xd_xhome", "XHOME Việt Nam", "https://xhome.com.vn/", "xay-nha-tron-goi"),
    ("xd_vinavic", "Kiến Trúc Vinavic", "https://vinavic.vn/", "xay-nha-tron-goi"),
    ("xd_katahome", "KataHome", "https://katahome.com/", "xay-nha-tron-goi"),
    ("xd_laco", "Xây Dựng LACO", "https://xaydunglaco.vn/", "xay-nha-tron-goi"),
    ("xd_vietquang", "Việt Quang Group", "https://kientrucvietquang.net/", "xay-nha-tron-goi"),
    ("xd_vietarchitect", "Việt Architect Group", "https://kientrucsuvietnam.vn/", "xay-nha-tron-goi"),
    ("xd_kienanvinh", "Kiến An Vinh", "https://kienanvinh.vn/", "xay-nha-tron-goi"),
    ("xd_minhbao", "Xây Dựng Minh Bảo", "https://minhbao.vn/", "xay-nha-tron-goi"),

    # Nhóm 3: Tổng Thầu & Xây Dựng Quốc Tế Chuẩn UI/UX (Đợt 2)
    ("xd_turner", "Turner Construction", "https://www.turnerconstruction.com/", "cong-nghiep-quoc-te"),
    ("xd_dpr", "DPR Construction", "https://www.dpr.com/", "cong-nghiep-quoc-te"),
    ("xd_pcl", "PCL Construction", "https://www.pcl.com/", "cong-nghiep-quoc-te"),
    ("xd_mortenson", "Mortenson", "https://www.mortenson.com/", "cong-nghiep-quoc-te"),
    ("xd_lendlease", "Lendlease", "https://www.lendlease.com/", "cong-nghiep-quoc-te"),
    ("xd_mace", "Mace Group", "https://www.macegroup.com/", "cong-nghiep-quoc-te"),
    ("xd_swinerton", "Swinerton", "https://www.swinerton.com/", "cong-nghiep-quoc-te"),
    ("xd_henselphelps", "Hensel Phelps", "https://www.henselphelps.com/", "cong-nghiep-quoc-te"),
]

results = []
passed = 0
for slug, name, url, group in CANDIDATES:
    ok, reason, final_url, title = verify_url_health(url, timeout=12)
    status = "OK" if ok else "FAIL"
    if ok:
        passed += 1
    print(f"[{status}] {slug:18s} | {name:32s} | {reason} | {final_url}")
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

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "03_Du_Lieu_Tam_Va_Test", "xay_dung_batch2_health.json"))
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nTOTAL HEALTHY: {passed}/{len(CANDIDATES)}")
