import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page(viewport={"width": 1440, "height": 900})
    page.goto("https://thanglongevent.com/", wait_until="domcontentloaded")
    
    # Scroll down to 1000px
    page.evaluate("window.scrollTo(0, 1000)")
    page.wait_for_timeout(1000)
    
    headers = page.evaluate("""() => {
        let res = [];
        document.querySelectorAll('header, nav, div, [class*="header"], [class*="menu"]').forEach(el => {
            let s = window.getComputedStyle(el);
            let r = el.getBoundingClientRect();
            if (r.top <= 10 && r.height > 30 && r.height < 250 && (s.position === 'fixed' || s.position === 'sticky')) {
                res.push({
                    tag: el.tagName,
                    id: el.id,
                    className: el.className,
                    pos: s.position,
                    top: r.top,
                    height: r.height
                });
            }
        });
        return res;
    }""")
    print("Sticky headers on Thang Long when scrolled to 1000:", headers)
    b.close()
