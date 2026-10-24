import asyncio
import os
from playwright.async_api import async_playwright

async def test_card_copy_button():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(permissions=["clipboard-read", "clipboard-write"])
        page = await context.new_page()

        file_path = os.path.abspath("index.html")
        await page.goto(f"file:///{file_path.replace(os.sep, '/')}")
        await page.wait_for_selector(".website-card")

        # Let's inspect copyDirectImageToClipboard function
        # Click the "Copy Ảnh FB (1080x1920)" on first card
        copy_img_btn = page.locator(".btn-fb-image").first
        await copy_img_btn.click()
        await page.wait_for_timeout(1000)

        # Check if guideModal appeared
        guide_modal = await page.locator("#guideModal").count()
        print(f"Guide modal count: {guide_modal}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_card_copy_button())
