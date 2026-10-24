import sys
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page(viewport={"width": 1440, "height": 900})
    
    # Test HoaBinh Events
    print("Testing HoaBinh Events...")
    page.goto("https://hoabinhevents.com/", wait_until="networkidle", timeout=30000)
    time.sleep(2)
    
    # Check elements and animations
    hidden_elements = page.evaluate("""() => {
        let els = document.querySelectorAll('*');
        let hidden = 0;
        let aos = document.querySelectorAll('[data-aos], .wow, [data-wow-delay]');
        let lazyImgs = document.querySelectorAll('img[data-src], img[loading="lazy"], img[data-lazy-src]');
        return {
            totalElements: els.length,
            aosCount: aos.length,
            lazyImgsCount: lazyImgs.length,
            bodyHeight: document.body.scrollHeight
        };
    }""")
    print("HoaBinh Events stats:", hidden_elements)
    
    # Test AzEvent
    print("\nTesting AzEvent...")
    page.goto("https://azevent.vn/", wait_until="networkidle", timeout=30000)
    time.sleep(2)
    az_stats = page.evaluate("""() => {
        let els = document.querySelectorAll('*');
        let aos = document.querySelectorAll('[data-aos], .wow, [data-wow-delay], .lazyload');
        let lazyImgs = document.querySelectorAll('img[data-src], img[loading="lazy"], img[data-lazy-src]');
        return {
            totalElements: els.length,
            aosCount: aos.length,
            lazyImgsCount: lazyImgs.length,
            bodyHeight: document.body.scrollHeight
        };
    }""")
    print("AzEvent stats:", az_stats)
    b.close()
