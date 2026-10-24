import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page(viewport={"width": 1440, "height": 900})
    page.goto("https://zeitmedia.vn/", wait_until="domcontentloaded")
    page.wait_for_timeout(3000)
    
    # Check what ScrollTriggers exist on the page
    st_info = page.evaluate("""() => {
        let triggers = [];
        if (typeof ScrollTrigger !== 'undefined') {
            ScrollTrigger.getAll().forEach((st, idx) => {
                triggers.push({
                    idx: idx,
                    trigger: st.trigger ? (st.trigger.className || st.trigger.tagName) : 'none',
                    pin: !!st.pin,
                    start: st.start,
                    end: st.end,
                    scrub: !!st.vars.scrub
                });
            });
        }
        return triggers;
    }""")
    print("ScrollTriggers on Zeit Media:")
    for t in st_info:
        print(t)
        
    b.close()
