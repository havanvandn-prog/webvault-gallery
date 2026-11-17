# -*- coding: utf-8 -*-
import os, sys, json, time
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from playwright.sync_api import sync_playwright

in_path = os.path.join(os.path.dirname(__file__), "..", "03_Du_Lieu_Tam_Va_Test", "auto_lp_health_check.json")
with open(in_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Take top 34 healthy candidates (excluding 0-score)
candidates = [c for c in data["healthy"] if c["cro_score"] >= 80][:34]

inspected = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for idx, c in enumerate(candidates, 1):
        url = c["final_url"]
        ctx = browser.new_context(viewport={"width": 1440, "height": 900}, ignore_https_errors=True)
        page = ctx.new_page()
        try:
            page.goto(url, timeout=25000, wait_until="domcontentloaded")
            time.sleep(2.0)
            info = page.evaluate("""() => {
                const h = document.body ? document.body.scrollHeight : 0;
                const html = document.documentElement.outerHTML.toLowerCase();
                let theme = 'Custom';
                if (html.includes('ladipage') || html.includes('ldi-')) theme = 'LadiPage';
                else if (html.includes('flatsome')) theme = 'Flatsome-WP';
                else if (html.includes('elementor')) theme = 'Elementor-WP';
                else if (html.includes('wp-content')) theme = 'Other-WP';
                else if (html.includes('__next')) theme = 'Next.js';

                // Check above-the-fold (y < 900) forms, buttons, inputs
                let atfButtons = 0;
                let atfInputs = 0;
                let atfKeywords = [];
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

                // Check body text length & section count
                const sections = document.querySelectorAll('section, .section, [class*="section"]').length;
                const h1 = document.querySelector('h1') ? document.querySelector('h1').innerText.trim().slice(0, 80) : '';
                const hasPriceTable = html.includes('giá niêm yết') || html.includes('lăn bánh') || document.querySelectorAll('table').length > 0;
                const hasCalc = html.includes('tính trả góp') || html.includes('dự toán') || html.includes('lãi suất');
                const visibleImgs = Array.from(document.querySelectorAll('img')).filter(i => i.naturalWidth > 50).length;

                return {
                    height: h,
                    theme: theme,
                    atfButtons: atfButtons,
                    atfInputs: atfInputs,
                    sections: sections,
                    h1: h1,
                    hasPriceTable: hasPriceTable,
                    hasCalc: hasCalc,
                    visibleImgs: visibleImgs,
                    title: document.title.slice(0, 80)
                };
            }""")
            rec = {**c, **info, "ok": True}
            print(f"[{idx:02d}/{len(candidates)}] {c['name']:32s} | {info['theme']:12s} | H:{info['height']:5d} | ATF_Btn:{info['atfButtons']} ATF_Inp:{info['atfInputs']} | Price:{info['hasPriceTable']} Calc:{info['hasCalc']} Imgs:{info['visibleImgs']} | {url}")
            inspected.append(rec)
        except Exception as e:
            print(f"[{idx:02d}/{len(candidates)}] FAIL {c['name']}: {str(e)[:60]}")
        finally:
            ctx.close()
    browser.close()

out_path = os.path.join(os.path.dirname(__file__), "..", "03_Du_Lieu_Tam_Va_Test", "auto_lp_inspected.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(inspected, f, ensure_ascii=False, indent=2)
print(f"\nSaved {len(inspected)} inspected sites to {out_path}")
