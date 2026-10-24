import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

import time
from io import BytesIO
from PIL import Image
from playwright.sync_api import sync_playwright

def super_hydrate(page):
    """Ép animation hiển thị và kích hoạt toàn bộ lazy-load."""
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

def capture_smart_clean(page, output_path, viewport_height=900):
    """
    Chụp thông minh:
    1. Cuộn mượt để kích hoạt lazyload
    2. Chụp Chunk 0 (giữ nguyên Header)
    3. Từ Chunk 1: Ẩn toàn bộ sticky/fixed elements (Header, Navbar, Chat Widgets, Floating CTA)
    4. Ghép hoàn hảo không lặp header
    """
    super_hydrate(page)
    
    # 1. Cuộn kích hoạt
    total_height = page.evaluate("() => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
    y = 0
    while y < total_height:
        page.evaluate(f"window.scrollTo(0, {y})")
        time.sleep(0.12)
        y += 600
        total_height = page.evaluate("() => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
    
    super_hydrate(page)
    time.sleep(1.2)
    
    # 2. Về đầu trang
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(0.5)
    
    total_height = page.evaluate("() => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
    print(f"Bắt đầu chụp Smart Clean: Chiều cao = {total_height}px")
    
    chunks = []
    
    # --- CHUNK 0: Giữ nguyên Header ---
    chunk0_bytes = page.screenshot(full_page=False)
    img0 = Image.open(BytesIO(chunk0_bytes))
    chunks.append(img0)
    
    # --- TỪ CHUNK 1: ẨN TOÀN BỘ FIXED & STICKY ELEMENTS ---
    page.evaluate("""() => {
        // Tìm và ẩn tất cả phần tử fixed hoặc sticky
        const elements = document.querySelectorAll('*');
        window._hiddenFixedElements = [];
        elements.forEach(el => {
            const style = window.getComputedStyle(el);
            if (style.position === 'fixed' || style.position === 'sticky') {
                // Kiểm tra nếu là header, navbar hoặc floating widget
                window._hiddenFixedElements.push({
                    element: el,
                    prevVisibility: el.style.visibility,
                    prevOpacity: el.style.opacity
                });
                el.style.setProperty('visibility', 'hidden', 'important');
            }
        });
        
        // Thêm rule CSS khẩn cấp để đảm bảo các class sticky/fixed bị ẩn
        const styleSheet = document.createElement("style");
        styleSheet.id = "_anti_sticky_style";
        styleSheet.innerText = `
            header[style*="fixed"], nav[style*="fixed"], 
            [class*="sticky"], [class*="fixed"], [id*="sticky"], [id*="fixed"],
            .is-sticky, .header-sticky, .fixed-top, .elementor-sticky {
                visibility: hidden !important;
            }
        `;
        document.head.appendChild(styleSheet);
    }""")
    
    # Chụp các chunk tiếp theo
    y = viewport_height
    while y < total_height:
        page.evaluate(f"window.scrollTo(0, {y})")
        time.sleep(0.2)
        chunk_bytes = page.screenshot(full_page=False)
        img = Image.open(BytesIO(chunk_bytes))
        
        if y + viewport_height > total_height:
            overlap = (y + viewport_height) - total_height
            crop_box = (0, overlap, img.width, img.height)
            img = img.crop(crop_box)
            chunks.append(img)
            break
        else:
            chunks.append(img)
            y += viewport_height

    # Ghép ảnh
    final_width = chunks[0].width
    final_image = Image.new('RGB', (final_width, total_height))
    
    curr_y = 0
    for chunk in chunks:
        final_image.paste(chunk, (0, curr_y))
        curr_y += chunk.height

    final_image.save(output_path, optimize=True)
    print(f"Đã lưu ảnh hoàn chỉnh không lặp header: {output_path} ({final_image.size})")

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page(viewport={"width": 1440, "height": 900})
    
    # Test on Per-fectiv (was repeated)
    print("\n--- Test Per-fectiv ---")
    page.goto("https://per-fectiv.com/", wait_until="domcontentloaded", timeout=35000)
    time.sleep(2)
    capture_smart_clean(page, "Anh_Chup_Website/02_Per_fectiv_clean.png")
    
    # Test on HoaBinh Events (stitched)
    print("\n--- Test HoaBinh Events ---")
    page.goto("https://hoabinhevents.com/", wait_until="domcontentloaded", timeout=35000)
    time.sleep(2)
    capture_smart_clean(page, "Anh_Chup_Website/06_HoaBinh_Events_clean.png")
    
    # Test on AzEvent (stitched)
    print("\n--- Test AzEvent ---")
    page.goto("https://azevent.vn/", wait_until="domcontentloaded", timeout=35000)
    time.sleep(2)
    capture_smart_clean(page, "Anh_Chup_Website/20_AzEvent_clean.png")
    
    b.close()
