import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page(viewport={"width": 1440, "height": 900})
    page.goto("https://zeitmedia.vn/", wait_until="domcontentloaded")
    page.wait_for_timeout(3000)
    
    # 1. Inspect scripts and libraries used on Zeit Media
    libs = page.evaluate("""() => {
        let scripts = Array.from(document.querySelectorAll('script')).map(s => s.src);
        let hasGSAP = typeof gsap !== 'undefined';
        let hasScrollTrigger = typeof ScrollTrigger !== 'undefined';
        let hasLocomotive = typeof LocomotiveScroll !== 'undefined';
        let hasAOS = typeof AOS !== 'undefined';
        return {
            hasGSAP,
            hasScrollTrigger,
            hasLocomotive,
            hasAOS,
            scripts: scripts.filter(s => s.includes('.js')).slice(0, 10)
        };
    }""")
    print("Libraries on Zeit Media:", libs)
    
    # 2. Inspect the dragon section and its transforms
    section_info = page.evaluate("""() => {
        let sections = [];
        document.querySelectorAll('section, div[class*="section"], div[class*="banner"], div[class*="about"]').forEach(el => {
            let s = window.getComputedStyle(el);
            let r = el.getBoundingClientRect();
            if (el.innerText && (el.innerText.includes('250+') || el.innerText.includes('Ấn phẩm quảng cáo') || el.innerText.includes('Creative Agency'))) {
                sections.push({
                    tag: el.tagName,
                    className: el.className,
                    position: s.position,
                    transform: s.transform,
                    top: r.top,
                    height: r.height,
                    bgImage: s.backgroundImage.slice(0, 80),
                    overflow: s.overflow
                });
            }
        });
        return sections;
    }""")
    print("\nSection info around dragon banner:")
    for s in section_info:
        print(s)
        
    b.close()
