import asyncio
import os
from playwright.async_api import async_playwright

async def test_base64_clipboard():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(permissions=["clipboard-read", "clipboard-write"])
        page = await context.new_page()

        file_path = os.path.abspath("index.html")
        await page.goto(f"file:///{file_path.replace(os.sep, '/')}")
        await page.wait_for_selector(".website-card")

        # Create a 1x1 PNG base64 and write to clipboard
        res = await page.evaluate("""
            async () => {
                try {
                    // 1x1 transparent PNG base64
                    const b64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==";
                    const byteChars = atob(b64);
                    const byteNumbers = new Array(byteChars.length);
                    for (let i = 0; i < byteChars.length; i++) {
                        byteNumbers[i] = byteChars.charCodeAt(i);
                    }
                    const byteArray = new Uint8Array(byteNumbers);
                    const blob = new Blob([byteArray], { type: "image/png" });

                    await navigator.clipboard.write([
                        new ClipboardItem({ "image/png": blob })
                    ]);
                    return { success: true };
                } catch (e) {
                    return { success: false, error: e.name + ': ' + e.message };
                }
            }
        """)
        print("Base64 to Blob to Clipboard on file:///:", res)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_base64_clipboard())
