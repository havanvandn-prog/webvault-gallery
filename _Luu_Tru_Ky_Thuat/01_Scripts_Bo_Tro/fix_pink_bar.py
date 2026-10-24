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

def capture_smart_clean_v3(page, output_path, viewport_height=900):
    super_hydrate(page)
    
    # 1. Cuộn mượt từng bước để kích hoạt lazyload
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
    time.sleep(0.6)
    
    total_height = page.evaluate("() => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
    chunks = []
    
    # 3. Chụp từng khung hình:
    # - Ở MỌI KHUNG HÌNH: Ẩn tất cả thanh floating ở ĐÁY (bottom bars như footer-additional, nút chat, nút hotline)
    # - Ở KHUNG 0 (y=0): Giữ nguyên Top Header
    # - TỪ KHUNG 1 (y>0): Ẩn luôn Top Header (đã chụp ở khung 0 rồi)
    y = 0
    while y < total_height:
        page.evaluate(f"window.scrollTo(0, {y})")
        time.sleep(0.2)
        
        # Bơm script ẩn chuẩn xác
        page.evaluate(f"""() => {{
            const currentY = {y};
            document.querySelectorAll('*').forEach(el => {{
                const s = window.getComputedStyle(el);
                if (s.position === 'fixed' || s.position === 'sticky') {{
                    const r = el.getBoundingClientRect();
                    // 1. Luôn luôn ẩn các thanh dính ở ĐÁY màn hình (bottom bar, chat widget, hotline CTA)
                    if (r.bottom >= window.innerHeight - 120 && r.height < 300) {{
                        el.style.setProperty('visibility', 'hidden', 'important');
                    }}
                    // 2. Nếu đã cuộn qua khỏi đỉnh trang (y > 0), ẩn luôn Header đỉnh trang
                    if (currentY > 0 && r.top <= 10 && r.height < 250) {{
                        el.style.setProperty('visibility', 'hidden', 'important');
                    }}
                }}
            }});
        }}""")
            
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
    page = b.new_page(viewport={"width": 1440, "height": 900})
    print("Navigating to sukienachau.com...")
    page.goto("https://sukienachau.com/", wait_until="domcontentloaded", timeout=35000)
    time.sleep(2)
    output_path = r"D:\AI Agent\Website\Tìm mẫu website\Anh_Chup_Website\sukienachau.com.png"
    dims = capture_smart_clean_v3(page, output_path)
    b.close()
    print("Successfully captured clean sukienachau:", dims)
