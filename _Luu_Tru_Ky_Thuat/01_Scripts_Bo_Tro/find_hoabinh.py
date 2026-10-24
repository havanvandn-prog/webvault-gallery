import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('https://hoabinhevents.com/', wait_until='networkidle')
    info = page.evaluate("""() => {
        let els = document.body.querySelectorAll('*');
        let below1000 = [];
        els.forEach(el => {
            let rect = el.getBoundingClientRect();
            let style = window.getComputedStyle(el);
            if (rect.top > 800 && rect.height > 50) {
                below1000.push({
                    tag: el.tagName,
                    id: el.id,
                    className: typeof el.className === 'string' ? el.className : '',
                    top: rect.top,
                    height: rect.height,
                    opacity: style.opacity,
                    visibility: style.visibility,
                    display: style.display,
                    color: style.color,
                    bg: style.backgroundColor,
                    text: el.innerText ? el.innerText.slice(0, 50).replace(/\\n/g, ' ') : ''
                });
            }
        });
        return below1000.slice(0, 15);
    }""")
    for item in info:
        print(item)
    b.close()
