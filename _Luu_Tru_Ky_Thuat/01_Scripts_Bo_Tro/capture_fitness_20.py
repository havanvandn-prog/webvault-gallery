# -*- coding: utf-8 -*-
import os
import sys
import time
import json
from io import BytesIO
from PIL import Image

# Ensure UTF-8 output on Windows console
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)
from capture_engine import capture_smart_clean, check_for_blank_spaces, compress_tri_layer, verify_captured_image
from playwright.sync_api import sync_playwright

output_dir = os.path.join(BASE_DIR, "Anh_Chup_Website")
kho_webp_dir = os.path.join(BASE_DIR, "Kho_Anh_Webp")
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "fitness_metadata.json")

os.makedirs(output_dir, exist_ok=True)
os.makedirs(kho_webp_dir, exist_ok=True)
os.makedirs(os.path.dirname(metadata_file), exist_ok=True)

websites = [
    # NHÓM 1: ĐẠI GIA 5 SAO & TỔ HỢP THỂ THAO THƯỢNG LƯU (VIỆT NAM)
    {
        "id": "fit01",
        "name": "California Fitness & Yoga",
        "short_name": "California Fitness",
        "url": "https://cali.vn/",
        "domain": "cali.vn",
        "slug": "cali_vn",
        "industry": "phong-tap-fitness",
        "industry_name": "Phòng Tập Fitness & Gym",
        "category": "Luxury Multi-club Fitness & Wellness",
        "category_vn": "Chuỗi Thể Thao & Wellness 5 Sao Quốc Tế",
        "tag": "luxury-fitness",
        "vibe": "dark-luxury",
        "vibe_name": "Đẳng cấp & 5 Sao Quốc Tế",
        "location": "Toàn quốc",
        "desc": "Thương hiệu thể hình & phong cách sống 5 sao quy mô lớn nhất Việt Nam. Không gian thiết kế sang trọng, hồ bơi, jacuzzi, sauna cùng hệ thống lớp học bản quyền Les Mills và Yoga Master Ấn Độ."
    },
    {
        "id": "fit02",
        "name": "CITIGYM",
        "short_name": "CITIGYM",
        "url": "https://citigym.asia/",
        "domain": "citigym.asia",
        "slug": "citigym_asia",
        "industry": "phong-tap-fitness",
        "industry_name": "Phòng Tập Fitness & Gym",
        "category": "Luxury Green & Lifestyle Fitness",
        "category_vn": "Chuỗi Fitness Không Gian Xanh & Đẳng Cấp",
        "tag": "luxury-fitness",
        "vibe": "modern-green",
        "vibe_name": "Hiện đại & Không gian xanh",
        "location": "TP.HCM & Bình Dương",
        "desc": "Hệ thống phòng tập dẫn đầu xu hướng mang mảng xanh thiên nhiên vào không gian thể hình. Trang thiết bị Technogym & Life Fitness cao cấp, phòng xông hơi tuyết và dịch vụ chuẩn 5 sao."
    },
    {
        "id": "fit03",
        "name": "Elite Fitness",
        "short_name": "Elite Fitness",
        "url": "https://elitefitness.com.vn/",
        "domain": "elitefitness.com.vn",
        "slug": "elitefitness_com_vn",
        "industry": "phong-tap-fitness",
        "industry_name": "Phòng Tập Fitness & Gym",
        "category": "Premium Wellness & Social Club",
        "category_vn": "Câu Lạc Bộ Thể Thao Thượng Lưu Chuẩn Quốc Tế",
        "tag": "luxury-fitness",
        "vibe": "dark-luxury",
        "vibe_name": "Sang trọng & Chuẩn mực thượng lưu",
        "location": "Hà Nội, Quảng Ninh & TP.HCM",
        "desc": "Chuỗi câu lạc bộ thể thao cao cấp hàng đầu dành riêng cho tầng lớp trung và thượng lưu. Nằm tại các tòa nhà đắc địa, tích hợp bể bơi 4 mùa, công nghệ InBody và gói tập luyện đặc quyền."
    },
    {
        "id": "fit04",
        "name": "The A Fitness",
        "short_name": "The A Fitness",
        "url": "https://thea.com.vn/",
        "domain": "thea.com.vn",
        "slug": "thea_com_vn",
        "industry": "phong-tap-fitness",
        "industry_name": "Phòng Tập Fitness & Gym",
        "category": "Eco Wellness & Complex Club",
        "category_vn": "Tổ Hợp Thể Thao & Chăm Sóc Sức Khỏe Sinh Thái",
        "tag": "wellness-fitness",
        "vibe": "clean-white",
        "vibe_name": "Sinh thái & Trị liệu toàn diện",
        "location": "Hà Nội & Ecopark",
        "desc": "Tổ hợp Fitness & Wellness 5 sao quy mô lớn với triết lý chăm sóc sức khỏe toàn diện. Tích hợp Gym, Boxing, Bể bơi bốn mùa, dịch vụ Pilates chuyên sâu và liệu trình giãn cơ phục hồi."
    },
    {
        "id": "fit05",
        "name": "Level Fitness & Yoga",
        "short_name": "Level Fitness",
        "url": "https://levelfyc.com/",
        "domain": "levelfyc.com",
        "slug": "levelfyc_com",
        "industry": "phong-tap-fitness",
        "industry_name": "Phòng Tập Fitness & Gym",
        "category": "High-ceiling Multi-sport Complex",
        "category_vn": "Tổ Hợp Thể Thao Trần Cao & Đa Bộ Môn Thủ Đô",
        "tag": "luxury-fitness",
        "vibe": "dark-luxury",
        "vibe_name": "Trần cao khoáng đạt & Đa năng",
        "location": "Hà Nội",
        "desc": "Tổ hợp thể thao đẳng cấp tại Hà Nội với thiết kế trần kính panoramic view tuyệt đẹp. Kết hợp độc đáo giữa Gym, Yoga, Pilates, sân bóng rổ và tường leo núi trong nhà chuẩn quốc tế."
    },

    # NHÓM 2: CHUỖI TIỆN LỢI 24/7 & ĐẠI CHÚNG HIỆN ĐẠI
    {
        "id": "fit06",
        "name": "The New Gym",
        "short_name": "The New Gym",
        "url": "https://thenewgym.vn/",
        "domain": "thenewgym.vn",
        "slug": "thenewgym_vn",
        "industry": "phong-tap-fitness",
        "industry_name": "Phòng Tập Fitness & Gym",
        "category": "24/7 Budget & Flexible Gym",
        "category_vn": "Chuỗi Phòng Tập 24/7 Tiên Phong Số 1 Việt Nam",
        "tag": "convenience-247",
        "vibe": "vibrant-modern",
        "vibe_name": "Năng động & Mở cửa 24/7",
        "location": "Hà Nội, TP.HCM & Đà Nẵng",
        "desc": "Chuỗi phòng gym mở cửa xuyên suốt 24/7 tiên phong tại Việt Nam. Không gian rộng rãi, chi phí minh bạch linh hoạt không áp lực hợp đồng, hội viên thoải mái tập luyện bất kể ngày đêm."
    },
    {
        "id": "fit07",
        "name": "Anytime Fitness Vietnam",
        "short_name": "Anytime Fitness",
        "url": "https://anytimefitness.vn/",
        "domain": "anytimefitness.vn",
        "slug": "anytimefitness_vn",
        "industry": "phong-tap-fitness",
        "industry_name": "Phòng Tập Fitness & Gym",
        "category": "Global 24/7 Franchise Network",
        "category_vn": "Thương Hiệu Phòng Tập 24/7 Lớn Nhất Thế Giới",
        "tag": "convenience-247",
        "vibe": "clean-white",
        "vibe_name": "Chuẩn hóa toàn cầu & Thân thiện",
        "location": "Hà Nội & TP.HCM",
        "desc": "Chuỗi phòng tập thể hình 24/7 lớn nhất thế giới với hơn 5.000 câu lạc bộ toàn cầu. Một thẻ tập mở khóa mọi phòng tập trên toàn thế giới với hệ thống kiểm soát an toàn tuyệt đối."
    },
    {
        "id": "fit08",
        "name": "Unity Fitness",
        "short_name": "Unity Fitness",
        "url": "https://unityfitness.vn/",
        "domain": "unityfitness.vn",
        "slug": "unityfitness_vn",
        "industry": "phong-tap-fitness",
        "industry_name": "Phòng Tập Fitness & Gym",
        "category": "Modern Multi-discipline Gym",
        "category_vn": "Hệ Thống Gym & Yoga Hiện Đại Trẻ Trung",
        "tag": "modern-fitness",
        "vibe": "vibrant-modern",
        "vibe_name": "Trẻ trung & Tối ưu chuyển đổi",
        "location": "TP.HCM & Hà Nội",
        "desc": "Hệ thống phòng tập thế hệ mới với phong cách thiết kế hiện đại, diện tích rộng lớn, đầy đủ các khu vực Free Weights, Máy khối cơ, phòng tập Yoga ánh sáng dịu và sàn nhảy Group X sôi động."
    },

    # NHÓM 3: CÔNG NGHỆ EMS, VÕ THUẬT & BOUTIQUE FITNESS CHUYÊN SÂU
    {
        "id": "fit09",
        "name": "25 FIT",
        "short_name": "25 FIT",
        "url": "https://25fit.com/",
        "domain": "25fit.com",
        "slug": "25fit_com",
        "industry": "phong-tap-fitness",
        "industry_name": "Phòng Tập Fitness & Gym",
        "category": "High-Tech EMS Training Studio",
        "category_vn": "Tiên Phong Công Nghệ Xung Điện Cơ EMS Training",
        "tag": "high-tech-fitness",
        "vibe": "minimal-tech",
        "vibe_name": "Công nghệ cao & Tối ưu thời gian",
        "location": "Hà Nội, TP.HCM & Đà Nẵng",
        "desc": "Chuỗi phòng tập công nghệ EMS đầu tiên và lớn nhất Việt Nam. Chỉ 25 phút mỗi buổi kích hoạt toàn diện 300+ nhóm cơ sâu, giải pháp hoàn hảo cho doanh nhân và người bận rộn muốn vóc dáng săn chắc."
    },
    {
        "id": "fit10",
        "name": "GymHaus Boutique Fitness",
        "short_name": "GymHaus",
        "url": "https://gymhausvietnam.com/",
        "domain": "gymhausvietnam.com",
        "slug": "gymhausvietnam_com",
        "industry": "phong-tap-fitness",
        "industry_name": "Phòng Tập Fitness & Gym",
        "category": "Boutique Personal Training & Posture",
        "category_vn": "Phòng Tập HLV Cá Nhân & Sửa Tư Thế Khoa Học",
        "tag": "boutique-fitness",
        "vibe": "boutique-warm",
        "vibe_name": "Ấm cúng & Chăm sóc cá nhân hóa",
        "location": "Hà Nội & TP.HCM",
        "desc": "Mô hình Boutique Fitness văn minh, không đông đúc, chuyên biệt về huấn luyện cá nhân 1:1, chỉnh sửa sai lệch tư thế cột sống (gù lưng, võng lưng) và nâng cao thể lực theo khoa học vận động."
    },
    {
        "id": "fit11",
        "name": "Swequity Ultimate Fitness",
        "short_name": "Swequity",
        "url": "https://swequity.vn/",
        "domain": "swequity.vn",
        "slug": "swequity_vn",
        "industry": "phong-tap-fitness",
        "industry_name": "Phòng Tập Fitness & Gym",
        "category": "Evidence-based Strength & Bodybuilding",
        "category_vn": "Thể Hình Khoa Học & Sức Khỏe Chuyển Hóa",
        "tag": "strength-science",
        "vibe": "dark-hardcore",
        "vibe_name": "Mạnh mẽ & Chuẩn khoa học",
        "location": "Hà Nội",
        "desc": "Trung tâm thể hình theo trường phái khoa học vận động và sức khỏe chuyển hóa chuẩn quốc tế. Trang bị dàn tạ Rogue, Eleiko danh tiếng cùng giáo trình đào tạo cá nhân hóa theo từng mục tiêu giải phẫu."
    },
    {
        "id": "fit12",
        "name": "Kickfit Sports",
        "short_name": "Kickfit Sports",
        "url": "https://kickfit-sports.com/",
        "domain": "kickfit-sports.com",
        "slug": "kickfit-sports_com",
        "industry": "phong-tap-fitness",
        "industry_name": "Phòng Tập Fitness & Gym",
        "category": "Martial Arts & Multi-sport Center",
        "category_vn": "Hệ Thống Trung Tâm Võ Thuật & Thể Thao Đa Năng",
        "tag": "martial-arts",
        "vibe": "vibrant-modern",
        "vibe_name": "Rực lửa & Đốt mỡ thần tốc",
        "location": "Hà Nội",
        "desc": "Hệ thống trung tâm thể thao kết hợp võ thuật hàng đầu miền Bắc. Nổi bật với các bộ môn Kickboxing, Muay Thai, Boxing đối kháng giải tỏa stress và giảm cân cấp tốc trong không gian tiêu chuẩn thi đấu."
    },
    {
        "id": "fit13",
        "name": "HD Fitness Đà Nẵng",
        "short_name": "HD Fitness",
        "url": "https://hdfitness.vn/",
        "domain": "hdfitness.vn",
        "slug": "hdfitness_vn",
        "industry": "phong-tap-fitness",
        "industry_name": "Phòng Tập Fitness & Gym",
        "category": "Regional Fitness & Aquatics Leader",
        "category_vn": "Hệ Thống Thể Hình & Bơi Lội Lớn Nhất Miền Trung",
        "tag": "regional-leader",
        "vibe": "modern-blue",
        "vibe_name": "Rộng mở & Quy mô miền Trung",
        "location": "Đà Nẵng & Miền Trung",
        "desc": "Hệ thống tổ hợp thể thao và bơi lội quy mô số 1 tại Đà Nẵng. Không gian rộng hàng ngàn mét vuông, trang bị máy tập hiện đại, bể bơi tiêu chuẩn cùng khu vực xông hơi đá muối thảo dược."
    },
    {
        "id": "fit14",
        "name": "Gym One",
        "short_name": "Gym One",
        "url": "https://gymone.vn/",
        "domain": "gymone.vn",
        "slug": "gymone_vn",
        "industry": "phong-tap-fitness",
        "industry_name": "Phòng Tập Fitness & Gym",
        "category": "Urban Boutique Fitness Center",
        "category_vn": "Trung Tâm Gym & Yoga Đô Thị Năng Động",
        "tag": "urban-fitness",
        "vibe": "vibrant-modern",
        "vibe_name": "Trẻ trung & Năng động trung tâm",
        "location": "TP.HCM",
        "desc": "Không gian rèn luyện thể chất năng động tại trung tâm Sài Gòn. Tích hợp Gym, Yoga, Zumba, Dance và dịch vụ Personal Trainer tận tâm với phong cách thiết kế hiện đại, đầy cảm hứng."
    },
    {
        "id": "fit15",
        "name": "Advance Fitness & Gym",
        "short_name": "Advance Fitness",
        "url": "https://advancegym.com.vn/",
        "domain": "advancegym.com.vn",
        "slug": "advancegym_com_vn",
        "industry": "phong-tap-fitness",
        "industry_name": "Phòng Tập Fitness & Gym",
        "category": "Premium Boutique Fitness Chain",
        "category_vn": "Chuỗi Thể Thao & Chăm Sóc Vóc Dáng Cá Nhân Hóa",
        "tag": "boutique-fitness",
        "vibe": "clean-white",
        "vibe_name": "Tinh tế & Huấn luyện sát sao",
        "location": "TP.HCM",
        "desc": "Chuỗi phòng tập định hướng dịch vụ cá nhân hóa với không gian thoáng mát, số lượng hội viên giới hạn tránh tình trạng chờ máy, dịch vụ PT trực sàn chỉnh form tỉ mỉ và chu đáo."
    },

    # NHÓM 4: PILATES STUDIO CHUYÊN BIỆT
    {
        "id": "fit16",
        "name": "Elite Premium Pilates",
        "short_name": "Elite Pilates",
        "url": "https://elitepilates.vn/",
        "domain": "elitepilates.vn",
        "slug": "elitepilates_vn",
        "industry": "phong-tap-fitness",
        "industry_name": "Phòng Tập Fitness & Gym",
        "category": "Luxury Reformer Pilates Studio",
        "category_vn": "Studio Chuyên Sâu Pilates Reformer Cao Cấp",
        "tag": "pilates-yoga",
        "vibe": "clean-minimal",
        "vibe_name": "Thanh lịch & Thẩm mỹ vóc dáng",
        "location": "Hà Nội & TP.HCM",
        "desc": "Studio chuyên sâu về bộ môn Pilates Reformer chuẩn quốc tế thuộc hệ sinh thái Elite. Không gian thiền định tinh tế, dàn máy Reformer nhập khẩu nguyên chiếc từ Mỹ giúp kéo giãn và định hình đường cong."
    },
    {
        "id": "fit17",
        "name": "Pilates Station",
        "short_name": "Pilates Station",
        "url": "https://pilatesstation.vn/",
        "domain": "pilatesstation.vn",
        "slug": "pilatesstation_vn",
        "industry": "phong-tap-fitness",
        "industry_name": "Phòng Tập Fitness & Gym",
        "category": "Therapeutic Pilates & Core Rehab",
        "category_vn": "Trung Tâm Pilates Trị Liệu & Cải Thiện Vóc Dáng",
        "tag": "pilates-yoga",
        "vibe": "clean-white",
        "vibe_name": "Nhẹ nhàng & Phục hồi chuyên sâu",
        "location": "TP.HCM",
        "desc": "Trung tâm Pilates trị liệu và cải thiện vóc dáng hàng đầu tại khu Nam Sài Gòn. Đội ngũ Master Instructor được chứng nhận quốc tế, giáo trình 1:1 chuyên biệt cho từng tình trạng cột sống và mẹ bầu."
    },

    # NHÓM 5: BIỂU TƯỢNG FITNESS QUỐC TẾ (UI/UX ĐỈNH CAO THẾ GIỚI)
    {
        "id": "fit18",
        "name": "Equinox",
        "short_name": "Equinox",
        "url": "https://www.equinox.com/",
        "domain": "equinox.com",
        "slug": "equinox_com",
        "industry": "phong-tap-fitness",
        "industry_name": "Phòng Tập Fitness & Gym",
        "category": "Global Luxury Lifestyle & Fitness Icon",
        "category_vn": "Biểu Tượng Thể Hình & Phong Cách Sống Siêu Xa Xỉ",
        "tag": "global-benchmarks",
        "vibe": "dark-luxury",
        "vibe_name": "Đẳng cấp tột bậc & Nghệ thuật",
        "location": "New York, Los Angeles, London",
        "desc": "Thương hiệu thể hình xa xỉ số 1 thế giới với triết lý 'It's Not Fitness, It's Life'. Điểm chuẩn mực toàn cầu về thiết kế giao diện tối giản quyền lực, nghệ thuật nhiếp ảnh điện ảnh và trải nghiệm hội viên đẳng cấp VIP."
    },
    {
        "id": "fit19",
        "name": "Third Space London",
        "short_name": "Third Space",
        "url": "https://www.thirdspace.london/",
        "domain": "thirdspace.london",
        "slug": "thirdspace_london",
        "industry": "phong-tap-fitness",
        "industry_name": "Phòng Tập Fitness & Gym",
        "category": "Iconic Luxury Health Club & Architecture",
        "category_vn": "Đỉnh Cao Thiết Kế Kiến Trúc Câu Lạc Bộ Sức Khỏe London",
        "tag": "global-benchmarks",
        "vibe": "dark-luxury",
        "vibe_name": "Kiến trúc tương lai & Sang trọng bậc nhất",
        "location": "London, UK",
        "desc": "Chuỗi câu lạc bộ sức khỏe biểu tượng của thủ đô London. Kiệt tác kiến trúc giao thoa giữa ánh sáng kim loại, hồ bơi lọc ozone tự nhiên, sàn đấu boxing và giao diện số mượt mà như một tạp chí thời trang kiến trúc."
    },
    {
        "id": "fit20",
        "name": "Barry's Bootcamp",
        "short_name": "Barry's",
        "url": "https://www.barrys.com/",
        "domain": "barrys.com",
        "slug": "barrys_com",
        "industry": "phong-tap-fitness",
        "industry_name": "Phòng Tập Fitness & Gym",
        "category": "Global High-Intensity Boutique HIIT Studio",
        "category_vn": "Chuỗi Studio HIIT Đỏ Rực Biểu Tượng Toàn Cầu",
        "tag": "global-benchmarks",
        "vibe": "vibrant-dark",
        "vibe_name": "Red Room bùng nổ & Năng lượng cao",
        "location": "Toàn cầu",
        "desc": "Nhà tiên phong của mô hình tập luyện ngắt quãng cường độ cao (HIIT) với căn phòng ánh sáng đỏ 'Red Room' nổi tiếng. Giao diện trực quan tràn đầy năng lượng, tối ưu luồng đặt lịch tập và trải nghiệm cộng đồng cuồng nhiệt."
    }
]

print(f"=== BẮT ĐẦU CHỤP FULL-PAGE 20 WEBSITE PHÒNG TẬP FITNESS & GYM ===", flush=True)

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
        slug = item["slug"]
        print(f"\n[{idx}/20] ({item['category_vn']}) Đang xử lý: {item['name']} -> {item['url']}...", flush=True)
        start_t = time.time()
        
        success = False
        res_info = (1440, 900)
        
        # Check if already captured recently and valid (> 100KB)
        thumb_name = f"{slug}_thumb.webp"
        full_name = f"{slug}_full.webp"
        fb_name = f"{slug}_fb.png"
        thumb_path = os.path.join(kho_webp_dir, thumb_name)
        full_path = os.path.join(kho_webp_dir, full_name)
        fb_path = os.path.join(kho_webp_dir, fb_name)
        
        if os.path.exists(thumb_path) and os.path.getsize(thumb_path) > 10 * 1024 and os.path.exists(filepath):
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            print(f"  -> File gốc và WebP đã tồn tại: {filename} ({size_mb:.2f} MB), đọc lại thông số...", flush=True)
            thumb_kb = round(os.path.getsize(thumb_path) / 1024, 1)
            full_kb = round(os.path.getsize(full_path) / 1024, 1) if os.path.exists(full_path) else 0
            fb_kb = round(os.path.getsize(fb_path) / 1024, 1) if os.path.exists(fb_path) else 0
            
            # Post-capture audit check
            ok, audit_msg = verify_captured_image(full_path)
            print(f"  -> Kiểm định chất lượng: {'PASS' if ok else 'FAIL'} ({audit_msg})", flush=True)
            
            final_metadata.append({
                **item,
                "image": f"Anh_Chup_Website/{filename}",
                "thumb": f"Kho_Anh_Webp/{thumb_name}",
                "full": f"Kho_Anh_Webp/{full_name}",
                "fb": f"Kho_Anh_Webp/{fb_name}",
                "thumb_kb": thumb_kb,
                "full_kb": full_kb,
                "fb_kb": fb_kb,
                "size_mb": f"{size_mb:.2f} MB",
                "status": "SUCCESS" if ok else "WARN"
            })
            continue

        # Attempt smart clean capture
        try:
            page.goto(item['url'], wait_until="domcontentloaded", timeout=40000)
            time.sleep(2.5)
            res_info = capture_smart_clean(page, filepath)
            is_blank, reason = check_for_blank_spaces(filepath)
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            print(f"  -> Smart Clean thành công: {filename} ({res_info[0]}x{res_info[1]}, {size_mb:.2f} MB, {time.time()-start_t:.1f}s, Blank: {reason})", flush=True)
            success = True
        except Exception as e:
            print(f"  -> Smart Clean gặp lỗi: {e}, chuyển sang Fallback Full-page...", flush=True)
            try:
                page.goto(item['url'], wait_until="load", timeout=35000)
                time.sleep(2.5)
                page.screenshot(path=filepath, full_page=True)
                size_mb = os.path.getsize(filepath) / (1024 * 1024)
                print(f"  -> Fallback Full-page thành công: {filename} ({size_mb:.2f} MB)", flush=True)
                success = True
            except Exception as e2:
                print(f"  -> THẤT BẠI: {e2}", flush=True)

        if success and os.path.exists(filepath):
            thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb = compress_tri_layer(filepath, slug, kho_webp_dir)
            
            # Post-capture audit check
            ok, audit_msg = verify_captured_image(full_path)
            print(f"  -> Đã nén: Thumb {thumb_kb} KB, Full {full_kb} KB, FB {fb_kb} KB | Audit: {audit_msg}", flush=True)
            
            final_metadata.append({
                **item,
                "image": f"Anh_Chup_Website/{filename}",
                "thumb": f"Kho_Anh_Webp/{thumb_name}",
                "full": f"Kho_Anh_Webp/{full_name}",
                "fb": f"Kho_Anh_Webp/{fb_name}",
                "thumb_kb": thumb_kb,
                "full_kb": full_kb,
                "fb_kb": fb_kb,
                "size_mb": f"{os.path.getsize(filepath)/(1024*1024):.2f} MB",
                "status": "SUCCESS" if ok else "WARN"
            })
        else:
            final_metadata.append({
                **item,
                "image": f"Anh_Chup_Website/{filename}",
                "thumb": "",
                "full": "",
                "fb": "",
                "thumb_kb": 0,
                "full_kb": 0,
                "fb_kb": 0,
                "size_mb": "N/A",
                "status": "FAILED"
            })

    browser.close()

with open(metadata_file, "w", encoding="utf-8") as f:
    json.dump(final_metadata, f, ensure_ascii=False, indent=2)

print(f"\n=== HOÀN TẤT CHỤP VÀ NÉN 20 WEBSITE FITNESS! Đã lưu metadata vào {metadata_file} ===", flush=True)
