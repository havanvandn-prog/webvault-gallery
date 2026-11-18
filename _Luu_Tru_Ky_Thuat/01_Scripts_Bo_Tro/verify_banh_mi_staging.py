# -*- coding: utf-8 -*-
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file:///d:/AI%20Agent/Website/T%C3%ACm%20m%E1%BA%ABu%20website/web_nhap_staging.html?industry=banh-mi-quoc-te")
    pg.wait_for_timeout(2000)
    cnt = pg.evaluate("document.querySelectorAll('#cardsGrid > *').length")
    imgs = pg.evaluate("Array.from(document.querySelectorAll('#cardsGrid img')).length")
    broken = pg.evaluate("Array.from(document.querySelectorAll('#cardsGrid img')).filter(i => i.complete && i.naturalWidth === 0).length")
    topic = pg.locator("#statTopicName").inner_text()
    badge = pg.locator("#badgeBanhMiQuocTe").inner_text()
    print(f"Topic: {topic} | Badge: {badge} | Grid items: {cnt} | Imgs: {imgs} | Broken: {broken} | Errors: {errs}")
    b.close()
