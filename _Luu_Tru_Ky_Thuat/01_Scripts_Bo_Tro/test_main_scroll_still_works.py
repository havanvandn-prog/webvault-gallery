import asyncio
import os
from playwright.async_api import async_playwright

async def check():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 800})
        file_path = os.path.abspath('index.html').replace(os.sep, '/')
        await page.goto(f'file:///{file_path}')
        await page.wait_for_selector('.website-card')

        # 1. Hover on sidebar and wheel -> window MUST NOT scroll
        await page.mouse.move(100, 400)
        await page.mouse.wheel(0, 800)
        await page.wait_for_timeout(300)
        s_sb = await page.evaluate('() => ({ win: window.scrollY, sb: document.querySelector(".sidebar").scrollTop })')
        print("Scrolled over sidebar:", s_sb)
        assert s_sb['win'] == 0, "Window must not scroll when cursor is over sidebar!"

        # 2. Move mouse to right-side content area (e.g. x=600, y=400)
        await page.mouse.move(600, 400)
        await page.mouse.wheel(0, 600)
        await page.wait_for_timeout(300)
        s_main = await page.evaluate('() => ({ win: window.scrollY, sb: document.querySelector(".sidebar").scrollTop })')
        print("Scrolled over main content:", s_main)
        assert s_main['win'] > 0, "Main window must scroll normally when cursor is over main content!"

        print("\nPERFECT: Sidebar scroll is strictly isolated, and main content scrolling works 100% normally!")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(check())
