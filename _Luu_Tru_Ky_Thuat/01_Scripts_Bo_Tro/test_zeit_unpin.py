import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page(viewport={"width": 1440, "height": 900})
    print("Navigating to Zeit Media...")
    page.goto("https://zeitmedia.vn/", wait_until="domcontentloaded", timeout=40000)
    page.wait_for_timeout(3000)
    
    # 1. Unpin all ScrollTrigger pinned sections and disable parallax
    page.evaluate("""() => {
        // Kill ScrollTriggers that pin elements
        if (typeof ScrollTrigger !== 'undefined') {
            ScrollTrigger.getAll().forEach(st => {
                // If it pins an element, kill it and revert to natural DOM flow
                if (st.pin) {
                    st.kill(true);
                }
            });
        }
        
        // Disable parallax transforms so background doesn't shift between chunks
        const style = document.createElement('style');
        style.id = '_anti_parallax_style';
        style.innerHTML = `
            [class*="parallax"], .parallax-bg, .parallax-demo-card {
                transform: none !important;
                transition: none !important;
            }
            .pin-spacer {
                height: auto !important;
                padding: 0 !important;
            }
        `;
        document.head.appendChild(style);
    }""")
    
    print("Disabled parallax and unpinned sections successfully.")
    
    # Check dragon banner position and transform
    dragon_info = page.evaluate("""() => {
        let el = document.querySelector('.parallax-bg');
        if (!el) return null;
        let s = window.getComputedStyle(el);
        let r = el.getBoundingClientRect();
        return {
            transform: s.transform,
            top: r.top,
            height: r.height
        };
    }""")
    print("Dragon banner after anti-parallax:", dragon_info)
    
    # Check client component
    client_info = page.evaluate("""() => {
        let el = document.querySelector('.featured_client_component');
        if (!el) return null;
        let s = window.getComputedStyle(el);
        let r = el.getBoundingClientRect();
        return {
            position: s.position,
            top: r.top,
            height: r.height,
            textSnippet: el.innerText.slice(0, 100)
        };
    }""")
    print("Featured client component after unpin:", client_info)
    
    b.close()
