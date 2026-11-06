# -*- coding: utf-8 -*-
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')
ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(user_agent=ua, viewport={"width": 1440, "height": 900})
    page = context.new_page()
    page.goto("https://res.edu.vn/", timeout=30000, wait_until="domcontentloaded")
    page.wait_for_timeout(2000)
    
    w_h1 = page.evaluate("document.querySelector('#wrapper').offsetHeight")
    print("Step 0 wrapper height:", w_h1)
    
    # Check what inside wrapper has display none
    # Let's run just the evaluate in super_hydrate
    page.evaluate("""() => {
        // Gỡ bỏ hoàn toàn các class khóa cuộn màn hình
        ['is-locked', 'locked', 'overflow-hidden', 'no-scroll', 'modal-open', 'has-intro', 'intro-ready', 'noscroll'].forEach(cls => {
            document.documentElement.classList.remove(cls);
            document.body.classList.remove(cls);
        });

        // 3. Ẩn triệt để các phần tử Splash Screen / Fixed Intro Gate toàn màn hình
        document.querySelectorAll('#introLux, .introAgency, [class*="splash-screen"], [class*="preloader-overlay"], [class*="welcome-gate"]').forEach(el => {
            el.style.setProperty('display', 'none', 'important');
            el.style.setProperty('visibility', 'hidden', 'important');
        });

        // 4. Ép mở khóa cuộn tự nhiên trên cả html và body
        document.documentElement.style.setProperty('overflow', 'auto', 'important');
        document.documentElement.style.setProperty('height', 'auto', 'important');
        document.body.style.setProperty('overflow', 'auto', 'important');
        document.body.style.setProperty('height', 'auto', 'important');
    }""")
    print("Step 1 (evaluate overflow) wrapper height:", page.evaluate("document.querySelector('#wrapper').offsetHeight"))
    
    # Now check image / lazyload loop
    page.evaluate("""() => {
        document.querySelectorAll('img').forEach(img => {
            const dataSrc = img.getAttribute('data-src') || img.getAttribute('data-lazy-src') || img.getAttribute('data-original');
            if (dataSrc && (!img.src || img.src.includes('data:image') || img.src !== dataSrc)) {
                img.src = dataSrc;
            }
            img.loading = 'eager';
            img.classList.remove('lazyload', 'perfmatters-lazy');
            img.classList.add('lazyloaded');
        });
    }""")
    print("Step 2 (lazyload) wrapper height:", page.evaluate("document.querySelector('#wrapper').offsetHeight"))
    
    # Now check animate loop
    page.evaluate("""() => {
        document.querySelectorAll('*').forEach(el => {
            if (el.hasAttribute('data-aos')) {
                el.classList.add('aos-animate');
            }
            if (el.contains && el.classList.contains('wow')) {
                el.classList.add('animated');
            }
        });
    }""")
    print("Step 3 (aos/wow) wrapper height:", page.evaluate("document.querySelector('#wrapper').offsetHeight"))
    
    # Now check style tag in super_hydrate
    page.add_style_tag(content="""
        * {
            animation-duration: 0.001s !important;
            animation-delay: 0s !important;
            transition-duration: 0.001s !important;
            transition-delay: 0s !important;
        }
        [data-aos] {
            opacity: 1 !important;
            transform: none !important;
            visibility: visible !important;
        }
        .wow {
            opacity: 1 !important;
            visibility: visible !important;
            transform: none !important;
        }
        .lazyload, .perfmatters-lazy, [data-lazy-src] {
            opacity: 1 !important;
            visibility: visible !important;
        }
    """)
    print("Step 4 (style tag 1) wrapper height:", page.evaluate("document.querySelector('#wrapper').offsetHeight"))
    
    # Now check style tag 2 (the display none rules)
    page.add_style_tag(content="""
        .footer-additional, .fixed-bottom, .floating-cta,
        .hotline-phone-ring, .quick-call-button, .zalo-chat-widget,
        .tt-chat-layer, [class*="chat-layer"],
        [class*="popup"], [id*="popup"],
        [class*="modal"], [id*="modal"],
        [class*="dialog"], [id*="dialog"],
        [class*="lightbox"], [id*="lightbox"],
        [class*="banner-ads"], [class*="adv-popup"],
        [class*="popup-drawer"], [id*="cookie-notice"], [class*="overlay-fixed"],
        .ast-mobile-popup-drawer, .ast-mobile-popup-overlay,
        #introLux, .introAgency, [class*="splash-screen"], [class*="preloader-overlay"],
        [class*="site-intro"], [id*="site-intro"], [class*="welcome-overlay"], [id*="welcome-overlay"],
        #hv3-gate, .hv3-hero-sticky, .hv3-journey-sticky, #maydoAppointmentModal, .maydo-modal-backdrop,
        .lead-form-popup, .dialog-container {
            display: none !important;
            visibility: hidden !important;
        }
    """)
    print("Step 5 (style tag 2 - display none) wrapper height:", page.evaluate("document.querySelector('#wrapper').offsetHeight"))

    # Now check pin-spacer
    page.add_style_tag(content="""
        .pin-spacer {
            height: auto !important;
            padding: 0 !important;
        }
    """)
    print("Step 6 (pin-spacer) wrapper height:", page.evaluate("document.querySelector('#wrapper').offsetHeight"))
    
    context.close()
    browser.close()
