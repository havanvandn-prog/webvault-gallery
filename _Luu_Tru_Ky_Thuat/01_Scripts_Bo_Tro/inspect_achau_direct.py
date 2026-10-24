import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page(viewport={"width": 1440, "height": 900})
    page.goto("https://sukienachau.com/", wait_until="domcontentloaded")
    
    # Check if footer-additional exists right after load
    res = page.evaluate("""() => {
        let el = document.querySelector('.footer-additional');
        if (!el) return {found: false};
        let s = window.getComputedStyle(el);
        let r = el.getBoundingClientRect();
        return {
            found: true,
            display: s.display,
            visibility: s.visibility,
            opacity: s.opacity,
            position: s.position,
            top: r.top,
            bottom: r.bottom,
            height: r.height,
            outerHTML: el.outerHTML
        };
    }""")
    print("Direct check on .footer-additional:", res)
    b.close()
