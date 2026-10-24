import asyncio
import os
from playwright.async_api import async_playwright

async def test_canvas_blob_on_file():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(permissions=["clipboard-read", "clipboard-write"])
        page = await context.new_page()

        file_path = os.path.abspath("index.html")
        await page.goto(f"file:///{file_path.replace(os.sep, '/')}")
        await page.wait_for_selector(".website-card")

        res = await page.evaluate("""
            async () => {
                const item = WEBSITES_DATA[0];
                const img = new Image();
                img.src = item.full || item.thumb;
                await new Promise((res, rej) => {
                    img.onload = res;
                    img.onerror = rej;
                });
                const canvas = document.createElement('canvas');
                canvas.width = 1080;
                canvas.height = 1920;
                const ctx = canvas.getContext('2d');
                ctx.drawImage(img, 0, 0, img.naturalWidth, Math.min(img.naturalHeight, img.naturalWidth * 16/9), 0, 0, 1080, 1920);
                try {
                    const blob = await new Promise(r => canvas.toBlob(r, 'image/png'));
                    await navigator.clipboard.write([new ClipboardItem({'image/png': blob})]);
                    return { success: true, blobSize: blob.size };
                } catch (e) {
                    return { success: false, error: e.name + ': ' + e.message };
                }
            }
        """)
        print("Test canvas blob result:", res)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_canvas_blob_on_file())
