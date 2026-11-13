# -*- coding: utf-8 -*-
import os
import sys
import time
import json

# Ensure UTF-8 output on Windows console
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)
from capture_engine import capture_smart_clean, compress_tri_layer, verify_captured_image
from playwright.sync_api import sync_playwright

output_dir = os.path.join(BASE_DIR, "Anh_Chup_Website")
kho_webp_dir = os.path.join(BASE_DIR, "Kho_Anh_Webp")
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "phong_kham_thu_y_metadata.json")

os.makedirs(output_dir, exist_ok=True)
os.makedirs(kho_webp_dir, exist_ok=True)
os.makedirs(os.path.dirname(metadata_file), exist_ok=True)

websites = [
    # NHÓM 1: BỆNH VIỆN & CHUỖI THÚ Y CÔNG NGHỆ CAO QUỐC TẾ
    {
        "id": "vet01",
        "name": "Bond Vet — Chuỗi Phòng Khám Thú Y Công Nghệ Cao Hàng Đầu Mỹ",
        "short_name": "Bond Vet (USA)",
        "url": "https://bondvet.com/",
        "domain": "bondvet.com",
        "slug": "phong_kham_thu_y_bond_vet",
        "industry": "phong-kham-thu-y",
        "industry_name": "Phòng Khám & Bệnh Viện Thú Y",
        "category": "Modern Tech-Enabled Vet Clinic",
        "category_vn": "Chuỗi Thú Y Công Nghệ Cao • Khám Định Kỳ & Cấp Cứu 24/7",
        "tag": "tech-vet-chain",
        "vibe": "Hiện Đại • Đặt Lịch Online 3 Bước • Không Gian Ấm Áp Giảm Stress",
        "location": "New York, Boston, Chicago (Mỹ)",
        "desc": "Thương hiệu thú y công nghệ cao hàng đầu tại Mỹ với hơn 50 cơ sở. Giao diện trực quan cho phép đặt lịch hẹn trong 30 giây, minh bạch dịch vụ khám định kỳ lẫn cấp cứu khẩn cấp, thiết kế lấy cảm hứng từ không gian phòng khám giảm âu lo cho thú cưng (Fear-Free)."
    },
    {
        "id": "vet02",
        "name": "Small Door Veterinary — Chuỗi Thú Y Phong Cách Hội Viên Cao Cấp",
        "short_name": "Small Door Vet",
        "url": "https://www.smalldoorvet.com/",
        "domain": "smalldoorvet.com",
        "slug": "phong_kham_thu_y_small_door",
        "industry": "phong-kham-thu-y",
        "industry_name": "Phòng Khám & Bệnh Viện Thú Y",
        "category": "Membership Boutique Veterinary Care",
        "category_vn": "Mô Hình Chăm Sóc Thú Y Theo Gói Thành Viên Cao Cấp",
        "tag": "boutique-vet",
        "vibe": "Chuẩn Lifestyle Hiện Đại • Minh Bạch Chi Phí • Tư Vấn 24/7 Qua App",
        "location": "New York, Washington DC, Boston (Mỹ)",
        "desc": "Được đánh giá là một trong những website thú y có UI/UX xuất sắc nhất thế giới. Tái định nghĩa ngành thú y thành dịch vụ chăm sóc sức khỏe boutique: giao diện tone màu ấm, bảng giá hội viên rõ ràng, tích hợp ứng dụng chat trực tiếp với bác sĩ thú y."
    },
    {
        "id": "vet03",
        "name": "Modern Animal — Kỳ Lân Thú Y Thế Hệ Mới Giao Diện Mobile-First",
        "short_name": "Modern Animal",
        "url": "https://www.modernanimal.com/",
        "domain": "modernanimal.com",
        "slug": "phong_kham_thu_y_modern_animal",
        "industry": "phong-kham-thu-y",
        "industry_name": "Phòng Khám & Bệnh Viện Thú Y",
        "category": "Next-Gen Tech Veterinary Platform",
        "category_vn": "Nền Tảng Thú Y Công Nghệ Trải Nghiệm Mượt Mà",
        "tag": "mobile-first-vet",
        "vibe": "Gam Màu Pastel Tinh Tế • Trải Nghiệm Mượt Như Sản Phẩm Apple",
        "location": "California, Texas (Mỹ)",
        "desc": "Startup kỳ lân thú y tại Mỹ mang đến trải nghiệm khám chữa bệnh liền mạch giữa ứng dụng điện thoại và phòng khám thực tế. Giao diện tối giản, hình ảnh chân thực, bảng điều hướng thông minh tạo cảm giác thân thuộc cho chủ thú cưng."
    },
    {
        "id": "vet04",
        "name": "Sploot Veterinary Care — Chuỗi Phòng Khám Thú Y Mở Cửa 365 Ngày",
        "short_name": "Sploot Vets",
        "url": "https://www.splootvets.com/",
        "domain": "splootvets.com",
        "slug": "phong_kham_thu_y_sploot_vets",
        "industry": "phong-kham-thu-y",
        "industry_name": "Phòng Khám & Bệnh Viện Thú Y",
        "category": "Modern Primary & Urgent Vet Care",
        "category_vn": "Khám Định Kỳ & Cấp Cứu Mở Cửa 10h-22h Cả Năm",
        "tag": "urgent-primary-care",
        "vibe": "Màu Sắc Trẻ Trung Năng Động • Đặt Lịch Trong Ngày Nhanh Chóng",
        "location": "Denver, Chicago (Mỹ)",
        "desc": "Mô hình phòng khám kết hợp giữa chăm sóc thường nhật và xử lý ca khẩn cấp không cần chờ đợi. Thiết kế web sử dụng typography đậm nét, đồ họa hiện đại, nổi bật cam kết mở cửa từ 10h sáng tới 10h tối tất cả các ngày trong năm."
    },
    {
        "id": "vet05",
        "name": "GoodVets — Mạng Lưới Bệnh Viện Thú Y Hiện Đại Sang Trọng",
        "short_name": "GoodVets",
        "url": "https://www.goodvets.com/",
        "domain": "goodvets.com",
        "slug": "phong_kham_thu_y_goodvets",
        "industry": "phong-kham-thu-y",
        "industry_name": "Phòng Khám & Bệnh Viện Thú Y",
        "category": "Hospital Network & Elevate Pet Care",
        "category_vn": "Mạng Lưới Bệnh Viện Thú Y Tiêu Chuẩn Cao Đô Thị",
        "tag": "hospital-network",
        "vibe": "Kiến Trúc Tối Giản • Phân Chuỗi Địa Điểm Khoa Học • Tỷ Lệ Chuyển Đổi Cao",
        "location": "Toàn quốc (Mỹ)",
        "desc": "Chuỗi bệnh viện thú y định vị phân khúc cao cấp tại các trung tâm thành phố lớn. Thiết kế website với bố cục lưới sắc sảo, công cụ tìm kiếm chi nhánh theo bang/thành phố và bảng phân tích chi tiết dịch vụ chẩn đoán, phẫu thuật, phòng ngừa."
    },
    {
        "id": "vet06",
        "name": "Modern Love Veterinary — Phòng Khám Thú Y Thấu Cảm & Tối Giản",
        "short_name": "Modern Love Vet",
        "url": "https://www.modernlovevet.com/",
        "domain": "modernlovevet.com",
        "slug": "phong_kham_thu_y_modern_love",
        "industry": "phong-kham-thu-y",
        "industry_name": "Phòng Khám & Bệnh Viện Thú Y",
        "category": "Empathetic Boutique Animal Clinic",
        "category_vn": "Phòng Khám Thú Y Tối Giản Giảm Thiểu Căng Thẳng",
        "tag": "empathetic-vet",
        "vibe": "Nhẹ Nhàng Thấu Cảm • Phù Hợp Trải Nghiệm Mobile • CTA Đặt Hẹn Nổi Bật",
        "location": "Bắc Mỹ",
        "desc": "Được cộng đồng thiết kế UI/UX khen ngợi nhờ văn phong ấm áp, typography tròn trịa và sự tối giản trong từng section. Giúp người nuôi thú cưng lập tức tìm thấy số hotline cấp cứu và nút đặt hẹn chỉ với một thao tác chạm ngón tay."
    },
    {
        "id": "vet07",
        "name": "VEG — Bệnh Viện Cấp Cứu Thú Y Khẩn Cấp 24/7 Toàn Nước Mỹ",
        "short_name": "VEG 24/7 Emergency",
        "url": "https://veterinaryemergencygroup.com/",
        "domain": "veterinaryemergencygroup.com",
        "slug": "phong_kham_thu_y_veg_emergency",
        "industry": "phong-kham-thu-y",
        "industry_name": "Phòng Khám & Bệnh Viện Thú Y",
        "category": "24/7 Emergency Pet Hospital",
        "category_vn": "Bệnh Viện Cấp Cứu Thú Cưng Khẩn Cấp 24/7 Chuyên Sâu",
        "tag": "emergency-247",
        "vibe": "Nổi Bật Khẩn Cấp • Bác Sĩ Đồng Hành Trực Tiếp • Cứu Trợ Tức Thì",
        "location": "Hơn 50 Bệnh Viện Khắp Nước Mỹ",
        "desc": "Bệnh viện cấp cứu thú y danh tiếng với triết lý đột phá: cho phép chủ nhân đồng hành cùng thú cưng trong suốt quá trình thăm khám và phẫu thuật. Website thiết kế với thanh điều hướng khẩn cấp đỏ nổi bật, bản đồ bệnh viện trực tiếp và gọi cấp cứu tức thì."
    },
    {
        "id": "vet08",
        "name": "CityVet — Hệ Thống Chăm Sóc Sức Khỏe & Làm Đẹp Thú Cưng Toàn Diện",
        "short_name": "CityVet",
        "url": "https://www.cityvet.com/",
        "domain": "cityvet.com",
        "slug": "phong_kham_thu_y_cityvet",
        "industry": "phong-kham-thu-y",
        "industry_name": "Phòng Khám & Bệnh Viện Thú Y",
        "category": "Comprehensive Pet Care & Veterinary",
        "category_vn": "Hệ Sinh Thái Thú Y, Spa Grooming & Khách Sạn Thú Cưng",
        "tag": "full-service-vet",
        "vibe": "Toàn Diện Dịch Vụ • Đăng Ký Gói Tiết Kiệm CityVet Care • Giao Diện Thân Thiện",
        "location": "Texas, Colorado, Georgia (Mỹ)",
        "desc": "Mô hình kết hợp phòng khám thú y tiêu chuẩn y khoa cao với dịch vụ spa làm đẹp và lưu trú thú cưng. Website thể hiện hoàn hảo giải pháp All-In-One, tích hợp chương trình thẻ thành viên chăm sóc sức khỏe dự phòng trọn gói."
    },
    {
        "id": "vet09",
        "name": "Urban Animal — Phòng Khám Thú Y Phục Vụ Khám Tức Thì (Walk-in Vet)",
        "short_name": "Urban Animal",
        "url": "https://www.urbananimalnw.com/",
        "domain": "urbananimalnw.com",
        "slug": "phong_kham_thu_y_urban_animal",
        "industry": "phong-kham-thu-y",
        "industry_name": "Phòng Khám & Bệnh Viện Thú Y",
        "category": "Walk-In Veterinary Care",
        "category_vn": "Phòng Khám Thú Y Không Cần Hẹn Trước Phong Cách Cá Tính",
        "tag": "walk-in-vet",
        "vibe": "Đậm Chất Nghệ Thuật Đô Thị • Cập Nhật Thời Gian Chờ Trực Tuyến",
        "location": "Seattle, Washington (Mỹ)",
        "desc": "Phòng khám thú y độc đáo với tôn chỉ phục vụ cộng đồng không cần đặt hẹn trước. Thiết kế website cá tính, hiển thị bảng thời gian chờ khám theo thời gian thực (Wait Time Tracker) giúp khách hàng linh hoạt sắp xếp thời gian."
    },
    {
        "id": "vet10",
        "name": "Lincoln Hills Veterinary Hospital — Bệnh Viện Thú Y Đạt Giải Thưởng Thiết Kế",
        "short_name": "Lincoln Hills Vet",
        "url": "https://lincolnhillsvet.com/",
        "domain": "lincolnhillsvet.com",
        "slug": "phong_kham_thu_y_lincoln_hills",
        "industry": "phong-kham-thu-y",
        "industry_name": "Phòng Khám & Bệnh Viện Thú Y",
        "category": "Award-Winning Veterinary Hospital Design",
        "category_vn": "Website Bệnh Viện Thú Y Đoạt Giải Thưởng Thiết Kế Quốc Tế",
        "tag": "award-winning-vet",
        "vibe": "Hình Ảnh Chân Thực • Video Background Chiều Sâu • Bố Cục Thân Thiện",
        "location": "Lincoln, California (Mỹ)",
        "desc": "Website mẫu đạt giải thưởng thiết kế ngành thú y tại Mỹ nhờ sự kết hợp hài hòa giữa video clip chân thực về đội ngũ y tế, palette màu dịu mát và cách bố trí các nhóm dịch vụ chẩn đoán hình ảnh, nha khoa thú y khoa học."
    },

    # NHÓM 2: HỆ THỐNG BỆNH VIỆN & PHÒNG KHÁM THÚ Y HÀNG ĐẦU VIỆT NAM
    {
        "id": "vet11",
        "name": "Bệnh Viện Thú Y PetHealth — Hệ Thống Bệnh Viện Thú Y Lớn Nhất Miền Bắc",
        "short_name": "PetHealth Hà Nội",
        "url": "https://pethealth.vn/",
        "domain": "pethealth.vn",
        "slug": "phong_kham_thu_y_pethealth",
        "industry": "phong-kham-thu-y",
        "industry_name": "Phòng Khám & Bệnh Viện Thú Y",
        "category": "Large-Scale Veterinary Hospital Chain",
        "category_vn": "Hệ Thống Bệnh Viện Thú Y Quy Mô Lớn Đa Chi Nhánh Miền Bắc",
        "tag": "vietnam-chain-hospital",
        "vibe": "Uy Tín Lâu Năm • Cấp Cứu 24/7 • Đầy Đủ Chuyên Khoa Phẫu Thuật & Xét Nghiệm",
        "location": "Hà Nội & Các Tỉnh Phía Bắc",
        "desc": "Hệ thống bệnh viện thú y uy tín lâu năm tại Hà Nội với mạng lưới cơ sở rộng khắp. Website chuẩn SEO hàng đầu, cung cấp bảng dịch vụ khám chữa bệnh toàn diện, phẫu thuật ngoại khoa phức tạp, cấp cứu 24/7 và khách sạn thú cưng."
    },
    {
        "id": "vet12",
        "name": "Bệnh Viện Thú Y PetCare — Tiêu Chuẩn Y Khoa Thú Y Hàng Đầu TP.HCM",
        "short_name": "PetCare TP.HCM",
        "url": "https://petcare.vn/",
        "domain": "petcare.vn",
        "slug": "phong_kham_thu_y_petcare_vn",
        "industry": "phong-kham-thu-y",
        "industry_name": "Phòng Khám & Bệnh Viện Thú Y",
        "category": "International Standard Vet Hospital",
        "category_vn": "Hệ Thống Bệnh Viện Thú Y Quốc Tế Lâu Đời Tại TP.HCM & Vũng Tàu",
        "tag": "premium-vet-vn",
        "vibe": "Chẩn Đoán Hình Ảnh Chuyên Sâu • Đội Ngũ Bác Sĩ Đầu Ngành • Bố Cục Chuyên Nghiệp",
        "location": "TP. Hồ Chí Minh & Bà Rịa - Vũng Tàu",
        "desc": "Thành lập từ năm 2005 bởi Tiến sĩ Huỳnh Thị Thanh Ngọc, PetCare là chuẩn mực về điều trị thú y tại TP.HCM. Website trình bày rõ ràng trang thiết bị siêu âm màu, X-quang kỹ thuật số, phẫu thuật nội soi và dịch vụ chăm sóc thú cưng cao cấp."
    },
    {
        "id": "vet13",
        "name": "Hệ Thống Thú Y 2Vet — Chuỗi Bệnh Viện Thú Y Đa Chuyên Khoa Hiện Đại",
        "short_name": "2Vet Hospital",
        "url": "https://2vet.vn/",
        "domain": "2vet.vn",
        "slug": "phong_kham_thu_y_2vet",
        "industry": "phong-kham-thu-y",
        "industry_name": "Phòng Khám & Bệnh Viện Thú Y",
        "category": "Multi-Specialty Veterinary Network",
        "category_vn": "Chuỗi Bệnh Viện Thú Y Đa Chuyên Khoa & Điều Trị Nội Trú",
        "tag": "vet-chain-vn",
        "vibe": "Phân Rõ Chuyên Khoa Y Tế & Spa • Đặt Lịch Tiện Lợi • Mạng Lưới Chi Nhánh Lớn",
        "location": "Hà Nội, Hải Phòng, Quảng Ninh...",
        "desc": "Chuỗi hệ thống thú y công nghệ cao với đội ngũ bác sĩ chuyên khoa giàu kinh nghiệm. Website được tổ chức khoa học với các mảng khám chữa bệnh chuyên sâu (châm cứu, nội ngoại khoa), phòng điều trị cách ly và dịch vụ chăm sóc thú cưng trọn gói."
    },
    {
        "id": "vet14",
        "name": "Samyang Animal Clinic — Phòng Khám Thú Y Tiêu Chuẩn Hàn Quốc Chất Lượng Cao",
        "short_name": "Samyang Clinic",
        "url": "https://samyanganimalclinic.com.vn/",
        "domain": "samyanganimalclinic.com.vn",
        "slug": "phong_kham_thu_y_samyang",
        "industry": "phong-kham-thu-y",
        "industry_name": "Phòng Khám & Bệnh Viện Thú Y",
        "category": "Korean Standard Vet Clinic",
        "category_vn": "Thú Y Tiêu Chuẩn Hàn Quốc & Hồ Sơ Xuất Cảnh Thú Cưng",
        "tag": "korean-standard-vet",
        "vibe": "Y Khoa Hiện Đại • Chuyên Nghiệp Tận Tâm • Hỗ Trợ Xuất Cảnh Quốc Tế",
        "location": "Hà Nội & TP. Hồ Chí Minh",
        "desc": "Phòng khám thú y ứng dụng phác đồ điều trị và máy móc theo tiêu chuẩn Hàn Quốc. Nổi bật với dịch vụ xét nghiệm sinh hóa chuyên sâu, điều trị bệnh truyền nhiễm, phẫu thuật chỉnh hình và thủ tục visa/hồ sơ xuất nhập cảnh thú cưng quốc tế."
    },
    {
        "id": "vet15",
        "name": "Phòng Khám Thú Y Thi Thi Pet — Cấp Cứu Thú Y 24/24 Uy Tín TP.HCM",
        "short_name": "Thi Thi Pet Clinic",
        "url": "https://thuythithi.com/",
        "domain": "thuythithi.com",
        "slug": "phong_kham_thu_y_thi_thi",
        "industry": "phong-kham-thu-y",
        "industry_name": "Phòng Khám & Bệnh Viện Thú Y",
        "category": "24/7 Emergency & In-Home Vet Care",
        "category_vn": "Cấp Cứu Thú Y 24/24 & Dịch Vụ Bác Sĩ Khám Tận Nhà",
        "tag": "emergency-inhome-vet",
        "vibe": "Hỗ Trợ Khẩn Cấp Nhanh Chóng • Khám Tận Nơi • Bảng Giá Rõ Ràng",
        "location": "TP. Hồ Chí Minh (Nhiều Quận Huyện)",
        "desc": "Hệ thống thú y hoạt động từ 2012 với thế mạnh cấp cứu thú cưng 24/24 và dịch vụ bác sĩ thú y đến tận nhà. Bố cục website tập trung vào tính tương tác khẩn cấp, số điện thoại hotline nổi bật và chia sẻ cẩm nang chăm sóc thú cưng hữu ích."
    },
    {
        "id": "vet16",
        "name": "Bệnh Viện Thú Y Tropicpet — Không Gian Thú Y Thân Thiện & Trang Thiết Bị Tiên Tiến",
        "short_name": "Tropicpet Hà Nội",
        "url": "https://tropicpet.vn/",
        "domain": "tropicpet.vn",
        "slug": "phong_kham_thu_y_tropicpet",
        "industry": "phong-kham-thu-y",
        "industry_name": "Phòng Khám & Bệnh Viện Thú Y",
        "category": "Modern Pet Healthcare Hospital",
        "category_vn": "Bệnh Viện Thú Y Trẻ Trung & Thân Thiện Với Người Nuôi",
        "tag": "friendly-pet-hospital",
        "vibe": "Thiết Kế Tươi Sáng • Trang Thiết Bị Mới • Dịch Vụ Chu Đáo",
        "location": "Hà Nội",
        "desc": "Chuỗi bệnh viện thú y hiện đại được người nuôi thú cưng thủ đô yêu thích nhờ phong cách trẻ trung, không gian khám chữa bệnh sạch đẹp không mùi và trang bị đầy đủ máy xét nghiệm máu, máy X-quang, máy siêu âm kỹ thuật số."
    },
    {
        "id": "vet17",
        "name": "Bệnh Viện Thú Y AniPet — Trung Tâm Y Tế Thú Cưng Quy Mô Lớn TP. Thủ Đức",
        "short_name": "AniPet Hospital",
        "url": "https://benhvienthuyanipet.com/",
        "domain": "benhvienthuyanipet.com",
        "slug": "phong_kham_thu_y_anipet",
        "industry": "phong-kham-thu-y",
        "industry_name": "Phòng Khám & Bệnh Viện Thú Y",
        "category": "Comprehensive Animal Medical Center",
        "category_vn": "Trung Tâm Y Tế Thú Y Quy Mô Lớn Đầy Đủ Chuyên Khoa",
        "tag": "medical-center-vet",
        "vibe": "Chuyên Khoa Sâu Rộng • Khu Lưu Trú Riêng Chó Mèo • Cấp Cứu 24/7",
        "location": "TP. Thủ Đức, TP. Hồ Chí Minh",
        "desc": "Bệnh viện thú y lớn tại khu Đông TP.HCM với đầy đủ các khoa: Nội khoa, Ngoại khoa phẫu thuật, Sản khoa, Da liễu và Chẩn đoán hình ảnh. Website có giao diện chỉn chu, giới thiệu rõ từng quy trình y khoa và dịch vụ pet hotel chu đáo."
    },
    {
        "id": "vet18",
        "name": "Bệnh Viện Thú Y Procare — Chăm Sóc Sức Khỏe Toàn Diện Thú Cưng Lâu Năm",
        "short_name": "Thú Y Procare",
        "url": "https://thuyprocare.com/",
        "domain": "thuyprocare.com",
        "slug": "phong_kham_thu_y_procare",
        "industry": "phong-kham-thu-y",
        "industry_name": "Phòng Khám & Bệnh Viện Thú Y",
        "category": "Full-Spectrum Veterinary Care",
        "category_vn": "Chăm Sóc Thú Y Toàn Diện, Nha Khoa & Dịch Vụ An Táng Thú Cưng",
        "tag": "veterinary-full-care",
        "vibe": "Dày Dặn Kinh Nghiệm • Danh Mục Dịch Vụ Chi Tiết • Tận Tâm Nhân Văn",
        "location": "TP. Hồ Chí Minh",
        "desc": "Địa chỉ thú y lâu năm chuyên nghiệp với dịch vụ phong phú: từ khám tổng quát, tiêm phòng vaccine, phẫu thuật triệt sản, nha khoa thú cưng cho đến dịch vụ hỏa táng và an táng thú cưng đầy nhân văn."
    },
    {
        "id": "vet19",
        "name": "Saigon Pet Hospital — Bệnh Viện Thú Y Quốc Tế Thảo Điền Cao Cấp",
        "short_name": "Saigon Pet Hospital",
        "url": "https://saigonpet.com/",
        "domain": "saigonpet.com",
        "slug": "phong_kham_thu_y_saigon_pet",
        "industry": "phong-kham-thu-y",
        "industry_name": "Phòng Khám & Bệnh Viện Thú Y",
        "category": "International Expat Veterinary Hospital",
        "category_vn": "Bệnh Viện Thú Y Quốc Tế Phục Vụ Chuyên Gia Nước Ngoài",
        "tag": "expat-veterinary",
        "vibe": "Tiêu Chuẩn Tây Âu • Đội Ngũ Đa Ngôn Ngữ • Phác Đồ Điều Trị Nghiêm Ngặt",
        "location": "Thảo Điền, TP. Thủ Đức (TP.HCM)",
        "desc": "Bệnh viện thú y quốc tế uy tín tại khu đô thị Thảo Điền, chuyên phục vụ cộng đồng chuyên gia nước ngoài và khách hàng cao cấp. Đội ngũ bác sĩ thú y có chứng chỉ quốc tế, quy trình chẩn đoán nghiêm ngặt và chăm sóc tận tâm."
    },
    {
        "id": "vet20",
        "name": "ASVELIS Veterinary Clinic — Phòng Khám Thú Y Tiêu Chuẩn Châu Âu Tại Hà Nội",
        "short_name": "ASVELIS Clinic Hà Nội",
        "url": "https://asvelis.com/",
        "domain": "asvelis.com",
        "slug": "phong_kham_thu_y_asvelis",
        "industry": "phong-kham-thu-y",
        "industry_name": "Phòng Khám & Bệnh Viện Thú Y",
        "category": "European Standard Veterinary Clinic",
        "category_vn": "Phòng Khám Thú Y Tiêu Chuẩn Châu Âu Hàng Đầu Thủ Đô",
        "tag": "european-standard-vet",
        "vibe": "Y Đức Tiêu Chuẩn Châu Âu • Bác Sĩ Quốc Tế • Thiết Bị Y Tế Tối Tân",
        "location": "Tây Hồ, Hà Nội",
        "desc": "Phòng khám thú y do các bác sĩ Pháp và chuyên gia quốc tế sáng lập tại khu vực Hồ Tây, Hà Nội. Nổi bật với trang thiết bị y khoa tiêu chuẩn châu Âu, phác đồ điều trị an toàn tuyệt đối và quy trình kiểm dịch xuất cảnh động vật chuyên nghiệp."
    }
]

print(f"=== BẮT ĐẦU CHỤP FULL-PAGE 1440PX CHO 20 MẪU PHÒNG KHÁM THÚ Y ===", flush=True)

final_metadata = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    for idx, item in enumerate(websites, 1):
        slug = item["slug"]
        filename = f"{slug}.png"
        filepath = os.path.join(output_dir, filename)
        thumb_name = f"{slug}_thumb.webp"
        full_name = f"{slug}_full.webp"
        fb_name = f"{slug}_fb.png"
        thumb_path = os.path.join(kho_webp_dir, thumb_name)
        full_path = os.path.join(kho_webp_dir, full_name)
        fb_path = os.path.join(kho_webp_dir, fb_name)

        print(f"\n[{idx}/20] Đang xử lý: {item['name']} ({item['url']})", flush=True)

        # Kiểm tra nếu ảnh đã tồn tại & đạt chuẩn thì bỏ qua
        if os.path.exists(filepath) and os.path.exists(full_path) and os.path.exists(thumb_path):
            ok, audit_msg = verify_captured_image(full_path)
            if ok:
                size_mb = os.path.getsize(filepath) / (1024 * 1024)
                thumb_kb = round(os.path.getsize(thumb_path) / 1024, 1)
                full_kb = round(os.path.getsize(full_path) / 1024, 1)
                fb_kb = round(os.path.getsize(fb_path) / 1024, 1) if os.path.exists(fb_path) else 0
                print(f"  -> File đã tồn tại & đạt chuẩn: {audit_msg}", flush=True)
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
                    "audit_msg": audit_msg,
                    "status": "SUCCESS"
                })
                continue

        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            ignore_https_errors=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        max_retries = 2
        success = False

        for attempt in range(max_retries):
            try:
                page.goto(item["url"], wait_until="domcontentloaded", timeout=45000)
                time.sleep(2.5)

                # Đóng các popup modal / cookie banner nếu có
                page.evaluate("""() => {
                    const selectors = [
                        '.modal', '.popup', '#onesignal-slidedown-dialog',
                        '.cookie-notice', '#cookie-notice', '.fancybox-overlay',
                        '[class*="newsletter-popup"]', '[id*="newsletter-popup"]',
                        '.agree-button', '#cookie-law-info-bar'
                    ];
                    selectors.forEach(s => {
                        document.querySelectorAll(s).forEach(el => el.style.display = 'none');
                    });
                }""")

                capture_smart_clean(page, filepath, viewport_height=900, scroll_delay=0.20)
                thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb = compress_tri_layer(filepath, slug, kho_webp_dir)
                ok, audit_msg = verify_captured_image(full_path)

                if ok:
                    print(f"  -> Đã chụp & nén THÀNH CÔNG: {audit_msg} (Thumb {thumb_kb}KB, Full {full_kb}KB)", flush=True)
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
                        "audit_msg": audit_msg,
                        "status": "SUCCESS"
                    })
                    success = True
                    break
                else:
                    print(f"  -> CẢNH BÁO KIỂM ĐỊNH LẦN {attempt+1}: {audit_msg}. Đang kích hoạt Self-Healing...", flush=True)
                    time.sleep(2.0)
            except Exception as e:
                print(f"  -> LỖI CHỤP LẦN {attempt+1}: {e}", flush=True)
                time.sleep(2.0)

        if not success:
            print(f"  -> THẤT BẠI sau {max_retries} lần thử: {item['name']}", flush=True)
            final_metadata.append({
                **item,
                "status": "ERROR"
            })
        
        context.close()

    browser.close()

with open(metadata_file, "w", encoding="utf-8") as f:
    json.dump(final_metadata, f, ensure_ascii=False, indent=2)

passed = sum(1 for x in final_metadata if x.get("status") == "SUCCESS")
print(f"\n=== HOÀN TẤT CHỤP! ĐẠT CHUẨN: {passed}/20 ===", flush=True)
