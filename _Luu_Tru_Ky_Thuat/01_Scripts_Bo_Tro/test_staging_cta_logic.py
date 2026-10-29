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

        # 1. Kiểm tra ban đầu: 0 mẫu được chọn
        initial_count = await page.locator('#statApproved').inner_text()
        print('1. Initial approved count:', initial_count)
        assert initial_count == '0', f'Expected 0, got {initial_count}'

        # 2. Kiểm tra text nút card 1 ban đầu
        first_btn = page.locator('.approval-toggle-btn').first
        btn_text = await first_btn.inner_text()
        print('2. Initial first button text:', repr(btn_text))
        assert '+ Thêm Mẫu Này Để Đồng Bộ' in btn_text, f'Expected "+ Thêm...", got {btn_text}'

        # 3. Bấm vào nút để THÊM VÀO ĐỒNG BỘ
        await first_btn.click()
        count_after_add = await page.locator('#statApproved').inner_text()
        first_btn_after = page.locator('.approval-toggle-btn').first
        btn_text_after = await first_btn_after.inner_text()
        first_card = page.locator('.staging-card').first
        card_class = await first_card.get_attribute('class')
        print('3. After clicking add - Count:', count_after_add, '| Btn text:', repr(btn_text_after), '| Card class:', card_class)
        assert count_after_add == '1', f'Expected 1, got {count_after_add}'
        assert 'Đã Thêm' in btn_text_after
        assert 'is-selected' in card_class

        # 4. Bấm lại để HỦY THÊM
        await first_btn_after.click()
        count_after_cancel = await page.locator('#statApproved').inner_text()
        btn_text_cancel = await page.locator('.approval-toggle-btn').first.inner_text()
        print('4. After cancel click - Count:', count_after_cancel, '| Btn text:', repr(btn_text_cancel))
        assert count_after_cancel == '0'
        assert '+ Thêm Mẫu Này Để Đồng Bộ' in btn_text_cancel

        # 5. Kiểm tra trong Lightbox
        first_thumb = page.locator('.card-thumbnail-box').first
        await first_thumb.click()
        lb_btn = page.locator('#lbToggleBtn')
        lb_btn_text = await lb_btn.inner_text()
        print('5. Lightbox initial toggle button:', repr(lb_btn_text))
        assert '+ Thêm Mẫu Này Để Đồng Bộ' in lb_btn_text

        # Bấm phím Space trong Lightbox để thêm
        await page.keyboard.press('Space')
        lb_btn_text_after_space = await lb_btn.inner_text()
        print('6. Lightbox button after Space:', repr(lb_btn_text_after_space))
        assert 'Đã Thêm' in lb_btn_text_after_space

        # Đóng Lightbox
        await page.keyboard.press('Escape')
        count_after_lb = await page.locator('#statApproved').inner_text()
        print('7. Page count after closing Lightbox:', count_after_lb)
        assert count_after_lb == '1'

        # 8. Test Chọn tất cả / Bỏ chọn tất cả
        toggle_all_btn = page.locator('#btnToggleAll')
        await toggle_all_btn.click()
        count_all = await page.locator('#statApproved').inner_text()
        print('8. After Select All click - Count:', count_all)
        assert count_all == '20'

        await toggle_all_btn.click()
        count_none = await page.locator('#statApproved').inner_text()
        print('9. After Deselect All click - Count:', count_none)
        assert count_none == '0'

        print('JS errors:', errors)
        assert len(errors) == 0, 'Found JS errors'
        await browser.close()
        print('ALL STAGING CTA LOGIC TESTS PASSED 100%!')

if __name__ == '__main__':
    asyncio.run(main())
