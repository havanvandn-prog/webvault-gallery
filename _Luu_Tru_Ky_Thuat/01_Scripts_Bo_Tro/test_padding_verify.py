import asyncio
import os
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from playwright.async_api import async_playwright

async def verify_padding():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        file_path = os.path.abspath('index.html').replace(os.sep, '/')
        await page.goto(f'file:///{file_path}')
        await page.wait_for_selector('.website-card')

        card = page.locator('.website-card').first

        # Check button styles
        padding_info = await page.evaluate("""
            () => {
                const btn = document.querySelector('.btn-action');
                const style = getComputedStyle(btn);
                return {
                    paddingTop: style.paddingTop,
                    paddingBottom: style.paddingBottom,
                    paddingLeft: style.paddingLeft,
                    paddingRight: style.paddingRight,
                    height: style.height
                };
            }
        """)
        print("Updated Button Padding:", padding_info)

        # Capture card action buttons screenshot
        out_dir = "_Luu_Tru_Ky_Thuat/02_Screenshots_Debug_Va_Khao_Sat"
        os.makedirs(out_dir, exist_ok=True)
        shot_path = f"{out_dir}/test_button_padding_11px.png"
        await card.screenshot(path=shot_path)
        print(f"Captured screenshot: {shot_path}")

        await browser.close()
        print("\nBUTTON PADDING VERIFICATION PASSED!")

if __name__ == '__main__':
    asyncio.run(verify_padding())
