# -*- coding: utf-8 -*-
import os
import sys
import time
import json

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)

from capture_engine import (
    setup_page_protection,
    capture_smart_clean,
    compress_tri_layer,
    verify_captured_image,
)
from playwright.sync_api import sync_playwright

output_dir = os.path.join(BASE_DIR, "Anh_Chup_Website")
kho_webp_dir = os.path.join(BASE_DIR, "Kho_Anh_Webp")
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "noi_that_metadata.json")

os.makedirs(output_dir, exist_ok=True)
os.makedirs(kho_webp_dir, exist_ok=True)
os.makedirs(os.path.dirname(metadata_file), exist_ok=True)

websites = [
    # =========================================================================
    # NHÓM 1: THIẾT KẾ & THI CÔNG NỘI THẤT CAO CẤP / STUDIO NGHỆ THUẬT (VN)
    # =========================================================================
    {
        "id": "nt01",
        "name": "Thái Công Interior Design",
        "short_name": "Thái Công",
        "url": "https://thaicong.com/vi/",
        "domain": "thaicong.com",
        "slug": "noi_that_thaicong",
        "industry": "noi-that",
        "industry_name": "Nội Thất & Kiến Trúc Không Gian",
        "category": "Ultra-Luxury Interior Design Studio",
        "category_vn": "Thiết Kế Nội Thất Xa Xỉ & Nghệ Thuật Thượng Lưu",
        "tag": "luxury-studio",
        "vibe": "Hoàng Gia Châu Âu • Storytelling Thương Hiệu • Ảnh Dự Án Triệu Đô",
        "location": "TP.HCM (Việt Nam)",
        "desc": "Thương hiệu thiết kế nội thất xa xỉ hàng đầu Việt Nam do NTK Quách Thái Công sáng lập. Giao diện mang đậm ngôn ngữ thượng lưu, tập trung vào triết lý thẩm mỹ, bộ sưu tập công trình biệt thự siêu sang và tích hợp hệ sinh thái showroom – nhà hàng."
    },
    {
        "id": "nt02",
        "name": "Nội Thất Đồng Gia — Gỗ Óc Chó Cao Cấp",
        "short_name": "Đồng Gia",
        "url": "https://donggia.vn/",
        "domain": "donggia.vn",
        "slug": "noi_that_donggia",
        "industry": "noi-that",
        "industry_name": "Nội Thất & Kiến Trúc Không Gian",
        "category": "Bespoke Walnut Wood Interior",
        "category_vn": "Tiên Phong Nội Thất Gỗ Óc Chó Độc Bản",
        "tag": "luxury-studio",
        "vibe": "Đẳng Cấp Độc Bản • Tông Nâu Trầm Ấm • Showreel Biệt Thự",
        "location": "Hà Nội (Việt Nam)",
        "desc": "Đơn vị dẫn đầu phân khúc nội thất gỗ Óc Chó tự nhiên Bắc Mỹ tại Việt Nam. Website nổi bật với bảng màu trầm ấm sang trọng, trình diễn dự án biệt thự Vinhomes/Ecopark sắc nét cùng phễu đặt lịch tham quan showroom."
    },
    {
        "id": "nt03",
        "name": "EuroStyle — Luxury Defined",
        "short_name": "EuroStyle",
        "url": "https://eurostyle.com.vn/",
        "domain": "eurostyle.com.vn",
        "slug": "noi_that_eurostyle",
        "industry": "noi-that",
        "industry_name": "Nội Thất & Kiến Trúc Không Gian",
        "category": "European Luxury Furniture & Turnkey Fit-out",
        "category_vn": "Nội Thất Hàng Hiệu Châu Âu & Tổng Thầu Cao Cấp",
        "tag": "luxury-studio",
        "vibe": "Minimal Luxury • Tạp Chí Kiến Trúc • Bố Cục Editorial",
        "location": "Hà Nội & TP.HCM",
        "desc": "Nhà phân phối độc quyền gần 40 thương hiệu nội thất xa xỉ châu Âu (Minotti, Bruno Zampa, Porcelanosa...). Giao diện đậm chất tạp chí kiến trúc quốc tế với khoảng thở lớn, typography tinh tế và hồ sơ năng lực dự án 5 sao."
    },
    {
        "id": "nt04",
        "name": "Byzan Design — Kiến Trúc & Nội Thất Hiện Đại",
        "short_name": "Byzan Design",
        "url": "https://byzan.vn/",
        "domain": "byzan.vn",
        "slug": "noi_that_byzan",
        "industry": "noi-that",
        "industry_name": "Nội Thất & Kiến Trúc Không Gian",
        "category": "Modern & Luxury Residential Interior",
        "category_vn": "Thiết Kế Thi Công Nội Thất Hiện Đại & Luxury",
        "tag": "luxury-studio",
        "vibe": "Sắc Sảo Hiện Đại • Tương Phản Tối Giản • Ảnh Công Trình Thật",
        "location": "Hà Nội (Việt Nam)",
        "desc": "Thương hiệu chuyên sâu phong cách Hiện đại và Modern Luxury cho căn hộ hạng sang, penthouse và biệt thự. Website bố cục tinh gọn, ưu tiên ảnh thi công thực tế độ phân giải cao và bảng báo giá trực quan."
    },
    {
        "id": "nt05",
        "name": "Decox Design — Thiết Kế & Xây Dựng Nội Thất",
        "short_name": "Decox Design",
        "url": "https://decoxdesign.com/",
        "domain": "decoxdesign.com",
        "slug": "noi_that_decoxdesign",
        "industry": "noi-that",
        "industry_name": "Nội Thất & Kiến Trúc Không Gian",
        "category": "Full-Service Interior Architecture",
        "category_vn": "Công Ty Thiết Kế Thi Công Nội Thất Đa Phong Cách",
        "tag": "luxury-studio",
        "vibe": "Thanh Lịch • Phân Tầng Dự Án Rõ Ràng • CRO Tư Vấn Nhanh",
        "location": "TP.HCM (Việt Nam)",
        "desc": "Đơn vị thiết kế và thi công nội thất uy tín tại TP.HCM. Trang chủ trình bày mạch lạc theo từng nhóm không gian (chung cư, nhà phố, biệt thự, văn phòng) kết hợp hệ thống bài viết chuyên sâu chuẩn SEO và form nhận dự toán."
    },
    {
        "id": "nt06",
        "name": "Nội Thất Kenli — Sofa Da Thật & Bàn Ăn Ý",
        "short_name": "Kenli",
        "url": "https://noithatkenli.vn/",
        "domain": "noithatkenli.vn",
        "slug": "noi_that_kenli",
        "industry": "noi-that",
        "industry_name": "Nội Thất & Kiến Trúc Không Gian",
        "category": "Imported Italian Leather Sofas & Dining",
        "category_vn": "Showroom Nội Thất Nhập Khẩu Châu Âu Cao Cấp",
        "tag": "luxury-studio",
        "vibe": "Sang Trọng Tinh Tế • Trình Diễn Chất Liệu • Catalogue Rõ Nét",
        "location": "Hà Nội & TP.HCM",
        "desc": "Thương hiệu phân phối sofa da thật Milano&Design, Chateau d'Ax và bàn ăn đá nhân tạo gốc thạch anh. Website kết hợp hài hòa giữa câu chuyện chất liệu cao cấp, danh mục sản phẩm chuẩn thương mại điện tử và đặt lịch trải nghiệm."
    },

    # =========================================================================
    # NHÓM 2: DOANH NGHIỆP THIẾT KẾ THI CÔNG TRỌN GÓI & TOP SEO (VIỆT NAM)
    # =========================================================================
    {
        "id": "nt07",
        "name": "XHOME Việt Nam — Hệ Thống Thiết Kế Nội Thất",
        "short_name": "XHOME",
        "url": "https://xhome.com.vn/",
        "domain": "xhome.com.vn",
        "slug": "noi_that_xhome",
        "industry": "noi-that",
        "industry_name": "Nội Thất & Kiến Trúc Không Gian",
        "category": "Nationwide Interior Design & Build Chain",
        "category_vn": "Hệ Thống Thiết Kế Thi Công Nội Thất Quy Mô Toàn Quốc",
        "tag": "thiet-ke-thi-cong",
        "vibe": "Quy Mô Doanh Nghiệp • Đa Phong Cách • Mạng Lưới Showroom",
        "location": "Hà Nội, TP.HCM, Đà Nẵng & Toàn quốc",
        "desc": "Một trong những thương hiệu thiết kế & thi công nội thất có mạng lưới chi nhánh lớn nhất Việt Nam. Website chuẩn mực về cấu trúc danh mục dịch vụ, thư viện mẫu nhà đẹp theo phong cách (Indochine, Wabi Sabi, Tân cổ điển) và năng lực xưởng."
    },
    {
        "id": "nt08",
        "name": "Nội Thất MoreHome — Kho Dự Án & Xưởng Sản Xuất",
        "short_name": "MoreHome",
        "url": "https://thietkenoithat.com/",
        "domain": "thietkenoithat.com",
        "slug": "noi_that_morehome",
        "industry": "noi-that",
        "industry_name": "Nội Thất & Kiến Trúc Không Gian",
        "category": "Top SEO Interior Design & Manufacturing",
        "category_vn": "Cổng Mẫu Thiết Kế Nội Thất & Xưởng Sản Xuất Top SEO",
        "tag": "thiet-ke-thi-cong",
        "vibe": "Chuẩn SEO Mega-Portal • Kho Dữ Liệu Khổng Lồ • Xưởng Trực Tiếp",
        "location": "Hà Nội, Hải Phòng, Đà Nẵng, TP.HCM",
        "desc": "Website đầu ngành về lưu lượng tìm kiếm tự nhiên (SEO) mảng thiết kế nội thất tại Việt Nam. Bố cục tối ưu tìm kiếm theo loại hình nhà ở, phong cách thiết kế, sản phẩm đồ gỗ và đối chiếu năng lực sản xuất trực tiếp."
    },
    {
        "id": "nt09",
        "name": "Nội Thất Mạnh Hệ — Chuyên Chung Cư & Nhà Phố",
        "short_name": "Mạnh Hệ",
        "url": "https://noithatmanhhe.vn/",
        "domain": "noithatmanhhe.vn",
        "slug": "noi_that_manhhe",
        "industry": "noi-that",
        "industry_name": "Nội Thất & Kiến Trúc Không Gian",
        "category": "Turnkey Apartment & Townhouse Interior",
        "category_vn": "Thiết Kế Thi Công Trọn Gói Có Xưởng Trực Tiếp",
        "tag": "thiet-ke-thi-cong",
        "vibe": "Chuyển Đổi Cao (CRO) • Bảng Giá Minh Bạch • Video Thực Tế",
        "location": "TP.HCM (Việt Nam)",
        "desc": "Hình mẫu website tối ưu chuyển đổi (CRO) cực tốt cho ngành thi công nội thất tại TP.HCM: nhấn mạnh lợi thế giá gốc tận xưởng, so sánh 3D với ảnh bàn giao thực tế và công khai quy trình báo giá minh bạch."
    },
    {
        "id": "nt10",
        "name": "S.Housing — Thiết Kế Thi Công Nội Thất Trọn Gói",
        "short_name": "S.Housing",
        "url": "https://s-housing.vn/",
        "domain": "s-housing.vn",
        "slug": "noi_that_shousing",
        "industry": "noi-that",
        "industry_name": "Nội Thất & Kiến Trúc Không Gian",
        "category": "Transparent Interior Design & Build",
        "category_vn": "Giải Pháp Nội Thất Tối Ưu Công Năng & Báo Giá Rõ Ràng",
        "tag": "thiet-ke-thi-cong",
        "vibe": "Hiện Đại Gọn Gàng • Chứng Thực Năng Lực • Dễ Tra Cứu",
        "location": "TP.HCM (Việt Nam)",
        "desc": "Đơn vị thiết kế và thi công nội thất nổi bật ở khu vực phía Nam. Giao diện sạch sẽ, phân tách rõ gói dịch vụ, bảng dự toán vật liệu An Cường và thư viện công trình thực tế giúp khách hàng dễ dàng ra quyết định."
    },
    {
        "id": "nt11",
        "name": "Nội Thất Tứ Gia — Kiến Trúc & Thi Công Trọn Gói",
        "short_name": "Nội Thất Tứ Gia",
        "url": "https://noithattugia.com/",
        "domain": "noithattugia.com",
        "slug": "noi_that_tugia",
        "industry": "noi-that",
        "industry_name": "Nội Thất & Kiến Trúc Không Gian",
        "category": "Residential Interior & Cost Calculator",
        "category_vn": "Thiết Kế Thi Công Nội Thất Nhà Ở & Dự Toán Chi Phí",
        "tag": "thiet-ke-thi-cong",
        "vibe": "Thực Tế Bàn Giao • Phễu Dự Toán • Top SEO Miền Bắc",
        "location": "Hà Nội (Việt Nam)",
        "desc": "Đơn vị thiết kế thi công nội thất uy tín tại miền Bắc sở hữu xưởng trực tiếp hơn 1000m². Website kết hợp kho mẫu căn hộ theo diện tích (45m² - 120m²), bảng giá chi tiết từng hạng mục và nhật ký bàn giao."
    },

    # =========================================================================
    # NHÓM 3: SHOWROOM & THƯƠNG MẠI ĐIỆN TỬ ĐỒ NỘI THẤT HIỆN ĐẠI (VN)
    # =========================================================================
    {
        "id": "nt12",
        "name": "Nội Thất Nhà Xinh — Đồ Gỗ & Trang Trí Cao Cấp",
        "short_name": "Nhà Xinh",
        "url": "https://nhaxinh.com/",
        "domain": "nhaxinh.com",
        "slug": "noi_that_nhaxinh",
        "industry": "noi-that",
        "industry_name": "Nội Thất & Kiến Trúc Không Gian",
        "category": "Premium Furniture Retail & Inspiration",
        "category_vn": "Chuỗi Showroom Đồ Gỗ & Nội Thất Đương Đại Hàng Đầu",
        "tag": "showroom-ecommerce",
        "vibe": "Ấm Áp Đương Đại • Lookbook Không Gian Sống • E-commerce Chuẩn",
        "location": "TP.HCM, Hà Nội, Bình Dương",
        "desc": "Thương hiệu nội thất biểu tượng thuộc AKA Furniture. Website cân bằng xuất sắc giữa bán lẻ trực tuyến (filter theo phòng khách, phòng ăn, phòng ngủ) và mục Góc cảm hứng – Thiết kế nội thất đầy tính thẩm mỹ."
    },
    {
        "id": "nt13",
        "name": "Nội Thất MOHO — Chuẩn Xuất Khẩu & Thân Thiện",
        "short_name": "MOHO",
        "url": "https://moho.com.vn/",
        "domain": "moho.com.vn",
        "slug": "noi_that_moho",
        "industry": "noi-that",
        "industry_name": "Nội Thất & Kiến Trúc Không Gian",
        "category": "Modern Eco-Friendly Furniture E-Commerce",
        "category_vn": "Nội Thất Hiện Đại Chuẩn Xuất Khẩu & An Toàn Sức Khỏe",
        "tag": "showroom-ecommerce",
        "vibe": "Tối Giản Bắc Âu • Tối Ưu Mua Sắm Online • Trust Badges Mạnh",
        "location": "TP.HCM & Hà Nội",
        "desc": "Thương hiệu bán lẻ nội thất trực tuyến hàng đầu của Savimex. Giao diện e-commerce cực kỳ mượt mà, làm nổi bật chứng nhận CARB-P2/FSC, bảo hành 5 năm, miễn phí giao lắp và bộ sưu tập phân loại theo căn hộ."
    },
    {
        "id": "nt14",
        "name": "Make My Home — Nội Thất Tối Giản Minimalism",
        "short_name": "Make My Home",
        "url": "https://makemyhomevn.com/",
        "domain": "makemyhomevn.com",
        "slug": "noi_that_makemyhome",
        "industry": "noi-that",
        "industry_name": "Nội Thất & Kiến Trúc Không Gian",
        "category": "Minimalist Furniture & Modular Living",
        "category_vn": "Thương Hiệu Nội Thất Tối Giản Cho Gia Đình Trẻ",
        "tag": "showroom-ecommerce",
        "vibe": "Minimalism Tinh Gọn • Tông Màu Trung Tính • Trẻ Trung Hiện Đại",
        "location": "TP.HCM (Việt Nam)",
        "desc": "Studio và thương hiệu nội thất theo đuổi lối sống tối giản (Minimalism). Website ghi điểm nhờ bảng màu trung tính dịu mắt, hình ảnh lifestyle đồng bộ, combo nội thất căn hộ trọn gói và trải nghiệm đặt hàng gọn nhẹ."
    },
    {
        "id": "nt15",
        "name": "BEYOURs — Nội Thất Lắp Ráp & Phong Cách Sống",
        "short_name": "BEYOURs",
        "url": "https://beyours.vn/",
        "domain": "beyours.vn",
        "slug": "noi_that_beyours",
        "industry": "noi-that",
        "industry_name": "Nội Thất & Kiến Trúc Không Gian",
        "category": "Flat-pack & Youthful Lifestyle Furniture",
        "category_vn": "Nội Thất Thông Minh Lắp Ráp Chuẩn Hàn Quốc",
        "tag": "showroom-ecommerce",
        "vibe": "Tươi Sáng Trẻ Trung • E-commerce D2C • Dễ Tự Lắp Ráp",
        "location": "TP.HCM & Toàn quốc",
        "desc": "Thương hiệu nội thất D2C tiên phong mô hình lắp ráp gọn nhẹ cho căn hộ và giới trẻ. Website bố trí thẻ sản phẩm rõ ràng, phân mục không gian sinh hoạt trực quan cùng các gói ưu đãi theo mùa thu hút."
    },
    {
        "id": "nt16",
        "name": "JYSK Việt Nam — Chuỗi Nội Thất Bắc Âu Đan Mạch",
        "short_name": "JYSK",
        "url": "https://jysk.vn/",
        "domain": "jysk.vn",
        "slug": "noi_that_jysk",
        "industry": "noi-that",
        "industry_name": "Nội Thất & Kiến Trúc Không Gian",
        "category": "Scandinavian Sleeping & Living Retail",
        "category_vn": "Chuỗi Bán Lẻ Nội Thất & Trang Trí Bắc Âu Toàn Cầu",
        "tag": "showroom-ecommerce",
        "vibe": "Scandinavian Chuẩn Mực • Phân Danh Mục Khoa Học • Catalogue Rõ",
        "location": "Hà Nội, TP.HCM, Đà Nẵng, Bình Dương",
        "desc": "Thương hiệu bán lẻ nội thất và trang trí đến từ Đan Mạch. Giao diện website chuẩn chuỗi bán lẻ quốc tế với thanh tìm kiếm thông minh, hệ thống lọc danh mục đồ gỗ – chăn ga – decor cực kỳ khoa học và tra cứu tồn kho cửa hàng."
    },

    # =========================================================================
    # NHÓM 4: THƯƠNG HIỆU & STUDIO NỘI THẤT ĐẲNG CẤP QUỐC TẾ (UI/UX MẪU MỰC)
    # =========================================================================
    {
        "id": "nt17",
        "name": "Herman Miller — Modern Furnishings & Ergonomics",
        "short_name": "Herman Miller",
        "url": "https://www.hermanmiller.com/",
        "domain": "hermanmiller.com",
        "slug": "noi_that_hermanmiller",
        "industry": "noi-that",
        "industry_name": "Nội Thất & Kiến Trúc Không Gian",
        "category": "Iconic Modern & Ergonomic Furniture",
        "category_vn": "Huyền Thoại Nội Thất Hiện Đại & Công Thái Học Mỹ",
        "tag": "global-luxury",
        "vibe": "Industrial Minimalism • Customizer Sản Phẩm • Đỉnh Cao D2C",
        "location": "Mỹ & Toàn cầu",
        "desc": "Biểu tượng nội thất thiết kế thế kỷ 20 và ghế công thái học hàng đầu thế giới. Website chuẩn mực về kiến trúc thông tin, trình bày câu chuyện thiết kế kết hợp cấu hình tùy biến vật liệu (product configurator) mượt mà."
    },
    {
        "id": "nt18",
        "name": "Minotti — Italian Contemporary Luxury Furniture",
        "short_name": "Minotti",
        "url": "https://www.minotti.com/en",
        "domain": "minotti.com",
        "slug": "noi_that_minotti",
        "industry": "noi-that",
        "industry_name": "Nội Thất & Kiến Trúc Không Gian",
        "category": "Ultra-Luxury Italian Furniture Lookbook",
        "category_vn": "Thương Hiệu Nội Thất Xa Xỉ Đương Đại Ý",
        "tag": "global-luxury",
        "vibe": "High-Fashion Lookbook • Dark & Warm Tone • Ảnh Full-Bleed",
        "location": "Ý & Toàn cầu",
        "desc": "Đế chế nội thất đương đại Ý với ngôn ngữ thiết kế website như một sàn diễn kiến trúc. Trải nghiệm hình ảnh tràn viền độ phân giải cao, bộ sưu tập theo năm, thông số kỹ thuật CAD/BIM cho kiến trúc sư và bản đồ Flagship."
    },
    {
        "id": "nt19",
        "name": "Poliform — Contemporary Italian Living Systems",
        "short_name": "Poliform",
        "url": "https://www.poliform.it/en/",
        "domain": "poliform.it",
        "slug": "noi_that_poliform",
        "industry": "noi-that",
        "industry_name": "Nội Thất & Kiến Trúc Không Gian",
        "category": "Architectural Interior Systems & Kitchens",
        "category_vn": "Hệ Thống Tủ Bếp, Phòng Thay Đồ & Nội Thất Ý",
        "tag": "global-luxury",
        "vibe": "Kiến Trúc Tinh Khiết • Typography Đẳng Cấp • Digital Portfolio",
        "location": "Ý & Toàn cầu",
        "desc": "Thương hiệu dẫn đầu về hệ thống nội thất kiến trúc đồng bộ (tủ bếp, hệ tủ âm tường, phòng khách). Website sử dụng bố cục lưới bất đối xứng tinh tế, video không gian sống và tài liệu kỹ thuật chuyên sâu."
    },
    {
        "id": "nt20",
        "name": "Vincent Van Duysen — Architecture & Interiors",
        "short_name": "Vincent Van Duysen",
        "url": "https://vincentvanduysen.com/",
        "domain": "vincentvanduysen.com",
        "slug": "noi_that_vincentvanduysen",
        "industry": "noi-that",
        "industry_name": "Nội Thất & Kiến Trúc Không Gian",
        "category": "Quiet Luxury Architectural Studio",
        "category_vn": "Studio Kiến Trúc & Nội Thất Quiet Luxury Bỉ",
        "tag": "global-luxury",
        "vibe": "Quiet Luxury • Tối Giản Nguyên Bản • Lưới Ảnh Kinh Điển",
        "location": "Antwerp (Bỉ) & Toàn cầu",
        "desc": "Website của kiến trúc sư lừng danh Vincent Van Duysen — hình mẫu kinh điển về phong cách Quiet Luxury và tối giản kiến trúc. Bảng màu đơn sắc ấm áp, typography thanh mảnh và cách kể chuyện không gian bằng ánh sáng – vật liệu."
    }
]

print(f"=== BẮT ĐẦU CHỤP VÀ NÉN ẢNH CHO {len(websites)} WEBSITE NỘI THẤT ===")

results_summary = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    for idx, site in enumerate(websites, 1):
        print(f"\n[{idx:02d}/{len(websites)}] Đang xử lý: {site['name']} ({site['url']})...")

        raw_png = os.path.join(output_dir, f"{site['slug']}.png")
        full_webp = os.path.join(kho_webp_dir, f"{site['slug']}_full.webp")
        thumb_webp = os.path.join(kho_webp_dir, f"{site['slug']}_thumb.webp")
        fb_png = os.path.join(kho_webp_dir, f"{site['slug']}_fb.png")

        site["image"] = f"Anh_Chup_Website/{site['slug']}.png"
        site["thumb"] = f"Kho_Anh_Webp/{site['slug']}_thumb.webp"
        site["full"] = f"Kho_Anh_Webp/{site['slug']}_full.webp"
        site["fb"] = f"Kho_Anh_Webp/{site['slug']}_fb.png"

        if os.path.exists(full_webp) and os.path.exists(thumb_webp) and os.path.exists(fb_png):
            valid, msg = verify_captured_image(full_webp)
            if valid:
                print(f"  -> Đã có ảnh đạt chuẩn: {full_webp} ({msg}). Tái sử dụng.")
                site["thumb_kb"] = round(os.path.getsize(thumb_webp) / 1024, 1)
                site["full_kb"] = round(os.path.getsize(full_webp) / 1024, 1)
                site["fb_kb"] = round(os.path.getsize(fb_png) / 1024, 1)
                site["size_mb"] = f"{round(os.path.getsize(raw_png) / (1024*1024), 2)} MB" if os.path.exists(raw_png) else "0.0 MB"
                site["audit_msg"] = msg
                site["status"] = "SUCCESS"
                results_summary.append((site["id"], site["domain"], "PASS", msg))
                continue

        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            ignore_https_errors=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        setup_page_protection(page)

        try:
            page.goto(site['url'], timeout=45000, wait_until="domcontentloaded")
            time.sleep(2.5)

            # Đóng các overlay cookie/popup phổ biến nếu có thể click nút đóng
            page.evaluate("""() => {
                const closeSelectors = [
                    'button[aria-label*="Close" i]', 'button[aria-label*="accept" i]',
                    '.onetrust-close-btn-handler', '#onetrust-accept-btn-handler',
                    '.cookie-accept', '.btn-close-popup', '.popup-close', '.close-modal'
                ];
                closeSelectors.forEach(sel => {
                    document.querySelectorAll(sel).forEach(btn => {
                        try { btn.click(); } catch(e) {}
                    });
                });
            }""")
            time.sleep(0.5)

            capture_smart_clean(page, raw_png, viewport_height=900, scroll_delay=0.22)

            if not os.path.exists(raw_png) or os.path.getsize(raw_png) == 0:
                print(f"  [-] Lỗi: Không thể chụp ảnh cho {site['domain']}")
                site["status"] = "FAIL"
                site["audit_msg"] = "Không tạo được ảnh gốc"
                results_summary.append((site["id"], site["domain"], "FAIL", "No raw png"))
                continue

            thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb = compress_tri_layer(raw_png, site['slug'], kho_webp_dir)

            valid, msg = verify_captured_image(full_webp)
            print(f"  [+] QA Audit {site['domain']}: {'PASS' if valid else 'FAIL'} - {msg}")

            if not valid:
                print(f"  [!] Cảnh báo: Tự động khắc phục và chụp lại với độ trễ cao hơn...")
                page.goto(site['url'], timeout=45000, wait_until="networkidle")
                time.sleep(3.0)
                capture_smart_clean(page, raw_png, viewport_height=900, scroll_delay=0.35)
                thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb = compress_tri_layer(raw_png, site['slug'], kho_webp_dir)
                valid, msg = verify_captured_image(full_webp)
                print(f"  [+] QA Audit Vòng 2 {site['domain']}: {'PASS' if valid else 'FAIL'} - {msg}")

            site["thumb_kb"] = thumb_kb
            site["full_kb"] = full_kb
            site["fb_kb"] = fb_kb
            site["size_mb"] = f"{round(os.path.getsize(raw_png) / (1024*1024), 2)} MB"
            site["audit_msg"] = msg
            site["status"] = "SUCCESS" if valid else "FAIL"
            results_summary.append((site["id"], site["domain"], "PASS" if valid else "FAIL", msg))

        except Exception as e:
            print(f"  [-] Lỗi trong quá trình chụp {site['domain']}: {e}")
            site["status"] = "FAIL"
            site["audit_msg"] = str(e)[:120]
            results_summary.append((site["id"], site["domain"], "FAIL", str(e)[:80]))
        finally:
            context.close()

    browser.close()

with open(metadata_file, "w", encoding="utf-8") as f:
    json.dump(websites, f, ensure_ascii=False, indent=2)

print("\n=== TỔNG KẾT QA AUDIT 20 WEBSITE NỘI THẤT ===")
for r in results_summary:
    print(f"  {r[0]} | {r[1]:24s} | {r[2]:4s} | {r[3]}")
print(f"\n[+] Đã lưu metadata vào: {metadata_file}")
