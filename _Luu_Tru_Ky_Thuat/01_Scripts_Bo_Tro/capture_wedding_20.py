import os
import sys
import time
import json

# Ensure UTF-8 output on Windows console
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)
from capture_engine import capture_smart_clean, check_for_blank_spaces
from playwright.sync_api import sync_playwright

output_dir = "Anh_Chup_Website"
os.makedirs(output_dir, exist_ok=True)
metadata_file = r"_Luu_Tru_Ky_Thuat\03_Du_Lieu_Tam_Va_Test\wedding_metadata.json"
os.makedirs(os.path.dirname(metadata_file), exist_ok=True)

websites = [
    # NHÓM 1: WEDDING PLANNER & TRANG TRÍ TIỆC CƯỚI CAO CẤP
    {
        "id": "w01",
        "name": "The Planners",
        "domain": "theplannersvn.com",
        "url": "https://theplannersvn.com/",
        "category": "Wedding Planner & Decor",
        "category_vn": "Wedding Planner & Trang Trí",
        "vibe": "Luxury & Bespoke",
        "location": "Hà Nội, Đà Nẵng & TP.HCM",
        "desc": "Đơn vị Wedding Planner tiên phong hàng đầu Việt Nam. Chuyên tổ chức tiệc cưới độc bản, cá nhân hóa và Destination Wedding tại các resort 5 sao quốc tế."
    },
    {
        "id": "w02",
        "name": "Meraki Wedding Planner",
        "domain": "merakiweddingplanner.com",
        "url": "https://merakiweddingplanner.com/",
        "category": "Wedding Planner & Decor",
        "category_vn": "Wedding Planner & Trang Trí",
        "vibe": "Poetic & Outdoor",
        "location": "TP.HCM & Miền Trung",
        "desc": "Phong cách lãng mạn, nên thơ và ngập tràn cảm xúc. Chuyên gia tiệc cưới ngoài trời, bãi biển và concept nghệ thuật độc đáo tôn vinh tình yêu."
    },
    {
        "id": "w03",
        "name": "K.I.S.S Wedding Planner",
        "domain": "kisswe.com",
        "url": "https://kisswe.com/",
        "category": "Wedding Planner & Decor",
        "category_vn": "Wedding Planner & Trang Trí",
        "vibe": "Storytelling & Intimate",
        "location": "TP.HCM",
        "desc": "Định hướng 'Keep It Special Story', tập trung sâu vào câu chuyện tình yêu của từng cặp đôi để kiến tạo không gian cưới ấm cúng, tinh tế."
    },
    {
        "id": "w04",
        "name": "VOAN Wedding & Event",
        "domain": "voan.vn",
        "url": "https://voan.vn/",
        "category": "Wedding Planner & Decor",
        "category_vn": "Wedding Planner & Trang Trí",
        "vibe": "Luxury Ballroom",
        "location": "Hà Nội & Miền Bắc",
        "desc": "Thương hiệu trang trí và tổ chức tiệc cưới kỳ cựu tại Hà Nội. Đối tác chiến lược tại các khách sạn 5 sao lớn (JW Marriott, InterContinental, Daewoo)."
    },
    {
        "id": "w05",
        "name": "TIFF Wedding Planner",
        "domain": "tiff.vn",
        "url": "https://tiff.vn/",
        "category": "Wedding Planner & Decor",
        "category_vn": "Wedding Planner & Trang Trí",
        "vibe": "Modern Elegance",
        "location": "TP.HCM & Hà Nội",
        "desc": "Chuyên sâu lập kế hoạch và điều phối tiệc cưới cao cấp (Luxury Wedding), phong cách hiện đại, chỉn chu đến từng chi tiết nhỏ."
    },

    # NHÓM 2: TRUNG TÂM HỘI NGHỊ & NHÀ HÀNG TIỆC CƯỚI SANG TRỌNG
    {
        "id": "w06",
        "name": "White Palace",
        "domain": "whitepalace.com.vn",
        "url": "https://whitepalace.com.vn/",
        "category": "Convention & Wedding Venue",
        "category_vn": "Trung Tâm Tiệc Cưới & Yến Tiệc",
        "vibe": "Architectural Luxury",
        "location": "TP.HCM",
        "desc": "Biểu tượng trung tâm sự kiện và tiệc cưới đẳng cấp quốc tế tại TP.HCM. Kiến trúc mái vòm tráng lệ, không gian yến tiệc hoàng gia."
    },
    {
        "id": "w07",
        "name": "Capella Gallery Hall",
        "domain": "capellagallery.com",
        "url": "https://capellagallery.com/",
        "category": "Convention & Wedding Venue",
        "category_vn": "Trung Tâm Tiệc Cưới & Yến Tiệc",
        "vibe": "Contemporary Chic",
        "location": "TP.HCM",
        "desc": "Không gian yến tiệc đương đại tọa lạc tại trung tâm Quận 10. Sự kết hợp tinh tế giữa ánh sáng nghệ thuật và dịch vụ cưới chuyên nghiệp."
    },
    {
        "id": "w08",
        "name": "Riverside Palace",
        "domain": "riversidepalace.vn",
        "url": "https://riversidepalace.vn/",
        "category": "Convention & Wedding Venue",
        "category_vn": "Trung Tâm Tiệc Cưới & Yến Tiệc",
        "vibe": "European Romance",
        "location": "TP.HCM",
        "desc": "Trung tâm hội nghị tiệc cưới ven sông Bến Vân Đồn mang phong cách tân cổ điển Châu Âu thanh lịch, lãng mạn."
    },
    {
        "id": "w09",
        "name": "Asiana Plaza",
        "domain": "asiana-plaza.com",
        "url": "https://asiana-plaza.com/",
        "category": "Convention & Wedding Venue",
        "category_vn": "Trung Tâm Tiệc Cưới & Yến Tiệc",
        "vibe": "Royal Neoclassical",
        "location": "TP.HCM",
        "desc": "Cung điện yến tiệc tráng lệ với kiến trúc chiết trung vương giả, ẩm thực phong phú và hệ thống âm thanh ánh sáng hiện đại."
    },
    {
        "id": "w10",
        "name": "Trống Đồng Palace",
        "domain": "trongdongpalace.com",
        "url": "https://trongdongpalace.com/",
        "category": "Convention & Wedding Venue",
        "category_vn": "Trung Tâm Tiệc Cưới & Yến Tiệc",
        "vibe": "Grand Scale & SEO Leader",
        "location": "Hà Nội & Miền Bắc",
        "desc": "Chuỗi trung tâm tiệc cưới và sự kiện quy mô lớn nhất miền Bắc với hơn 12 chi nhánh sang trọng tại Hà Nội và các tỉnh lân cận."
    },

    # NHÓM 3: STUDIO CHỤP ẢNH CƯỚI & VÁY CƯỚI THIẾT KẾ
    {
        "id": "w11",
        "name": "TuArt Wedding",
        "domain": "tuarts.net",
        "url": "https://tuarts.net/",
        "category": "Bridal Studio & Dress",
        "category_vn": "Studio Ảnh Cưới & Váy Cưới",
        "vibe": "Comprehensive Ecosystem",
        "location": "Toàn quốc",
        "desc": "Hệ sinh thái cưới all-in-one lớn nhất Việt Nam: Studio ảnh cưới, học viện đào tạo, xưởng váy cưới Bella Bridal và phim trường độc quyền."
    },
    {
        "id": "w12",
        "name": "Nupakachi Wedding",
        "domain": "nupakachi.com",
        "url": "https://nupakachi.com/",
        "category": "Bridal Studio & Dress",
        "category_vn": "Studio Ảnh Cưới & Váy Cưới",
        "vibe": "European Art Photography",
        "location": "Hà Nội, TP.HCM & Đà Nẵng",
        "desc": "Nổi tiếng với những bộ ảnh pre-wedding phong cách Châu Âu phóng khoáng, nghệ thuật; có chi nhánh tại cả Việt Nam và nước ngoài (Pháp, Singapore)."
    },
    {
        "id": "w13",
        "name": "Rin Wedding",
        "domain": "rinwedding.vn",
        "url": "https://rinwedding.vn/",
        "category": "Bridal Studio & Dress",
        "category_vn": "Studio Ảnh Cưới & Váy Cưới",
        "vibe": "Korean Sweet & Fresh",
        "location": "TP.HCM, Đà Nẵng, Đà Lạt",
        "desc": "Studio ảnh cưới được giới trẻ yêu thích hàng đầu với phong cách trong trẻo Hàn Quốc, bắt trọn từng khoảnh khắc cảm xúc tự nhiên."
    },
    {
        "id": "w14",
        "name": "Nicole Bridal",
        "domain": "nicolebridal.vn",
        "url": "https://nicolebridal.vn/",
        "category": "Bridal Studio & Dress",
        "category_vn": "Studio Ảnh Cưới & Váy Cưới",
        "vibe": "Minimalist & Timeless",
        "location": "TP.HCM & Hà Nội",
        "desc": "Thương hiệu may đo và thiết kế váy cưới tối giản phong cách Châu Âu (Minimalist/Boho), form dáng tinh xảo tôn vinh vẻ đẹp tự nhiên của cô dâu."
    },
    {
        "id": "w15",
        "name": "Linh Nga Bridal",
        "domain": "linhnga.vn",
        "url": "https://linhnga.vn/",
        "category": "Bridal Studio & Dress",
        "category_vn": "Studio Ảnh Cưới & Váy Cưới",
        "vibe": "Haute Couture & Celebrity",
        "location": "Hà Nội & TP.HCM",
        "desc": "Thương hiệu váy cưới thiết kế cao cấp (Haute Couture) được các ngôi sao, người nổi tiếng và dâu hào môn tin tưởng lựa chọn."
    },

    # NHÓM 4: NỀN TẢNG TẠO WEBSITE CƯỚI & THIỆP CƯỚI ONLINE
    {
        "id": "w16",
        "name": "Biihappy (iWedding)",
        "domain": "biihappy.com",
        "url": "https://biihappy.com/",
        "category": "Digital Invitation & Platform",
        "category_vn": "Nền Tảng Website Cưới & Thiệp Online",
        "vibe": "Tech & Interactive Platform",
        "location": "Toàn quốc",
        "desc": "Nền tảng tạo website đám cưới & thiệp cưới online hàng đầu Việt Nam. Tích hợp album ảnh, video, RSVP xác nhận khách mời và QR mừng cưới thông minh."
    },
    {
        "id": "w17",
        "name": "ZenLove",
        "domain": "zenlove.me",
        "url": "https://zenlove.me/",
        "category": "Digital Invitation & Platform",
        "category_vn": "Nền Tảng Website Cưới & Thiệp Online",
        "vibe": "Modern Digital Invitation",
        "location": "Toàn quốc",
        "desc": "Nền tảng tạo thiệp cưới online và website đám cưới nhanh chóng, giao diện hiện đại tối ưu trên mobile, cá nhân hóa tên khách mời."
    },
    {
        "id": "w18",
        "name": "Chung Đôi",
        "domain": "chungdoi.com",
        "url": "https://chungdoi.com/",
        "category": "Digital Invitation & Platform",
        "category_vn": "Nền Tảng Website Cưới & Thiệp Online",
        "vibe": "Cultural & Neo-Traditional",
        "location": "Toàn quốc",
        "desc": "Dịch vụ thiệp cưới online và website cưới mang đậm nét đẹp văn hóa truyền thống kết hợp giao diện số hiện đại, chia sẻ dễ dàng qua Zalo."
    },
    {
        "id": "w19",
        "name": "Trao Thiệp",
        "domain": "traothiep.vn",
        "url": "https://traothiep.vn/",
        "category": "Digital Invitation & Platform",
        "category_vn": "Nền Tảng Website Cưới & Thiệp Online",
        "vibe": "Smart Invitation & RSVP",
        "location": "Toàn quốc",
        "desc": "Nền tảng gửi thiệp điện tử tiện lợi, theo dõi trạng thái phản hồi RSVP thời gian thực và quản trị danh sách khách mời thông minh."
    },
    {
        "id": "w20",
        "name": "CineLove",
        "domain": "cinelove.me",
        "url": "https://cinelove.me/",
        "category": "Digital Invitation & Platform",
        "category_vn": "Nền Tảng Website Cưới & Thiệp Online",
        "vibe": "Cinematic Storytelling",
        "location": "Toàn quốc",
        "desc": "Nền tảng thiệp cưới trực tuyến với trải nghiệm thị giác điện ảnh (cinematic), âm nhạc du dương và hiệu ứng chuyển động cảm xúc."
    }
]

print(f"=== BẮT ĐẦU CHỤP FULL-PAGE 20 WEBSITE NGÀNH WEDDING ===", flush=True)

final_metadata = []

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
        filename = f"{item['domain']}.png"
        filepath = os.path.join(output_dir, filename)
        print(f"\n[{idx}/20] ({item['category_vn']}) Đang xử lý: {item['name']} -> {item['url']}...", flush=True)
        start_t = time.time()
        
        # Check if already captured recently and valid
        if os.path.exists(filepath) and os.path.getsize(filepath) > 500 * 1024 and item['domain'] == 'theplannersvn.com':
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            print(f"  -> File đã tồn tại: {filename} ({size_mb:.2f} MB), bỏ qua chụp lại.", flush=True)
            final_metadata.append({
                **item,
                "image": f"Anh_Chup_Website/{filename}",
                "size_mb": f"{size_mb:.2f} MB",
                "status": "SUCCESS"
            })
            continue

        success = False
        res_info = (1440, 900)
        
        # Attempt smart clean capture
        try:
            page.goto(item['url'], wait_until="domcontentloaded", timeout=40000)
            time.sleep(2)
            res_info = capture_smart_clean(page, filepath)
            is_blank, reason = check_for_blank_spaces(filepath)
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            print(f"  -> THÀNH CÔNG: {filename} ({res_info[0]}x{res_info[1]}, {size_mb:.2f} MB, {time.time()-start_t:.1f}s, Blank: {reason})", flush=True)
            success = True
        except Exception as e:
            print(f"  -> Smart Clean gặp lỗi: {e}, chuyển sang Full-Page dự phòng...", flush=True)
            try:
                page.goto(item['url'], wait_until="load", timeout=30000)
                time.sleep(2)
                page.screenshot(path=filepath, full_page=True)
                size_mb = os.path.getsize(filepath) / (1024 * 1024)
                print(f"  -> Fallback Full-page thành công: {filename} ({size_mb:.2f} MB)", flush=True)
                success = True
            except Exception as e2:
                print(f"  -> THẤT BẠI: {e2}", flush=True)

        if success:
            final_metadata.append({
                **item,
                "image": f"Anh_Chup_Website/{filename}",
                "size_mb": f"{size_mb:.2f} MB",
                "status": "SUCCESS"
            })
        else:
            final_metadata.append({
                **item,
                "image": f"Anh_Chup_Website/{filename}",
                "size_mb": "N/A",
                "status": "FAILED"
            })

    browser.close()

with open(metadata_file, "w", encoding="utf-8") as f:
    json.dump(final_metadata, f, ensure_ascii=False, indent=2)

print(f"\n=== HOÀN TẤT CHỤP 20 WEBSITE WEDDING! Đã lưu metadata vào {metadata_file} ===", flush=True)
