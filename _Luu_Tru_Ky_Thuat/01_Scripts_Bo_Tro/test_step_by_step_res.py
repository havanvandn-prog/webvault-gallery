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
    print("Initial body.scrollHeight:", page.evaluate("document.body.scrollHeight"))
    
    # Test step 1: style tag
    page.add_style_tag(content="""
        .footer-additional, .fixed-bottom, .floating-cta,
        .hotline-phone-ring, .quick-call-button, .zalo-chat-widget,
        .tt-chat-layer, [class*="chat-layer"],
        [class*="popup"], [id*="popup"],
        [class*="modal"], [id*="modal"] {
            display: none !important;
        }
    """)
    print("After style 1 body.scrollHeight:", page.evaluate("document.body.scrollHeight"))
    
    # Test step 2: style 2
    page.add_style_tag(content="""
        #introLux, .introAgency, [class*="splash-screen"], [class*="preloader-overlay"],
        [class*="site-intro"], [id*="site-intro"], [class*="welcome-overlay"], [id*="welcome-overlay"] {
            display: none !important;
        }
    """)
    print("After style 2 body.scrollHeight:", page.evaluate("document.body.scrollHeight"))

    # Test step 3: html/body styles
    page.evaluate("""() => {
        document.documentElement.style.setProperty('overflow', 'auto', 'important');
        document.documentElement.style.setProperty('height', 'auto', 'important');
        document.body.style.setProperty('overflow', 'auto', 'important');
        document.body.style.setProperty('height', 'auto', 'important');
    }""")
    print("After html/body overflow auto:", page.evaluate("document.body.scrollHeight"))
    
    context.close()
    browser.close()
