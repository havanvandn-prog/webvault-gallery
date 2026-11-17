# -*- coding: utf-8 -*-
import os, sys, time
sys.path.append(r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts")
from capture_engine import setup_page_protection, super_hydrate, capture_smart_clean, compress_tri_layer, verify_captured_image
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    ctx = b.new_context(viewport={"width": 1440, "height": 900}, ignore_https_errors=True,
                        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    pg = ctx.new_page()
    setup_page_protection(pg)
    pg.goto("https://www.badmooncafe.co.uk/", timeout=30000, wait_until="domcontentloaded")
    time.sleep(3)
    print("Before hydrate:", pg.evaluate("() => ({len: document.body.innerText.length, classes: document.body.className, divClasses: [...document.querySelectorAll('body > div')].map(d => d.id + ':' + d.className)})"))
    super_hydrate(pg)
    time.sleep(1)
    print("After hydrate:", pg.evaluate("() => [...document.querySelectorAll('body > div')].map(d => ({id: d.id, cls: d.className, disp: getComputedStyle(d).display, vis: getComputedStyle(d).visibility}))"))
    b.close()
