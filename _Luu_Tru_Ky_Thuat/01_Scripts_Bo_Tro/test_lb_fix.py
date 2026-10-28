import asyncio
import os
from playwright.async_api import async_playwright

async def test_fix():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        file_path = os.path.abspath('index.html').replace(os.sep, '/')
        await page.goto(f'file:///{file_path}')
        await page.wait_for_selector('.website-card')

        await page.evaluate("""
            () => {
                const body = document.querySelector('.lightbox-body');
                body.style.alignItems = 'flex-start';
                openLightbox('20');
            }
        """)
        await page.wait_for_timeout(500)

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
        print("With align-items: flex-start:")
        print(info)

        # Now test wheel scroll
        await page.mouse.move(700, 500)
        await page.mouse.wheel(0, 1500)
        await page.wait_for_timeout(500)

        scrollTop = await page.evaluate("document.querySelector('.lightbox-body').scrollTop")
        print("After wheel 1500px, scrollTop is:", scrollTop)

        await browser.close()

if __name__ == '__main__':
    asyncio.run(test_fix())
