# -*- coding: utf-8 -*-
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    file_path = os.path.join(BASE_DIR, "web_nhap_staging.html").replace("\\", "/")
    file_url = f"file:///{file_path}?industry=trung-tam-anh-ngu"
    
    page.goto(file_url)
    page.wait_for_timeout(1500)
    
    cards_count = page.evaluate("document.querySelectorAll('.staging-card').length")
    active_tab = page.evaluate("document.querySelector('.staging-tab-btn.active')?.textContent?.trim()")
    active_tab_id = page.evaluate("document.querySelector('.staging-tab-btn.active')?.getAttribute('data-industry')")
    
    first_title = page.evaluate("document.querySelector('.staging-card .card-title')?.textContent?.trim()")
    
    print(f"URL: {file_url}")
    print(f"Cards rendered: {cards_count}")
    print(f"Active tab: {active_tab} (id: {active_tab_id})")
    print(f"First card title: {first_title}")
    
    browser.close()
