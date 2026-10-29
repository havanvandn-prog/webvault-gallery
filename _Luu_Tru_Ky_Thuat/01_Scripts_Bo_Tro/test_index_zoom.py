# -*- coding: utf-8 -*-
import asyncio, os, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        errors = []
        page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
        page.on('pageerror', lambda exc: errors.append(str(exc)))

        file_url = 'file:///' + os.path.abspath('index.html').replace('\\', '/')
        await page.goto(file_url)

        # 1. Click thumbnail card 1
        first_thumb = page.locator('.card-thumbnail-box').first
        await first_thumb.click()

        # 2. Check modal active & mode-fit
        lb_body = page.locator('#lbBody')
        body_class = await lb_body.get_attribute('class')
        print('1. Initial modal class in index.html:', body_class)
        assert 'mode-fit' in body_class, 'Should open in mode-fit'

        # Check zoom label
        zoom_text = await page.locator('#lbZoomLevel').inner_text()
        print('2. Initial zoom label:', zoom_text)
        assert 'Fit 100%' in zoom_text

        # 3. Click image to toggle to mode-full
        await page.locator('#lbImgWrapper').click()
        body_class_2 = await lb_body.get_attribute('class')
        print('3. After 1st click - Body class:', body_class_2)
        assert 'mode-full' in body_class_2

        # 4. Click image to toggle back to mode-fit
        await page.locator('#lbImgWrapper').click()
        body_class_3 = await lb_body.get_attribute('class')
        print('4. After 2nd click - Body class:', body_class_3)
        assert 'mode-fit' in body_class_3

        # 5. ESC to close
        await page.keyboard.press('Escape')
        is_active = await page.locator('#lightboxModal').evaluate('el => el.classList.contains("active")')
        assert not is_active, 'Modal should be closed'

        print('JS errors in index.html:', errors)
        assert len(errors) == 0, 'Found JS errors'
        await browser.close()
        print('ALL TESTS ON INDEX.HTML PASSED!')

if __name__ == '__main__':
    asyncio.run(main())
