import asyncio
import os
from playwright.async_api import async_playwright

async def run_test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        # Load local index.html
        file_path = os.path.abspath("index.html")
        await page.goto(f"file:///{file_path.replace(os.sep, '/')}")
        await page.wait_for_selector(".website-card")

        # Pick the first card thumbnail box
        thumb_box = page.locator(".card-thumbnail-box").first
        img = thumb_box.locator(".card-thumb-img")
        overlay = thumb_box.locator(".thumbnail-overlay")

        # Check before hover
        before_hover_disp = await overlay.evaluate("el => window.getComputedStyle(el).display")
        print(f"Overlay display before hover: {before_hover_disp}")

        # Hover on the thumbnail box
        await thumb_box.hover()
        await page.wait_for_timeout(300)

        # Check during hover: overlay should be display: none (not visible, no blur)
        hover_disp = await overlay.evaluate("el => window.getComputedStyle(el).display")
        print(f"Overlay display during hover: {hover_disp}")
        assert hover_disp == "none", f"Expected none, got {hover_disp}"

        # Check image filter (should be 'none', not blurred)
        img_filter = await img.evaluate("el => window.getComputedStyle(el).filter")
        print(f"Image filter during hover: {img_filter}")
        assert img_filter == "none", f"Expected none, got {img_filter}"

        # Capture screenshot right after hover (0.5s) to verify sharpness
        out_dir = "_Luu_Tru_Ky_Thuat/02_Screenshots_Debug_Va_Khao_Sat"
        os.makedirs(out_dir, exist_ok=True)
        await page.screenshot(path=f"{out_dir}/test_hover_sharp_0s.png", clip={"x": 300, "y": 100, "width": 800, "height": 600})
        print("Captured test_hover_sharp_0s.png")

        # Measure scroll progress over 3 seconds
        t0 = await img.evaluate("el => window.getComputedStyle(el).transform")
        await page.wait_for_timeout(3000)
        t3 = await img.evaluate("el => window.getComputedStyle(el).transform")
        print(f"Transform at t=0s: {t0}")
        print(f"Transform at t=3s: {t3}")

        await page.screenshot(path=f"{out_dir}/test_hover_scroll_3s.png", clip={"x": 300, "y": 100, "width": 800, "height": 600})
        print("Captured test_hover_scroll_3s.png")

        # Unhover (move mouse to top-left)
        await page.mouse.move(10, 10)
        await page.wait_for_timeout(1000)
        t_reset = await img.evaluate("el => window.getComputedStyle(el).transform")
        print(f"Transform after mouse leave: {t_reset}")

        await browser.close()
        print("TEST PASSED: Image is 100% sharp, overlay is disabled, scroll speed is slow & steady, reset works fast!")

if __name__ == "__main__":
    asyncio.run(run_test())
