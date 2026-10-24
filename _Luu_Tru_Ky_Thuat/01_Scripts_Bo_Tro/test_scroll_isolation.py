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

        # Apply overscroll-behavior: contain and JS wheel prevent
        await page.evaluate("""
            () => {
                const sb = document.querySelector('.sidebar');
                sb.style.overscrollBehavior = 'contain';
                sb.addEventListener('wheel', (e) => {
                    const { scrollTop, scrollHeight, clientHeight } = sb;
                    const isAtTop = scrollTop <= 0 && e.deltaY < 0;
                    const isAtBottom = (scrollTop + clientHeight >= scrollHeight - 1) && e.deltaY > 0;
                    if (scrollHeight <= clientHeight || isAtTop || isAtBottom) {
                        e.preventDefault();
                    }
                    e.stopPropagation();
                }, { passive: false });
            }
        """)

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

        # Scroll up 1000px
        await page.mouse.wheel(0, -1000)
        await page.wait_for_timeout(500)
        s3 = await page.evaluate('() => ({ win: window.scrollY, sb: document.querySelector(".sidebar").scrollTop })')
        print('After wheeling back to top:', s3)

        # Scroll up 500px more past top
        await page.mouse.wheel(0, -500)
        await page.wait_for_timeout(500)
        s4 = await page.evaluate('() => ({ win: window.scrollY, sb: document.querySelector(".sidebar").scrollTop })')
        print('After wheeling past top:', s4)

        assert s1['win'] == 0, "Window should be 0"
        assert s2['win'] == 0, "Window should be 0 at bottom"
        assert s3['win'] == 0, "Window should be 0 when back up"
        assert s4['win'] == 0, "Window should be 0 past top"
        print("\nSUCCESS: Window NEVER scrolled! The main interface is completely locked while scrolling sidebar!")

        await browser.close()

if __name__ == '__main__':
    asyncio.run(check())
