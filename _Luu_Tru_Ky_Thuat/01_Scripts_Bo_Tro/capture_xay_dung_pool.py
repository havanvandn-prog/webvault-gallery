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
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "xay_dung_pool_audit.json")

os.makedirs(output_dir, exist_ok=True)
os.makedirs(kho_webp_dir, exist_ok=True)

pool = [
    # --- NHÓM 1: TỔNG THẦU & TẬP ĐOÀN XÂY DỰNG HÀNG ĐẦU VIỆT NAM ---
    {
        "name": "Coteccons — Tập Đoàn Tổng Thầu Xây Dựng Hàng Đầu Việt Nam",
        "short_name": "Coteccons",
        "url": "https://www.coteccons.vn/",
        "domain": "coteccons.vn",
        "slug": "xd_coteccons",
        "category": "Top Tier General Contractor VN",
        "category_vn": "Tổng Thầu Xây Dựng Số 1 Việt Nam — Corporate Hiện Đại",
        "tag": "tong-thau-vn",
        "vibe": "Corporate Prestige • Số Liệu Năng Lực • Bố Cục Doanh Nghiệp Lớn",
        "location": "TP. Hồ Chí Minh & Toàn Quốc",
        "desc": "Website chuẩn mực của tổng thầu xây dựng lớn nhất Việt Nam (dấu ấn Landmark 81). Giao diện sắc nét, thể hiện mạnh mẽ năng lực thi công, văn hóa ESG, hệ thống dự án quy mô lớn và cổng quan hệ cổ đông chuyên nghiệp."
    },
    {
        "name": "Newtecons — Tổng Thầu Thiết Kế & Thi Công Công Trình Quy Mô Lớn",
        "short_name": "Newtecons",
        "url": "https://newtecons.vn/",
        "domain": "newtecons.vn",
        "slug": "xd_newtecons",
        "category": "Design & Build General Contractor",
        "category_vn": "Tổng Thầu Thiết Kế & Thi Công — Giao Diện Sang Trọng",
        "tag": "tong-thau-vn",
        "vibe": "Architectural Grid • Ảnh Công Trình Toàn Màn Hình • Nhận Diện Mạnh",
        "location": "TP. Hồ Chí Minh & Hà Nội",
        "desc": "Website của tổng thầu Newtecons nổi bật với tông xanh dương - trắng hiện đại, trình diễn trực quan các dự án cao ốc, trung tâm thương mại và hạ tầng lớn với bố cục gọn gàng, tốc độ tải mượt."
    },
    {
        "name": "Central Construction — Tổng Thầu Xây Dựng Dân Dụng & Công Nghiệp",
        "short_name": "Central Construction",
        "url": "https://www.centralcons.vn/",
        "domain": "centralcons.vn",
        "slug": "xd_centralcons",
        "category": "General Contractor Corporate",
        "category_vn": "Tổng Thầu CENTRAL — Bố Cục Chuyên Nghiệp & Chuẩn Mực",
        "tag": "tong-thau-vn",
        "vibe": "Clean Corporate • Hero Công Trình • Phân Nhóm Lĩnh Vực Rõ",
        "location": "TP. Hồ Chí Minh & Toàn Quốc",
        "desc": "Trang chủ CENTRAL gây ấn tượng bằng hình ảnh công trình thực tế sắc nét, phân tách rành mạch các mảng dân dụng, công nghiệp, hạ tầng và dự án nghỉ dưỡng cao cấp."
    },
    {
        "name": "Unicons — Tổng Thầu Thi Công Chủ Lực Thuộc Coteccons Group",
        "short_name": "Unicons",
        "url": "https://unicons.vn/",
        "domain": "unicons.vn",
        "slug": "xd_unicons",
        "category": "Enterprise Construction Contractor",
        "category_vn": "Tổng Thầu Unicons — Hiện Đại & Đậm Chất Kỹ Thuật",
        "tag": "tong-thau-vn",
        "vibe": "Bold Industrial • Thống Kê Năng Lực • Danh Mục Dự Án Trực Quan",
        "location": "TP. Hồ Chí Minh & Toàn Quốc",
        "desc": "Giao diện Unicons mang phong thái tổng thầu chuyên nghiệp với cấu trúc trình bày năng lực thi công, số liệu dự án bàn giao và bộ lọc công trình tiêu biểu mạch lạc."
    },
    {
        "name": "SOL E&C — Tổng Thầu Xây Dựng Công Nghiệp, Dân Dụng & Cơ Điện",
        "short_name": "SOL E&C",
        "url": "https://solenc.vn/",
        "domain": "solenc.vn",
        "slug": "xd_solenc",
        "category": "Industrial & Civil Contractor",
        "category_vn": "Tổng Thầu SOL E&C — Tối Giản & Chuẩn Quốc Tế",
        "tag": "tong-thau-vn",
        "vibe": "Modern Editorial • Khoảng Thở Rộng • Chuẩn FDI & Quốc Tế",
        "location": "TP. Hồ Chí Minh & Toàn Quốc",
        "desc": "Website SOL E&C có thiết kế rất hiện đại, hướng tới khách hàng doanh nghiệp và chủ đầu tư FDI với bố cục thoáng, hình ảnh nhà máy/tòa nhà sắc nét và điều hướng tối giản."
    },
    {
        "name": "Hòa Bình Construction Group (HBC) — Tập Đoàn Xây Dựng Quốc Gia",
        "short_name": "Hòa Bình (HBC)",
        "url": "https://hbcg.vn/",
        "domain": "hbcg.vn",
        "slug": "xd_hoabinh",
        "category": "National Construction Group",
        "category_vn": "Tập Đoàn Xây Dựng Hòa Bình — Thương Hiệu Quốc Gia",
        "tag": "tong-thau-vn",
        "vibe": "Enterprise Portal • Thương Hiệu Lâu Đời • Đa Chuyên Mục",
        "location": "TP. Hồ Chí Minh & Toàn Quốc",
        "desc": "Cổng thông tin tập đoàn xây dựng Hòa Bình thể hiện bề dày lịch sử, hệ sinh thái dự án dân dụng - hạ tầng - công nghiệp và hệ thống tin tức doanh nghiệp đồ sộ."
    },
    {
        "name": "Delta Group — Tập Đoàn Xây Dựng & Thi Công Tầng Hầm Hàng Đầu",
        "short_name": "Delta Group",
        "url": "https://deltagroup.vn/",
        "domain": "deltagroup.vn",
        "slug": "xd_deltagroup",
        "category": "Civil & Underground Contractor",
        "category_vn": "Tập Đoàn Xây Dựng Delta — Mạnh Mẽ & Chuyên Sâu",
        "tag": "tong-thau-vn",
        "vibe": "Strong Identity • Năng Lực Kỹ Thuật • Bố Cục Doanh Nghiệp",
        "location": "Hà Nội & Toàn Quốc",
        "desc": "Website Delta Group nổi bật với tông đỏ - xám mạnh mẽ, nhấn mạnh thế mạnh thi công nền móng, tầng hầm và các công trình cao tầng quy mô lớn trên cả nước."
    },
    {
        "name": "FECON — Tập Đoàn Hạ Tầng, Nền Móng & Công Trình Ngầm",
        "short_name": "FECON",
        "url": "https://fecon.com.vn/",
        "domain": "fecon.com.vn",
        "slug": "xd_fecon",
        "category": "Infrastructure & Foundation Group",
        "category_vn": "Tập Đoàn FECON — Chuyên Sâu Hạ Tầng & Nền Móng",
        "tag": "tong-thau-vn",
        "vibe": "Engineering Focus • Hạ Tầng & Năng Lượng • Trình Bày Khoa Học",
        "location": "Hà Nội & Toàn Quốc",
        "desc": "Trang chủ FECON truyền tải tốt năng lực tổng thầu hạ tầng, công trình ngầm và năng lượng tái tạo với cấu trúc rõ ràng, chuyên nghiệp."
    },
    {
        "name": "Phục Hưng Holdings — Tổng Thầu Xây Dựng Dân Dụng & Hạ Tầng",
        "short_name": "Phục Hưng Holdings",
        "url": "https://phuchung.com.vn/",
        "domain": "phuchung.com.vn",
        "slug": "xd_phuchung",
        "category": "General Contractor Holdings",
        "category_vn": "Phục Hưng Holdings — Tổng Thầu Uy Tín Miền Bắc",
        "tag": "tong-thau-vn",
        "vibe": "Corporate Classic • Dự Án Tiêu Biểu • Quan Hệ Cổ Đông",
        "location": "Hà Nội & Toàn Quốc",
        "desc": "Website doanh nghiệp xây dựng niêm yết lâu năm tại miền Bắc, trình bày rõ lĩnh vực hoạt động, năng lực thiết bị và danh mục các dự án chung cư, khu đô thị đã bàn giao."
    },
    {
        "name": "Dinco E&C — Tổng Thầu Thiết Kế & Thi Công Nhà Xưởng Miền Trung",
        "short_name": "Dinco E&C",
        "url": "https://dinco.com.vn/",
        "domain": "dinco.com.vn",
        "slug": "xd_dinco",
        "category": "Design & Build Industrial VN",
        "category_vn": "Tổng Thầu Dinco E&C — Dẫn Đầu Khu Vực Miền Trung",
        "tag": "tong-thau-vn",
        "vibe": "Clean Industrial • Dự Án FDI • Cam Kết Chất Lượng",
        "location": "Đà Nẵng & Miền Trung",
        "desc": "Đại diện tiêu biểu cho nhóm tổng thầu khu vực Miền Trung chuyên thiết kế & thi công nhà máy, khu công nghiệp và khách sạn với giao diện gọn gàng, giàu tính thuyết phục."
    },

    # --- NHÓM 2: XÂY NHÀ TRỌN GÓI, BIỆT THỰ & THIẾT KẾ THI CÔNG (VIỆT NAM) ---
    {
        "name": "SBS House — Thiết Kế & Thi Công Nhà Phố, Biệt Thự Hiện Đại",
        "short_name": "SBS House",
        "url": "https://sbshouse.vn/",
        "domain": "sbshouse.vn",
        "slug": "xd_sbshouse",
        "category": "Modern Residential Design-Build",
        "category_vn": "Thiết Kế & Thi Công Nhà Phố Hiện Đại — UI Rất Đẹp",
        "tag": "xay-nha-tron-goi",
        "vibe": "Minimalist Warm • Portfolio Nhà Phố Xanh • CTA Tư Vấn Mượt",
        "location": "Đà Nẵng, TP.HCM & Toàn Quốc",
        "desc": "Một trong những website thiết kế thi công nhà ở có thẩm mỹ tốt nhất Việt Nam. Bố cục tinh tế, ảnh công trình hoàn thiện thực tế đẹp mắt, phân loại mẫu nhà và bảng giá trọn gói dễ tra cứu."
    },
    {
        "name": "Kiến Trúc Akisa — Thiết Kế & Thi Công Biệt Thự, Dinh Thự Cao Cấp",
        "short_name": "Kiến Trúc Akisa",
        "url": "https://akisa.vn/",
        "domain": "akisa.vn",
        "slug": "xd_akisa",
        "category": "Luxury Villa Design & Build",
        "category_vn": "Thiết Kế Thi Công Biệt Thự Cao Cấp — Top SEO Toàn Quốc",
        "tag": "xay-nha-tron-goi",
        "vibe": "Luxury Villa Showcase • Kho Mẫu Biệt Thự Lớn • Chuyển Đổi Cao",
        "location": "Hà Nội, TP.HCM & Toàn Quốc",
        "desc": "Website top đầu SEO mảng thiết kế thi công biệt thự và dinh thự. Hệ thống danh mục mẫu nhà theo phong cách và số tầng rất trực quan, tối ưu mạnh cho nhu cầu tìm kiếm và nhận tư vấn."
    },
    {
        "name": "Betaviet Group — Kiến Trúc & Xây Dựng Biệt Thự Trọn Gói",
        "short_name": "Betaviet Group",
        "url": "https://betaviet.vn/",
        "domain": "betaviet.vn",
        "slug": "xd_betaviet",
        "category": "Villa Architecture & Construction",
        "category_vn": "Betaviet Group — Chuyên Sâu Biệt Thự & Dinh Thự",
        "tag": "xay-nha-tron-goi",
        "vibe": "Classic Luxury • Bộ Lọc Mẫu Nhà • Showroom Nội Thất",
        "location": "Hà Nội & Toàn Quốc",
        "desc": "Thương hiệu lâu năm về thiết kế và thi công biệt thự trọn gói, nổi bật với thư viện hàng nghìn công trình thực tế, phân loại theo diện tích và phong cách kiến trúc."
    },
    {
        "name": "NeoHouse — Thiết Kế Kiến Trúc & Xây Nhà Trọn Gói",
        "short_name": "NeoHouse",
        "url": "https://neohouse.vn/",
        "domain": "neohouse.vn",
        "slug": "xd_neohouse",
        "category": "Residential Design & Build",
        "category_vn": "NeoHouse — Thiết Kế Thi Công Nhà Phố & Biệt Thự",
        "tag": "xay-nha-tron-goi",
        "vibe": "Modern Conversion • Bảng Báo Giá Rõ • Kho Dự Án Phong Phú",
        "location": "TP. Hồ Chí Minh & Đà Nẵng",
        "desc": "Giao diện tối ưu chuyển đổi cho dịch vụ xây nhà trọn gói và thiết kế biệt thự, trình bày mạch lạc quy trình làm việc, báo giá tham khảo và đánh giá từ gia chủ."
    },
    {
        "name": "Xây Dựng Nhất Tín — Nhà Thầu Xây Nhà Trọn Gói & Phần Thô Uy Tín",
        "short_name": "Xây Dựng Nhất Tín",
        "url": "https://xaydungnhattin.com/",
        "domain": "xaydungnhattin.com",
        "slug": "xd_nhattin",
        "category": "Turnkey Home Construction",
        "category_vn": "Xây Nhà Trọn Gói Nhất Tín — Báo Giá Minh Bạch & CRO Tốt",
        "tag": "xay-nha-tron-goi",
        "vibe": "Lead-Gen Focused • Công Cụ Tính Chi Phí • Cam Kết Bảo Hành",
        "location": "TP. Hồ Chí Minh & Miền Nam",
        "desc": "Mẫu website nhà thầu dân dụng tối ưu mạnh cho chuyển đổi khách hàng: nổi bật bảng đơn giá xây dựng, cam kết vật tư rõ ràng, công trình bàn giao thực tế và form báo giá nhanh."
    },
    {
        "name": "Kiến An Vinh — Tư Vấn Thiết Kế & Thi Công Xây Dựng Trọn Gói",
        "short_name": "Kiến An Vinh",
        "url": "https://kienanvinh.vn/",
        "domain": "kienanvinh.vn",
        "slug": "xd_kienanvinh",
        "category": "Home Design & Construction",
        "category_vn": "Kiến An Vinh — Kho Mẫu Nhà & Thi Công Phía Nam",
        "tag": "xay-nha-tron-goi",
        "vibe": "Catalog Driven • Top SEO Nhà Phố • Xưởng Nội Thất Riêng",
        "location": "TP. Hồ Chí Minh",
        "desc": "Website lâu đời có lưu lượng truy cập tự nhiên lớn trong mảng thiết kế thi công nhà phố, biệt thự, tập trung vào kho mẫu thiết kế đa dạng và bảng giá thi công phần thô/trọn gói."
    },
    {
        "name": "GreenHN — Thiết Kế Kiến Trúc Xanh & Xây Nhà Trọn Gói Miền Bắc",
        "short_name": "GreenHN",
        "url": "https://greenhn.vn/",
        "domain": "greenhn.vn",
        "slug": "xd_greenhn",
        "category": "Green Architecture & Build",
        "category_vn": "GreenHN — Kiến Trúc Xanh & Thi Công Trọn Gói",
        "tag": "xay-nha-tron-goi",
        "vibe": "Fresh Modern • Mô Hình Một Cửa • Quy Trình Rõ Ràng",
        "location": "Hà Nội & Miền Bắc",
        "desc": "Trang chủ hiện đại với điểm nhấn kiến trúc xanh và dịch vụ xây nhà trọn gói một cửa từ xin phép xây dựng, thiết kế 3D đến thi công hoàn thiện."
    },
    {
        "name": "Xây Dựng An Cư — Nhà Thầu Thi Công Phần Thô & Nhà Phố TP.HCM",
        "short_name": "Xây Dựng An Cư",
        "url": "https://xaydungancu.com.vn/",
        "domain": "xaydungancu.com.vn",
        "slug": "xd_ancu",
        "category": "Residential Contractor HCMC",
        "category_vn": "Xây Dựng An Cư — Chuyên Thi Công Nhà Phố & Biệt Thự",
        "tag": "xay-nha-tron-goi",
        "vibe": "Trust-First • Nhật Ký Công Trình • Báo Giá Chi Tiết",
        "location": "TP. Hồ Chí Minh",
        "desc": "Mẫu website nhà thầu tập trung xây dựng niềm tin thực tế qua hình ảnh công trường, tiêu chuẩn kỹ thuật thi công phần thô, bảng vật tư và chính sách bảo hành dài hạn."
    },
    {
        "name": "Xây Dựng Minh Bảo — Dịch Vụ Xây Nhà Trọn Gói & Sửa Chữa Nhà",
        "short_name": "Xây Dựng Minh Bảo",
        "url": "https://minhbao.vn/",
        "domain": "minhbao.vn",
        "slug": "xd_minhbao",
        "category": "Turnkey & Renovation Contractor",
        "category_vn": "Xây Dựng Minh Bảo — Xây Mới & Cải Tạo Nhà Trọn Gói",
        "tag": "xay-nha-tron-goi",
        "vibe": "Service Clarity • Báo Giá Trọn Gói • Phễu Tư Vấn Nhanh",
        "location": "TP. Hồ Chí Minh & Miền Nam",
        "desc": "Website nhà thầu dân dụng cấu trúc rõ ràng, tập trung vào hai dịch vụ chủ lực là xây nhà trọn gói và cải tạo sửa chữa nhà với nhiều dự án thực tế bàn giao."
    },

    # --- NHÓM 3: KẾT CẤU THÉP CÔNG NGHIỆP & TỔNG THẦU QUỐC TẾ CHUẨN UI/UX ---
    {
        "name": "ATAD Steel Structure — Tổng Thầu Kết Cấu Thép & Nhà Thép Tiền Chế",
        "short_name": "ATAD Steel",
        "url": "https://atad.vn/",
        "domain": "atad.vn",
        "slug": "xd_atad",
        "category": "Global Steel Structure Leader",
        "category_vn": "Kết Cấu Thép ATAD — Thiết Kế Chuẩn Tập Đoàn Quốc Tế",
        "tag": "cong-nghiep-quoc-te",
        "vibe": "Industrial Excellence • Đa Ngôn Ngữ • Dự Án Quy Mô Toàn Cầu",
        "location": "Việt Nam & 60+ Quốc Gia",
        "desc": "Website chuẩn mực toàn cầu của doanh nghiệp kết cấu thép hàng đầu Đông Nam Á. Bố cục sắc sảo, trình bày rõ giải pháp nhà xưởng, sân bay, nhà máy công nghiệp nặng và năng lực sản xuất."
    },
    {
        "name": "BMB Steel — Thiết Kế & Thi Công Nhà Thép Tiền Chế Công Nghiệp",
        "short_name": "BMB Steel",
        "url": "https://bmbsteel.com.vn/en",
        "domain": "bmbsteel.com.vn",
        "slug": "xd_bmbsteel",
        "category": "Pre-Engineered Steel Buildings",
        "category_vn": "BMB Steel — Nhà Thép Tiền Chế & Kho Xưởng Công Nghiệp",
        "tag": "cong-nghiep-quoc-te",
        "vibe": "Clean B2B • Industrial Grid • Năng Lực Quốc Tế",
        "location": "Việt Nam & Đông Nam Á",
        "desc": "Giao diện B2B chuyên nghiệp của BMB Steel tập trung vào khách hàng công nghiệp và FDI, trình diễn trực quan hệ thống nhà xưởng, tiêu chuẩn thiết kế và mạng lưới chi nhánh quốc tế."
    },
    {
        "name": "Suffolk Construction — Tổng Thầu Công Nghệ Xây Dựng Hàng Đầu Mỹ",
        "short_name": "Suffolk Construction",
        "url": "https://suffolk.com/",
        "domain": "suffolk.com",
        "slug": "xd_suffolk",
        "category": "US Tech-Driven General Contractor",
        "category_vn": "Suffolk (Mỹ) — Chuẩn Mực UI/UX Ngành Xây Dựng Hiện Đại",
        "tag": "cong-nghiep-quoc-te",
        "vibe": "World-Class UI • Bold Typography • Construction Tech",
        "location": "Boston & Toàn Nước Mỹ",
        "desc": "Một trong những mẫu website ngành xây dựng đẹp và hiện đại nhất thế giới. Tuyên ngôn giá trị mạnh mẽ, số liệu doanh thu ấn tượng, phân tầng lĩnh vực và công nghệ xây dựng cực kỳ thuyết phục."
    },
    {
        "name": "Turner Construction — Tập Đoàn Xây Dựng Thương Mại Lớn Nhất Mỹ",
        "short_name": "Turner Construction",
        "url": "https://www.turnerconstruction.com/",
        "domain": "turnerconstruction.com",
        "slug": "xd_turner",
        "category": "Global Commercial Contractor",
        "category_vn": "Turner Construction (Mỹ) — Tổng Thầu Thương Mại Số 1 Mỹ",
        "tag": "cong-nghiep-quoc-te",
        "vibe": "Asymmetrical Grid • Editorial Corporate • Mega Projects",
        "location": "New York, Mỹ & Toàn Cầu",
        "desc": "Website tập đoàn xây dựng hàng đầu Hoa Kỳ với lưới thiết kế bất đối xứng tinh tế, typography hiện đại, trình diễn sân vận động, bệnh viện, trung tâm dữ liệu và tòa nhà chọc trời."
    },
    {
        "name": "Bechtel — Tập Đoàn Kỹ Thuật & Tổng Thầu Hạ Tầng Toàn Cầu",
        "short_name": "Bechtel",
        "url": "https://www.bechtel.com/",
        "domain": "bechtel.com",
        "slug": "xd_bechtel",
        "category": "Global Engineering & Construction",
        "category_vn": "Bechtel (Mỹ) — Bậc Thầy Tổ Chức Dữ Liệu Hạ Tầng Toàn Cầu",
        "tag": "cong-nghiep-quoc-te",
        "vibe": "Structured Enterprise • High Clarity • Megaproject Showcase",
        "location": "Virginia, Mỹ & Toàn Cầu",
        "desc": "Hình mẫu kinh điển về cách tổ chức thông tin cho tập đoàn xây dựng đa ngành (hạ tầng, năng lượng, sản xuất, môi trường) với lưới bố cục cực kỳ khoa học và dễ đọc."
    },
    {
        "name": "Skanska Group — Tập Đoàn Xây Dựng & Phát Triển Xanh Bắc Âu",
        "short_name": "Skanska Group",
        "url": "https://www.skanska.com/group/en",
        "domain": "skanska.com",
        "slug": "xd_skanska",
        "category": "Nordic Sustainable Construction",
        "category_vn": "Skanska (Thụy Điển) — Phong Cách Bắc Âu Tối Giản & Bền Vững",
        "tag": "cong-nghiep-quoc-te",
        "vibe": "Scandinavian Minimal • Green Building • Corporate Clarity",
        "location": "Stockholm, Thụy Điển & Toàn Cầu",
        "desc": "Website của ông lớn xây dựng Bắc Âu Skanska nổi bật với phong cách tối giản thanh lịch, đề cao tính bền vững, an toàn lao động và các công trình hạ tầng xanh."
    },
    {
        "name": "Olson Kundig — Studio Kiến Trúc & Thi Công Công Trình Độc Bản",
        "short_name": "Olson Kundig",
        "url": "https://olsonkundig.com/",
        "domain": "olsonkundig.com",
        "slug": "xd_olsonkundig",
        "category": "Architectural Design-Build Icon",
        "category_vn": "Olson Kundig (Mỹ) — Tối Giản Nghệ Thuật & Ảnh Toàn Màn Hình",
        "tag": "cong-nghiep-quoc-te",
        "vibe": "Ultra Minimal • Full-Bleed Architecture • High-End Prestige",
        "location": "Seattle, Mỹ & Toàn Cầu",
        "desc": "Hình mẫu đỉnh cao của triết lý 'công trình là lời thuyết trình mạnh nhất': giao diện tối giản tối đa, ảnh kiến trúc toàn màn hình đầy cảm xúc và hệ thống lọc dự án mượt mà."
    }
]

results = []
passed_list = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for idx, site in enumerate(pool, 1):
        site["id"] = f"xd{idx:02d}"
        site["industry"] = "xay-dung"
        site["industry_name"] = "Mảng Xây Dựng"
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
                    '.elementor-popup-modal .dialog-close-button'
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

print(f"\n=== TỔNG KẾT QA: ĐẠT {len(passed_list)}/{len(pool)} MẪU ===")
for r in results:
    print(f"  {r[0]:20s} | {r[1]:28s} | {r[2]:9s} | {r[3]}")
