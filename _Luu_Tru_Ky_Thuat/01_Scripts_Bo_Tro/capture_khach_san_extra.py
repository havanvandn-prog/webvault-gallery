# -*- coding: utf-8 -*-
import os, sys, time, json

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)

from capture_engine import verify_url_health, setup_page_protection, capture_smart_clean, compress_tri_layer, verify_captured_image
from playwright.sync_api import sync_playwright

output_dir = os.path.join(BASE_DIR, "Anh_Chup_Website")
kho_webp_dir = os.path.join(BASE_DIR, "Kho_Anh_Webp")
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "khach_san_candidates.json")

with open(metadata_file, "r", encoding="utf-8") as f:
    existing = json.load(f)

extra_pool = [
    {
        "name": "The Hoxton — Chuỗi Khách Sạn Boutique Lifestyle Quốc Tế",
        "short_name": "The Hoxton",
        "url": "https://thehoxton.com/",
        "domain": "thehoxton.com",
        "slug": "ks_the_hoxton",
        "category": "Urban Lifestyle Hotel Chain",
        "category_vn": "Chuỗi Boutique Lifestyle Quốc Tế — Thiết Kế Phóng Khoáng",
        "tag": "international-awwwards",
        "vibe": "Playful Editorial • Màu Sắc Cá Tính • Đặt Phòng Đa Thành Phố",
        "location": "London / Paris / New York / Amsterdam",
        "desc": "Website chuỗi khách sạn boutique đình đám toàn cầu với ngôn ngữ thiết kế trẻ trung, bảng màu đặc trưng, font chữ biểu cảm và thanh đặt phòng trực quan ở mọi thành phố lớn."
    },
    {
        "name": "Soneva — Chuỗi Resort & Khách Sạn Sinh Thái Xa Xỉ Thế Giới",
        "short_name": "Soneva Resorts",
        "url": "https://soneva.com/",
        "domain": "soneva.com",
        "slug": "ks_soneva",
        "category": "Barefoot Luxury Resort",
        "category_vn": "Chuỗi Nghỉ Dưỡng Sinh Thái Siêu Sang — Barefoot Luxury",
        "tag": "international-awwwards",
        "vibe": "Barefoot Luxury • Storytelling Xanh • Bộ Sưu Tập Biệt Thự Biển",
        "location": "Maldives & Thái Lan",
        "desc": "Thương hiệu tiên phong trong phân khúc nghỉ dưỡng bền vững siêu sang với bố cục trình diễn hình ảnh thiên nhiên tinh khiết, video trải nghiệm và quy trình đặt biệt thự rõ ràng."
    },
    {
        "name": "Salinda Resort Phú Quốc — Boutique Resort Nghệ Thuật Bãi Dài",
        "short_name": "Salinda Resort Phú Quốc",
        "url": "https://salindaresort.com/",
        "domain": "salindaresort.com",
        "slug": "ks_salinda_phu_quoc",
        "category": "Boutique Beachfront Resort",
        "category_vn": "Boutique Resort 5 Sao Phú Quốc — Ánh Hoàng Hôn",
        "tag": "resort-hotel",
        "vibe": "Artisan Boutique • Sunset Storytelling • Booking Engine Trực Tiếp",
        "location": "Phú Quốc",
        "desc": "Giao diện khách sạn nghỉ dưỡng boutique nổi tiếng tại Phú Quốc với tông màu ấm áp, nhấn mạnh yếu tố thủ công bản địa, ẩm thực đa dạng và các gói ưu đãi đặt phòng trực tiếp."
    },
    {
        "name": "Apricot Hotel Hanoi — Khách Sạn Nghệ Thuật Bên Hồ Hoàn Kiếm",
        "short_name": "Apricot Hotel Hanoi",
        "url": "https://apricothotels.com/",
        "domain": "apricothotels.com",
        "slug": "ks_apricot_hanoi",
        "category": "Art & Heritage City Hotel",
        "category_vn": "Khách Sạn Nghệ Thuật 5 Sao — Hàng Trống, Hà Nội",
        "tag": "boutique-luxury",
        "vibe": "Neoclassical Art • Hồ Hoàn Kiếm • Triển Lãm Tranh Đương Đại",
        "location": "Hà Nội",
        "desc": "Website khách sạn 5 sao đối diện Hồ Gươm với phong cách tân cổ điển kết hợp nghệ thuật hội họa Việt Nam, trình bày khoa học các hạng phòng, rooftop bar và sự kiện cưới."
    },
    {
        "name": "Hotel Majestic Saigon — Khách Sạn Di Sản Đông Dương 1925",
        "short_name": "Hotel Majestic Saigon",
        "url": "https://www.majesticsaigon.com/",
        "domain": "majesticsaigon.com",
        "slug": "ks_majestic_saigon",
        "category": "Historic Colonial Hotel",
        "category_vn": "Khách Sạn Di Sản Trăm Năm — Ven Sông Sài Gòn",
        "tag": "luxury-heritage",
        "vibe": "Historic 1925 • Pháp Cổ Sang Trọng • Đặt Phòng & Tiệc Cưới",
        "location": "Quận 1, TP.HCM",
        "desc": "Website biểu tượng khách sạn lịch sử gần 100 năm trên đường Đồng Khởi, làm nổi bật giá trị di sản, các hạng phòng hướng sông và gói dịch vụ hội nghị – tiệc cưới."
    },
    {
        "name": "Banyan Tree — Thương Hiệu Khách Sạn & Resort Sanctuary Toàn Cầu",
        "short_name": "Banyan Tree",
        "url": "https://www.banyantree.com/",
        "domain": "banyantree.com",
        "slug": "ks_banyan_tree",
        "category": "Global Luxury Sanctuary",
        "category_vn": "Chuỗi Khách Sạn & Resort Sanctuary Đẳng Cấp Quốc Tế",
        "tag": "international-awwwards",
        "vibe": "Sanctuary for the Senses • Thanh Đặt Phòng Đa Quốc Gia • Wellness",
        "location": "Quốc tế (có Lăng Cô VN)",
        "desc": "Website thương hiệu khách sạn nghỉ dưỡng hàng đầu châu Á với bộ lọc điểm đến thông minh, hình ảnh kiến trúc nhiệt đới tinh tế và nhấn mạnh trải nghiệm spa, ẩm thực địa phương."
    }
]

print(f"Hiện đã có {len(existing)} mẫu. Cần bổ sung thêm {20 - len(existing)} mẫu đạt chuẩn 100%...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for site in extra_pool:
        if len(existing) >= 20:
            break
        ok, reason, final_url, _ = verify_url_health(site["url"], timeout=12)
        if not ok:
            print(f"[-] Health fail {site['domain']}: {reason}")
            continue
        site["url"] = final_url

        site_id = f"ks{len(existing)+1:02d}"
        site["id"] = site_id
        site["industry"] = "khach-san"
        site["industry_name"] = "Khách Sạn & Khu Nghỉ Dưỡng"

        print(f"\n[Extra -> Target {site_id}] {site['name']} ({site['url']})...")
        raw_png = os.path.join(output_dir, f"{site['slug']}.png")
        full_webp = os.path.join(kho_webp_dir, f"{site['slug']}_full.webp")
        site["image"] = f"Anh_Chup_Website/{site['slug']}.png"
        site["thumb"] = f"Kho_Anh_Webp/{site['slug']}_thumb.webp"
        site["full"] = f"Kho_Anh_Webp/{site['slug']}_full.webp"
        site["fb"] = f"Kho_Anh_Webp/{site['slug']}_fb.png"

        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            ignore_https_errors=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        setup_page_protection(page)
        try:
            page.goto(site['url'], timeout=45000, wait_until="domcontentloaded")
            time.sleep(3.5)
            page.evaluate("""() => {
                const selectors = [
                    'button[aria-label*="Close" i]', 'button[aria-label*="accept" i]',
                    '.onetrust-close-btn-handler', '#onetrust-accept-btn-handler',
                    '#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll',
                    '.didomi-continue-without-agreeing', '#didomi-notice-agree-button',
                    '.cky-btn-accept', '.cookie-accept', '.btn-close-popup',
                    '.popup-close', '.close-modal', '.mfp-close', '.fancybox-close-small',
                    '.elementor-popup-modal .dialog-close-button'
                ];
                selectors.forEach(sel => {
                    try { document.querySelectorAll(sel).forEach(btn => { try { btn.click(); } catch(e) {} }); } catch(e) {}
                });
            }""")
            time.sleep(1.0)
            capture_smart_clean(page, raw_png, viewport_height=900, scroll_delay=0.35)
            thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb = compress_tri_layer(raw_png, site['slug'], kho_webp_dir)
            valid, msg = verify_captured_image(full_webp)
            print(f"  [+] QA Vòng 1: {'PASS' if valid else 'FAIL'} - {msg}")

            if valid:
                site["thumb_kb"] = thumb_kb
                site["full_kb"] = full_kb
                site["fb_kb"] = fb_kb
                site["size_mb"] = f"{round(os.path.getsize(raw_png) / (1024*1024), 2)} MB"
                site["audit_msg"] = msg
                site["status"] = "SUCCESS"
                existing.append(site)
            else:
                for p_clean in [raw_png, full_webp, os.path.join(kho_webp_dir, f"{site['slug']}_thumb.webp"), os.path.join(kho_webp_dir, f"{site['slug']}_fb.png")]:
                    if os.path.exists(p_clean):
                        try: os.remove(p_clean)
                        except: pass
        except Exception as e:
            print(f"  [-] Error {site['domain']}: {e}")
            for p_clean in [raw_png, full_webp, os.path.join(kho_webp_dir, f"{site['slug']}_thumb.webp"), os.path.join(kho_webp_dir, f"{site['slug']}_fb.png")]:
                if os.path.exists(p_clean):
                    try: os.remove(p_clean)
                    except: pass
        finally:
            context.close()
    browser.close()

with open(metadata_file, "w", encoding="utf-8") as f:
    json.dump(existing, f, ensure_ascii=False, indent=2)

print(f"\n=== HOÀN TẤT: TỔNG {len(existing)}/20 MẪU KHÁCH SẠN ===")
