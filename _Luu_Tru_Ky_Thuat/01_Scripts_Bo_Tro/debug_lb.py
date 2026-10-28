import asyncio
import os
from playwright.async_api import async_playwright

async def debug_lightbox():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        file_path = os.path.abspath('index.html').replace(os.sep, '/')
        await page.goto(f'file:///{file_path}')
        await page.wait_for_selector('.website-card')

        await page.evaluate("openLightbox('20')")
        await page.wait_for_timeout(500)

        info = await page.evaluate("""
            () => {
                const modal = document.querySelector('.lightbox-modal');
                const body = document.querySelector('.lightbox-body');
                const wrap = document.querySelector('.lightbox-img-wrapper');
                const img = document.querySelector('#lbImage');
                
                return {
                    modal: {
                        display: getComputedStyle(modal).display,
                        height: modal.clientHeight,
                        overflow: getComputedStyle(modal).overflow,
                    },
                    body: {
                        clientHeight: body.clientHeight,
                        scrollHeight: body.scrollHeight,
                        overflowY: getComputedStyle(body).overflowY,
                        display: getComputedStyle(body).display,
                    },
                    wrap: {
                        clientHeight: wrap.clientHeight,
                        scrollHeight: wrap.scrollHeight,
                    },
                    img: {
                        clientHeight: img.clientHeight,
                        naturalHeight: img.naturalHeight,
                        src: img.src
                    }
                };
            }
        """)
        import pprint
        pprint.pprint(info)
        await browser.close()

if __name__ == '__main__':
    asyncio.run(debug_lightbox())
