# -*- coding: utf-8 -*-
import os, sys, time, json

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)

from capture_engine import setup_page_protection, capture_smart_clean, compress_tri_layer, verify_captured_image
from playwright.sync_api import sync_playwright

output_dir = os.path.join(BASE_DIR, "Anh_Chup_Website")
kho_webp_dir = os.path.join(BASE_DIR, "Kho_Anh_Webp")
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "noi_that_luxury_candidates.json")

os.makedirs(output_dir, exist_ok=True)
os.makedirs(kho_webp_dir, exist_ok=True)

candidates = [
    {
        "id": "lux01",
        "name": "XLUXURY — Thiết Kế Nội Thất Độc Bản Thượng Lưu",
        "short_name": "XLUXURY",
        "url": "https://xluxury.vn/",
        "domain": "xluxury.vn",
        "slug": "noi_that_lux_xluxury",
        "industry": "noi-that-sang-trong",
        "industry_name": "Nội Thất Sang Trọng (Luxury)",
        "category": "Bespoke Luxury Villa Interior (VN)",
        "category_vn": "Thiết Kế Thi Công Biệt Thự Độc Bản Thượng Lưu",
        "tag": "luxury-vn",
        "vibe": "Độc Bản Thượng Lưu • Tông Đen Vàng Đồng • Biệt Thự Triệu Đô",
        "location": "Hà Nội & TP.HCM",
        "desc": "Thương hiệu chuyên sâu phân khúc biệt thự, penthouse độc bản cho giới tinh hoa Việt. Giao diện tông màu trầm sang trọng, làm nổi bật dấu ấn cá nhân hóa vật liệu quý và trình diễn các công trình đẳng cấp."
    },
    {
        "id": "lux02",
        "name": "KIM Design & Furniture — Modern Classic & Luxury",
        "short_name": "KIM Furniture",
        "url": "https://kimfurniture.com/",
        "domain": "kimfurniture.com",
        "slug": "noi_that_lux_kimfurniture",
        "industry": "noi-that-sang-trong",
        "industry_name": "Nội Thất Sang Trọng (Luxury)",
        "category": "Modern Classic & Luxury Penthouse",
        "category_vn": "Nội Thất Modern Classic & Luxury Đương Đại",
        "tag": "luxury-vn",
        "vibe": "Tinh Tế Châu Âu • Tối Giản Sang Trọng • Portfolio Sắc Nét",
        "location": "Hà Nội (Việt Nam)",
        "desc": "Studio thiết kế và thi công nội thất cao cấp theo phong cách Modern Classic và Luxury. Website có gu thẩm mỹ thời thượng, bố cục tinh giản nhiều khoảng thở để tôn vinh đường nét công trình thực tế."
    },
    {
        "id": "lux03",
        "name": "3A Signature — Thiết Kế Biệt Thự Nghỉ Dưỡng Cao Cấp",
        "short_name": "3A Signature",
        "url": "https://3asignature.com/",
        "domain": "3asignature.com",
        "slug": "noi_that_lux_3asignature",
        "industry": "noi-that-sang-trong",
        "industry_name": "Nội Thất Sang Trọng (Luxury)",
        "category": "Resort-at-Home Luxury Architecture",
        "category_vn": "Thiết Kế Thi Công Biệt Thự Luxury & Nghỉ Dưỡng",
        "tag": "luxury-vn",
        "vibe": "Nghệ Thuật Không Gian • Tông Kem Trầm • Trải Nghiệm Sống",
        "location": "TP.HCM (Việt Nam)",
        "desc": "Đơn vị kiến tạo không gian sống chuẩn resort tại gia cho phân khúc biệt thự cao cấp. Giao diện website đậm tính nghệ thuật, tập trung kể chuyện ánh sáng, chất liệu tự nhiên và quy trình Turnkey."
    },
    {
        "id": "lux04",
        "name": "AA Corporation — Interior Fit-out Khách Sạn 5 Sao",
        "short_name": "AA Corporation",
        "url": "https://aacorporation.com/",
        "domain": "aacorporation.com",
        "slug": "noi_that_lux_aacorporation",
        "industry": "noi-that-sang-trong",
        "industry_name": "Nội Thất Sang Trọng (Luxury)",
        "category": "5-Star Hospitality & Luxury Interior Contractor",
        "category_vn": "Tổng Thầu Nội Thất Khách Sạn 5 Sao & Siêu Sang Quốc Tế",
        "tag": "luxury-vn",
        "vibe": "Đẳng Cấp Toàn Cầu • Hồ Sơ Năng Lực 5 Sao • Bố Cục Editorial",
        "location": "TP.HCM & Toàn cầu",
        "desc": "Tập đoàn sản xuất và thi công nội thất xa xỉ hàng đầu Đông Nam Á (đối tác của Park Hyatt, Aman, Four Seasons...). Website chuẩn tập đoàn quốc tế với showcase dự án 5 sao toàn cầu ấn tượng."
    },
    {
        "id": "lux05",
        "name": "B&B Italia — Contemporary Italian Luxury",
        "short_name": "B&B Italia",
        "url": "https://www.bebitalia.com/en-us/",
        "domain": "bebitalia.com",
        "slug": "noi_that_lux_bebitalia",
        "industry": "noi-that-sang-trong",
        "industry_name": "Nội Thất Sang Trọng (Luxury)",
        "category": "Iconic Italian Luxury Design",
        "category_vn": "Biểu Tượng Nội Thất Xa Xỉ Đương Đại Ý",
        "tag": "luxury-global",
        "vibe": "Avant-Garde Luxury • Lookbook Điện Ảnh • Kiến Trúc Ý",
        "location": "Milan (Ý) & Toàn cầu",
        "desc": "Thương hiệu huyền thoại định hình nội thất xa xỉ đương đại thế giới. Website mang phong cách tạp chí kiến trúc điện ảnh với hình ảnh không gian siêu thực, typography thanh lịch và hệ thống lọc bộ sưu tập tinh xảo."
    },
    {
        "id": "lux06",
        "name": "Cassina — Italian Designer Furniture Heritage",
        "short_name": "Cassina",
        "url": "https://www.cassina.com/ww/en.html",
        "domain": "cassina.com",
        "slug": "noi_that_lux_cassina",
        "industry": "noi-that-sang-trong",
        "industry_name": "Nội Thất Sang Trọng (Luxury)",
        "category": "Architectural Luxury & Design Icons",
        "category_vn": "Di Sản Thiết Kế Nội Thất Kiến Trúc Cao Cấp Ý",
        "tag": "luxury-global",
        "vibe": "Museum-Grade Luxury • Storytelling Di Sản • Editorial Cao Cấp",
        "location": "Milan (Ý) & Toàn cầu",
        "desc": "Nhà mốt nội thất cao cấp sở hữu bản quyền các kiệt tác của Le Corbusier, Charlotte Perriand... Giao diện website giống một bảo tàng nghệ thuật sống động, tôn vinh tay nghề thủ công và đẳng cấp sưu tầm."
    },
    {
        "id": "lux07",
        "name": "Flexform — Made in Italy Quiet Luxury",
        "short_name": "Flexform",
        "url": "https://www.flexform.it/en",
        "domain": "flexform.it",
        "slug": "noi_that_lux_flexform",
        "industry": "noi-that-sang-trong",
        "industry_name": "Nội Thất Sang Trọng (Luxury)",
        "category": "Quiet Luxury Living & Sofas",
        "category_vn": "Chuẩn Mực Quiet Luxury & Sofa Thượng Lưu Ý",
        "tag": "luxury-global",
        "vibe": "Quiet Luxury • Thanh Lịch Vượt Thời Gian • Bảng Màu Trung Tính",
        "location": "Meda (Ý) & Toàn cầu",
        "desc": "Đại diện tiêu biểu nhất cho triết lý Quiet Luxury (sang trọng thầm lặng) của Ý. Website gây ấn tượng mạnh với nhịp điệu khoảng trắng tinh tế, ảnh phòng khách ngập tràn ánh sáng tự nhiên và sự tối giản quyền quý."
    },
    {
        "id": "lux08",
        "name": "Baxter — Leather & Marble Luxury Art",
        "short_name": "Baxter",
        "url": "https://www.baxter.it/en/",
        "domain": "baxter.it",
        "slug": "noi_that_lux_baxter",
        "industry": "noi-that-sang-trong",
        "industry_name": "Nội Thất Sang Trọng (Luxury)",
        "category": "Artisanal Leather & Moody Luxury",
        "category_vn": "Nghệ Thuật Da Thật & Đá Tự Nhiên Xa Xỉ Ý",
        "tag": "luxury-global",
        "vibe": "Moody Dark Luxury • Chất Liệu Da & Đá Quý • Đậm Chất Nghệ Sĩ",
        "location": "Como (Ý) & Toàn cầu",
        "desc": "Thương hiệu nội thất xa xỉ nổi tiếng với kỹ thuật chế tác da thuộc thủ công và đá cẩm thạch. Website sử dụng tông màu trầm quyền lực, ảnh cận cảnh chất liệu đầy cảm xúc và trải nghiệm như phòng triển lãm nghệ thuật."
    },
    {
        "id": "lux09",
        "name": "NICOLEHOLLIS — Luxury Residential & Hospitality Studio",
        "short_name": "NICOLEHOLLIS",
        "url": "https://www.nicolehollis.com/",
        "domain": "nicolehollis.com",
        "slug": "noi_that_lux_nicolehollis",
        "industry": "noi-that-sang-trong",
        "industry_name": "Nội Thất Sang Trọng (Luxury)",
        "category": "Luxury Residential & Hospitality Design",
        "category_vn": "Studio Thiết Kế Biệt Thự & Khách Sạn Siêu Sang Mỹ",
        "tag": "luxury-global",
        "vibe": "Dark Editorial Luxury • Bố Cục Spec Sheet • Vật Liệu Xa Xỉ",
        "location": "San Francisco (Mỹ)",
        "desc": "Studio thiết kế nội thất biệt thự và khách sạn hạng sang hàng đầu nước Mỹ. Website mang phong cách tạp chí kiến trúc đương đại, bảng màu trầm sang trọng và hồ sơ dự án giàu chiều sâu vật liệu."
    },
    {
        "id": "lux10",
        "name": "Gilles & Boissier — Parisian Luxury Architecture",
        "short_name": "Gilles & Boissier",
        "url": "https://www.gillesetboissier.com/",
        "domain": "gillesetboissier.com",
        "slug": "noi_that_lux_gillesetboissier",
        "industry": "noi-that-sang-trong",
        "industry_name": "Nội Thất Sang Trọng (Luxury)",
        "category": "Parisian Haute Architecture & Interiors",
        "category_vn": "Kiến Trúc & Nội Thất Hoàng Gia Đương Đại Paris",
        "tag": "luxury-global",
        "vibe": "Parisian Chic • Kiến Trúc Cổ Điển Pha Đương Đại • Sang Trọng Tinh Tế",
        "location": "Paris (Pháp)",
        "desc": "Bộ đôi kiến trúc sư đứng sau hàng loạt khách sạn Baccarat New York, Mandarin Oriental và biệt thự xa xỉ tại Paris. Website tối giản chuẩn Pháp, typography thanh mảnh và hình ảnh nghệ thuật tinh xảo."
    },
    {
        "id": "lux11",
        "name": "Humbert & Poyet — Dark Glamour Interior Studio",
        "short_name": "Humbert & Poyet",
        "url": "https://www.humbertpoyet.com/",
        "domain": "humbertpoyet.com",
        "slug": "noi_that_lux_humbertpoyet",
        "industry": "noi-that-sang-trong",
        "industry_name": "Nội Thất Sang Trọng (Luxury)",
        "category": "Dark-Mode Glamour & Hospitality Design",
        "category_vn": "Studio Thiết Kế Nội Thất Hào Nhoáng & Dark Luxury Monaco",
        "tag": "luxury-global",
        "vibe": "Dark Mode Quyến Rũ • Đá Cẩm Thạch & Đồng Thau • High Glamour",
        "location": "Monaco & Paris",
        "desc": "Bộ đôi kiến trúc sư lừng danh tại Monaco chuyên thiết kế nhà hàng, khách sạn và biệt thự thượng lưu. Website mang phong cách Dark Editorial quyến rũ, tôn vinh ánh sáng kịch tính, đá quý và kim loại mạ vàng."
    },
    {
        "id": "lux12",
        "name": "Rimadesio — Architectural Glass & Luxury Systems",
        "short_name": "Rimadesio",
        "url": "https://www.rimadesio.it/en/",
        "domain": "rimadesio.it",
        "slug": "noi_that_lux_rimadesio",
        "industry": "noi-that-sang-trong",
        "industry_name": "Nội Thất Sang Trọng (Luxury)",
        "category": "Minimalist Architectural Glass & Wardrobe Systems",
        "category_vn": "Hệ Kính Kiến Trúc & Phòng Thay Đồ Siêu Sang Ý",
        "tag": "luxury-global",
        "vibe": "Hi-Tech Luxury • Kính & Nhôm Tinh Khiết • Độ Chính Xác Tuyệt Đối",
        "location": "Milan (Ý) & Toàn cầu",
        "desc": "Đỉnh cao thế giới về hệ thống cửa trượt kính, vách ngăn và tủ walk-in closet xa xỉ. Website thể hiện tinh thần tối giản chuẩn xác bằng bố cục lưới sắc lẹm, tông màu khói – xám – champagne sang trọng."
    }
]

print(f"=== CHỤP & KIỂM ĐỊNH {len(candidates)} WEBSITE NỘI THẤT SANG TRỌNG ===")
results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for idx, site in enumerate(candidates, 1):
        print(f"\n[{idx:02d}/{len(candidates)}] {site['name']} ({site['url']})...")
        raw_png = os.path.join(output_dir, f"{site['slug']}.png")
        full_webp = os.path.join(kho_webp_dir, f"{site['slug']}_full.webp")
        thumb_webp = os.path.join(kho_webp_dir, f"{site['slug']}_thumb.webp")
        fb_png = os.path.join(kho_webp_dir, f"{site['slug']}_fb.png")

        site["image"] = f"Anh_Chup_Website/{site['slug']}.png"
        site["thumb"] = f"Kho_Anh_Webp/{site['slug']}_thumb.webp"
        site["full"] = f"Kho_Anh_Webp/{site['slug']}_full.webp"
        site["fb"] = f"Kho_Anh_Webp/{site['slug']}_fb.png"

        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            ignore_https_errors=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        setup_page_protection(page)
        try:
            page.goto(site['url'], timeout=45000, wait_until="domcontentloaded")
            time.sleep(3.0)
            page.evaluate("""() => {
                ['button[aria-label*="Close" i]', 'button[aria-label*="accept" i]', '.onetrust-close-btn-handler', '#onetrust-accept-btn-handler', '.cookie-accept', '.btn-close-popup', '.popup-close', '.close-modal', '#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll', '.iubenda-cs-accept-btn'].forEach(sel => {
                    document.querySelectorAll(sel).forEach(btn => { try { btn.click(); } catch(e) {} });
                });
            }""")
            time.sleep(0.6)
            capture_smart_clean(page, raw_png, viewport_height=900, scroll_delay=0.25)
            thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb = compress_tri_layer(raw_png, site['slug'], kho_webp_dir)
            valid, msg = verify_captured_image(full_webp)
            print(f"  [+] QA: {'PASS' if valid else 'FAIL'} - {msg}")
            if not valid:
                print("  [!] Thử chụp lại với networkidle...")
                page.goto(site['url'], timeout=45000, wait_until="networkidle")
                time.sleep(3.0)
                capture_smart_clean(page, raw_png, viewport_height=900, scroll_delay=0.35)
                thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb = compress_tri_layer(raw_png, site['slug'], kho_webp_dir)
                valid, msg = verify_captured_image(full_webp)
                print(f"  [+] QA Vòng 2: {'PASS' if valid else 'FAIL'} - {msg}")

            site["thumb_kb"] = thumb_kb
            site["full_kb"] = full_kb
            site["fb_kb"] = fb_kb
            site["size_mb"] = f"{round(os.path.getsize(raw_png) / (1024*1024), 2)} MB"
            site["audit_msg"] = msg
            site["status"] = "SUCCESS" if valid else "FAIL"
            results.append((site["id"], site["domain"], "PASS" if valid else "FAIL", msg))
        except Exception as e:
            print(f"  [-] Error {site['domain']}: {e}")
            site["status"] = "FAIL"
            site["audit_msg"] = str(e)[:120]
            results.append((site["id"], site["domain"], "FAIL", str(e)[:80]))
        finally:
            context.close()
    browser.close()

with open(metadata_file, "w", encoding="utf-8") as f:
    json.dump(candidates, f, ensure_ascii=False, indent=2)

print("\n=== TỔNG KẾT QA 12 ỨNG VIÊN LUXURY ===")
for r in results:
    print(f"  {r[0]} | {r[1]:22s} | {r[2]:4s} | {r[3]}")
