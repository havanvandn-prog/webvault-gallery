import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')
import time
from playwright.sync_api import sync_playwright

def super_hydrate_and_scroll(page):
    print("  -> Bắt đầu cuộn mượt và kích hoạt toàn bộ nội dung...")
    
    # 1. Inject CSS để ép hiển thị các animation bị ẩn
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

    # 2. Cuộn từng nấc xuống đáy trang để kích hoạt IntersectionObserver
    scroll_step = 600
    current_pos = 0
    max_retries_at_bottom = 3
    retries = 0
    last_height = 0
    
    while True:
        current_height = page.evaluate("() => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
        current_pos += scroll_step
        page.evaluate(f"window.scrollTo(0, {current_pos});")
        time.sleep(0.15)
        
        # Nếu đã chạm đáy hoặc vượt đáy
        viewport_bottom = page.evaluate("() => window.scrollY + window.innerHeight")
        if viewport_bottom >= current_height:
            if current_height == last_height:
                retries += 1
                if retries >= max_retries_at_bottom:
                    break
            else:
                retries = 0
            last_height = current_height
            time.sleep(0.3)
        if current_pos > 30000: # Capped max safety
            break

    # 3. Kích hoạt toàn bộ data-src, background lazyload trên toàn DOM
    page.evaluate("""() => {
        // Ép đổi tất cả data-src sang src
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

        // Ép load background images
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

    # 4. Chờ tất cả ảnh hoàn tất tải
    page.evaluate("""() => {
        return Promise.all(
            Array.from(document.images).map(img => {
                if (img.complete) return Promise.resolve();
                return new Promise(resolve => {
                    img.onload = img.onerror = resolve;
                    setTimeout(resolve, 1500);
                });
            })
        );
    }""")

    # 5. Cuộn lại lên đầu trang và chờ ổn định
    page.evaluate("window.scrollTo(0, 0);")
    time.sleep(1.5)
    print("  -> Hoàn tất kích hoạt toàn bộ nội dung.")

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    page = b.new_page(viewport={"width": 1440, "height": 900})
    
    print("Testing fixed capture for AzEvent...")
    page.goto("https://azevent.vn/", wait_until="networkidle", timeout=35000)
    super_hydrate_and_scroll(page)
    page.screenshot(path="Anh_Chup_Website/20_AzEvent_fixed.png", full_page=True)
    
    print("Testing fixed capture for HoaBinh Events...")
    page.goto("https://hoabinhevents.com/", wait_until="networkidle", timeout=35000)
    super_hydrate_and_scroll(page)
    page.screenshot(path="Anh_Chup_Website/06_HoaBinh_Events_fixed.png", full_page=True)
    
    b.close()
    print("DONE TESTING FIX!")
