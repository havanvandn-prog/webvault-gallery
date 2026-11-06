# -*- coding: utf-8 -*-
import sys
from io import BytesIO
from PIL import Image
import numpy as np
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(user_agent=ua, viewport={"width": 1440, "height": 900})
    page = context.new_page()
    page.goto("https://apollo.edu.vn/", timeout=30000, wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    
    skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
    sys.path.append(skill_path)
    from capture_engine import super_hydrate
    super_hydrate(page)
    
    # Take chunk at y=0, 900, 1800, 2700, 3600
    prev_img = None
    for y in range(0, 4500, 900):
        page.evaluate(f"window.scrollTo(0, {y})")
        page.wait_for_timeout(200)
        
        # apply the isTop hiding logic
        page.evaluate("""(isTop) => {
            document.querySelectorAll('*').forEach(el => {
                const s = window.getComputedStyle(el);
                if (s.position === 'fixed' || s.position === 'sticky') {
                    if (isTop) {
                        const r = el.getBoundingClientRect();
                        if (r.bottom >= window.innerHeight - 100 || (r.top > 80 && (parseInt(s.zIndex) || 0) >= 90)) {
                            el.style.setProperty('display', 'none', 'important');
                            el.style.setProperty('visibility', 'hidden', 'important');
                        }
                    } else {
                        el.style.setProperty('display', 'none', 'important');
                        el.style.setProperty('visibility', 'hidden', 'important');
                    }
                }
            });
        }""", y == 0)
        
        chunk_bytes = page.screenshot(full_page=False)
        img = Image.open(BytesIO(chunk_bytes))
        arr = np.array(img)
        
        diff = -1
        if prev_img is not None:
            diff = np.mean(np.abs(np.array(prev_img).astype(int) - arr.astype(int)))
        print(f"y={y}: chunk size={img.size}, diff with prev={diff:.4f}")
        prev_img = img
        
    context.close()
    browser.close()
