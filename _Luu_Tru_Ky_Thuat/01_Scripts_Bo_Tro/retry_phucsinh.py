# -*- coding: utf-8 -*-
import os, sys, time, json

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)

from capture_engine import setup_page_protection, compress_tri_layer, verify_captured_image
from playwright.sync_api import sync_playwright

output_dir = os.path.join(BASE_DIR, "Anh_Chup_Website")
kho_webp_dir = os.path.join(BASE_DIR, "Kho_Anh_Webp")
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "logistics_xnk_approved.json")

site = {
    "id": "70",
    "name": "Phúc Sinh Group — Xuất Khẩu Cà Phê, Hồ Tiêu & Gia Vị Hàng Đầu",
    "short_name": "Phúc Sinh Group",
    "url": "https://phucsinh.com/",
    "domain": "phucsinh.com",
    "slug": "xnk_phucsinh",
    "industry": "logistics-xnk",
    "industry_name": "Logistics & Xuất Nhập Khẩu",
    "tag": "xuat-nhap-khau-vn",
    "vibe": "Rich Heritage • Nông Sản & Gia Vị • Chuẩn Xuất Khẩu Châu Âu",
    "vibe_name": "Xuất Khẩu Nông Sản",
    "location": "TP. Hồ Chí Minh & Toàn Quốc",
    "desc": "Website xuất khẩu nông sản kết hợp câu chuyện thương hiệu mạnh mẽ, hệ thống nhà máy đạt chuẩn BRC và mạng lưới phân phối hơn 100 quốc gia.",
    "thumb": "Kho_Anh_Webp/xnk_phucsinh_thumb.webp",
    "full": "Kho_Anh_Webp/xnk_phucsinh_full.webp",
    "fb": "Kho_Anh_Webp/xnk_phucsinh_fb.png",
}

raw_png = os.path.join(output_dir, f"{site['slug']}.png")
full_webp = os.path.join(kho_webp_dir, f"{site['slug']}_full.webp")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1440, "height": 900},
        ignore_https_errors=True,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    page = context.new_page()
    setup_page_protection(page)
    page.goto(site["url"], timeout=60000, wait_until="domcontentloaded")
    time.sleep(5.0)

    # Force eager load for all lazy images and reveal animated elements
    page.evaluate("""() => {
        document.querySelectorAll('img').forEach(img => {
            img.loading = 'eager';
            const ds = img.getAttribute('data-src') || img.getAttribute('data-lazy-src') || img.getAttribute('data-original');
            if (ds && (!img.src || img.src.includes('data:image') || img.src.includes('blank'))) {
                img.src = ds;
            }
            img.style.setProperty('opacity', '1', 'important');
            img.style.setProperty('visibility', 'visible', 'important');
        });
        document.querySelectorAll('[data-aos], .wow, .animated, .fadeIn, .fadeInUp').forEach(el => {
            el.style.setProperty('opacity', '1', 'important');
            el.style.setProperty('visibility', 'visible', 'important');
            el.style.setProperty('transform', 'none', 'important');
        });
    }""")

    # Scroll through page to trigger any JS-based lazy loading
    total_h = page.evaluate("document.body.scrollHeight")
    for y in range(0, min(total_h, 16000), 700):
        page.evaluate(f"window.scrollTo(0, {y})")
        time.sleep(0.4)

    # Wait up to 15s for images to decode
    page.evaluate("""async () => {
        const imgs = Array.from(document.querySelectorAll('img'));
        await Promise.all(imgs.map(img => {
            if (img.complete) return Promise.resolve();
            return new Promise(res => {
                img.addEventListener('load', res, {once: true});
                img.addEventListener('error', res, {once: true});
                setTimeout(res, 6000);
            });
        }));
    }""")
    time.sleep(2.0)
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(1.0)

    # Hide fixed overlays/popups
    page.evaluate("""() => {
        document.querySelectorAll('*').forEach(el => {
            const st = window.getComputedStyle(el);
            if (st.position === 'fixed' && el.offsetHeight > 120 && el.offsetWidth > 200) {
                el.style.setProperty('display', 'none', 'important');
            }
            if (st.backgroundAttachment === 'fixed') {
                el.style.setProperty('background-attachment', 'scroll', 'important');
            }
        });
    }""")
    page.screenshot(path=raw_png, full_page=True)
    thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb = compress_tri_layer(raw_png, site['slug'], kho_webp_dir)
    valid, msg = verify_captured_image(full_webp)
    print(f"QA phucsinh.com: {'PASS' if valid else 'FAIL'} - {msg}")
    context.close()
    browser.close()

if valid:
    site["thumb_kb"] = thumb_kb
    site["full_kb"] = full_kb
    site["fb_kb"] = fb_kb
    data = json.loads(open(metadata_file, encoding="utf-8").read())
    data = [d for d in data if d["slug"] != site["slug"]]
    data.append(site)
    data.sort(key=lambda x: int(x["id"]))
    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Updated metadata: {len(data)} items total.")
