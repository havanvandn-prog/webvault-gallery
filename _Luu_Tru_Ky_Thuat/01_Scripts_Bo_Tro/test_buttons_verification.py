import asyncio
import os
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from playwright.async_api import async_playwright

async def verify_buttons():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        file_path = os.path.abspath('index.html').replace(os.sep, '/')
        await page.goto(f'file:///{file_path}')
        await page.wait_for_selector('.website-card')

        card = page.locator('.website-card').first

        # 1. Check btn-fb-text is completely gone
        fb_text_count = await card.locator('.btn-fb-text').count()
        print("btn-fb-text count (must be 0):", fb_text_count)
        assert fb_text_count == 0, "btn-fb-text should be removed!"

        # 2. Check Row 1: Copy Ảnh FB & Xem Ảnh Full
        btn_fb_img = card.locator('.btn-fb-image')
        btn_view_full = card.locator('.btn-view-full')
        btn_open_web = card.locator('.btn-open-web')

        print("btn-fb-image text:", (await btn_fb_img.inner_text()).strip())
        print("btn-view-full text:", (await btn_view_full.inner_text()).strip())
        print("btn-open-web text:", (await btn_open_web.inner_text()).strip())

        # Check styles
        styles = await page.evaluate("""
            () => {
                const card = document.querySelector('.website-card');
                const btnFb = card.querySelector('.btn-fb-image');
                const btnFull = card.querySelector('.btn-view-full');
                const btnWeb = card.querySelector('.btn-open-web');

                return {
                    btnFbBg: getComputedStyle(btnFb).backgroundImage,
                    btnWebBg: getComputedStyle(btnWeb).backgroundColor,
                    btnWebGridCol: getComputedStyle(btnWeb).gridColumn
                };
            }
        """)
        print("Button Styles:", styles)
        assert "rgb(255, 59, 48)" in styles['btnFbBg'], "Copy Ảnh FB button must have red gradient!"
        assert "rgb(24, 119, 242)" in styles['btnWebBg'], "Truy cập website button must be Facebook blue!"

        # Capture card action buttons screenshot
        out_dir = "_Luu_Tru_Ky_Thuat/02_Screenshots_Debug_Va_Khao_Sat"
        os.makedirs(out_dir, exist_ok=True)
        shot_path = f"{out_dir}/test_new_buttons_layout.png"
        await card.screenshot(path=shot_path)
        print(f"Captured card screenshot: {shot_path}")

        await browser.close()
        print("\nALL BUTTON LAYOUT VERIFICATIONS PASSED 100%!")

if __name__ == '__main__':
    asyncio.run(verify_buttons())
