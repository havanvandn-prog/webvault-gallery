import asyncio
import os
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from playwright.async_api import async_playwright

async def test_button_click_copy():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(permissions=["clipboard-read", "clipboard-write"])
        page = await context.new_page()

        file_path = os.path.abspath("index.html")
        await page.goto(f"file:///{file_path.replace(os.sep, '/')}")
        await page.wait_for_selector(".website-card")

        # Find the first card's copy image button
        copy_img_btn = page.locator(".btn-fb-image").first
        btn_text_before = await copy_img_btn.inner_text()
        print(f"Button text before click: {btn_text_before.strip()}")

        # Click the button
        await copy_img_btn.click()

        # Wait for operation to complete
        await page.wait_for_timeout(2000)

        # Check guide modal: MUST NOT EXIST
        guide_modal = await page.locator("#guideModal").count()
        print(f"Guide modal count (should be 0): {guide_modal}")
        assert guide_modal == 0, "Guide modal should NOT appear!"

        # Check toast message
        toast = page.locator("#toastMsg")
        toast_text = await toast.inner_text()
        print(f"Toast notification text: {toast_text}")
        assert "1080x1920" in toast_text, "Toast should mention 1080x1920!"

        # Check button text during/after copy
        btn_text_after = await copy_img_btn.inner_text()
        print(f"Button text after click: {btn_text_after.strip()}")
        assert "Đã Copy" in btn_text_after, "Button should show 'Đã Copy'!"

        # Check clipboard content
        clip_has_png = await page.evaluate("""
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
        print(f"Clipboard verification: {clip_has_png}")
        assert clip_has_png["hasPng"] is True, "Clipboard must contain image/png!"
        assert clip_has_png["size"] > 100000, "Image size must be substantial!"

        await browser.close()
        print("\nALL VERIFICATIONS PASSED: 1-Click Copy directly to Clipboard works on file:/// with ZERO modals!")

if __name__ == "__main__":
    asyncio.run(test_button_click_copy())
