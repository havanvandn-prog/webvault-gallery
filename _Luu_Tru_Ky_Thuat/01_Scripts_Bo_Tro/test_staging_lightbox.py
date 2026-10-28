# -*- coding: utf-8 -*-
import asyncio, os, sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        errors = []
        page.on('console', lambda msg: errors.append(msg.text) if msg.type == 'error' else None)
        page.on('pageerror', lambda exc: errors.append(str(exc)))

        file_url = 'file:///' + os.path.abspath('web_nhap_staging.html').replace('\\', '/')
        await page.goto(file_url)

        # 1. Kiểm tra 20 card
        cards = await page.locator('.staging-card').count()
        print('Total staging cards:', cards)
        assert cards == 20, f'Expected 20 cards, got {cards}'

        # 2. Click thumbnail đầu tiên
        first_thumb = page.locator('.card-thumbnail-box').first
        await first_thumb.click()

        # 3. Kiểm tra modal active
        modal = page.locator('#lightboxModal')
        is_active = await modal.evaluate('el => el.classList.contains("active")')
        print('Modal active after click:', is_active)
        assert is_active, 'Modal should be active'

        # 4. Kiểm tra ảnh full của dc01
        img_src = await page.locator('#lbImage').get_attribute('src')
        print('Loaded image src:', img_src)
        assert '7799wedding_vn_full.webp' in img_src, f'Unexpected img src: {img_src}'

        # 5. Bấm Next (chuyển sang dc02)
        await page.keyboard.press('ArrowRight')
        img_src_2 = await page.locator('#lbImage').get_attribute('src')
        title_2 = await page.locator('#lbTitle').inner_text()
        print('After ArrowRight - Title:', title_2, 'Src:', img_src_2)
        assert 'lutece_vn_full.webp' in img_src_2, f'Expected lutece, got {img_src_2}'

        # 6. Bấm phím Space để đổi trạng thái
        btn_class_before = await page.locator('#lbToggleBtn').get_attribute('class')
        await page.keyboard.press('Space')
        btn_class_after = await page.locator('#lbToggleBtn').get_attribute('class')
        print('Toggle button before:', btn_class_before, 'after:', btn_class_after)
        assert 'is-rejected' in btn_class_after, 'Should be rejected after space'

        # 7. Bấm Escape để đóng
        await page.keyboard.press('Escape')
        is_active_after_esc = await modal.evaluate('el => el.classList.contains("active")')
        print('Modal active after ESC:', is_active_after_esc)
        assert not is_active_after_esc, 'Modal should be closed'

        print('JS errors:', errors)
        assert len(errors) == 0, 'Found JS errors!'
        await browser.close()
        print('ALL STAGING LIGHTBOX TESTS PASSED PERFECTLY!')

if __name__ == '__main__':
    asyncio.run(main())
