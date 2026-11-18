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

# Loại bỏ Wimbledon (WimBot chat widget) để thay bằng British Council LearnEnglish sạch đẹp
filtered = [x for x in existing if x["slug"] != "anhngu_dep_wimbledon"]

targets = [
    next(x for x in filtered if x["slug"] == "anhngu_dep_lingoda"),
    next(x for x in filtered if x["slug"] == "anhngu_dep_ihlondon"),
    next(x for x in filtered if x["slug"] == "anhngu_dep_englishpath"),
    {
        "name": "British Council LearnEnglish — Cổng Học Tiếng Anh Hội Đồng Anh",
        "short_name": "British Council",
        "url": "https://learnenglish.britishcouncil.org/",
        "domain": "learnenglish.britishcouncil.org",
        "slug": "anhngu_dep_bc_learn",
        "category": "Global British English Authority",
        "category_vn": "Tổ Chức Anh Ngữ Hoàng Gia — Giao Diện Chuẩn Mực & Tin Cậy",
        "tag": "quoc-te-editorial",
        "vibe": "Chuẩn Quốc Tế • Xanh Tím Đậm Uy Tín • Phân Tầng Kỹ Năng Rõ",
        "location": "Toàn cầu",
        "desc": "Cổng học tiếng Anh chính thức của Hội đồng Anh với hệ thống điều hướng chuẩn mực, phân tầng theo trình độ A1-C1 và kỹ năng rõ nét."
    },
]

def remove_widgets_and_cookies(page):
    try:
        page.evaluate("""() => {
            ['#onetrust-accept-btn-handler', '#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll',
             'button[id*="accept-cookie" i]', 'button[aria-label*="accept" i]'].forEach(sel => {
                const b = document.querySelector(sel);
                if (b) { try { b.click(); } catch(e) {} }
            });
            document.querySelectorAll(
                '#usercentrics-root, #usercentrics-cmp-ui, #onetrust-consent-sdk, #CybotCookiebotDialog, ' +
                '.cookie-banner, [id*="hubspot" i], [class*="hubspot" i], ' +
                'iframe[src*="chat" i], iframe[title*="chat" i], [class*="chat-widget" i], [id*="chat-widget" i]'
            ).forEach(el => {
                try { el.remove(); } catch(e) {
                    el.style.setProperty('display', 'none', 'important');
                }
            });
        }""")
    except Exception:
        pass

def capture_one(page, item):
    slug = item["slug"]
    png_path = os.path.join(output_dir, f"{slug}.png")
    print(f"\n[*] Xử lý: {item['short_name']} ({item['url']})")
    for attempt in range(2):
        delay = 0.16 if attempt == 0 else 0.30
        try:
            setup_page_protection(page)
            page.goto(item["url"], timeout=45000, wait_until="domcontentloaded")
            try:
                page.wait_for_load_state("networkidle", timeout=10000)
            except Exception:
                pass
            time.sleep(2.5)
            remove_widgets_and_cookies(page)
            time.sleep(0.5)
            w, h = capture_smart_clean(page, png_path, viewport_height=900, scroll_delay=delay)
            print(f"    -> Đã chụp: {w}x{h}px (Lần {attempt+1})")
            thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb = compress_tri_layer(png_path, slug, kho_webp_dir)
            full_webp_path = os.path.join(kho_webp_dir, full_name)
            ok, msg = verify_captured_image(full_webp_path)
            print(f"    -> Kiểm định: [{'PASS' if ok else 'FAIL'}] {msg}")
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
                return True
        except Exception as e:
            print(f"    -> Lỗi lần {attempt+1}: {str(e)[:120]}")
    return False

def main():
    updated_map = {x["slug"]: x for x in filtered}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            ignore_https_errors=True
        )
        page = context.new_page()
        for item in targets:
            if capture_one(page, item):
                updated_map[item["slug"]] = item
        browser.close()

    final_list = list(updated_map.values())[:20]
    for idx, it in enumerate(final_list, 1):
        it["id"] = f"eng{idx:02d}"

    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(final_list, f, ensure_ascii=False, indent=2)

    print(f"\n=== ĐÃ CẬP NHẬT {len(final_list)}/20 MẪU CHUẨN SẠCH ===")

if __name__ == "__main__":
    main()
