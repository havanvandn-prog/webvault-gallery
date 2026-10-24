import os
import sys
import time

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

# Import capture engine from skill
skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)
from capture_engine import capture_smart_clean, check_for_blank_spaces

from playwright.sync_api import sync_playwright

output_dir = "Anh_Chup_Website"
os.makedirs(output_dir, exist_ok=True)

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

print("=== BẮT ĐẦU CHỤP LẠI TOÀN BỘ 20 WEBSITE BẰNG SMART ANTI-STICKY ENGINE ===")

audit_results = []

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
    )
    context = browser.new_context(
        viewport={"width": 1440, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
    page = context.new_page()

    for idx, item in enumerate(websites, start=1):
        filepath = os.path.join(output_dir, item["filename"])
        print(f"\n[{idx}/20] Đang xử lý: {item['name']} ({item['url']})...")
        start_t = time.time()
        
        try:
            page.goto(item["url"], wait_until="domcontentloaded", timeout=40000)
            time.sleep(2)
            
            # Chụp bằng thuật toán chống khoảng trắng và chống lặp header
            w, h = capture_smart_clean(page, filepath)
            elapsed = time.time() - start_t
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            
            # Quét kiểm tra khoảng trắng
            is_blank, blank_msg = check_for_blank_spaces(filepath)
            
            print(f"  -> HOÀN TẤT: {item['filename']} | Kích thước: {w}x{h} | Dung lượng: {size_mb:.2f} MB | {elapsed:.1f}s | Kiểm tra: {blank_msg}")
            audit_results.append({
                "id": item["id"],
                "name": item["name"],
                "file": item["filename"],
                "dims": f"{w}x{h}",
                "size_mb": round(size_mb, 2),
                "blank_check": blank_msg,
                "status": "PASS" if not is_blank else "BLANK_WARNING"
            })
        except Exception as e:
            print(f"  -> LỖI khi chụp {item['name']}: {e}")
            audit_results.append({
                "id": item["id"],
                "name": item["name"],
                "file": item["filename"],
                "dims": "N/A",
                "size_mb": 0,
                "blank_check": str(e),
                "status": "ERROR"
            })

    browser.close()

print("\n=== KẾT QUẢ TỔNG KIỂM TRA 20 WEBSITE ===")
for r in audit_results:
    print(f"[{r['id']}] {r['name']}: {r['dims']} | {r['size_mb']} MB | {r['status']} ({r['blank_check']})")
