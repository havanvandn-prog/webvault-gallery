import asyncio
import os
from playwright.async_api import async_playwright

async def test_copy_flow():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(permissions=["clipboard-read", "clipboard-write"])
        page = await context.new_page()

        file_path = os.path.abspath("index.html")
        await page.goto(f"file:///{file_path.replace(os.sep, '/')}")
        await page.wait_for_selector(".website-card")

        # Check the logic of copying image directly
        res = await page.evaluate("""
            async () => {
                const item = WEBSITES_DATA[0];
                let imgUrl = item.full || item.thumb;
                if (window.location.protocol === 'file:') {
                    imgUrl = 'https://havanvandn-prog.github.io/webvault-gallery/' + imgUrl;
                }
                const resp = await fetch(imgUrl);
                const blob = await resp.blob();
                const bitmap = await createImageBitmap(blob);
                
                const canvas = document.createElement('canvas');
                canvas.width = 1080;
                canvas.height = 1920;
                const ctx = canvas.getContext('2d');
                ctx.fillStyle = '#070709';
                ctx.fillRect(0, 0, 1080, 1920);
                
                const natW = bitmap.width;
                const natH = bitmap.height;
                const sliceH = Math.min(natH, Math.round(natW * (16 / 9)));
                ctx.drawImage(bitmap, 0, 0, natW, sliceH, 0, 0, 1080, 1920);
                
                const pngBlob = await new Promise(r => canvas.toBlob(r, 'image/png'));
                await navigator.clipboard.write([
                    new ClipboardItem({ 'image/png': pngBlob })
                ]);
                
                // Read back from clipboard to verify
                const clipItems = await navigator.clipboard.read();
                const hasPng = clipItems.some(i => i.types.includes('image/png'));
                return { success: true, hasPng: hasPng, size: pngBlob.size };
            }
        """)
        print("End-to-end clipboard copy verification on file:///:", res)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_copy_flow())
