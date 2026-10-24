import time
from PIL import Image
from playwright.sync_api import sync_playwright

def capture_by_stitching(page, output_path):
    # Hide fixed/sticky elements while scrolling if needed, or leave them
    # First get total height and viewport height
    viewport_height = page.viewport_size['height']
    total_height = page.evaluate("() => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
    
    print(f"Total height to capture: {total_height}px (viewport: {viewport_height}px)")
    
    chunks = []
    y = 0
    # First scroll all the way down and up to trigger everything
    while y < total_height:
        page.evaluate(f"window.scrollTo(0, {y})")
        time.sleep(0.1)
        y += 600
    
    # Now capture chunks
    y = 0
    chunk_idx = 0
    while y < total_height:
        page.evaluate(f"window.scrollTo(0, {y})")
        time.sleep(0.3)
        # Capture viewport
        chunk_img_bytes = page.screenshot(full_page=False)
        from io import BytesIO
        img = Image.open(BytesIO(chunk_img_bytes))
        
        # Calculate actual slice height for the last chunk
        if y + viewport_height > total_height:
            overlap = (y + viewport_height) - total_height
            crop_box = (0, overlap, img.width, img.height)
            img = img.crop(crop_box)
            chunks.append((y, img))
            break
        else:
            chunks.append((y, img))
            y += viewport_height
            chunk_idx += 1
            
    # Stitch chunks together
    final_width = chunks[0][1].width
    final_image = Image.new('RGB', (final_width, total_height))
    
    curr_y = 0
    for pos_y, chunk in chunks:
        final_image.paste(chunk, (0, curr_y))
        curr_y += chunk.height
        
    final_image.save(output_path, optimize=True)
    print(f"Saved stitched image: {output_path} (size: {final_image.size})")

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page(viewport={"width": 1440, "height": 900})
    page.goto("https://hoabinhevents.com/", wait_until="networkidle")
    time.sleep(2)
    capture_by_stitching(page, "Anh_Chup_Website/06_HoaBinh_Events_stitched.png")
    b.close()
