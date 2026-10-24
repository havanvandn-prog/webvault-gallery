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
        /* Anti-Parallax & Static Flow */
        [class*="parallax"], .parallax-bg, .parallax-demo-card {
            transform: none !important;
            transition: none !important;
        }
        .pin-spacer {
            height: auto !important;
            padding: 0 !important;
        }
    """)

    page.evaluate("""() => {
        // Kill ScrollTriggers that pin elements
        if (typeof ScrollTrigger !== 'undefined') {
            ScrollTrigger.getAll().forEach(st => {
                if (st.pin) {
                    st.kill(true);
                }
            });
        }
        
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
        });
    }""")

def capture_zeit_perfect(page, output_path, viewport_height=900):
    super_hydrate(page)
    
    # Cuộn 1 vòng để kích hoạt
    total_height = page.evaluate("() => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
    y = 0
    while y < total_height:
        page.evaluate(f"window.scrollTo(0, {y})")
        time.sleep(0.1)
        y += 600
        total_height = page.evaluate("() => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
    
    super_hydrate(page)
    time.sleep(1.0)
    
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(0.6)
    
    total_height = page.evaluate("() => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
    print(f"Total height of Zeit Media after unpin: {total_height}px")
    chunks = []
    
    y = 0
    while y < total_height:
        page.evaluate(f"window.scrollTo(0, {y})")
        time.sleep(0.2)
        
        # Ẩn header dính và floating widget khi y > 0
        if y > 0:
            page.evaluate("""() => {
                document.querySelectorAll('*').forEach(el => {
                    const s = window.getComputedStyle(el);
                    if (s.position === 'fixed' || s.position === 'sticky') {
                        const r = el.getBoundingClientRect();
                        if (r.height > 0 && r.height < 250) {
                            if (r.top <= 10 || r.bottom >= window.innerHeight - 100) {
                                el.style.setProperty('visibility', 'hidden', 'important');
                            }
                        }
                    }
                });
            }""")
            
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
    print("Navigating to Zeit Media...")
    page.goto("https://zeitmedia.vn/", wait_until="domcontentloaded", timeout=40000)
    time.sleep(3)
    out_file = r"D:\AI Agent\Website\Tìm mẫu website\Anh_Chup_Website\zeitmedia.vn.png"
    dims = capture_zeit_perfect(page, out_file)
    b.close()
    print("Successfully captured clean Zeit Media:", dims)
