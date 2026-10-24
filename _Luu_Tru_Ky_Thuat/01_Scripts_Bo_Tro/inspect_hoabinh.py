import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page(viewport={"width": 1440, "height": 900})
    page.goto("https://hoabinhevents.com/", wait_until="networkidle", timeout=30000)
    
    # Check what styles are causing invisibility
    res = page.evaluate("""() => {
        let sections = Array.from(document.querySelectorAll('section, div.container, main > div'));
        return sections.slice(0, 15).map(s => {
            let style = window.getComputedStyle(s);
            let rect = s.getBoundingClientRect();
            return {
                tag: s.tagName,
                class: s.className,
                opacity: style.opacity,
                visibility: style.visibility,
                display: style.display,
                top: rect.top,
                height: rect.height
            };
        });
    }""")
    for r in res:
        print(r)
    b.close()
