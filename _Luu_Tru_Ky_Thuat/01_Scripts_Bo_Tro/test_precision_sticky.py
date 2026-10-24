import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
import time
from io import BytesIO
from PIL import Image
from playwright.sync_api import sync_playwright

def super_hydrate(page):
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
    super_hydrate(page)
    
    # 1. Cuộn mượt để kích hoạt lazyload
    total_height = page.evaluate("() => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
    y = 0
    while y < total_height:
        page.evaluate(f"window.scrollTo(0, {y})")
        time.sleep(0.1)
        y += 600
        total_height = page.evaluate("() => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
    
    super_hydrate(page)
    time.sleep(1.0)
    
    # 2. Về đầu trang
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(0.5)
    
    total_height = page.evaluate("() => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
    chunks = []
    
    # --- CHUNK 0: Giữ nguyên Header ---
    chunk0_bytes = page.screenshot(full_page=False)
    img0 = Image.open(BytesIO(chunk0_bytes))
    chunks.append(img0)
    
    # --- TỪ CHUNK 1: Ẩn CHÍNH XÁC Header cố định và nút floating (Chỉ ẩn phần tử thanh bar < 250px) ---
    page.evaluate("""() => {
        document.querySelectorAll('*').forEach(el => {
            const s = window.getComputedStyle(el);
            if (s.position === 'fixed' || s.position === 'sticky') {
                const r = el.getBoundingClientRect();
                // Chỉ ẩn nếu là thanh bar hẹp (< 250px) ở đỉnh hoặc đáy, KHÔNG ẩn khối nội dung lớn
                if (r.height > 0 && r.height < 250) {
                    if (r.top <= 10 || r.bottom >= window.innerHeight - 100) {
                        el.style.setProperty('visibility', 'hidden', 'important');
                    }
                }
            }
        });
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

    final_width = chunks[0].width
    final_image = Image.new('RGB', (final_width, total_height))
    
    curr_y = 0
    for chunk in chunks:
        final_image.paste(chunk, (0, curr_y))
        curr_y += chunk.height

    final_image.save(output_path, optimize=True)
    return final_image.size

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    context = b.new_context(viewport={"width": 1440, "height": 900})
    
    # Test AzEvent
    print("Testing AzEvent with Precision Sticky Hiding...")
    page = context.new_page()
    page.goto("https://azevent.vn/", wait_until="domcontentloaded", timeout=30000)
    time.sleep(2)
    dims = capture_smart_clean(page, "Anh_Chup_Website/20_AzEvent.png")
    page.close()
    print("AzEvent captured:", dims)
    
    # Test HoaBinh Events
    print("Testing HoaBinh Events with Precision Sticky Hiding...")
    page = context.new_page()
    page.goto("https://hoabinhevents.com/", wait_until="domcontentloaded", timeout=30000)
    time.sleep(2)
    dims = capture_smart_clean(page, "Anh_Chup_Website/06_HoaBinh_Events.png")
    page.close()
    print("HoaBinh captured:", dims)
    
    # Test Dat Viet Event
    print("Testing Dat Viet Event...")
    page = context.new_page()
    page.goto("https://datvietevent.com/", wait_until="domcontentloaded", timeout=30000)
    time.sleep(2)
    dims = capture_smart_clean(page, "Anh_Chup_Website/15_Dat_Viet_Event.png")
    page.close()
    print("Dat Viet captured:", dims)
    
    b.close()
