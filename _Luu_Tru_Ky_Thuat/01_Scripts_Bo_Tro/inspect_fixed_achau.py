import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page(viewport={"width": 1440, "height": 900})
    page.goto("https://sukienachau.com/", wait_until="domcontentloaded")
    page.wait_for_timeout(3000)
    
    # Scroll down to 1000px
    page.evaluate("window.scrollTo(0, 1000)")
    page.wait_for_timeout(2000)
    
    # Search for all elements that have pink/magenta or red background or fixed position
    res = page.evaluate("""() => {
        let items = [];
        document.querySelectorAll('*').forEach(el => {
            let s = window.getComputedStyle(el);
            let r = el.getBoundingClientRect();
            // check background color (magenta/pink is usually rgb(255, 0, 128) or similar)
            let isFixed = s.position === 'fixed' || s.position === 'sticky';
            let isPink = s.backgroundColor.includes('255') || s.backgroundColor.includes('23') || s.backgroundColor.includes('233');
            if (isFixed && r.height > 20) {
                items.push({
                    tag: el.tagName,
                    id: el.id,
                    className: el.className,
                    position: s.position,
                    top: r.top,
                    bottom: r.bottom,
                    height: r.height,
                    width: r.width,
                    bg: s.backgroundColor,
                    text: el.innerText ? el.innerText.slice(0, 80).replace(/\\n/g, ' ') : ''
                });
            }
        });
        return items;
    }""")
    
    print(f"Total fixed/sticky elements found: {len(res)}")
    for it in res:
        print(it)
        
    b.close()
