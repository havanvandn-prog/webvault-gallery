import asyncio
import os
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from playwright.async_api import async_playwright

async def test_vietlink_copy():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(permissions=["clipboard-read", "clipboard-write"])
        page = await context.new_page()

        file_path = os.path.abspath("index.html")
        await page.goto(f"file:///{file_path.replace(os.sep, '/')}")
        await page.wait_for_selector(".website-card")

        # Find card 08 (Vietlink Event)
        cards = page.locator(".website-card")
        card_count = await cards.count()
        print(f"Total cards: {card_count}")

        # Card 08 is the 8th card (index 7)
        card_08 = cards.nth(7)
        title = await card_08.locator(".card-title").inner_text()
        print(f"Testing card: {title}")

        btn_copy = card_08.locator(".btn-fb-image")
        await btn_copy.click()
        await page.wait_for_timeout(1000)

        # Check toast
        toast = await page.locator("#toastMsg").inner_text()
        print(f"Toast: {toast}")
        assert "Vietlink Event" in toast

        btn_text = await btn_copy.inner_text()
        print(f"Button after click: {btn_text}")
        assert "Đã Copy" in btn_text

        # Verify clipboard
        clip = await page.evaluate("""
            async () => {
                const items = await navigator.clipboard.read();
                for (const item of items) {
                    if (item.types.includes('image/png')) {
                        const blob = await item.getType('image/png');
                        return { hasPng: true, size: blob.size };
                    }
                }
                return { hasPng: false };
            }
        """)
        print(f"Clipboard result: {clip}")
        assert clip["hasPng"] is True

        await browser.close()
        print("VIETLINK EVENT 1-CLICK COPY PASSED 100%!")

if __name__ == "__main__":
    asyncio.run(test_vietlink_copy())
