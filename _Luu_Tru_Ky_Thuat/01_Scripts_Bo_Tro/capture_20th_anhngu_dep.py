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
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "anhngu_dep_candidates.json")

with open(metadata_file, "r", encoding="utf-8") as f:
    existing = json.load(f)

candidates = [
    {
        "name": "St Giles International — Trường Anh Ngữ Quốc Tế Anh & Canada",
        "short_name": "St Giles International",
        "url": "https://www.stgiles-international.com/",
        "domain": "stgiles-international.com",
        "slug": "anhngu_dep_stgiles",
        "category": "Accredited International English School",
        "category_vn": "Trường Anh Ngữ Quốc Tế — Bố Cục Hiện Đại & Dễ Tra Cứu",
        "tag": "quoc-te-editorial",
        "vibe": "Chuẩn Anh Quốc • Màu Sắc Sạch Sẽ • Bảng Khóa Học Trực Quan",
        "location": "Anh & Canada",
        "desc": "Giao diện trường tiếng Anh quốc tế uy tín từ năm 1955 được thiết kế lại hiện đại, thân thiện và tối ưu trải nghiệm chọn cơ sở học."
    },
    {
        "name": "Babbel — Nền Tảng Học Ngoại Ngữ & Tiếng Anh Giao Tiếp Hàng Đầu",
        "short_name": "Babbel",
        "url": "https://www.babbel.com/",
        "domain": "babbel.com",
        "slug": "anhngu_dep_babbel",
        "category": "Modern Editorial Language Platform",
        "category_vn": "Nền Tảng Học Tiếng Anh — Giao Diện Editorial Tối Giản Đẹp",
        "tag": "edtech-hien-dai",
        "vibe": "Editorial Tối Giản • Tông Cam Ấm Nổi Bật • Typography Đẳng Cấp",
        "location": "Quốc tế",
        "desc": "Website chuẩn mực về thiết kế tối giản hiện đại với bảng màu cam-trắng giàu năng lượng, phân khối nội dung khoa học và trải nghiệm thị giác sạch sẽ."
    },
    {
        "name": "LSI Education — Mạng Lưới Trường Anh Ngữ Quốc Tế",
        "short_name": "LSI Education",
        "url": "https://www.lsi.edu/en/",
        "domain": "lsi.edu",
        "slug": "anhngu_dep_lsi",
        "category": "International English School Network",
        "category_vn": "Mạng Lưới Trường Anh Ngữ Quốc Tế — Giao Diện Gọn Đẹp",
        "tag": "quoc-te-editorial",
        "vibe": "Sạch Sẽ Hiện Đại • Bộ Lọc Điểm Đến • Tin Cậy Quốc Tế",
        "location": "Anh, Mỹ, Canada, Úc",
        "desc": "Thiết kế web trường tiếng Anh đa quốc gia gọn gàng, tối ưu trải nghiệm chọn khóa học và thành phố du học tiếng Anh."
    }
]

def remove_widgets(page):
    try:
        page.evaluate("""() => {
            document.querySelectorAll('#usercentrics-root, #usercentrics-cmp-ui, #onetrust-consent-sdk, #CybotCookiebotDialog, .cookie-banner, iframe[src*="chat" i]').forEach(el => {
                try { el.remove(); } catch(e) {}
            });
        }""")
    except Exception:
        pass

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1440, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        ignore_https_errors=True
    )
    page = context.new_page()

    for item in candidates:
        slug = item["slug"]
        png_path = os.path.join(output_dir, f"{slug}.png")
        print(f"[*] Thử: {item['short_name']} ({item['url']})")
        try:
            setup_page_protection(page)
            page.goto(item["url"], timeout=45000, wait_until="domcontentloaded")
            try:
                page.wait_for_load_state("networkidle", timeout=10000)
            except Exception:
                pass
            time.sleep(2.5)
            remove_widgets(page)
            time.sleep(0.5)
            w, h = capture_smart_clean(page, png_path, viewport_height=900, scroll_delay=0.18)
            thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb = compress_tri_layer(png_path, slug, kho_webp_dir)
            ok, msg = verify_captured_image(os.path.join(kho_webp_dir, full_name))
            print(f"    -> [{'PASS' if ok else 'FAIL'}] {msg}")
            if ok:
                item["industry"] = "trung-tam-tieng-anh-dep"
                item["industry_name"] = "Trung Tâm Tiếng Anh (Bố Cục Đẹp)"
                item["image"] = f"Anh_Chup_Website/{slug}.png"
                item["thumb"] = f"Kho_Anh_Webp/{thumb_name}"
                item["full"] = f"Kho_Anh_Webp/{full_name}"
                item["fb"] = f"Kho_Anh_Webp/{fb_name}"
                item["thumb_kb"] = thumb_kb
                item["full_kb"] = full_kb
                item["fb_kb"] = fb_kb
                item["size_mb"] = f"{round(os.path.getsize(png_path)/(1024*1024), 2)} MB"
                item["audit_msg"] = msg
                item["status"] = "SUCCESS"
                existing.append(item)
                break
        except Exception as e:
            print(f"    -> Lỗi: {str(e)[:120]}")

    browser.close()

for idx, it in enumerate(existing[:20], 1):
    it["id"] = f"eng{idx:02d}"

with open(metadata_file, "w", encoding="utf-8") as f:
    json.dump(existing[:20], f, ensure_ascii=False, indent=2)

print(f"[+] Tổng cộng: {len(existing[:20])}/20 mẫu!")
