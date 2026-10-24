import asyncio
import os
from playwright.async_api import async_playwright

async def test_clipboard_on_file():
    async with async_playwright() as p:
        # Launch with clipboard permissions
        browser = await p.chromium.launch(headless=True, args=["--enable-features=ClipboardAPI"])
        context = await browser.new_context(permissions=["clipboard-read", "clipboard-write"])
        page = await context.new_page()

        file_path = os.path.abspath("index.html")
        await page.goto(f"file:///{file_path.replace(os.sep, '/')}")
        await page.wait_for_selector(".website-card")

        # Test evaluating clipboard write directly on file:///
        result = await page.evaluate("""
            async () => {
                try {
                    const canvas = document.createElement('canvas');
                    canvas.width = 10;
                    canvas.height = 10;
                    const blob = await new Promise(r => canvas.toBlob(r, 'image/png'));
                    await navigator.clipboard.write([new ClipboardItem({'image/png': blob})]);
                    return { success: true };
                } catch (e) {
                    return { success: false, error: e.name + ': ' + e.message };
                }
            }
        """)
        print("Direct clipboard write result on file:///:", result)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_clipboard_on_file())
