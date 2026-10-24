# -*- coding: utf-8 -*-
import os
import sys
from playwright.sync_api import sync_playwright

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    path = os.path.abspath('index.html')
    page.goto(f'file:///{path}')
    page.wait_for_selector('.website-card')
    
    # 1. Check initial position
    sidebar_top_init = page.evaluate('document.querySelector(".sidebar").getBoundingClientRect().top')
    print(f"Vị trí Sidebar ban đầu: {sidebar_top_init}px")
    
    # 2. Scroll down 2500px
    page.evaluate('window.scrollTo(0, 2500)')
    page.wait_for_timeout(300)
    
    sidebar_top_after = page.evaluate('document.querySelector(".sidebar").getBoundingClientRect().top')
    header_top_after = page.evaluate('document.querySelector(".top-header").getBoundingClientRect().top')
    scroll_y = page.evaluate('window.scrollY')
    
    print(f"Khoảng cách đã cuộn: {scroll_y}px")
    print(f"Vị trí Sidebar sau khi cuộn: {sidebar_top_after}px (Kỳ vọng: 0)")
    print(f"Vị trí Top Header sau khi cuộn: {header_top_after}px (Kỳ vọng: 0)")
    
    assert sidebar_top_after == 0, f"Sidebar bị trôi: {sidebar_top_after}"
    assert header_top_after == 0, f"Header bị trôi: {header_top_after}"
    
    # 3. Test clicking sidebar while scrolled
    page.locator("text=Dark Mode & Sang trọng").first.click()
    page.wait_for_timeout(300)
    cards_count = page.locator('.website-card:visible').count()
    print(f"Sau khi nhấp chọn Dark Mode khi đang ở lưng chừng trang: {cards_count} cards (Kỳ vọng: 5)")
    assert cards_count == 5, f"Lỗi click sidebar: {cards_count}"
    
    print("\n[CHÚC MỪNG] THANH SIDEBAR ĐÃ CỐ ĐỊNH 100% HOÀN HẢO!")
    browser.close()
