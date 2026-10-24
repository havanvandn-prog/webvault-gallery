import time
from PIL import Image
from io import BytesIO
from playwright.sync_api import sync_playwright

def capture_by_stitching(page, output_path):
    viewport_height = page.viewport_size['height']
    
    # 1. Inject CSS để huỷ bỏ hoàn toàn các hiệu ứng ẩn của AOS, WOW, animation
    page.add_style_tag(content="""
        * {
            animation-duration: 0.001s !important;
            animation-delay: 0s !important;
            transition-duration: 0.001s !important;
            transition-delay: 0s !important;
        }
        [data-aos] {
            opacity: 1 !important;
            transform: none !important;
            visibility: visible !important;
        }
        .wow {
            opacity: 1 !important;
            visibility: visible !important;
            transform: none !important;
        }
        .lazyload, .perfmatters-lazy, [data-lazy-src] {
            opacity: 1 !important;
            visibility: visible !important;
        }
    """)
    
    # 2. Scroll all the way down to bottom in steps to trigger IntersectionObserver
    total_height = page.evaluate("() => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
    y = 0
    while y < total_height:
        page.evaluate(f"window.scrollTo(0, {y})")
        time.sleep(0.15)
        y += 600
        total_height = page.evaluate("() => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
    
    # 3. Ép hydrate toàn bộ ảnh
    page.evaluate("""() => {
        document.querySelectorAll('img').forEach(img => {
            const dataSrc = img.getAttribute('data-src') || img.getAttribute('data-lazy-src') || img.getAttribute('data-original');
            if (dataSrc && (!img.src || img.src.includes('data:image') || img.src !== dataSrc)) {
                img.src = dataSrc;
            }
            const dataSrcset = img.getAttribute('data-srcset') || img.getAttribute('data-lazy-srcset');
            if (dataSrcset) {
                img.srcset = dataSrcset;
            }
            img.loading = 'eager';
            img.classList.remove('lazyload', 'perfmatters-lazy');
            img.classList.add('lazyloaded');
        });
        document.querySelectorAll('*').forEach(el => {
            const bg = el.getAttribute('data-bg') || el.getAttribute('data-background');
            if (bg) {
                el.style.backgroundImage = `url("${bg}")`;
            }
            if (el.hasAttribute('data-aos')) {
                el.classList.add('aos-animate');
            }
            if (el.classList.contains('wow')) {
                el.classList.add('animated');
            }
        });
    }""")
    
    # Wait for images
    time.sleep(1.5)
    
    # 4. Now capture chunks by scrolling
    total_height = page.evaluate("() => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
    print(f"Stitching AzEvent: Total height = {total_height}px")
    
    chunks = []
    y = 0
    while y < total_height:
        page.evaluate(f"window.scrollTo(0, {y})")
        time.sleep(0.3)
        chunk_img_bytes = page.screenshot(full_page=False)
        img = Image.open(BytesIO(chunk_img_bytes))
        
        if y + viewport_height > total_height:
            overlap = (y + viewport_height) - total_height
            crop_box = (0, overlap, img.width, img.height)
            img = img.crop(crop_box)
            chunks.append(img)
            break
        else:
            chunks.append(img)
            y += viewport_height
            
    final_width = chunks[0].width
    final_image = Image.new('RGB', (final_width, total_height))
    
    curr_y = 0
    for chunk in chunks:
        final_image.paste(chunk, (0, curr_y))
        curr_y += chunk.height
        
    final_image.save(output_path, optimize=True)
    print(f"Saved stitched AzEvent: {output_path} (size: {final_image.size})")

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page(viewport={"width": 1440, "height": 900})
    page.goto("https://azevent.vn/", wait_until="networkidle", timeout=35000)
    time.sleep(2)
    capture_by_stitching(page, "Anh_Chup_Website/20_AzEvent_stitched.png")
    b.close()
