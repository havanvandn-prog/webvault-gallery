# -*- coding: utf-8 -*-
import os, sys, json, time
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)
from capture_engine import verify_url_health
from playwright.sync_api import sync_playwright

EXTRA_URLS = [
    ("BYD Tây Hồ", "https://bydtayho.com.vn/"),
    ("Giá Xe BYD", "https://giaxebyd.vn/"),
    ("BYD Hà Nội", "https://bydhanoi.com.vn/"),
    ("BYD Miền Nam", "https://bydmiennam.com.vn/"),
    ("Hyundai Ngọc Phát", "https://hyundaingocphat.com.vn/"),
    ("Ô Tô Hyundai", "https://otohyundai.com.vn/"),
    ("Giá Xe Ô Tô 24h", "https://giaxeoto24h.vn/"),
    ("Toyota Mỹ Đình", "https://toyotamydinh.com.vn/"),
    ("Toyota Giải Phóng", "https://toyotagiaiphong.com.vn/"),
    ("Mazda Phạm Văn Đồng", "https://mazdaphamvandong.vn/"),
    ("Kia Long Biên", "https://kialongbien.vn/"),
    ("LadiPage Mercedes Template 1", "https://ladipage.vn/"),
]

# Also check dedicated landing subpages on top Mercedes sites if root is multi-page
SUBPAGES = [
    ("Mercedes Automobile (GLC Landing)", "https://mercedesbenz-automobile.com.vn/mercedes-glc/"),
    ("Mercedes Vietnam Star (Bảng Giá)", "https://mercedes-vietnamstar.com.vn/bang-gia-xe-mercedes/"),
    ("Mercedes Phú Mỹ Hưng (Đăng Ký Lái Thử)", "https://mercedesphumyhung.com.vn/dang-ky-lai-thu/"),
]

results = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for name, url in EXTRA_URLS[:11]:
        ok, reason, final_url, title = verify_url_health(url, timeout=10)
        if not ok:
            print(f"FAIL {name}: {reason}")
            continue
        ctx = browser.new_context(viewport={"width": 1440, "height": 900}, ignore_https_errors=True)
        page = ctx.new_page()
        try:
            page.goto(final_url, timeout=25000, wait_until="domcontentloaded")
            time.sleep(2.0)
            info = page.evaluate("""() => {
                const h = document.body ? document.body.scrollHeight : 0;
                const html = document.documentElement.outerHTML.toLowerCase();
                let theme = 'Custom';
                if (html.includes('ladipage') || html.includes('ldi-')) theme = 'LadiPage';
                else if (html.includes('flatsome')) theme = 'Flatsome-WP';
                else if (html.includes('elementor')) theme = 'Elementor-WP';
                else if (html.includes('wp-content')) theme = 'Other-WP';
                let atfButtons = 0, atfInputs = 0;
                const kws = ['báo giá', 'lái thử', 'lăn bánh', 'trả góp', 'ưu đãi', 'đặt cọc', 'liên hệ', 'tư vấn'];
                document.querySelectorAll('a, button').forEach(el => {
                    const r = el.getBoundingClientRect();
                    if (r.top >= 0 && r.top < 900 && r.width > 40 && r.height > 20) {
                        const t = (el.innerText || '').toLowerCase();
                        if (kws.some(k => t.includes(k))) atfButtons++;
                    }
                });
                document.querySelectorAll('input, select').forEach(el => {
                    const r = el.getBoundingClientRect();
                    if (r.top >= 0 && r.top < 900 && r.width > 40 && r.height > 15) atfInputs++;
                });
                const hasPriceTable = html.includes('giá niêm yết') || html.includes('lăn bánh') || document.querySelectorAll('table').length > 0;
                const hasCalc = html.includes('tính trả góp') || html.includes('dự toán') || html.includes('lãi suất');
                const visibleImgs = Array.from(document.querySelectorAll('img')).filter(i => i.naturalWidth > 50).length;
                const forms = document.querySelectorAll('form').length;
                return {height:h, theme, atfButtons, atfInputs, hasPriceTable, hasCalc, visibleImgs, forms, title: document.title.slice(0,80)};
            }""")
            print(f"OK   {name:24s} | {info['theme']:12s} | H:{info['height']:5d} | ATF_B:{info['atfButtons']} ATF_I:{info['atfInputs']} | Forms:{info['forms']} Price:{info['hasPriceTable']} Calc:{info['hasCalc']} Imgs:{info['visibleImgs']} | {final_url}")
            results.append({"name": name, "url": url, "final_url": final_url, **info})
        except Exception as e:
            print(f"ERR  {name}: {str(e)[:60]}")
        finally:
            ctx.close()
    browser.close()

out_path = os.path.join(os.path.dirname(__file__), "..", "03_Du_Lieu_Tam_Va_Test", "auto_lp_extra.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
