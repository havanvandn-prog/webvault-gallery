import os
import sys
import time
from playwright.sync_api import sync_playwright

def test_clean_capture(url, output_path):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        page.goto(url, wait_until="networkidle", timeout=60000)
        time.sleep(2)

        # 1. Scroll down to trigger lazy loading
        total_h = page.evaluate("() => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
        for y in range(0, total_h, 800):
            page.evaluate(f"window.scrollTo(0, {y})")
            time.sleep(0.1)

        # 2. Scroll back to top
        page.evaluate("window.scrollTo(0, 0)")
        time.sleep(1)

        # 3. CLEAN UP ALL STICKY / FIXED FLOATING ELEMENTS
        page.evaluate("""() => {
            // Biến tất cả sticky thành relative/static để chúng nằm đúng vị trí gốc ở đầu trang, không trượt theo
            const style = document.createElement('style');
            style.innerHTML = `
                /* Vô hiệu hóa bám dính của header và menu phụ */
                .is-sticky, .sticky-header, .header-sticky, [class*="sticky"], [class*="fixed-top"] {
                    position: relative !important;
                    top: auto !important;
                }
                /* Ẩn hoàn toàn các nút hotline rung lắc, zalo chat, popup nổi ở đáy/cạnh màn hình */
                .hotline-phone-ring, .quick-call-button, [class*="call-now"], [class*="phone-vr"],
                [class*="zalo"], [id*="zalo"], .footer-additional, .floating-cta,
                .btn-phone-ring, .phonering-alo-phone, [class*="phonering"] {
                    display: none !important;
                    visibility: hidden !important;
                }
            `;
            document.head.appendChild(style);
        }""")

        # 4. Native full-page screenshot
        page.screenshot(path=output_path, full_page=True)
        print(f"Captured clean: {output_path} (size: {os.path.getsize(output_path)/1024:.1f} KB)")
        browser.close()

if __name__ == "__main__":
    out_dir = "_Luu_Tru_Ky_Thuat/02_Screenshots_Debug_Va_Khao_Sat"
    test_clean_capture("https://hoangsaviet.com/", f"{out_dir}/clean_hoangsaviet.png")
    test_clean_capture("https://azevent.vn/", f"{out_dir}/clean_azevent.png")
