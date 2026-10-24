import asyncio
import os
from playwright.async_api import async_playwright

async def test_sidebar_scroll_leak():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        file_path = os.path.abspath("index.html")
        await page.goto(f"file:///{file_path.replace(os.sep, '/')}")
        await page.wait_for_selector(".website-card")

        # 1. Hover on sidebar
        sidebar = page.locator(".sidebar")
        box = await sidebar.bounding_box()
        print(f"Sidebar bounding box: {box}")

        # Move mouse to center of sidebar
        await page.mouse.move(box["x"] + box["width"] / 2, box["y"] + 200)

        # Record scroll position before wheel
        scroll_before = await page.evaluate("window.scrollY")
        print(f"Window scrollY before wheel on sidebar: {scroll_before}")

        # Wheel scroll 500px down while hovering sidebar
        await page.mouse.wheel(0, 500)
        await page.wait_for_timeout(500)

        scroll_after = await page.evaluate("window.scrollY")
        print(f"Window scrollY after wheel on sidebar: {scroll_after}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_sidebar_scroll_leak())
