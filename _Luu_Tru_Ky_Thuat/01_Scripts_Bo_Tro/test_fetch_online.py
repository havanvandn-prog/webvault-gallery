import asyncio
import os
from playwright.async_api import async_playwright

async def test_fetch_online_on_file():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(permissions=["clipboard-read", "clipboard-write"])
        page = await context.new_page()

        file_path = os.path.abspath("index.html")
        await page.goto(f"file:///{file_path.replace(os.sep, '/')}")
        await page.wait_for_selector(".website-card")

        res = await page.evaluate("""
            async () => {
                try {
                    // Try fetching an image from GitHub Pages with CORS
                    const onlineUrl = "https://havanvandn-prog.github.io/webvault-gallery/Kho_Anh_Webp/square-vn_com_thumb.webp";
                    const resp = await fetch(onlineUrl);
                    const blob = await resp.blob();
                    const bitmap = await createImageBitmap(blob);
                    
                    const canvas = document.createElement('canvas');
                    canvas.width = 1080;
                    canvas.height = 1920;
                    const ctx = canvas.getContext('2d');
                    ctx.drawImage(bitmap, 0, 0, bitmap.width, Math.min(bitmap.height, bitmap.width * 16/9), 0, 0, 1080, 1920);
                    
                    const outBlob = await new Promise(r => canvas.toBlob(r, 'image/png'));
                    await navigator.clipboard.write([
                        new ClipboardItem({ 'image/png': outBlob })
                    ]);
                    return { success: true, size: outBlob.size };
                } catch (e) {
                    return { success: false, error: e.name + ': ' + e.message };
                }
            }
        """)
        print("Fetch online image from file:/// result:", res)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_fetch_online_on_file())
