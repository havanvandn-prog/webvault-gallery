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

        await page.mouse.move(100, 400)

        # Scroll 300px
        await page.mouse.wheel(0, 300)
        await page.wait_for_timeout(300)
        s1 = await page.evaluate('() => ({ win: window.scrollY, sb: document.querySelector(".sidebar").scrollTop })')
        print('After first wheel:', s1)

        # Scroll more 500px while at sidebar bottom
        await page.mouse.wheel(0, 500)
        await page.wait_for_timeout(500)
        s2 = await page.evaluate('() => ({ win: window.scrollY, sb: document.querySelector(".sidebar").scrollTop })')
        print('After second wheel at bottom:', s2)

        # Scroll up while at top
        await page.mouse.wheel(0, -1000)
        await page.wait_for_timeout(500)
        await page.mouse.wheel(0, -500)
        await page.wait_for_timeout(500)
        s3 = await page.evaluate('() => ({ win: window.scrollY, sb: document.querySelector(".sidebar").scrollTop })')
        print('After wheeling up past top:', s3)

        await browser.close()

if __name__ == '__main__':
    asyncio.run(check())
