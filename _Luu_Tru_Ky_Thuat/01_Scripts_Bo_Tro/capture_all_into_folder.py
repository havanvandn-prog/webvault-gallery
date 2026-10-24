import os
import sys
import time
from io import BytesIO
from PIL import Image

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

from playwright.sync_api import sync_playwright

target_dir = r"D:\AI Agent\Website\Tìm mẫu website\Anh_Chup_Website"
os.makedirs(target_dir, exist_ok=True)

websites = [
    {"id": "01", "name": "Square Experiential Communications", "filename": "01_Square_Experiential.png", "url": "https://square-vn.com/"},
    {"id": "02", "name": "Per-fectiv", "filename": "02_Per_fectiv.png", "url": "https://per-fectiv.com/"},
    {"id": "03", "name": "Le Bros", "filename": "03_Le_Bros.png", "url": "https://lebros.vn/"},
    {"id": "04", "name": "BS Group", "filename": "04_BS_Group.png", "url": "https://bsgroup.com.vn/"},
    {"id": "05", "name": "Zeit Media", "filename": "05_Zeit_Media.png", "url": "https://zeitmedia.vn/"},
    {"id": "06", "name": "HoaBinh Events", "filename": "06_HoaBinh_Events.png", "url": "https://hoabinhevents.com/"},
    {"id": "07", "name": "Á Châu Event", "filename": "07_A_Chau_Event.png", "url": "https://sukienachau.com/"},
    {"id": "08", "name": "Vietlink Event", "filename": "08_Vietlink_Event.png", "url": "https://vietlinkevent.vn/"},
    {"id": "09", "name": "Apex Media", "filename": "09_Apex_Media.png", "url": "https://apexevent.vn/"},
    {"id": "10", "name": "Newday Media", "filename": "10_Newday_Media.png", "url": "https://newdaymedia.com.vn/"},
    {"id": "11", "name": "Cyber Show", "filename": "11_Cyber_Show.png", "url": "https://cybershow.vn/"},
    {"id": "12", "name": "YesEvents", "filename": "12_YesEvents.png", "url": "https://www.yesevents.vn/"},
    {"id": "13", "name": "CAT Event", "filename": "13_CAT_Event.png", "url": "https://cat-event.com.vn/"},
    {"id": "14", "name": "Hoàng Sa Việt", "filename": "14_Hoang_Sa_Viet.png", "url": "https://hoangsaviet.com/"},
    {"id": "15", "name": "Đất Việt Event", "filename": "15_Dat_Viet_Event.png", "url": "https://datvietevent.com/"},
    {"id": "16", "name": "Danang Events", "filename": "16_Danang_Events.png", "url": "https://danangevents.com.vn/"},
    {"id": "17", "name": "Sea Event", "filename": "17_Sea_Event.png", "url": "https://seaevent.vn/"},
    {"id": "18", "name": "AN Media", "filename": "18_AN_Media.png", "url": "https://anmedia.vn/"},
    {"id": "19", "name": "Thăng Long Event", "filename": "19_Thang_Long_Event.png", "url": "https://thanglongevent.com/"},
    {"id": "20", "name": "AzEvent", "filename": "20_AzEvent.png", "url": "https://azevent.vn/"}
]

def super_hydrate(page):
    """Vô hiệu hóa animation ẩn và ép nạp data-src trong DOM."""
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
    
    # 2. Cuộn về đỉnh trang
    page.evaluate("window.scrollTo(0, 0)")
    time.sleep(0.6)
    
    total_height = page.evaluate("() => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight)")
    chunks = []
    
    # 3. Chụp từng khung hình và ẩn động sticky header từ y > 0
    y = 0
    while y < total_height:
        page.evaluate(f"window.scrollTo(0, {y})")
        time.sleep(0.2)
        
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

print(f"=== BẮT ĐẦU CHỤP LẠI VÀ LƯU 20 WEBSITE VÀO: {target_dir} ===")

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
    )

    for idx, item in enumerate(websites, start=1):
        filepath = os.path.join(target_dir, item["filename"])
        print(f"\n[{idx}/20] Đang chụp: {item['name']} ({item['url']})...")
        start_t = time.time()
        
        ctx = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = ctx.new_page()
        
        try:
            page.goto(item["url"], wait_until="domcontentloaded", timeout=45000)
            time.sleep(2.5)
            w, h = capture_smart_clean(page, filepath)
            elapsed = time.time() - start_t
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            print(f"  -> THÀNH CÔNG: {item['filename']} | {w}x{h} px | {size_mb:.2f} MB | {elapsed:.1f}s")
        except Exception as e:
            print(f"  -> LỖI khi chụp {item['name']}: {e}")
            # Fallback direct screenshot if stitching had any issue
            try:
                print(f"  -> Đang thử chế độ Fallback Full-Page...")
                page.screenshot(path=filepath, full_page=True, timeout=20000)
                size_mb = os.path.getsize(filepath) / (1024 * 1024)
                print(f"  -> THÀNH CÔNG (Fallback): {item['filename']} | {size_mb:.2f} MB")
            except Exception as e2:
                print(f"  -> Fallback cũng lỗi: {e2}")
        finally:
            page.close()
            ctx.close()

    browser.close()

print("\n=== HOÀN TẤT CHỤP TOÀN BỘ 20 WEBSITE VÀO FOLDER! ===")
