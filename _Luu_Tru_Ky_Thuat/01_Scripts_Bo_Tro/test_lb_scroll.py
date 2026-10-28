import asyncio
import os
from playwright.async_api import async_playwright

async def test_lightbox_scroll():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        file_path = os.path.abspath('index.html').replace(os.sep, '/')
        await page.goto(f'file:///{file_path}')
        await page.wait_for_selector('.website-card')

        # Click Xem Full-Page on AzEvent (card 20)
        await page.evaluate("openLightbox('20')")
        await page.wait_for_timeout(500)

        # Check initial scroll of lightbox-body
        s0 = await page.evaluate("document.querySelector('.lightbox-body').scrollTop")
        print('Initial lightbox scrollTop:', s0)

        # Move mouse to center of lightbox and wheel down
        await page.mouse.move(700, 500)
        await page.mouse.wheel(0, 500)
        await page.wait_for_timeout(500)

        s1 = await page.evaluate("document.querySelector('.lightbox-body').scrollTop")
        print('After wheel 500px, lightbox scrollTop:', s1)

        await browser.close()

if __name__ == '__main__':
    asyncio.run(test_lightbox_scroll())
