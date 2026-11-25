# -*- coding: utf-8 -*-
import os
import sys
import time
import json

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)

from capture_engine import (
    setup_page_protection,
    capture_smart_clean,
    compress_tri_layer,
    verify_captured_image,
    verify_url_health,
)
from playwright.sync_api import sync_playwright

output_dir = os.path.join(BASE_DIR, "Anh_Chup_Website")
kho_webp_dir = os.path.join(BASE_DIR, "Kho_Anh_Webp")
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "logistics_xnk_approved.json")

os.makedirs(output_dir, exist_ok=True)
os.makedirs(kho_webp_dir, exist_ok=True)
os.makedirs(os.path.dirname(metadata_file), exist_ok=True)

pool = [
    {
        "name": "Eimskip Vietnam — Chuỗi Cung Ứng Lạnh & Logistics Quốc Tế",
        "short_name": "Eimskip Vietnam",
        "url": "https://eimskip.vn/",
        "domain": "eimskip.vn",
        "slug": "log_eimskip",
        "tag": "logistics-vn",
        "vibe": "Corporate Blue • Chuỗi Cung Ứng Lạnh • Cấu Trúc Dịch Vụ Rõ Ràng",
        "vibe_name": "Logistics & Kho Lạnh",
        "location": "TP. Hồ Chí Minh & Toàn Quốc",
        "desc": "Website chuẩn doanh nghiệp logistics quốc tế tại Việt Nam. Bố cục mạch lạc, nổi bật năng lực vận tải biển, kho lạnh và dịch vụ giao nhận đa phương thức."
    },
    {
        "name": "TSL Logistics — Vận Chuyển Quốc Tế & Thủ Tục Hải Quan",
        "short_name": "TSL Logistics",
        "url": "https://tsl.com.vn/",
        "domain": "tsl.com.vn",
        "slug": "log_tsl",
        "tag": "logistics-vn",
        "vibe": "Modern Industrial • Tông Xanh Dương Chuyên Nghiệp • CTA Báo Giá Nhanh",
        "vibe_name": "Giao Nhận & Hải Quan",
        "location": "TP. Hồ Chí Minh & Hà Nội",
        "desc": "Giao diện logistics hiện đại tập trung vào dịch vụ ủy thác xuất nhập khẩu, khai báo hải quan và vận tải đường biển/hàng không với các khối dịch vụ trực quan."
    },
    {
        "name": "Sotrans Group — Tập Đoàn Kho Vận, Cảng & Logistics Hàng Đầu",
        "short_name": "Sotrans Group",
        "url": "https://sotrans.com.vn/",
        "domain": "sotrans.com.vn",
        "slug": "log_sotrans",
        "tag": "logistics-vn",
        "vibe": "Enterprise Navy • Hệ Sinh Thái Cảng & Kho Bãi • Uy Tín Lâu Năm",
        "vibe_name": "Tập Đoàn Kho Vận",
        "location": "TP. Hồ Chí Minh & Toàn Quốc",
        "desc": "Website doanh nghiệp logistics quy mô lớn, trình bày rõ nét hệ thống cảng ICD, kho bãi ngoại quan và năng lực vận tải siêu trường siêu trọng."
    },
    {
        "name": "Visimex — Xuất Khẩu Nông Sản Hữu Cơ Việt Nam Ra Toàn Cầu",
        "short_name": "Visimex",
        "url": "https://visimex.com/",
        "domain": "visimex.com",
        "slug": "xnk_visimex",
        "tag": "xuat-nhap-khau-vn",
        "vibe": "Organic Earthy • Storytelling Nông Sản Sạch • Chuẩn Quốc Tế",
        "vibe_name": "Xuất Khẩu Nông Sản",
        "location": "Hà Nội & Toàn Quốc",
        "desc": "Hình mẫu website xuất khẩu nông sản hiện đại với hình ảnh vùng nguyên liệu sắc nét, nhấn mạnh chứng nhận hữu cơ (USDA, EU) và chuỗi giá trị bền vững."
    },
    {
        "name": "Vĩnh Hoàn — Tập Đoàn Xuất Khẩu Thủy Sản Hàng Đầu Thế Giới",
        "short_name": "Vĩnh Hoàn",
        "url": "https://www.vinhhoan.com/",
        "domain": "vinhhoan.com",
        "slug": "xnk_vinhhoan",
        "tag": "xuat-nhap-khau-vn",
        "vibe": "Clean Corporate • Blue & White • Chuẩn Mực B2B & Cổ Đông",
        "vibe_name": "Xuất Khẩu Thủy Sản",
        "location": "Đồng Tháp & TP. Hồ Chí Minh",
        "desc": "Giao diện tinh tế, chuẩn quốc tế của doanh nghiệp xuất khẩu thủy sản hàng đầu. Làm nổi bật quy trình nuôi trồng bền vững, nhà máy chế biến và danh mục sản phẩm B2B."
    },
    {
        "name": "Minh Phú Seafood — Vua Tôm Việt Nam & Chuỗi Giá Trị Toàn Cầu",
        "short_name": "Minh Phú Seafood",
        "url": "https://www.minhphu.com/",
        "domain": "minhphu.com",
        "slug": "xnk_minhphu",
        "tag": "xuat-nhap-khau-vn",
        "vibe": "Global Export • Ocean Blue • Chứng Nhận Quốc Tế & Quy Mô",
        "vibe_name": "Xuất Khẩu Thủy Sản",
        "location": "Cà Mau & TP. Hồ Chí Minh",
        "desc": "Website doanh nghiệp xuất khẩu thủy sản quy mô toàn cầu, trình bày ấn tượng các con số năng lực, vùng nuôi sinh thái và tiêu chuẩn truy xuất nguồn gốc."
    },
    {
        "name": "Phúc Sinh Group — Xuất Khẩu Cà Phê, Hồ Tiêu & Gia Vị Hàng Đầu",
        "short_name": "Phúc Sinh Group",
        "url": "https://phucsinh.com/",
        "domain": "phucsinh.com",
        "slug": "xnk_phucsinh",
        "tag": "xuat-nhap-khau-vn",
        "vibe": "Rich Heritage • Nông Sản & Gia Vị • Chuẩn Xuất Khẩu Châu Âu",
        "vibe_name": "Xuất Khẩu Nông Sản",
        "location": "TP. Hồ Chí Minh & Toàn Quốc",
        "desc": "Website xuất khẩu nông sản kết hợp câu chuyện thương hiệu mạnh mẽ, hệ thống nhà máy đạt chuẩn BRC và mạng lưới phân phối hơn 100 quốc gia."
    },
    {
        "name": "Freightos — Nền Tảng Đặt Cước Vận Tải & Logistics Số Toàn Cầu",
        "short_name": "Freightos",
        "url": "https://www.freightos.com/",
        "domain": "freightos.com",
        "slug": "log_freightos",
        "tag": "logistics-global",
        "vibe": "Global SaaS Logistics • Clean UI • Tra Cứu & Báo Giá Trực Tuyến",
        "vibe_name": "Digital Freight Tech",
        "location": "Quốc Tế (Global)",
        "desc": "Chuẩn mực giao diện nền tảng công nghệ logistics toàn cầu: hero sắc nét với công cụ báo giá tức thì, minh họa trực quan luồng vận tải biển/hàng không."
    },
    {
        "name": "Forto — Nền Tảng Quản Trị Chuỗi Cung Ứng & Vận Tải Số",
        "short_name": "Forto",
        "url": "https://forto.com/en/",
        "domain": "forto.com",
        "slug": "log_forto",
        "tag": "logistics-global",
        "vibe": "European Minimalist • Typography Sắc Nét • B2B Tech",
        "vibe_name": "Supply Chain Tech",
        "location": "Châu Âu (Global)",
        "desc": "Thiết kế tối giản chuẩn châu Âu với hệ thống lưới hiện đại, làm nổi bật nền tảng theo dõi lô hàng thời gian thực và giải pháp chuỗi cung ứng bền vững."
    },
    {
        "name": "Zencargo — Digital Freight Forwarder & Tối Ưu Chuỗi Cung Ứng",
        "short_name": "Zencargo",
        "url": "https://www.zencargo.com/",
        "domain": "zencargo.com",
        "slug": "log_zencargo",
        "tag": "logistics-global",
        "vibe": "Modern SaaS • Dashboard Preview • Tối Ưu Chuyển Đổi B2B",
        "vibe_name": "Digital Logistics",
        "location": "Anh Quốc (Global)",
        "desc": "Website logistics công nghệ cao với giao diện sạch, kết hợp mockup phần mềm quản lý vận đơn trực quan và các case study tăng trưởng thuyết phục."
    },
    {
        "name": "Kuehne+Nagel — Tập Đoàn Logistics & Vận Tải Đa Phương Thức Toàn Cầu",
        "short_name": "Kuehne+Nagel",
        "url": "https://www.kuehne-nagel.com/",
        "domain": "kuehne-nagel.com",
        "slug": "log_kuehne_nagel",
        "tag": "logistics-global",
        "vibe": "Global Enterprise • Editorial Grid • Chuyên Nghiệp Tuyệt Đối",
        "vibe_name": "Tập Đoàn Toàn Cầu",
        "location": "Thụy Sĩ (Global)",
        "desc": "Hình mẫu website tập đoàn logistics hàng đầu thế giới: cấu trúc điều hướng đa tầng rõ ràng, trình bày giải pháp vận tải biển, hàng không và hợp đồng kho vận chuẩn mực."
    }
]

results = []
passed_list = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for idx, site in enumerate(pool, 1):
        site["id"] = f"{63 + idx:02d}"
        site["industry"] = "logistics-xnk"
        site["industry_name"] = "Logistics & Xuất Nhập Khẩu"
        print(f"\n[{idx}/{len(pool)}] Processing: {site['short_name']} ({site['url']})")

        health_res = verify_url_health(site["url"])
        print(f"  [+] Health check: {health_res}")

        raw_png = os.path.join(output_dir, f"{site['slug']}.png")
        full_webp = os.path.join(kho_webp_dir, f"{site['slug']}_full.webp")

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
                    '.elementor-popup-modal .dialog-close-button',
                    'button[class*="cookie" i]', '[data-testid="cookie-accept"]'
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

            if not valid:
                print("  [!] Self-Healing Vòng 2: Chụp lại với networkidle + delay 0.55s...")
                try:
                    page.goto(site['url'], timeout=55000, wait_until="networkidle")
                except Exception:
                    page.goto(site['url'], timeout=55000, wait_until="load")
                time.sleep(4.0)
                page.evaluate("""() => {
                    document.querySelectorAll(
                        '[id*="cookie" i]:not(:has(main)):not(.dialog-off-canvas-main-canvas), ' +
                        '[class*="cookie" i]:not(:has(main)):not(.dialog-off-canvas-main-canvas), ' +
                        '[id*="consent" i]:not(:has(main)):not(.dialog-off-canvas-main-canvas), ' +
                        '[class*="consent" i]:not(:has(main)):not(.dialog-off-canvas-main-canvas), ' +
                        '[class*="onetrust" i]:not(:has(main)), [id*="onetrust" i]:not(:has(main)), ' +
                        '.modal-backdrop, .popup-overlay, [role="dialog"]:not(:has(main)):not(.dialog-off-canvas-main-canvas)'
                    ).forEach(el => {
                        el.style.setProperty('display', 'none', 'important');
                        el.style.setProperty('visibility', 'hidden', 'important');
                    });
                }""")
                capture_smart_clean(page, raw_png, viewport_height=900, scroll_delay=0.55)
                thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb = compress_tri_layer(raw_png, site['slug'], kho_webp_dir)
                valid, msg = verify_captured_image(full_webp)
                print(f"  [+] QA Vòng 2: {'PASS' if valid else 'FAIL'} - {msg}")

            if valid:
                site["thumb_kb"] = thumb_kb
                site["full_kb"] = full_kb
                site["fb_kb"] = fb_kb
                passed_list.append(site)
                results.append((site["slug"], site["domain"], "PASS", msg))
            else:
                results.append((site["slug"], site["domain"], "FAIL", msg))
        except Exception as e:
            print(f"  [-] Error {site['domain']}: {e}")
            results.append((site["slug"], site["domain"], "ERR", str(e)[:100]))
        finally:
            context.close()
    browser.close()

with open(metadata_file, "w", encoding="utf-8") as f:
    json.dump(passed_list, f, ensure_ascii=False, indent=2)

print(f"\n=== TỔNG KẾT QA LOGISTICS & XNK: ĐẠT {len(passed_list)}/{len(pool)} MẪU ===")
for r in results:
    print(f"  {r[0]:20s} | {r[1]:24s} | {r[2]:6s} | {r[3]}")
