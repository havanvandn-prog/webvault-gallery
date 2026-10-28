import asyncio
import os
from playwright.async_api import async_playwright

async def verify_lightbox_full_scroll():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        file_path = os.path.abspath('index.html').replace(os.sep, '/')
        await page.goto(f'file:///{file_path}')
        await page.wait_for_selector('.website-card')

        # 1. Open AzEvent (Card 20)
        await page.evaluate("openLightbox('20')")
        await page.wait_for_timeout(600)

        info = await page.evaluate("""
            () => {
                const body = document.querySelector('.lightbox-body');
                const wrap = document.querySelector('.lightbox-img-wrapper');
                return {
                    bodyClientHeight: body.clientHeight,
                    bodyScrollHeight: body.scrollHeight,
                    wrapClientHeight: wrap.clientHeight,
                    wrapScrollHeight: wrap.scrollHeight
                };
            }
        """)
        print("AzEvent Lightbox info:", info)
        assert info['bodyScrollHeight'] > 8000, f"Expected >8000, got {info['bodyScrollHeight']}"
        assert info['wrapClientHeight'] > 8000, f"Expected >8000, got {info['wrapClientHeight']}"

        # 2. Scroll down 3000px
        await page.mouse.move(700, 500)
        await page.mouse.wheel(0, 3000)
        await page.wait_for_timeout(400)
        st1 = await page.evaluate("document.querySelector('.lightbox-body').scrollTop")
        print("ScrollTop after 3000px wheel:", st1)
        assert st1 > 2000, f"Expected >2000, got {st1}"

        # 3. Scroll down further to near footer
        await page.mouse.wheel(0, 4000)
        await page.wait_for_timeout(400)
        st2 = await page.evaluate("document.querySelector('.lightbox-body').scrollTop")
        print("ScrollTop after additional 4000px wheel:", st2)
        assert st2 > 6000, f"Expected >6000, got {st2}"

        # Capture screenshot proving full page scroll works
        out_dir = "_Luu_Tru_Ky_Thuat/02_Screenshots_Debug_Va_Khao_Sat"
        os.makedirs(out_dir, exist_ok=True)
        shot_path = f"{out_dir}/test_lightbox_scrolled_footer.png"
        await page.screenshot(path=shot_path)
        print(f"Captured screenshot at footer: {shot_path}")

        # 4. Close with ESC
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(300)
        modal_active = await page.evaluate("document.querySelector('.lightbox-modal').classList.contains('active')")
        print("Modal active after ESC:", modal_active)
        assert modal_active is False

        # 5. Open Card 1 (Square)
        await page.evaluate("openLightbox('01')")
        await page.wait_for_timeout(500)
        st_reset = await page.evaluate("document.querySelector('.lightbox-body').scrollTop")
        print("Square Lightbox initial scrollTop (must be 0):", st_reset)
        assert st_reset == 0, f"Expected 0, got {st_reset}"

        info_sq = await page.evaluate("document.querySelector('.lightbox-body').scrollHeight")
        print("Square Lightbox scrollHeight:", info_sq)
        assert info_sq > 5000, f"Expected >5000, got {info_sq}"

        await browser.close()
        print("\nALL LIGHTBOX FULL WEB SCROLL VERIFICATIONS PASSED 100%!")

if __name__ == '__main__':
    asyncio.run(verify_lightbox_full_scroll())
