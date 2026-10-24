import os
import sys
import time
import json

# Ensure UTF-8 output on Windows console
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

from playwright.sync_api import sync_playwright

output_dir = "Anh_Chup_Website"
os.makedirs(output_dir, exist_ok=True)

websites = [
    {"id": "01", "name": "Square Experiential Communications", "short_name": "Square Experiential", "url": "https://square-vn.com/", "category": "Creative & Experiential Agency", "location": "TP.HCM & Toàn quốc"},
    {"id": "02", "name": "Per-fectiv", "short_name": "Per-fectiv", "url": "https://per-fectiv.com/", "category": "Creative Luxury Experiential", "location": "TP.HCM"},
    {"id": "03", "name": "Le Bros", "short_name": "Le Bros", "url": "https://lebros.vn/", "category": "Editorial & Cultural Events", "location": "Hà Nội & TP.HCM"},
    {"id": "04", "name": "BS Group", "short_name": "BS Group", "url": "https://bsgroup.com.vn/", "category": "Bespoke Events & Production", "location": "TP.HCM & Toàn quốc"},
    {"id": "05", "name": "Zeit Media", "short_name": "Zeit Media", "url": "https://zeitmedia.vn/", "category": "Creative & Art Event Agency", "location": "Hà Nội & TP.HCM"},
    {"id": "06", "name": "HoaBinh Events", "short_name": "HoaBinh Events", "url": "https://hoabinhevents.com/", "category": "Top 1 MICE & International Conferences", "location": "Toàn quốc & Quốc tế"},
    {"id": "07", "name": "Á Châu Event", "short_name": "Á Châu Event", "url": "https://sukienachau.com/", "category": "Top 1 SEO Full-Service Events", "location": "Hà Nội & TP.HCM"},
    {"id": "08", "name": "Vietlink Event", "short_name": "Vietlink Event", "url": "https://vietlinkevent.vn/", "category": "Corporate Events & Opening Ceremony", "location": "TP.HCM & Hà Nội"},
    {"id": "09", "name": "Apex Media", "short_name": "Apex Media", "url": "https://apexevent.vn/", "category": "Strategic Brand & High-level Events", "location": "TP.HCM"},
    {"id": "10", "name": "Newday Media", "short_name": "Newday Media", "url": "https://newdaymedia.com.vn/", "category": "Stevie Awards Winner & Cultural Megashow", "location": "Hà Nội & Toàn quốc"},
    {"id": "11", "name": "Cyber Show", "short_name": "Cyber Show", "url": "https://cybershow.vn/", "category": "Gala Dinner, YEP & Teambuilding", "location": "TP.HCM & Miền Nam"},
    {"id": "12", "name": "YesEvents", "short_name": "YesEvents", "url": "https://www.yesevents.vn/", "category": "5-Star Hotels & FDI Corporate Events", "location": "TP.HCM & Phú Quốc"},
    {"id": "13", "name": "CAT Event", "short_name": "CAT Event", "url": "https://cat-event.com.vn/", "category": "Khánh tiết & Sự kiện tập đoàn lớn", "location": "TP.HCM & Toàn quốc"},
    {"id": "14", "name": "Hoàng Sa Việt", "short_name": "Hoàng Sa Việt", "url": "https://hoangsaviet.com/", "category": "Thi công sân khấu, truss & Mega Concert", "location": "TP.HCM, HN, Phú Quốc"},
    {"id": "15", "name": "Đất Việt Event", "short_name": "Đất Việt Event", "url": "https://datvietevent.com/", "category": "Sự kiện kết hợp du lịch doanh nghiệp", "location": "TP.HCM & Toàn quốc"},
    {"id": "16", "name": "Danang Events", "short_name": "Danang Events", "url": "https://danangevents.com.vn/", "category": "Top 1 Sự kiện MICE Miền Trung", "location": "Đà Nẵng & Miền Trung"},
    {"id": "17", "name": "Sea Event", "short_name": "Sea Event", "url": "https://seaevent.vn/", "category": "Sự kiện doanh nghiệp & du lịch biển", "location": "Đà Nẵng & Duyên hải"},
    {"id": "18", "name": "AN Media", "short_name": "AN Media", "url": "https://anmedia.vn/", "category": "Truyền thông tích hợp & KOLs Management", "location": "Hà Nội & Miền Bắc"},
    {"id": "19", "name": "Thăng Long Event", "short_name": "Thăng Long Event", "url": "https://thanglongevent.com/", "category": "Lễ kỷ niệm & Sự kiện trang trọng", "location": "Hà Nội & Toàn quốc"},
    {"id": "20", "name": "AzEvent", "short_name": "AzEvent", "url": "https://azevent.vn/", "category": "Hội nghị khách hàng & Khai trương trọn gói", "location": "Hà Nội & Miền Bắc"}
]

def auto_scroll(page):
    try:
        total_height = page.evaluate("() => Math.max(document.body.scrollHeight, document.documentElement.scrollHeight, 1000)")
        max_scroll = min(total_height, 20000)
        current_scroll = 0
        step = 900
        while current_scroll < max_scroll:
            current_scroll += step
            page.evaluate(f"window.scrollTo(0, {current_scroll});")
            time.sleep(0.25)
        # Scroll back up to ensure sticky headers / hero elements look right
        page.evaluate("window.scrollTo(0, 0);")
        time.sleep(0.6)
    except Exception as e:
        print(f"  [AutoScroll Warning] {e}")

results = []

print("=== STARTING SCREENSHOT CAPTURE FOR 20 WEBSITES ===")
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
        filename = f"{item['id']}_{item['short_name'].replace(' ', '_').replace('-', '_')}.png"
        filepath = os.path.join(output_dir, filename)
        
        print(f"[{idx}/20] Chụp: {item['name']} ({item['url']})...")
        start_time = time.time()
        success = False
        error_msg = ""
        size_kb = 0
        
        # Try loading with fallback
        for wait_strategy in ["domcontentloaded", "load"]:
            try:
                page.goto(item['url'], wait_until=wait_strategy, timeout=35000)
                time.sleep(2)
                auto_scroll(page)
                page.screenshot(path=filepath, full_page=True)
                size_kb = os.path.getsize(filepath) / 1024
                success = True
                print(f"  -> THÀNH CÔNG: {filename} ({size_kb:.1f} KB, mất {time.time()-start_time:.1f}s)")
                break
            except Exception as e:
                error_msg = str(e)
                print(f"  -> Thử lại {item['short_name']} với chế độ khác... (Lỗi: {e})")
                time.sleep(1)
                
        if not success:
            # Fallback viewport only
            try:
                print(f"  -> Thử chế độ Fallback Viewport...")
                page.goto(item['url'], timeout=30000)
                time.sleep(2)
                page.screenshot(path=filepath, full_page=False)
                size_kb = os.path.getsize(filepath) / 1024
                success = True
                print(f"  -> THÀNH CÔNG (Viewport): {filename} ({size_kb:.1f} KB)")
            except Exception as e:
                print(f"  -> THẤT BẠI: {item['name']} ({e})")
                
        results.append({
            "id": item["id"],
            "name": item["name"],
            "short_name": item["short_name"],
            "url": item["url"],
            "category": item["category"],
            "location": item["location"],
            "filename": filename,
            "filepath": filepath.replace("\\", "/"),
            "success": success,
            "size_kb": round(size_kb, 1),
            "error": error_msg if not success else ""
        })

    browser.close()

# Save metadata json into _Luu_Tru_Ky_Thuat/03_Du_Lieu_Tam_Va_Test
data_dir = "_Luu_Tru_Ky_Thuat/03_Du_Lieu_Tam_Va_Test"
os.makedirs(data_dir, exist_ok=True)
with open(os.path.join(data_dir, "screenshots_metadata.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\n=== HOÀN TẤT CHỤP MÀN HÌNH 20 WEBSITE ===")
print(f"Tổng số thành công: {sum(1 for r in results if r['success'])}/{len(websites)}")
