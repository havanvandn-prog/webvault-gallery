import asyncio
import os
from PIL import Image
from playwright.async_api import async_playwright

async def verify_favicons():
    # 1. Verify physical files
    assert os.path.exists("favicon.svg"), "favicon.svg missing"
    assert os.path.exists("favicon.png"), "favicon.png missing"
    assert os.path.exists("favicon.ico"), "favicon.ico missing"

    png_im = Image.open("favicon.png")
    print(f"favicon.png size: {png_im.size}, mode: {png_im.mode}")
    assert png_im.size == (512, 512), "favicon.png should be 512x512"

    ico_im = Image.open("favicon.ico")
    print(f"favicon.ico size: {ico_im.size}, format: {ico_im.format}")

    # 2. Verify with browser
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        file_path = os.path.abspath("index.html").replace(os.sep, "/")
        await page.goto(f"file:///{file_path}")

        favicon_links = await page.evaluate("""
            () => {
                const links = Array.from(document.querySelectorAll("link[rel*='icon']"));
                return links.map(l => ({ rel: l.rel, href: l.getAttribute('href'), type: l.type }));
            }
        """)
        print("Favicon links in index.html:", favicon_links)
        assert len(favicon_links) >= 2, "Must have at least 2 icon links"

        await browser.close()

    print("\nALL FAVICON VERIFICATIONS PASSED!")

if __name__ == "__main__":
    asyncio.run(verify_favicons())
