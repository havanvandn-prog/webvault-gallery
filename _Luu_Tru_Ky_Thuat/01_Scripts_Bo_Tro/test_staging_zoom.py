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

        file_url = 'file:///' + os.path.abspath('web_nhap_staging.html').replace('\\', '/')
        await page.goto(file_url)

        # 1. Click thumbnail card 1
        first_thumb = page.locator('.card-thumbnail-box').first
        await first_thumb.click()

        # 2. Check modal active & mode-fit
        lb_body = page.locator('#lbBody')
        body_class = await lb_body.get_attribute('class')
        print('1. Initial modal class:', body_class)
        assert 'mode-fit' in body_class, 'Should open in mode-fit'

        # Check zoom label
        zoom_text = await page.locator('#lbZoomLevel').inner_text()
        print('2. Initial zoom label:', zoom_text)
        assert 'Fit 100%' in zoom_text, f'Expected Fit 100%, got {zoom_text}'

        # Check image height vs viewport height
        wrapper_box = await page.locator('#lbImgWrapper').bounding_box()
        print('3. Wrapper box in mode-fit:', wrapper_box)
        # In 900px viewport, wrapper height should be <= 800px (fitting entirely inside screen)
        assert wrapper_box['height'] <= 800, f'Wrapper height {wrapper_box["height"]} should be <= 800px in mode-fit'

        # 4. Click image to toggle to mode-full
        await page.locator('#lbImgWrapper').click()
        body_class_2 = await lb_body.get_attribute('class')
        zoom_text_2 = await page.locator('#lbZoomLevel').inner_text()
        print('4. After 1st click - Body class:', body_class_2, 'Zoom text:', zoom_text_2)
        assert 'mode-full' in body_class_2, 'Should switch to mode-full'
        assert '100%' in zoom_text_2, 'Should show 100%'

        # 5. Click image again to toggle back to mode-fit
        await page.locator('#lbImgWrapper').click()
        body_class_3 = await lb_body.get_attribute('class')
        zoom_text_3 = await page.locator('#lbZoomLevel').inner_text()
        print('5. After 2nd click - Body class:', body_class_3, 'Zoom text:', zoom_text_3)
        assert 'mode-fit' in body_class_3, 'Should toggle back to mode-fit'

        # 6. Test Ctrl + Wheel zoom
        await page.locator('#lbBody').hover()
        await page.keyboard.down('Control')
        await page.mouse.wheel(0, -200) # zoom in
        await page.keyboard.up('Control')
        await asyncio.sleep(0.3)
        body_class_4 = await lb_body.get_attribute('class')
        zoom_text_4 = await page.locator('#lbZoomLevel').inner_text()
        print('6. After Ctrl + Wheel up - Body class:', body_class_4, 'Zoom text:', zoom_text_4)
        assert 'mode-custom' in body_class_4 or 'mode-full' in body_class_4, 'Should enter zoom mode'

        # 7. Test zoom button [+]
        await page.locator('button.zoom-btn:has-text("+")').click()
        zoom_text_5 = await page.locator('#lbZoomLevel').inner_text()
        print('7. After [+] button click - Zoom text:', zoom_text_5)

        # 8. Test [Toàn bộ (Fit)] button
        await page.locator('#btnModeFit').click()
        body_class_6 = await lb_body.get_attribute('class')
        print('8. After [Toàn bộ (Fit)] click - Body class:', body_class_6)
        assert 'mode-fit' in body_class_6, 'Should return to mode-fit'

        # 9. Test Close ESC
        await page.keyboard.press('Escape')
        is_active = await page.locator('#lightboxModal').evaluate('el => el.classList.contains("active")')
        print('9. Modal active after ESC:', is_active)
        assert not is_active, 'Modal should be closed'

        print('JS errors:', errors)
        assert len(errors) == 0, 'Found JS errors'
        await browser.close()
        print('ALL FIT & ZOOM TESTS PASSED 100%!')

if __name__ == '__main__':
    asyncio.run(main())
