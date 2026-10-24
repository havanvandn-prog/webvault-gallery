import asyncio
import os
from playwright.async_api import async_playwright

async def test_xhr_local():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(permissions=["clipboard-read", "clipboard-write"])
        page = await context.new_page()

        file_path = os.path.abspath("index.html")
        await page.goto(f"file:///{file_path.replace(os.sep, '/')}")
        await page.wait_for_selector(".website-card")

        res = await page.evaluate("""
            async () => {
                return new Promise((resolve) => {
                    const xhr = new XMLHttpRequest();
                    xhr.open('GET', 'Kho_Anh_Webp/square-vn_com_fb.png', true);
                    xhr.responseType = 'blob';
                    xhr.onload = async function() {
                        if (xhr.status === 200 || xhr.status === 0) {
                            try {
                                const blob = xhr.response;
                                await navigator.clipboard.write([
                                    new ClipboardItem({ 'image/png': blob })
                                ]);
                                resolve({ success: true, size: blob.size });
                            } catch (e) {
                                resolve({ success: false, error: e.name + ': ' + e.message });
                            }
                        } else {
                            resolve({ success: false, status: xhr.status });
                        }
                    };
                    xhr.onerror = function(e) {
                        resolve({ success: false, error: 'XHR Error' });
                    };
                    xhr.send();
                });
            }
        """)
        print("XHR Local file test result:", res)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_xhr_local())
