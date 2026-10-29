# -*- coding: utf-8 -*-
import os, sys, time
from io import BytesIO
from PIL import Image
from playwright.sync_api import sync_playwright

sys.path.append(r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts")
from capture_engine import capture_smart_clean

def capture_the_planners():
    url = "https://theplannersvn.com/"
    slug = "theplannersvn_com"
    domain = "theplannersvn.com"
    
    png_path = os.path.join("Anh_Chup_Website", f"{domain}.png")
    full_webp = os.path.join("Kho_Anh_Webp", f"{slug}_full.webp")
    thumb_webp = os.path.join("Kho_Anh_Webp", f"{slug}_thumb.webp")
    fb_png = os.path.join("Kho_Anh_Webp", f"{slug}_fb.png")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        page = context.new_page()
        print(f"Navigating to {url}...")
        page.goto(url, wait_until="networkidle", timeout=30000)
        time.sleep(2)
        
        # Chụp full-page bằng capture_smart_clean
        w, h = capture_smart_clean(page, png_path, viewport_height=900)
        print(f"Captured raw PNG: {w}x{h} at {png_path}")
        browser.close()
        
    # Nén WebP 3 tầng
    with Image.open(png_path) as im:
        im_rgb = im.convert("RGB")
        w, h = im_rgb.size
        
        # 1. Full WebP (khóa width 1440)
        target_h = min(h, 15500)
        im_full = im_rgb.crop((0, 0, 1440, target_h))
        im_full.save(full_webp, "WEBP", quality=82, method=4)
        
        # 2. Thumb WebP (width 600)
        thumb_h = int(target_h * (600.0 / 1440.0))
        im_thumb = im_full.resize((600, thumb_h), Image.Resampling.LANCZOS)
        im_thumb.save(thumb_webp, "WEBP", quality=75, method=4)
        
        # 3. FB PNG (1080x1920)
        slice_h = min(h, int(w * 16 / 9))
        crop = im_rgb.crop((0, 0, w, slice_h))
        im_fb = crop.resize((1080, 1920), Image.Resampling.LANCZOS)
        im_fb.save(fb_png, format="PNG", optimize=True)
        
    print(f"SUCCESS: {slug}")
    print(f"  Full: {full_webp} ({os.path.getsize(full_webp)//1024} KB)")
    print(f"  Thumb: {thumb_webp} ({os.path.getsize(thumb_webp)//1024} KB)")
    print(f"  FB: {fb_png} ({os.path.getsize(fb_png)//1024} KB)")

if __name__ == '__main__':
    capture_the_planners()
