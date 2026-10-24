import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page(viewport={"width": 1440, "height": 900})
    page.goto("https://sukienachau.com/", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    
    # Check elements containing the text "Tư Vấn Miễn Phí" or "Nhận Báo Giá" or "093 885 9998"
    elements = page.evaluate("""() => {
        let results = [];
        document.querySelectorAll('*').forEach(el => {
            if (el.innerText && el.innerText.includes('Tư Vấn Miễn Phí') && el.innerText.includes('Nhận Báo Giá')) {
                let s = window.getComputedStyle(el);
                let r = el.getBoundingClientRect();
                results.push({
                    tag: el.tagName,
                    id: el.id,
                    className: el.className,
                    position: s.position,
                    top: r.top,
                    bottom: r.bottom,
                    left: r.left,
                    width: r.width,
                    height: r.height,
                    zIndex: s.zIndex,
                    bg: s.backgroundColor,
                    color: s.color,
                    outerHTMLSnippet: el.outerHTML.slice(0, 200)
                });
            }
        });
        return results;
    }""")
    
    print("Found pink bar elements:")
    for el in elements:
        print(el)
    b.close()
