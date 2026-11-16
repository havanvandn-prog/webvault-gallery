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
    capture_smart_clean,
    compress_tri_layer,
    verify_captured_image,
    setup_page_protection,
)
from playwright.sync_api import sync_playwright

output_dir = os.path.join(BASE_DIR, "Anh_Chup_Website")
kho_webp_dir = os.path.join(BASE_DIR, "Kho_Anh_Webp")
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "phong_thuy_metadata.json")

os.makedirs(output_dir, exist_ok=True)
os.makedirs(kho_webp_dir, exist_ok=True)
os.makedirs(os.path.dirname(metadata_file), exist_ok=True)

primary_websites = [
    # NHÓM 1: TƯ VẤN PHONG THỦY & KIẾN TRÚC QUỐC TẾ (LUXURY & MODERN UI/UX)
    {
        "name": "Dear Modern — Kiến Trúc & Phong Thủy Hiện Đại (Cliff Tan)",
        "short_name": "Dear Modern",
        "url": "https://www.dearmodern.com/",
        "domain": "dearmodern.com",
        "slug": "phong_thuy_dear_modern",
        "industry": "phong-thuy",
        "industry_name": "Phong Thủy & Kiến Trúc Tâm Linh",
        "category": "Modern Form Feng Shui & Architecture",
        "category_vn": "Phong Thủy Kiến Trúc & Quy Hoạch Không Gian Hiện Đại",
        "tag": "modern-feng-shui",
        "vibe": "Tối Giản Đương Đại • Typography Sắc Sảo • Triết Lý Không Gian Logic",
        "location": "London (Anh) / Toàn cầu",
        "desc": "Thương hiệu phong thủy kiến trúc hiện đại nổi tiếng toàn cầu của KTS Cliff Tan. Giao diện tối giản chuẩn studio thiết kế quốc tế, kết hợp phân tích luồng khí (Form Feng Shui) với bố cục nội thất đương đại dễ hiểu, thu hút giới trẻ và chủ nhà hiện đại."
    },
    {
        "name": "Feng Shui Concepts — Master Jane Langof (Phong Thủy Hạng Sang Úc)",
        "short_name": "Feng Shui Concepts",
        "url": "https://www.fengshuiconcepts.com.au/",
        "domain": "fengshuiconcepts.com.au",
        "slug": "phong_thuy_feng_shui_concepts",
        "industry": "phong-thuy",
        "industry_name": "Phong Thủy & Kiến Trúc Tâm Linh",
        "category": "Luxury Architectural Feng Shui",
        "category_vn": "Tư Vấn Phong Thủy Biệt Thự & Dự Án BĐS Cao Cấp",
        "tag": "luxury-architectural",
        "vibe": "Quiet Luxury • Bảng Màu Kem & Vàng Đồng • Case Study Kiến Trúc",
        "location": "Sydney (Úc)",
        "desc": "Website của Master Jane Langof đạt nhiều giải thưởng thiết kế và phong thủy tại Úc. Định vị phong thủy như một lớp giá trị tất yếu của kiến trúc hạng sang với hình ảnh biệt thự nghệ thuật, khoảng thở rộng và phễu đặt lịch tư vấn riêng tư."
    },
    {
        "name": "Joey Yap — Học Viện & Master Phong Thủy Hàng Đầu Thế Giới",
        "short_name": "Joey Yap Academy",
        "url": "https://home.joeyyap.com/",
        "domain": "joeyyap.com",
        "slug": "phong_thuy_joey_yap",
        "industry": "phong-thuy",
        "industry_name": "Phong Thủy & Kiến Trúc Tâm Linh",
        "category": "Global Feng Shui & BaZi Authority",
        "category_vn": "Hệ Sinh Thái Đào Tạo Phong Thủy, Bát Tự & Huyền Học Toàn Cầu",
        "tag": "global-academy",
        "vibe": "Chuyên Nghiệp Đẳng Cấp • Personal Branding Mạnh • Phễu Khóa Học & Sách",
        "location": "Kuala Lumpur / Quốc tế",
        "desc": "Cổng thông tin chính thức của Dato' Joey Yap — chuyên gia phong thủy và Bát Tự hàng đầu thế giới. Thiết kế web chuẩn doanh nghiệp giáo dục quốc tế, xây dựng uy tín chuyên gia qua hệ thống sách, khóa học và công cụ tra cứu mệnh lý."
    },
    {
        "name": "Way Fengshui Group — Tập Đoàn Phong Thủy Hàng Đầu Singapore",
        "short_name": "Way Fengshui Group",
        "url": "https://www.wayfengshui.com/",
        "domain": "wayfengshui.com",
        "slug": "phong_thuy_way_fengshui",
        "industry": "phong-thuy",
        "industry_name": "Phong Thủy & Kiến Trúc Tâm Linh",
        "category": "Corporate & Residential Feng Shui Group",
        "category_vn": "Tập Đoàn Tư Vấn Phong Thủy Doanh Nghiệp & Nhà Ở Singapore",
        "tag": "corporate-feng-shui",
        "vibe": "Hiện Đại Chuyên Sâu • Chuẩn Á Đông Đương Đại • Đặt Lịch Tư Vấn Rõ Ràng",
        "location": "Singapore",
        "desc": "Một trong những tập đoàn tư vấn phong thủy quy mô và uy tín nhất Singapore. Website phân tách rành mạch dịch vụ phong thủy nhà ở, doanh nghiệp, xem Bát Tự và đặt tên, sử dụng tông màu trang nhã kết hợp họa tiết phương Đông hiện đại."
    },
    {
        "name": "Master Sean Chan — Chuyên Gia Bát Tự & Phong Thủy Cổ Học Singapore",
        "short_name": "Master Sean Chan",
        "url": "https://www.masterseanchan.com/",
        "domain": "masterseanchan.com",
        "slug": "phong_thuy_master_sean_chan",
        "industry": "phong-thuy",
        "industry_name": "Phong Thủy & Kiến Trúc Tâm Linh",
        "category": "Classical Chinese Metaphysics Editorial",
        "category_vn": "Tư Vấn Bát Tự, Tử Vi Đẩu Số & Phong Thủy Cổ Học",
        "tag": "editorial-metaphysics",
        "vibe": "Editorial Sang Trọng • Chữ Serif Cổ Điển • Phễu Tư Vấn Cao Cấp",
        "location": "Singapore",
        "desc": "Trang cá nhân của chuyên gia Sean Chan nổi tiếng với văn phong khoa học, loại bỏ mê tín dị đoan. Giao diện mang phong cách tạp chí cao cấp (Editorial), nội dung blog chuyên sâu giúp giữ chân người đọc và chuyển đổi đặt lịch tư vấn trực tiếp."
    },
    {
        "name": "Feng Shui Agency London — Tư Vấn Phong Thủy Thương Mại & Nhà Ở",
        "short_name": "Feng Shui Agency UK",
        "url": "https://www.fengshuiagency.com/",
        "domain": "fengshuiagency.com",
        "slug": "phong_thuy_feng_shui_agency",
        "industry": "phong-thuy",
        "industry_name": "Phong Thủy & Kiến Trúc Tâm Linh",
        "category": "Bespoke Property & Commercial Feng Shui",
        "category_vn": "Tư Vấn Phong Thủy Bất Động Sản & Thương Hiệu Tại Anh Quốc",
        "tag": "agency-luxury",
        "vibe": "Tinh Tế Châu Âu • Bố Cục Cân Xứng • Tôn Vinh Không Gian Kiến Trúc",
        "location": "London (Anh)",
        "desc": "Agency chuyên tư vấn phong thủy cho các căn hộ cao cấp, văn phòng tài chính và khách sạn tại London. Giao diện nhấn mạnh tính thẩm mỹ không gian, kết hợp hình ảnh nội thất tinh tế cùng quy trình thẩm định bản vẽ mặt bằng chuyên nghiệp."
    },
    {
        "name": "The Tao of Dana — Phong Thủy Sáng Tạo & Chữa Lành Không Gian",
        "short_name": "The Tao of Dana",
        "url": "https://fengshuidana.com/",
        "domain": "fengshuidana.com",
        "slug": "phong_thuy_tao_of_dana",
        "industry": "phong-thuy",
        "industry_name": "Phong Thủy & Kiến Trúc Tâm Linh",
        "category": "Modern Lifestyle & Holistic Feng Shui",
        "category_vn": "Phong Thủy Đời Sống Hiện Đại & Thanh Lọc Năng Lượng Nhà Ở",
        "tag": "holistic-lifestyle",
        "vibe": "Nghệ Thuật Sống Nhẹ Nhàng • Tông Trắng Kem Thanh Thoát • Tối Ưu Lead Magnet",
        "location": "Los Angeles (Mỹ)",
        "desc": "Nền tảng phong thủy lifestyle hiện đại của Dana Claudat. Giao diện mang hơi thở tạp chí nghệ thuật và wellness phương Tây, kết hợp màu sắc tươi sáng, câu chuyện truyền cảm hứng và phễu đăng ký khóa học online mượt mà."
    },

    # NHÓM 2: TƯ VẤN PHONG THỦY, KIẾN TRÚC & TRA CỨU TỬ VI VIỆT NAM (TOP SEO & AUTHORITY)
    {
        "name": "Phong Thủy Phùng Gia — Master Phùng Phương (Chính Phái & Khoa Học)",
        "short_name": "Phong Thủy Phùng Gia",
        "url": "https://phongthuyphunggia.com/",
        "domain": "phongthuyphunggia.com",
        "slug": "phong_thuy_phung_gia",
        "industry": "phong-thuy",
        "industry_name": "Phong Thủy & Kiến Trúc Tâm Linh",
        "category": "Master Feng Shui & Consulting System",
        "category_vn": "Hệ Thống Tư Vấn Phong Thủy Chính Phái & Vật Phẩm Cao Cấp",
        "tag": "vn-top-master",
        "vibe": "Chuẩn Thương Hiệu Lớn • Tông Đỏ Đô & Vàng Kim Quyền Uy • Top SEO",
        "location": "Hà Nội & TP.HCM",
        "desc": "Thương hiệu phong thủy nổi tiếng do Master Phùng Phương sáng lập (thành viên Hiệp hội Phong thủy Thế giới IFSA). Website có cấu trúc bài bản kết hợp thương hiệu cá nhân, danh mục dịch vụ nhà ở/doanh nghiệp và hệ thống bài viết SEO phủ rộng."
    },
    {
        "name": "Phong Thủy Đại Nam — Hệ Thống Tư Vấn Phong Thủy Doanh Nghiệp",
        "short_name": "Phong Thủy Đại Nam",
        "url": "https://phongthuydainam.vn/vi",
        "domain": "phongthuydainam.vn",
        "slug": "phong_thuy_dai_nam",
        "industry": "phong-thuy",
        "industry_name": "Phong Thủy & Kiến Trúc Tâm Linh",
        "category": "Corporate & Scientific Feng Shui",
        "category_vn": "Trung Tâm Phong Thủy Khoa Học & Tư Vấn Kiến Trúc Quy Mô Lớn",
        "tag": "vn-corporate",
        "vibe": "Bề Thế Chuyên Nghiệp • Tích Hợp Công Nghệ App • Hệ Thống Chi Nhánh Toàn Quốc",
        "location": "Toàn quốc (Việt Nam)",
        "desc": "Hệ thống phong thủy quy mô lớn tại Việt Nam định hướng phong thủy khoa học cho doanh nghiệp và bất động sản. Giao diện nổi bật với các gói dịch vụ rõ ràng, lịch đào tạo, hệ sinh thái chuyên gia và ứng dụng tra cứu phong thủy."
    },
    {
        "name": "Phong Thủy Tam Nguyên — Hệ Thống Tư Vấn & Pháp Khí Chính Tông",
        "short_name": "Phong Thủy Tam Nguyên",
        "url": "https://phongthuytamnguyen.com/",
        "domain": "phongthuytamnguyen.com",
        "slug": "phong_thuy_tam_nguyen",
        "industry": "phong-thuy",
        "industry_name": "Phong Thủy & Kiến Trúc Tâm Linh",
        "category": "Traditional Feng Shui & Artifacts",
        "category_vn": "Thương Hiệu Phong Thủy Lâu Đời & Pháp Khí Khai Quang",
        "tag": "vn-heritage",
        "vibe": "Bản Sắc Truyền Thống • Tông Nâu Gỗ & Vàng Cổ • Kho Kiến Thức Đồ Sộ",
        "location": "Hà Nội & TP.HCM",
        "desc": "Website chủ lực của Thầy Tam Nguyên — một trong những chuyên gia phong thủy có độ nhận diện cao nhất Việt Nam. Thiết kế giao diện đậm nét văn hóa Á Đông, phân loại vật phẩm phong thủy theo tuổi mệnh và tích hợp đặt lịch xem phong thủy."
    },
    {
        "name": "Phong Thủy Tường Minh — Master Nguyễn Thành Phương",
        "short_name": "Phong Thủy Tường Minh",
        "url": "https://phongthuytuongminh.com/",
        "domain": "phongthuytuongminh.com",
        "slug": "phong_thuy_tuong_minh",
        "industry": "phong-thuy",
        "industry_name": "Phong Thủy & Kiến Trúc Tâm Linh",
        "category": "Classical Feng Shui & Qi Men Dun Jia",
        "category_vn": "Đào Tạo & Tư Vấn Huyền Không, Kỳ Môn Độn Giáp",
        "tag": "vn-academy",
        "vibe": "Học Thuật Sâu Sắc • Bố Cục Gọn Gàng • Trình Bày Khóa Học Rõ Ràng",
        "location": "TP.HCM & Quốc tế",
        "desc": "Trung tâm đào tạo và tư vấn phong thủy chính thống theo trường phái Huyền Không và Kỳ Môn Độn Giáp. Giao diện sáng rõ, tập trung làm nổi bật lộ trình đào tạo chuyên sâu, lịch khai giảng và hồ sơ năng lực thực chiến."
    },
    {
        "name": "Phong Thủy Hoàng Trà — KTS Phong Thủy Kiến Trúc & Biệt Thự",
        "short_name": "Phong Thủy Hoàng Trà",
        "url": "https://phongthuyhoangtra.vn/",
        "domain": "phongthuyhoangtra.vn",
        "slug": "phong_thuy_hoang_tra",
        "industry": "phong-thuy",
        "industry_name": "Phong Thủy & Kiến Trúc Tâm Linh",
        "category": "Architecture & Feng Shui Integration",
        "category_vn": "Kiến Trúc Sư & Chuyên Gia Phong Thủy Nhà Ở, Dinh Thự",
        "tag": "vn-architecture",
        "vibe": "Giao Thoa Kiến Trúc & Huyền Học • Portfolio Công Trình Thực Tế",
        "location": "Hà Nội",
        "desc": "Website của KTS - Chuyên gia phong thủy Hoàng Trà (Viện Lý Học Phương Đông). Điểm mạnh của giao diện là trình diễn các công trình biệt thự, nhà phố đã kết hợp hài hòa giữa công năng kiến trúc hiện đại và phong thủy Bát trạch, Tứ trụ."
    },
    {
        "name": "Kiến Trúc Phong Thủy Nhà Xuân — Thiết Kế Nhà Đẹp Hợp Mệnh",
        "short_name": "Nhà Xuân",
        "url": "https://nhaxuan.vn/",
        "domain": "nhaxuan.vn",
        "slug": "phong_thuy_nha_xuan",
        "industry": "phong-thuy",
        "industry_name": "Phong Thủy & Kiến Trúc Tâm Linh",
        "category": "Luxury Villa & Feng Shui Design",
        "category_vn": "Thiết Kế Kiến Trúc Biệt Thự VIP & Tư Vấn Phong Thủy Nhà Ở",
        "tag": "vn-villa-design",
        "vibe": "Hình Ảnh Biệt Thự Ấn Tượng • Tin Cậy Cao • Chuyển Đổi Tư Vấn Thiết Kế",
        "location": "Hà Nội",
        "desc": "Đơn vị tiên phong kết hợp thiết kế kiến trúc cao cấp với phong thủy thực chứng tại Việt Nam. Website đầu tư mạnh vào bộ sưu tập dự án dinh thự thực tế, quy trình khảo sát đất và các bài phân tích thế đất thu hút khách hàng xây nhà."
    },
    {
        "name": "Lịch Ngày Tốt — Cổng Tra Cứu Lịch Vạn Niên & Phong Thủy Top 1 SEO",
        "short_name": "Lịch Ngày Tốt",
        "url": "https://lichngaytot.com/",
        "domain": "lichngaytot.com",
        "slug": "phong_thuy_lich_ngay_tot",
        "industry": "phong-thuy",
        "industry_name": "Phong Thủy & Kiến Trúc Tâm Linh",
        "category": "Top SEO Almanac & Astrology Portal",
        "category_vn": "Cổng Thông Tin Tra Cứu Ngày Tốt Xấu, Tử Vi & Phong Thủy Lớn Nhất VN",
        "tag": "top-seo-portal",
        "vibe": "Cổng Dữ Liệu Khổng Lồ • Tiện Ích Tra Cứu Nhanh • Lưu Lượng Truy Cập Top Đầu",
        "location": "Việt Nam",
        "desc": "Website dẫn đầu thị trường tìm kiếm Việt Nam ở các từ khóa xem ngày, lịch âm, tử vi và phong thủy nhà ở. Giao diện dạng cổng thông tin (Portal) với các widget tra cứu nhanh ngày hoàng đạo, đổi ngày âm dương và phân chuyên mục khoa học."
    },

    # NHÓM 3: TRANG SỨC ĐÁ QUÝ, VÀNG & TRẦM HƯƠNG PHONG THỦY (E-COMMERCE & CRAFT)
    {
        "name": "Thiên Mộc Hương — Thương Hiệu Trầm Hương & Phong Thủy Di Sản",
        "short_name": "Thiên Mộc Hương",
        "url": "https://thienmochuong.com/",
        "domain": "thienmochuong.com",
        "slug": "phong_thuy_thien_moc_huong",
        "industry": "phong-thuy",
        "industry_name": "Phong Thủy & Kiến Trúc Tâm Linh",
        "category": "Luxury Agarwood & Spiritual Craft",
        "category_vn": "Thương Hiệu Trang Sức Trầm Hương & Đá Phong Thủy Hàng Đầu VN",
        "tag": "luxury-agarwood",
        "vibe": "Ấm Áp Trầm Mặc • Ảnh Chụp Studio Cao Cấp • Trải Nghiệm E-Commerce Mượt",
        "location": "TP.HCM & Hà Nội",
        "desc": "Thương hiệu trầm hương cao cấp nổi bật với câu chuyện di sản hơn 35 năm và sản phẩm từng làm quà tặng nguyên thủ. Giao diện e-commerce chuẩn mực với gam nâu trầm sang trọng, lọc sản phẩm theo cung mệnh và hình ảnh chế tác tinh xảo."
    },
    {
        "name": "Ancarat Jewelry — Định Chế Vàng & Bạc Phong Thủy 24K",
        "short_name": "Ancarat",
        "url": "https://ancarat.com/",
        "domain": "ancarat.com",
        "slug": "phong_thuy_ancarat",
        "industry": "phong-thuy",
        "industry_name": "Phong Thủy & Kiến Trúc Tâm Linh",
        "category": "24K Feng Shui Gold & Silver Jewelry",
        "category_vn": "Trang Sức Vàng Phong Thủy 24K & Bạc Tích Trữ Cao Cấp",
        "tag": "fengshui-gold",
        "vibe": "Trang Sức Xa Xỉ • Bảng Giá Kim Loại Trực Tiếp • Giao Diện Bán Lẻ Hiện Đại",
        "location": "TP.HCM & Hà Nội",
        "desc": "Thương hiệu tiên phong ứng dụng công nghệ 3D/5D chế tác charm vàng 24K phong thủy tại Việt Nam. Website tối ưu trải nghiệm mua sắm trang sức trực tuyến với banner theo mùa vụ, phân loại linh vật theo năm tuổi và tích hợp giá vàng bạc minh bạch."
    },
    {
        "name": "LIUGEMS — Đá Quý Phong Thủy Cá Nhân Hóa Theo Bát Tự",
        "short_name": "LIUGEMS",
        "url": "https://liu.com.vn/",
        "domain": "liu.com.vn",
        "slug": "phong_thuy_liugems",
        "industry": "phong-thuy",
        "industry_name": "Phong Thủy & Kiến Trúc Tâm Linh",
        "category": "Personalized Feng Shui Gemstone Jewelry",
        "category_vn": "Trang Sức Đá Quý Thiên Nhiên Tư Vấn Theo Dụng Thần Bát Tự",
        "tag": "modern-gemstone",
        "vibe": "Thanh Lịch Hiện Đại • Định Vị Chuyên Gia Đá Quý • Nội Dung Giáo Dục Sâu",
        "location": "TP.HCM",
        "desc": "Thương hiệu đá quý phong thủy thế hệ mới thoát khỏi lối mòn tâm linh cũ kỹ, kết hợp kiến thức Bát Tự với trang sức thiết kế tinh tế. Giao diện web sạch sẽ, nhiều ảnh chụp macro đá tự nhiên đẹp mắt và chuyên mục kiến thức ngũ hành chuyên sâu."
    },
    {
        "name": "KAIGOLD — Trang Sức Vàng Phong Thủy & Ngọc Cẩm Thạch",
        "short_name": "KAIGOLD",
        "url": "https://kaigold.vn/",
        "domain": "kaigold.vn",
        "slug": "phong_thuy_kaigold",
        "industry": "phong-thuy",
        "industry_name": "Phong Thủy & Kiến Trúc Tâm Linh",
        "category": "Feng Shui Gold & Jadeite Store",
        "category_vn": "Trang Sức Vàng 9999 Phong Thủy, Kim Cương & Ngọc Cẩm Thạch",
        "tag": "gold-jade-ecommerce",
        "vibe": "Sang Trọng Nổi Bật • Bộ Sưu Tập Tỳ Hưu & Kim Tiền • Chuẩn E-Commerce",
        "location": "TP.HCM",
        "desc": "Website chuyên doanh vàng phong thủy, nhẫn kim tiền và ngọc cẩm thạch thiên nhiên. Thiết kế làm nổi bật chất liệu vàng ánh kim trên nền sáng sạch, bố cục danh mục theo mệnh và linh vật giúp khách hàng tìm đúng sản phẩm cầu tài chỉ sau 2 cú nhấp."
    },
    {
        "name": "Mixi — Trang Sức Đá Quý Phong Thủy Tự Nhiên",
        "short_name": "Phong Thủy Mixi",
        "url": "https://mixi.vn/",
        "domain": "mixi.vn",
        "slug": "phong_thuy_mixi",
        "industry": "phong-thuy",
        "industry_name": "Phong Thủy & Kiến Trúc Tâm Linh",
        "category": "Natural Feng Shui Crystal Store",
        "category_vn": "Hệ Thống Vòng Tay Đá Quý & Vật Phẩm Phong Thủy Tự Nhiên",
        "tag": "crystal-ecommerce",
        "vibe": "Danh Mục Đa Dạng • Phân Loại Theo Mệnh Kim Mộc Thủy Hỏa Thổ Rõ Ràng",
        "location": "Hà Nội & TP.HCM",
        "desc": "Một trong những thương hiệu bán lẻ đá quý phong thủy lâu năm tại Việt Nam. Website tối ưu bộ lọc theo Ngũ Hành (Kim - Mộc - Thủy - Hỏa - Thổ), vật phẩm chiêu tài (Tỳ Hưu, Hồ Ly, Quả cầu) và chính sách kiểm định đá tự nhiên minh bạch."
    },
    {
        "name": "Energy Muse — Thương Hiệu Đá Quý Năng Lượng & Trang Sức Mỹ",
        "short_name": "Energy Muse",
        "url": "https://energymuse.com/",
        "domain": "energymuse.com",
        "slug": "phong_thuy_energy_muse",
        "industry": "phong-thuy",
        "industry_name": "Phong Thủy & Kiến Trúc Tâm Linh",
        "category": "International Crystal & Energy Jewelry",
        "category_vn": "Thương Hiệu Đá Năng Lượng & Trang Sức Phong Thủy Quốc Tế",
        "tag": "intl-crystal-brand",
        "vibe": "Shopify Cao Cấp • Filter Theo Mục Đích (Tài Lộc, Bình An) • Storytelling Cuốn Hút",
        "location": "California (Mỹ)",
        "desc": "Thương hiệu đá quý năng lượng hàng đầu tại Mỹ với thiết kế Shopify chuẩn mực quốc tế. Giao diện nổi bật nhờ cách phân loại sản phẩm theo ý định (Wealth, Protection, Love), hình ảnh lifestyle tinh tế và trang sản phẩm giàu cảm xúc."
    }
]

backup_websites = [
    {
        "name": "Chuyên Gia Phong Thủy Nguyễn Ngoan — Mandala Phong Thủy",
        "short_name": "Nguyễn Ngoan",
        "url": "https://chuyengianguyenngoan.com/",
        "domain": "chuyengianguyenngoan.com",
        "slug": "phong_thuy_nguyen_ngoan",
        "industry": "phong-thuy",
        "industry_name": "Phong Thủy & Kiến Trúc Tâm Linh",
        "category": "Executive Business Feng Shui",
        "category_vn": "Phong Thủy Quản Trị Doanh Nghiệp & Tài Chính",
        "tag": "business-feng-shui",
        "vibe": "Doanh Nhân Chuyên Nghiệp • Định Vị Phong Thủy Quản Trị",
        "location": "TP.HCM",
        "desc": "Website của chuyên gia phong thủy Nguyễn Ngoan chuyên sâu về phong thủy quản trị kinh doanh cho doanh nhân và tập đoàn tại miền Nam."
    },
    {
        "name": "Phong Thủy Vượng — Dịch Vụ Tư Vấn Phong Thủy Tam Nguyên",
        "short_name": "Phong Thủy Vượng",
        "url": "https://phongthuyvuong.com/",
        "domain": "phongthuyvuong.com",
        "slug": "phong_thuy_vuong",
        "industry": "phong-thuy",
        "industry_name": "Phong Thủy & Kiến Trúc Tâm Linh",
        "category": "Residential & Commercial Feng Shui Service",
        "category_vn": "Dịch Vụ Tư Vấn Thiết Kế Phong Thủy Nhà Ở & Âm Trạch",
        "tag": "vn-service",
        "vibe": "Tập Trung Chuyển Đổi Dịch Vụ • Bảng Giá & Quy Trình Rõ Ràng",
        "location": "Hà Nội & TP.HCM",
        "desc": "Cổng dịch vụ tư vấn chuyên biệt của hệ thống Phong Thủy Tam Nguyên, trình bày chi tiết quy trình khảo sát, hồ sơ phong thủy và các gói tư vấn nhà ở."
    },
    {
        "name": "Phong Thủy Tạ Gia — Đào Tạo & Tư Vấn Phong Thủy Thực Chiến",
        "short_name": "Phong Thủy Tạ Gia",
        "url": "https://phongthuytagia.com/",
        "domain": "phongthuytagia.com",
        "slug": "phong_thuy_ta_gia",
        "industry": "phong-thuy",
        "industry_name": "Phong Thủy & Kiến Trúc Tâm Linh",
        "category": "Feng Shui Training & Consulting",
        "category_vn": "Đào Tạo Phong Thủy Thực Chiến & Tư Vấn Trấn Trạch",
        "tag": "vn-training",
        "vibe": "Truyền Thống Chuẩn Mực • Khóa Học Nghề Phong Thủy Thực Tế",
        "location": "Hà Nội",
        "desc": "Website của Phong Thủy Tạ Gia do Thầy Tạ Hậu sáng lập, chuyên đào tạo nghề phong thủy ứng dụng, xem ngày giờ và tư vấn quy hoạch công trình."
    },
    {
        "name": "Siêu Thị Phong Thủy Joca — Vật Phẩm Đá Quý Phong Thủy",
        "short_name": "Siêu Thị Joca",
        "url": "https://joca.vn/",
        "domain": "joca.vn",
        "slug": "phong_thuy_joca",
        "industry": "phong-thuy",
        "industry_name": "Phong Thủy & Kiến Trúc Tâm Linh",
        "category": "Feng Shui Marketplace & Statues",
        "category_vn": "Siêu Thị Vật Phẩm, Tượng Đá & Quả Cầu Phong Thủy",
        "tag": "vn-marketplace",
        "vibe": "Kho Sản Phẩm Phong Phú • Tối Ưu SEO Danh Mục",
        "location": "TP.HCM",
        "desc": "Hệ thống bán lẻ vật phẩm phong thủy trưng bày bàn làm việc, phòng khách như quả cầu đá, tỳ hưu, thiềm thừ, cây tài lộc."
    },
    {
        "name": "Văn Hóa Trầm Hương — Chuỗi Hạt & Dụng Cụ Thưởng Trầm",
        "short_name": "Văn Hóa Trầm Hương",
        "url": "https://www.vanhoatramhuong.com/",
        "domain": "vanhoatramhuong.com",
        "slug": "phong_thuy_van_hoa_tram_huong",
        "industry": "phong-thuy",
        "industry_name": "Phong Thủy & Kiến Trúc Tâm Linh",
        "category": "Agarwood & Meditation Lifestyle",
        "category_vn": "Chuỗi Hạt Trầm Hương 108 Hạt & Vật Phẩm Thiền Định",
        "tag": "vn-agarwood",
        "vibe": "Thiền Định An Nhiên • Trầm Tự Nhiên Nguyên Chất",
        "location": "TP.HCM",
        "desc": "Thương hiệu chuyên cung cấp vòng tay trầm hương thiên nhiên, chuỗi 108 hạt và dụng cụ xông trầm cao cấp phục vụ thiền định và phong thủy."
    },
    {
        "name": "Phong Thủy Số — Cổng Tra Cứu Hướng Nhà & Tử Vi Trực Tuyến",
        "short_name": "Phong Thủy Số",
        "url": "https://phongthuyso.vn/",
        "domain": "phongthuyso.vn",
        "slug": "phong_thuy_so",
        "industry": "phong-thuy",
        "industry_name": "Phong Thủy & Kiến Trúc Tâm Linh",
        "category": "Online Feng Shui & Horoscope Tools",
        "category_vn": "Công Cụ Xem Hướng Nhà, Sim Phong Thủy & Tử Vi Trực Tuyến",
        "tag": "seo-tools",
        "vibe": "Nhiều Công Cụ Tính Toán Tự Động • Traffic Tự Nhiên Cao",
        "location": "Việt Nam",
        "desc": "Cổng tra cứu trực tuyến cung cấp công cụ tính Bát trạch, xem tuổi làm nhà, hướng bàn làm việc và phân tích phong thủy đời sống."
    },
    {
        "name": "Luminous Spaces — Modern Five Elements Feng Shui",
        "short_name": "Luminous Spaces",
        "url": "https://luminousspaces.com/",
        "domain": "luminousspaces.com",
        "slug": "phong_thuy_luminous_spaces",
        "industry": "phong-thuy",
        "industry_name": "Phong Thủy & Kiến Trúc Tâm Linh",
        "category": "Biophilic & Five Elements Interior",
        "category_vn": "Phong Thủy Ngũ Hành & Thiết Kế Nội Thất Thuận Tự Nhiên",
        "tag": "biophilic-fengshui",
        "vibe": "Tươi Mát Sinh Thái • Kết Hợp Biophilic Design & Ngũ Hành",
        "location": "New York (Mỹ)",
        "desc": "Website của chuyên gia Maureen K. Calamia kết hợp phong thủy Ngũ Hành với kiến trúc xanh (Biophilic Design) mang thiên nhiên vào không gian sống."
    },
]

def dismiss_popups(page):
    try:
        page.evaluate("""() => {
            const selectors = [
                '.modal', '.popup', '#onesignal-slidedown-dialog',
                '.cookie-notice', '#cookie-notice', '.fancybox-overlay',
                '[class*="newsletter-popup"]', '[id*="newsletter-popup"]',
                '.agree-button', '#cookie-law-info-bar', '.cky-consent-container',
                '#onetrust-consent-sdk', '.cc-window', '.klaviyo-form',
                '.tawk-min-container', '#fb-root', '.zalo-chat-widget',
                '[class*="chat-widget"]', '[id*="chat-widget"]', '.hotline-phone-ring'
            ];
            selectors.forEach(s => {
                document.querySelectorAll(s).forEach(el => {
                    el.style.setProperty('display', 'none', 'important');
                    el.style.setProperty('visibility', 'hidden', 'important');
                });
            });
        }""")
    except Exception:
        pass

def try_capture_item(browser, item, item_id):
    slug = item["slug"]
    filename = f"{slug}.png"
    filepath = os.path.join(output_dir, filename)
    thumb_name = f"{slug}_thumb.webp"
    full_name = f"{slug}_full.webp"
    fb_name = f"{slug}_fb.png"
    thumb_path = os.path.join(kho_webp_dir, thumb_name)
    full_path = os.path.join(kho_webp_dir, full_name)
    fb_path = os.path.join(kho_webp_dir, fb_name)

    # Nếu đã có sẵn & đạt chuẩn thì giữ nguyên
    if os.path.exists(filepath) and os.path.exists(full_path) and os.path.exists(thumb_path):
        ok, audit_msg = verify_captured_image(full_path)
        if ok:
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            thumb_kb = round(os.path.getsize(thumb_path) / 1024, 1)
            full_kb = round(os.path.getsize(full_path) / 1024, 1)
            fb_kb = round(os.path.getsize(fb_path) / 1024, 1) if os.path.exists(fb_path) else 0
            print(f"  -> Đã tồn tại & đạt chuẩn: {audit_msg}", flush=True)
            return True, {
                "id": item_id,
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
            }

    context = browser.new_context(
        viewport={"width": 1440, "height": 900},
        ignore_https_errors=True,
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    page = context.new_page()
    setup_page_protection(page)

    max_retries = 2
    for attempt in range(max_retries):
        try:
            scroll_delay = 0.22 if attempt == 0 else 0.35
            page.goto(item["url"], wait_until="domcontentloaded", timeout=45000)
            try:
                page.wait_for_load_state("networkidle", timeout=8000)
            except Exception:
                pass
            time.sleep(2.5 if attempt == 0 else 4.0)

            # Kiểm tra trang lỗi / Cloudflare challenge trên DOM
            title_lower = (page.title() or "").lower()
            if any(k in title_lower for k in ["just a moment", "attention required", "access denied", "403 forbidden", "404 not found"]):
                print(f"  -> Bị chặn hoặc trang lỗi (title: {page.title()[:50]})", flush=True)
                break

            dismiss_popups(page)
            capture_smart_clean(page, filepath, viewport_height=900, scroll_delay=scroll_delay)
            thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb = compress_tri_layer(filepath, slug, kho_webp_dir)
            ok, audit_msg = verify_captured_image(full_path)

            if ok:
                print(f"  -> THÀNH CÔNG: {audit_msg} (Thumb {thumb_kb}KB, Full {full_kb}KB)", flush=True)
                context.close()
                return True, {
                    "id": item_id,
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
                }
            else:
                print(f"  -> CẢNH BÁO KIỂM ĐỊNH LẦN {attempt+1}: {audit_msg}. Đang Self-Healing...", flush=True)
                time.sleep(2.0)
        except Exception as e:
            print(f"  -> LỖI CHỤP LẦN {attempt+1}: {str(e)[:120]}", flush=True)
            time.sleep(2.0)

    context.close()
    return False, None

print("=== BẮT ĐẦU CHỤP FULL-PAGE 1440PX CHO 20 MẪU PHONG THỦY ===", flush=True)
final_metadata = []
failed_items = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    pool = list(primary_websites) + list(backup_websites)

    for item in pool:
        if len(final_metadata) >= 20:
            break
        idx = len(final_metadata) + 1
        item_id = f"pt{idx:02d}"
        print(f"\n[{idx}/20 | ID: {item_id}] Đang chụp: {item['name']} ({item['url']})", flush=True)
        ok, record = try_capture_item(browser, item, item_id)
        if ok:
            final_metadata.append(record)
        else:
            print(f"  -> Loại bỏ & chuyển sang mẫu dự phòng: {item['url']}", flush=True)
            failed_items.append(item["url"])

    browser.close()

with open(metadata_file, "w", encoding="utf-8") as f:
    json.dump(final_metadata, f, ensure_ascii=False, indent=2)

print(f"\n=== HOÀN TẤT CHỤP! ĐẠT CHUẨN: {len(final_metadata)}/20 ===", flush=True)
if failed_items:
    print("Các URL bị loại do lỗi/chặn:", failed_items, flush=True)
