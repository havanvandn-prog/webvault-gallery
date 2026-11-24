# -*- coding: utf-8 -*-
import os, sys, time, json

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)

from capture_engine import setup_page_protection, capture_smart_clean, compress_tri_layer, verify_captured_image
from playwright.sync_api import sync_playwright

output_dir = os.path.join(BASE_DIR, "Anh_Chup_Website")
kho_webp_dir = os.path.join(BASE_DIR, "Kho_Anh_Webp")
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "bds_moigioi_pool_audit.json")

os.makedirs(output_dir, exist_ok=True)
os.makedirs(kho_webp_dir, exist_ok=True)

pool = [
    # --- NHÓM 1: SÀN ĐĂNG TIN & MÔI GIỚI NHÀ ĐẤT THỔ CƯ VIỆT NAM ---
    {
        "name": "OneHousing — Nền Tảng PropTech Mua Bán & Chuyển Nhượng Nhà Đất",
        "short_name": "OneHousing",
        "url": "https://onehousing.vn/",
        "domain": "onehousing.vn",
        "slug": "bds_onehousing",
        "category": "PropTech Brokerage & Valuation",
        "category_vn": "OneHousing — Sàn PropTech & Công Cụ Định Giá Nhà Đất",
        "tag": "san-nha-dat-vn",
        "vibe": "Modern PropTech • Bộ Lọc Đa Chiều • Định Giá & Vay Mua Nhà",
        "location": "Hà Nội & TP. Hồ Chí Minh",
        "desc": "Hình mẫu chuẩn mực cho website sàn môi giới nhà đất thế hệ mới tại Việt Nam: thanh tìm kiếm trực quan theo khu vực/giá, giỏ hàng nhà thổ cư & căn hộ xác thực kèm công cụ định giá thông minh."
    },
    {
        "name": "Rever — Sàn Giao Dịch Môi Giới Nhà Đất & Căn Hộ Minh Bạch",
        "short_name": "Rever",
        "url": "https://rever.vn/",
        "domain": "rever.vn",
        "slug": "bds_rever",
        "category": "Tech-Enabled Real Estate Brokerage",
        "category_vn": "Rever — Môi Giới Nhà Phố, Căn Hộ & Cho Thuê Minh Bạch",
        "tag": "san-nha-dat-vn",
        "vibe": "Clean Brokerage • Ảnh Thực Tế • Lọc Mua & Thuê Nhanh",
        "location": "TP. Hồ Chí Minh & Toàn Quốc",
        "desc": "Giao diện môi giới BĐS tối giản, tập trung vào hình ảnh nhà thật, thông tin pháp lý rõ ràng và bộ lọc chuyển đổi mượt giữa tab Mua nhà và Thuê nhà."
    },
    {
        "name": "Homedy — Cổng Thông Tin Mua Bán & Cho Thuê Nhà Đất Hiện Đại",
        "short_name": "Homedy",
        "url": "https://homedy.com/",
        "domain": "homedy.com",
        "slug": "bds_homedy",
        "category": "Modern Real Estate Portal",
        "category_vn": "Homedy — Sàn Đăng Tin Nhà Đất Giao Diện Phẳng Hiện Đại",
        "tag": "san-nha-dat-vn",
        "vibe": "Flat Modern UI • Phân Loại Rõ Ràng • Bộ Lọc Quận & Giá",
        "location": "Toàn Quốc (VN)",
        "desc": "Cổng đăng tin nhà đất nổi bật với thiết kế phẳng hiện đại, thẻ bất động sản sạch sẽ dễ đọc lướt giá/diện tích và bộ lọc theo quận huyện rất thân thiện."
    },
    {
        "name": "Mogi.vn — Chuyên Trang Môi Giới Nhà Đất Thổ Cư & Cho Thuê",
        "short_name": "Mogi",
        "url": "https://mogi.vn/",
        "domain": "mogi.vn",
        "slug": "bds_mogi",
        "category": "Residential Listing & Broker Directory",
        "category_vn": "Mogi — Sàn Nhà Đất Thổ Cư, Cho Thuê & Danh Bạ Môi Giới",
        "tag": "san-nha-dat-vn",
        "vibe": "Teal Clean Portal • Giá Nhà Theo Đường • Tìm Môi Giới",
        "location": "Toàn Quốc (VN)",
        "desc": "Website đăng tin nhà đất được yêu thích nhờ tông xanh ngọc dễ chịu, tích hợp tra cứu giá nhà theo từng tuyến đường và danh bạ môi giới chuyên khu vực."
    },
    {
        "name": "CenHomes — Sàn Giao Dịch & Bản Đồ Định Giá Bất Động Sản",
        "short_name": "CenHomes",
        "url": "https://cenhomes.vn/",
        "domain": "cenhomes.vn",
        "slug": "bds_cenhomes",
        "category": "Digital Brokerage & Map Search",
        "category_vn": "CenHomes — Nền Tảng Môi Giới & Kho Hàng Thứ Cấp Lớn",
        "tag": "san-nha-dat-vn",
        "vibe": "Corporate PropTech • Giỏ Hàng Đa Dạng • Trực Quan",
        "location": "Hà Nội, TP.HCM & Toàn Quốc",
        "desc": "Sàn giao dịch nhà đất kết hợp mạng lưới môi giới lớn, trình bày mạch lạc giữa phân khúc nhà lẻ thổ cư, căn hộ chuyển nhượng và cho thuê."
    },
    {
        "name": "Meey Land — Cổng Thông Tin Bất Động Sản Xác Thực & Quy Hoạch",
        "short_name": "Meey Land",
        "url": "https://meeyland.com/",
        "domain": "meeyland.com",
        "slug": "bds_meeyland",
        "category": "Verified Listings & Planning Map",
        "category_vn": "Meey Land — Sàn Đăng Tin Nhà Đất & Tích Hợp Bản Đồ",
        "tag": "san-nha-dat-vn",
        "vibe": "Proptech Blue • Bộ Lọc Bản Đồ • Tin Đăng Xác Thực",
        "location": "Toàn Quốc (VN)",
        "desc": "Cổng thông tin bất động sản tích hợp thanh tìm kiếm mạnh theo loại hình thổ cư, giá bán, hướng nhà và tiện ích xem bản đồ trực tiếp."
    },
    {
        "name": "BDS123.vn — Website Rao Vặt Mua Bán Nhà Đất Thổ Cư Tinh Gọn",
        "short_name": "BDS123",
        "url": "https://bds123.vn/",
        "domain": "bds123.vn",
        "slug": "bds_bds123",
        "category": "High-Speed Classifieds Portal",
        "category_vn": "BDS123 — Web Đăng Tin Nhà Đất Thổ Cư Tốc Độ Cao",
        "tag": "san-nha-dat-vn",
        "vibe": "Fast Classifieds • Chuẩn SEO • Dễ Dùng Mọi Lứa Tuổi",
        "location": "Toàn Quốc (VN)",
        "desc": "Mẫu web rao vặt nhà đất cực kỳ gọn nhẹ, tối ưu tốc độ và SEO địa phương, phù hợp cho khách muốn làm cổng đăng tin nhà đất thổ cư dễ tra cứu theo mức giá."
    },
    {
        "name": "Green House Agency — Môi Giới Nhà Phố & Biệt Thự Khu Nam Sài Gòn",
        "short_name": "Green House Agency",
        "url": "https://greenhouseagency.vn/",
        "domain": "greenhouseagency.vn",
        "slug": "bds_greenhouse",
        "category": "Local House & Villa Brokerage",
        "category_vn": "Green House — Công Ty Môi Giới Nhà Phố & Biệt Thự Chuyên Khu",
        "tag": "san-nha-dat-vn",
        "vibe": "Boutique Agency • Chuyên Sâu Khu Vực • Giỏ Hàng Cao Cấp",
        "location": "Phú Mỹ Hưng & TP.HCM",
        "desc": "Hình mẫu chuẩn cho website công ty/đội nhóm môi giới nhà phố, biệt thự chuyên khu vực: thanh lọc nhanh theo bán/thuê, giỏ hàng phân loại rõ và nút gọi chốt lịch xem nhà."
    },
    {
        "name": "MOSO — Nền Tảng AI PropTech Mua Bán Nhà Đất Xác Thực",
        "short_name": "MOSO",
        "url": "https://moso.vn/",
        "domain": "moso.vn",
        "slug": "bds_moso",
        "category": "AI PropTech Listing Platform",
        "category_vn": "MOSO — Web Tìm Nhà Đất & Căn Hộ Xác Thực Chuẩn Trẻ Trung",
        "tag": "san-nha-dat-vn",
        "vibe": "Fresh Startup UI • Tin Xác Thực Video • Trải Nghiệm Hiện Đại",
        "location": "TP.HCM & Toàn Quốc",
        "desc": "Nền tảng tìm kiếm bất động sản thế hệ mới với giao diện trẻ trung, thoáng mắt, nhấn mạnh tính năng tin đăng xác thực và bộ lọc tìm kiếm thông minh."
    },
    {
        "name": "Dot Property Việt Nam — Cổng BĐS Mua Bán & Cho Thuê Chuẩn Quốc Tế",
        "short_name": "Dot Property VN",
        "url": "https://www.dotproperty.com.vn/",
        "domain": "dotproperty.com.vn",
        "slug": "bds_dotproperty",
        "category": "International Style Property Portal",
        "category_vn": "Dot Property — Cổng BĐS & Căn Hộ Chuẩn Phong Cách Quốc Tế",
        "tag": "san-nha-dat-vn",
        "vibe": "International Portal • Ảnh Lớn Sắc Nét • Lọc Mua & Thuê",
        "location": "TP.HCM, Hà Nội & Đà Nẵng",
        "desc": "Cổng thông tin bất động sản mang phong cách quốc tế, bố cục lưới căn hộ và nhà phố thoáng rộng, phù hợp tham khảo cho web môi giới hướng tới cả khách Việt lẫn chuyên gia nước ngoài."
    },

    # --- NHÓM 2: CHO THUÊ CĂN HỘ DỊCH VỤ, CHUNG CƯ & NHÀ Ở VIỆT NAM ---
    {
        "name": "JHouse — Hệ Thống Cho Thuê Căn Hộ Dịch Vụ Cao Cấp TP.HCM",
        "short_name": "JHouse",
        "url": "https://jhouse.vn/",
        "domain": "jhouse.vn",
        "slug": "bds_jhouse",
        "category": "Serviced Apartment Rental Specialist",
        "category_vn": "JHouse — Cho Thuê Căn Hộ Dịch Vụ & Căn Hộ Full Nội Thất",
        "tag": "cho-thue-can-ho-vn",
        "vibe": "Clean Rental UI • Lọc Quận & Phòng Ngủ • Ảnh Nội Thất Sáng",
        "location": "TP. Hồ Chí Minh",
        "desc": "Mẫu website chuyên cho thuê căn hộ dịch vụ cực kỳ chỉnh chu: thanh lọc trực quan theo quận, mức giá thuê, số phòng ngủ và thẻ căn hộ hiển thị tiện ích rõ ràng."
    },
    {
        "name": "City Apartment — Môi Giới Cho Thuê Căn Hộ Trung Tâm TP.HCM",
        "short_name": "City Apartment",
        "url": "https://cityapartment.vn/",
        "domain": "cityapartment.vn",
        "slug": "bds_cityapartment",
        "category": "Urban Condo Rental Agency",
        "category_vn": "City Apartment — Cho Thuê Chung Cư & Căn Hộ Trung Tâm",
        "tag": "cho-thue-can-ho-vn",
        "vibe": "Urban Condo • Phân Khu Dự Án • Bảng Giá Thuê Rõ Ràng",
        "location": "TP. Hồ Chí Minh",
        "desc": "Website agency chuyên cho thuê căn hộ chung cư tại các khu trung tâm TP.HCM, cấu trúc danh mục theo từng tòa nhà/quận giúp khách chọn nhanh căn hộ đúng nhu cầu."
    },
    {
        "name": "Saigon Luxury — Môi Giới & Cho Thuê Căn Hộ Hạng Sang, Penthouse",
        "short_name": "Saigon Luxury",
        "url": "https://saigonluxury.com.vn/",
        "domain": "saigonluxury.com.vn",
        "slug": "bds_saigonluxury",
        "category": "Luxury Condo & Villa Brokerage",
        "category_vn": "Saigon Luxury — Môi Giới Penthouse, Biệt Thự & Căn Hộ Sang",
        "tag": "cho-thue-can-ho-vn",
        "vibe": "Dark Gold Luxury • BĐS Hàng Hiệu • Thẩm Mỹ Thượng Lưu",
        "location": "Thủ Thiêm, Thảo Điền & Quận 1",
        "desc": "Giao diện cao cấp dành cho sàn môi giới phân khúc hạng sang (Penthouse, Duplex, Biệt thự Thảo Điền), tối ưu hình ảnh không gian sống sang trọng và form tư vấn VIP."
    },
    {
        "name": "Hoozing — Nền Tảng Cho Thuê & Mua Bán Căn Hộ Thông Minh",
        "short_name": "Hoozing",
        "url": "https://hoozing.com/",
        "domain": "hoozing.com",
        "slug": "bds_hoozing",
        "category": "Smart Apartment Rental PropTech",
        "category_vn": "Hoozing — PropTech Cho Thuê & Chuyển Nhượng Căn Hộ",
        "tag": "cho-thue-can-ho-vn",
        "vibe": "Modern Rental App • Tìm Theo Dự Án • Đặt Lịch Xem Căn",
        "location": "TP. Hồ Chí Minh",
        "desc": "Thiết kế theo phong cách PropTech trẻ trung, làm nổi bật giỏ hàng căn hộ cho thuê có sẵn, giá thuê minh bạch theo tháng và luồng đặt lịch xem nhà trực tuyến."
    },
    {
        "name": "Thuecanho123 — Cổng Chuyên Cho Thuê Căn Hộ Chung Cư & Mini",
        "short_name": "Thuecanho123",
        "url": "https://thuecanho123.com/",
        "domain": "thuecanho123.com",
        "slug": "bds_thuecanho123",
        "category": "Apartment Rental Listing Portal",
        "category_vn": "Thuecanho123 — Chuyên Trang Đăng Tin Cho Thuê Căn Hộ Top SEO",
        "tag": "cho-thue-can-ho-vn",
        "vibe": "SEO Rental Portal • Lọc Giá & Diện Tích • Dễ Quét Tin",
        "location": "TP.HCM, Hà Nội & Toàn Quốc",
        "desc": "Mẫu cổng đăng tin chuyên biệt mảng cho thuê căn hộ chung cư & mini với bộ lọc cực nhanh theo tỉnh thành, khoảng giá thuê và số phòng ngủ, chuẩn SEO top đầu Google."
    },
    {
        "name": "Chothuenha.com.vn — Nền Tảng Giao Dịch Nhà Phố & Mặt Bằng Cho Thuê",
        "short_name": "Chothuenha.com.vn",
        "url": "https://chothuenha.com.vn/",
        "domain": "chothuenha.com.vn",
        "slug": "bds_chothuenha",
        "category": "House & Commercial Rental Portal",
        "category_vn": "Chothuenha — Nền Tảng Cho Thuê Nhà Nguyên Căn, Căn Hộ & Mặt Bằng",
        "tag": "cho-thue-can-ho-vn",
        "vibe": "Structured Rental • Đa Phân Khúc Thuê • Giao Diện Sáng",
        "location": "TP.HCM & Hà Nội",
        "desc": "Website chuyên sâu mảng cho thuê từ nhà nguyên căn, căn hộ dịch vụ đến mặt bằng kinh doanh, cấu trúc bộ lọc rõ ràng và thẻ tin đăng trực quan."
    },
    {
        "name": "Toàn Huy Hoàng Realty — Cho Thuê Căn Hộ & Biệt Thự Đà Nẵng",
        "short_name": "Toàn Huy Hoàng",
        "url": "https://toanhuyhoang.com/",
        "domain": "toanhuyhoang.com",
        "slug": "bds_toanhuyhoang",
        "category": "Regional Condo & Villa Rental",
        "category_vn": "Toàn Huy Hoàng — Môi Giới Căn Hộ & Biệt Thự Biển Đà Nẵng",
        "tag": "cho-thue-can-ho-vn",
        "vibe": "Regional Agency • Song Ngữ Anh-Việt • Căn Hộ & Villa",
        "location": "Đà Nẵng",
        "desc": "Đại diện tiêu biểu cho website công ty môi giới cho thuê căn hộ và biệt thự khu vực Đà Nẵng với giao diện sáng, hỗ trợ đa ngôn ngữ và bộ lọc tiện lợi."
    },
    {
        "name": "Vietnam Housing — Cho Thuê Nhà & Căn Hộ Dịch Vụ Hà Nội",
        "short_name": "Vietnam Housing",
        "url": "https://housing.vn/",
        "domain": "housing.vn",
        "slug": "bds_housingvn",
        "category": "Expat Apartment & House Rental",
        "category_vn": "Vietnam Housing — Cho Thuê Căn Hộ & Nhà Ở Chuyên Gia Hà Nội",
        "tag": "cho-thue-can-ho-vn",
        "vibe": "Expat Friendly • Tối Giản Rõ Ràng • Lọc Quận Tây Hồ/Ba Đình",
        "location": "Hà Nội",
        "desc": "Website môi giới cho thuê căn hộ dịch vụ và nhà ở hướng đến chuyên gia nước ngoài tại Hà Nội, bố cục gọn gàng, tập trung vào ảnh phòng và lọc nhanh theo quận trung tâm."
    },
    {
        "name": "Central Vietnam Realty (CVR) — Môi Giới Nhà Đất & Cho Thuê Miền Trung",
        "short_name": "CVR Realty",
        "url": "https://cvr.com.vn/",
        "domain": "cvr.com.vn",
        "slug": "bds_cvr",
        "category": "Boutique Real Estate Brokerage",
        "category_vn": "CVR — Môi Giới Căn Hộ, Biệt Thự & Nhà Đất Chuẩn Quốc Tế",
        "tag": "cho-thue-can-ho-vn",
        "vibe": "International Agency • Hero Sắc Nét • Lọc Mua & Thuê",
        "location": "Đà Nẵng & Hội An",
        "desc": "Agency môi giới bất động sản theo chuẩn quốc tế tại miền Trung, giao diện tinh tế, cân bằng tốt giữa tìm kiếm bất động sản mua bán và danh mục căn hộ/villa cho thuê."
    },
    {
        "name": "Savills Việt Nam — Tư Vấn & Môi Giới Nhà Ở, Căn Hộ Cao Cấp",
        "short_name": "Savills Việt Nam",
        "url": "https://www.savills.com.vn/",
        "domain": "savills.com.vn",
        "slug": "bds_savillsvn",
        "category": "Global Brokerage Local Portal",
        "category_vn": "Savills Việt Nam — Môi Giới Nhà Ở Hạng Sang & Báo Cáo Thị Trường",
        "tag": "cho-thue-can-ho-vn",
        "vibe": "Prestige Yellow-Charcoal • Uy Tín Toàn Cầu • Tìm Kiếm Đa Hạng Mục",
        "location": "TP.HCM, Hà Nội & Toàn Quốc",
        "desc": "Chuẩn mực giao diện tập đoàn tư vấn và môi giới bất động sản quốc tế tại Việt Nam, kết hợp thanh tìm kiếm nhà ở/căn hộ cho thuê với hệ thống nghiên cứu thị trường chuyên sâu."
    },

    # --- NHÓM 3: NỀN TẢNG MÔI GIỚI NHÀ ĐẤT & CHO THUÊ QUỐC TẾ CHUẨN UI/UX ---
    {
        "name": "Compass — Chuẩn Mực Vàng UI/UX Sàn Môi Giới Bất Động Sản Mỹ",
        "short_name": "Compass",
        "url": "https://www.compass.com/",
        "domain": "compass.com",
        "slug": "bds_compass",
        "category": "Gold Standard Brokerage UX",
        "category_vn": "Compass (Mỹ) — Chuẩn Mực Tối Giản & Tìm Kiếm Nhà Đất Đẳng Cấp",
        "tag": "quoc-te-uiux",
        "vibe": "Minimalist Editorial • Đen-Trắng Sang Trọng • Search-First Hero",
        "location": "New York, Mỹ",
        "desc": "Biểu tượng thiết kế UI/UX ngành môi giới nhà đất thế giới: giao diện tối giản đen-trắng cực sang, đặt thanh tìm kiếm Buy/Rent làm trung tâm và nghệ thuật trình bày ảnh nhà ở đỉnh cao."
    },
    {
        "name": "Blueground — Nền Tảng Cho Thuê Căn Hộ Full Nội Thất Toàn Cầu",
        "short_name": "Blueground",
        "url": "https://www.theblueground.com/",
        "domain": "theblueground.com",
        "slug": "bds_blueground",
        "category": "Global Furnished Apartment Rental",
        "category_vn": "Blueground — Chuẩn UX Cho Thuê Căn Hộ Full Nội Thất Hiện Đại",
        "tag": "quoc-te-uiux",
        "vibe": "Lifestyle Rental • Đặt Thuê Online • Thiết Kế Ấm Áp Tinh Tế",
        "location": "Toàn Cầu (Mỹ, Châu Âu, Châu Á)",
        "desc": "Hình mẫu xuất sắc nhất thế giới cho mảng cho thuê căn hộ dịch vụ/full nội thất: bộ lọc chọn thành phố & ngày nhận phòng mượt mà, ảnh nội thất tràn đầy cảm hứng sống và quy trình thuê 100% online."
    },
    {
        "name": "The Agency RE — Môi Giới Nhà Phố & Biệt Thự Phong Cách Boutique",
        "short_name": "The Agency",
        "url": "https://www.theagencyre.com/",
        "domain": "theagencyre.com",
        "slug": "bds_theagency",
        "category": "Boutique Luxury Real Estate",
        "category_vn": "The Agency (Mỹ) — Môi Giới BĐS Hạng Sang Phong Cách Tạp Chí",
        "tag": "quoc-te-uiux",
        "vibe": "Luxury Editorial • Tương Phản Mạnh • Lifestyle Storytelling",
        "location": "Beverly Hills, Mỹ & Toàn Cầu",
        "desc": "Thương hiệu môi giới nổi tiếng với phong cách thiết kế mang hơi thở tạp chí thời trang: hình ảnh khổ lớn giàu cảm xúc, thanh tìm kiếm tinh gọn và cách giới thiệu đội ngũ môi giới rất hiện đại."
    },
    {
        "name": "Knight Frank — Tư Vấn & Môi Giới Bất Động Sản Nhà Ở Toàn Cầu",
        "short_name": "Knight Frank",
        "url": "https://www.knightfrank.com/",
        "domain": "knightfrank.com",
        "slug": "bds_knightfrank",
        "category": "Global Prime Residential Advisory",
        "category_vn": "Knight Frank (Anh) — Môi Giới Nhà Ở Cao Cấp & Đẳng Cấp Châu Âu",
        "tag": "quoc-te-uiux",
        "vibe": "British Prestige • Bố Cục Mạch Lạc • Chuẩn Mực Tin Cậy",
        "location": "London, Anh & Toàn Cầu",
        "desc": "Website môi giới nhà ở lâu đời của Anh Quốc với giao diện thanh lịch, phân khu rõ ràng giữa Mua, Thuê, Định giá và Nghiên cứu thị trường — rất hợp cho các sàn môi giới muốn xây dựng uy tín lớn."
    },
    {
        "name": "Corcoran — Môi Giới Căn Hộ & Nhà Phố New York Tinh Tế",
        "short_name": "Corcoran",
        "url": "https://www.corcoran.com/",
        "domain": "corcoran.com",
        "slug": "bds_corcoran",
        "category": "Urban Residential Brokerage",
        "category_vn": "Corcoran (New York) — Môi Giới Căn Hộ & Nhà Phố Đô Thị",
        "tag": "quoc-te-uiux",
        "vibe": "New York Chic • Typography Đẹp • Khám Phá Khu Phố",
        "location": "New York, Mỹ",
        "desc": "Mẫu website môi giới căn hộ và nhà phố đô thị cực kỳ tinh tế, nổi bật với trải nghiệm khám phá từng khu phố (Neighborhood Guides) kết hợp lưới căn hộ bán/cho thuê sạch sẽ."
    },
    {
        "name": "Douglas Elliman — Sàn Môi Giới Bất Động Sản Cao Cấp Hàng Đầu Mỹ",
        "short_name": "Douglas Elliman",
        "url": "https://www.elliman.com/",
        "domain": "elliman.com",
        "slug": "bds_elliman",
        "category": "Premier Residential Brokerage",
        "category_vn": "Douglas Elliman (Mỹ) — Sàn Môi Giới Nhà Phố & Căn Hộ Cao Cấp",
        "tag": "quoc-te-uiux",
        "vibe": "Refined Luxury • Thanh Tìm Kiếm Thông Minh • Lưới Ảnh Sắc Nét",
        "location": "New York & Florida, Mỹ",
        "desc": "Website môi giới bất động sản cao cấp sở hữu thanh lọc địa điểm/giá trực quan ngay trên Hero, bố cục danh mục nhà bán và cho thuê cực kỳ khoa học, cân bằng giữa thẩm mỹ và hiệu năng."
    },
    {
        "name": "Engel & Völkers — Môi Giới Biệt Thự & Căn Hộ Quốc Tế Tối Giản",
        "short_name": "Engel & Völkers",
        "url": "https://www.engelvoelkers.com/en/",
        "domain": "engelvoelkers.com",
        "slug": "bds_engelvoelkers",
        "category": "European Luxury Brokerage",
        "category_vn": "Engel & Völkers (Đức) — Chuẩn Mực Tối Giản Châu Âu",
        "tag": "quoc-te-uiux",
        "vibe": "European Minimal • Điểm Nhấn Đỏ-Trắng • Bố Cục Sang Trọng",
        "location": "Hamburg, Đức & Toàn Cầu",
        "desc": "Thương hiệu môi giới châu Âu nổi tiếng với nhận diện đỏ-trắng tinh giản, khoảng thở rộng rãi và thanh tìm kiếm bất động sản mua/thuê chuẩn xác từng tiêu chí."
    },
]

results = []
passed_list = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for idx, site in enumerate(pool, 1):
        site["id"] = f"bds{idx:02d}"
        site["industry"] = "moi-gioi-nha-dat-cho-thue"
        site["industry_name"] = "Môi Giới Nhà Đất & Cho Thuê Căn Hộ"
        print(f"\n[{idx}/{len(pool)}] Processing: {site['short_name']} ({site['url']})")
        raw_png = os.path.join(output_dir, f"{site['slug']}.png")
        full_webp = os.path.join(kho_webp_dir, f"{site['slug']}_full.webp")

        site["image"] = f"Anh_Chup_Website/{site['slug']}.png"
        site["thumb"] = f"Kho_Anh_Webp/{site['slug']}_thumb.webp"
        site["full"] = f"Kho_Anh_Webp/{site['slug']}_full.webp"
        site["fb"] = f"Kho_Anh_Webp/{site['slug']}_fb.png"

        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            ignore_https_errors=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        setup_page_protection(page)
        try:
            page.goto(site['url'], timeout=40000, wait_until="domcontentloaded")
            time.sleep(3.5)
            page.evaluate("""() => {
                const selectors = [
                    'button[aria-label*="Close" i]', 'button[aria-label*="accept" i]',
                    '.onetrust-close-btn-handler', '#onetrust-accept-btn-handler',
                    '#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll',
                    '.didomi-continue-without-agreeing', '#didomi-notice-agree-button',
                    '.cky-btn-accept', '.cookie-accept', '.btn-close-popup',
                    '.popup-close', '.close-modal', '.mfp-close', '.fancybox-close-small',
                    '.elementor-popup-modal .dialog-close-button',
                    'button[class*="cookie" i]', '[data-testid="cookie-accept"]'
                ];
                selectors.forEach(sel => {
                    try { document.querySelectorAll(sel).forEach(btn => { try { btn.click(); } catch(e) {} }); } catch(e) {}
                });
            }""")
            time.sleep(1.0)
            capture_smart_clean(page, raw_png, viewport_height=900, scroll_delay=0.35)
            thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb = compress_tri_layer(raw_png, site['slug'], kho_webp_dir)
            valid, msg = verify_captured_image(full_webp)
            print(f"  [+] QA Vòng 1: {'PASS' if valid else 'FAIL'} - {msg}")

            if not valid:
                print("  [!] Self-Healing Vòng 2: Chụp lại với networkidle + delay 0.55s...")
                try:
                    page.goto(site['url'], timeout=50000, wait_until="networkidle")
                except Exception:
                    page.goto(site['url'], timeout=50000, wait_until="load")
                time.sleep(4.0)
                page.evaluate("""() => {
                    document.querySelectorAll(
                        '[id*="cookie" i]:not(:has(main)):not(.dialog-off-canvas-main-canvas), ' +
                        '[class*="cookie" i]:not(:has(main)):not(.dialog-off-canvas-main-canvas), ' +
                        '[id*="consent" i]:not(:has(main)):not(.dialog-off-canvas-main-canvas), ' +
                        '[class*="consent" i]:not(:has(main)):not(.dialog-off-canvas-main-canvas), ' +
                        '[class*="onetrust" i]:not(:has(main)), [id*="onetrust" i]:not(:has(main)), ' +
                        '.modal-backdrop, .popup-overlay, [role="dialog"]:not(:has(main)):not(.dialog-off-canvas-main-canvas)'
                    ).forEach(el => {
                        el.style.setProperty('display', 'none', 'important');
                        el.style.setProperty('visibility', 'hidden', 'important');
                    });
                }""")
                capture_smart_clean(page, raw_png, viewport_height=900, scroll_delay=0.55)
                thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb = compress_tri_layer(raw_png, site['slug'], kho_webp_dir)
                valid, msg = verify_captured_image(full_webp)
                print(f"  [+] QA Vòng 2: {'PASS' if valid else 'FAIL'} - {msg}")

            if valid:
                site["thumb_kb"] = thumb_kb
                site["full_kb"] = full_kb
                site["fb_kb"] = fb_kb
                site["size_mb"] = f"{round(os.path.getsize(raw_png) / (1024*1024), 2)} MB"
                site["audit_msg"] = msg
                site["status"] = "SUCCESS"
                passed_list.append(site)
                results.append((site["slug"], site["domain"], "PASS", msg))
            else:
                for p_clean in [raw_png, full_webp, os.path.join(kho_webp_dir, f"{site['slug']}_thumb.webp"), os.path.join(kho_webp_dir, f"{site['slug']}_fb.png")]:
                    if os.path.exists(p_clean):
                        try: os.remove(p_clean)
                        except: pass
                results.append((site["slug"], site["domain"], "SKIP-FAIL", msg))
        except Exception as e:
            print(f"  [-] Error {site['domain']}: {e}")
            for p_clean in [raw_png, full_webp, os.path.join(kho_webp_dir, f"{site['slug']}_thumb.webp"), os.path.join(kho_webp_dir, f"{site['slug']}_fb.png")]:
                if os.path.exists(p_clean):
                    try: os.remove(p_clean)
                    except: pass
            results.append((site["slug"], site["domain"], "SKIP-ERR", str(e)[:80]))
        finally:
            context.close()
    browser.close()

with open(metadata_file, "w", encoding="utf-8") as f:
    json.dump(passed_list, f, ensure_ascii=False, indent=2)

print(f"\n=== TỔNG KẾT QA NGÁCH 2 (MÔI GIỚI NHÀ ĐẤT & CHO THUÊ): ĐẠT {len(passed_list)}/{len(pool)} MẪU ===")
for r in results:
    print(f"  {r[0]:20s} | {r[1]:28s} | {r[2]:9s} | {r[3]}")
