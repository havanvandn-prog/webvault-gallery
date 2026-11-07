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
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "lap_mang_fpt_metadata.json")

os.makedirs(output_dir, exist_ok=True)
os.makedirs(kho_webp_dir, exist_ok=True)
os.makedirs(os.path.dirname(metadata_file), exist_ok=True)

websites = [
    # NHÓM 1: CỔNG TẬP ĐOÀN & KÊNH BÁN HÀNG QUỐC GIA (BRAND AUTHORITY)
    {
        "id": "fpt01",
        "name": "FPT Telecom (Trang Chủ Tập Đoàn)",
        "short_name": "FPT Telecom Portal",
        "url": "https://fpt.vn/",
        "domain": "fpt.vn",
        "slug": "fpt_vn",
        "industry": "lap-mang-fpt",
        "industry_name": "Lắp Mạng FPT (Google Ads)",
        "category": "Official Enterprise Telecom Portal",
        "category_vn": "Cổng Thông Tin Tập Đoàn & Thương Hiệu Chính Thống",
        "tag": "brand-authority",
        "vibe": "Chính Thống & Đẳng Cấp Tập Đoàn",
        "location": "Toàn quốc",
        "desc": "Cổng thông tin chính thức của FPT Telecom. Thiết kế hiện đại chuẩn tập đoàn công nghệ hàng đầu, trình bày toàn diện hệ sinh thái: Cáp quang WiFi 6/7, Truyền hình FPT Play, FPT Camera AI và FPT Smart Home với tính thẩm mỹ và độ tin cậy tuyệt đối."
    },
    {
        "id": "fpt02",
        "name": "Mạng FPT Toàn Quốc",
        "short_name": "Mạng FPT",
        "url": "https://mangfpt.vn/",
        "domain": "mangfpt.vn",
        "slug": "mangfpt_vn",
        "industry": "lap-mang-fpt",
        "industry_name": "Lắp Mạng FPT (Google Ads)",
        "category": "Nationwide Top Distributor Hub",
        "category_vn": "Kênh Phân Phối Cáp Quang Quy Mô Lớn Nhất Toàn Quốc",
        "tag": "brand-authority",
        "vibe": "Trực Quan & Đầy Đủ Bảng Cước",
        "location": "Toàn quốc (Hà Nội, TP.HCM, 63 tỉnh)",
        "desc": "Kênh bán hàng đại lý có lưu lượng truy cập hàng đầu ngành viễn thông. Cấu trúc Hero chào giá rõ ràng, bảng giá các gói cước Giga, Sky, Meta phân cấp chuẩn xác, tích hợp form tư vấn lắp đặt và danh sách khuyến mãi tặng modem Wi-Fi 6."
    },
    {
        "id": "fpt03",
        "name": "Cổng Đăng Ký FPT Telecom",
        "short_name": "FPT Telecom VN",
        "url": "https://fpt-vn.vn/",
        "domain": "fpt-vn.vn",
        "slug": "fpt_vn_vn",
        "industry": "lap-mang-fpt",
        "industry_name": "Lắp Mạng FPT (Google Ads)",
        "category": "High-Efficiency Registration Hub",
        "category_vn": "Cổng Tiếp Nhận Đăng Ký Trực Tuyến Toàn Quốc",
        "tag": "brand-authority",
        "vibe": "Rõ Ràng & Chuẩn Chuyển Đổi",
        "location": "Toàn quốc",
        "desc": "Trang thông tin tổng hợp với cấu trúc phân nhóm gói cước kinh điển: Internet cá nhân, Combo Internet + Truyền hình cáp FPT Play, và Gói Doanh nghiệp băng thông lớn. Hotline và nút Zalo tư vấn được neo cố định giúp khách gọi ngay."
    },
    {
        "id": "fpt04",
        "name": "FPT Telecom Net VN",
        "short_name": "FPT Telecom Net",
        "url": "https://fpttelecom.net.vn/",
        "domain": "fpttelecom.net.vn",
        "slug": "fpttelecom_net_vn",
        "industry": "lap-mang-fpt",
        "industry_name": "Lắp Mạng FPT (Google Ads)",
        "category": "Reputable Long-standing Distributor",
        "category_vn": "Đại Lý Viễn Thông Uy Tín Lâu Năm",
        "tag": "brand-authority",
        "vibe": "Tin Cậy & Đa Dạng Gói Cước",
        "location": "Toàn quốc",
        "desc": "Trang phân phối dịch vụ FPT kỳ cựu với hệ thống phân chia giá cước theo khu vực nội thành, ngoại thành và các tỉnh rõ rệt. Cung cấp chi tiết các chính sách tặng tháng cước khi thanh toán trước 6 tháng hoặc 12 tháng."
    },

    # NHÓM 2: LANDING PAGE TỐI ƯU CHUYỂN ĐỔI CAO (HIGH-CRO & GOOGLE ADS SEARCH)
    {
        "id": "fpt05",
        "name": "Lắp Mạng FPT VIP",
        "short_name": "Lắp Mạng FPT VIP",
        "url": "https://lapmangfpt.vip/",
        "domain": "lapmangfpt.vip",
        "slug": "lapmangfpt_vip",
        "industry": "lap-mang-fpt",
        "industry_name": "Lắp Mạng FPT (Google Ads)",
        "category": "High-Conversion Google Ads Landing Page",
        "category_vn": "Landing Page Tối Ưu Chuyển Đổi Google Ads Chuyên Sâu",
        "tag": "high-cro-ads",
        "vibe": "Kích Thích Mua Hàng & Khuyến Mãi Nổi Bật",
        "location": "Toàn quốc",
        "desc": "Bản mẫu Landing Page chạy Google Search Ads đạt tỷ lệ chuyển đổi xuất sắc. Thiết kế tiêu đề gắn nhãn khuyến mãi theo tháng, nút CTA gọi hotline nhấp nháy thu hút sự chú ý, bảng so sánh tốc độ nổi bật và cam kết lắp đặt thần tốc trong 24h."
    },
    {
        "id": "fpt06",
        "name": "Lắp Đặt Mạng FPT",
        "short_name": "Lắp Đặt Mạng FPT",
        "url": "https://lapdatmangfpt.vn/",
        "domain": "lapdatmangfpt.vn",
        "slug": "lapdatmangfpt_vn",
        "industry": "lap-mang-fpt",
        "industry_name": "Lắp Mạng FPT (Google Ads)",
        "category": "Fast Conversion Lead Generation",
        "category_vn": "Trang Thu Thập Khách Hàng Tiềm Năng Nhanh",
        "tag": "high-cro-ads",
        "vibe": "Tinh Gọn & Trực Diện Bảng Giá",
        "location": "Toàn quốc",
        "desc": "Landing page có bố cục tập trung 100% vào việc chốt lead: Hero đập ngay vào mắt bảng giá cước chỉ từ 180k-195k/tháng, form điền thông tin đăng ký lắp đặt chỉ 2 trường tối giản và ưu đãi tặng modem Wi-Fi 6 hai băng tần."
    },
    {
        "id": "fpt07",
        "name": "Đăng Ký WiFi FPT",
        "short_name": "Đăng Ký WiFi FPT",
        "url": "https://dangkywifi.com.vn/",
        "domain": "dangkywifi.com.vn",
        "slug": "dangkywifi_com_vn",
        "industry": "lap-mang-fpt",
        "industry_name": "Lắp Mạng FPT (Google Ads)",
        "category": "Search Ads BOFU Funnel Landing Page",
        "category_vn": "Trang Đích Phễu Đáy (BOFU) Chốt Sale Thần Tốc",
        "tag": "high-cro-ads",
        "vibe": "Thôi Thúc Hành Động & Ưu Đãi Giới Hạn",
        "location": "Toàn quốc",
        "desc": "Cực kỳ thích hợp cho các chiến dịch Google Ads nhắm vào cụm từ tìm kiếm 'đăng ký wifi', 'lắp đặt wifi fpt'. Giao diện tập trung vào đòn bẩy tâm lý: Tặng tháng cước thứ 7, miễn phí hòa mạng khi trả trước, hỗ trợ khảo sát tận nhà."
    },
    {
        "id": "fpt08",
        "name": "FPT Connect",
        "short_name": "FPT Connect",
        "url": "https://fptconnect.vn/",
        "domain": "fptconnect.vn",
        "slug": "fptconnect_vn",
        "industry": "lap-mang-fpt",
        "industry_name": "Lắp Mạng FPT (Google Ads)",
        "category": "Modern Clean UI Telecom Portal",
        "category_vn": "Giao Diện Phẳng Hiện Đại & Tốc Độ Tải Siêu Nhanh",
        "tag": "high-cro-ads",
        "vibe": "Hiện Đại & Chuẩn Trải Nghiệm Trang Đích",
        "location": "Toàn quốc",
        "desc": "Website có thiết kế chuẩn UI/UX hiện đại, tốc độ tải trang cực nhanh giúp tối ưu Điểm chất lượng (Quality Score) khi chạy Google Ads. Trình bày gói cước sạch sẽ, typography sắc nét, tối ưu hiển thị mượt mà trên điện thoại di động."
    },

    # NHÓM 3: ĐẠI DIỆN THỊ TRƯỜNG VÙNG MIỀN TRỌNG ĐIỂM (REGIONAL MARKET LEADERS)
    {
        "id": "fpt09",
        "name": "FPT Telecom Hà Nội",
        "short_name": "FPT Hà Nội",
        "url": "https://fpthanoi.com.vn/",
        "domain": "fpthanoi.com.vn",
        "slug": "fpthanoi_com_vn",
        "industry": "lap-mang-fpt",
        "industry_name": "Lắp Mạng FPT (Google Ads)",
        "category": "Northern Regional Authority Hub",
        "category_vn": "Cổng Dịch Vụ Khách Hàng Thủ Đô Hà Nội",
        "tag": "regional-leaders",
        "vibe": "Chuyên Nghiệp & Địa Phương Hóa Thủ Đô",
        "location": "Hà Nội & Miền Bắc",
        "desc": "Đại diện tiêu biểu cho chiến dịch Google Ads Local SEO nhắm thẳng vào khách hàng tại các quận Đống Đa, Cầu Giấy, Nam Từ Liêm, Hoàng Mai... Cung cấp chi tiết bảng giá khu vực nội/ngoại thành Hà Nội và danh bạ hỗ trợ kỹ thuật tại chỗ."
    },
    {
        "id": "fpt10",
        "name": "FPT Telecom TP.HCM",
        "short_name": "FPT Sài Gòn",
        "url": "https://hcmfpt.vn/",
        "domain": "hcmfpt.vn",
        "slug": "hcmfpt_vn",
        "industry": "lap-mang-fpt",
        "industry_name": "Lắp Mạng FPT (Google Ads)",
        "category": "Southern Regional Authority Hub",
        "category_vn": "Trung Tâm Kinh Doanh FPT Telecom TP. Hồ Chí Minh",
        "tag": "regional-leaders",
        "vibe": "Năng Động & Ưu Đãi Ngoại Thành Sài Gòn",
        "location": "TP.HCM & Nam Bộ",
        "desc": "Kênh kinh doanh trọng điểm tại thị trường miền Nam. Nắm bắt tâm lý khách hàng tại TP.HCM với các gói ưu đãi giá rẻ cho khu vực ngoại thành (Bình Chánh, Hóc Môn, Củ Chi) và các gói cáp quang siêu tốc cho căn hộ chung cư cao cấp."
    },
    {
        "id": "fpt11",
        "name": "Hà Nội FPT VN",
        "short_name": "Hà Nội FPT",
        "url": "https://hanoifpt.vn/",
        "domain": "hanoifpt.vn",
        "slug": "hanoifpt_vn",
        "industry": "lap-mang-fpt",
        "industry_name": "Lắp Mạng FPT (Google Ads)",
        "category": "Local Urban Fast Action Page",
        "category_vn": "Trang Khảo Sát & Ký Hợp Đồng Tại Nhà Hà Nội",
        "tag": "regional-leaders",
        "vibe": "Nhanh Gọn & Cam Kết Triển Khai Trong Ngày",
        "location": "Hà Nội",
        "desc": "Trang web vệ tinh chuyên chạy từ khóa địa phương tại Hà Nội. Nổi bật với cam kết có mặt khảo sát tận nhà sau 30 phút liên hệ, hỗ trợ làm thủ tục hợp đồng điện tử tiện lợi chỉ với ảnh chụp CCCD."
    },
    {
        "id": "fpt12",
        "name": "Lắp Mạng FPT Đà Nẵng",
        "short_name": "FPT Đà Nẵng",
        "url": "https://lapmangfptdanang.com.vn/",
        "domain": "lapmangfptdanang.com.vn",
        "slug": "lapmangfptdanang_com_vn",
        "industry": "lap-mang-fpt",
        "industry_name": "Lắp Mạng FPT (Google Ads)",
        "category": "Central Region Local Leader",
        "category_vn": "Đại Diện Cáp Quang Khu Vực Miền Trung & Đà Nẵng",
        "tag": "regional-leaders",
        "vibe": "Thân Thiện & Báo Giá Miền Trung Chuẩn Xác",
        "location": "Đà Nẵng & Quảng Nam",
        "desc": "Website đại diện thị trường Đà Nẵng và các tỉnh miền Trung. Bảng giá cập nhật theo chính sách vùng 3 với mức cước vô cùng cạnh tranh, hỗ trợ lắp đặt nhanh tại các quận Hải Châu, Thanh Khê, Sơn Trà, Ngũ Hành Sơn."
    },
    {
        "id": "fpt13",
        "name": "FPT Telecom Biên Hòa - Đồng Nai",
        "short_name": "FPT Biên Hòa",
        "url": "https://fptbienhoa.vn/",
        "domain": "fptbienhoa.vn",
        "slug": "fptbienhoa_vn",
        "industry": "lap-mang-fpt",
        "industry_name": "Lắp Mạng FPT (Google Ads)",
        "category": "Industrial Zone Telecom Specialist",
        "category_vn": "Chuyên Gia Cáp Quang Khu Công Nghiệp Đông Nam Bộ",
        "tag": "regional-leaders",
        "vibe": "Thực Tế & Đáp Ứng Nhà Trọ, Doanh Nghiệp",
        "location": "Đồng Nai & Bình Dương",
        "desc": "Tập trung khai thác khách hàng tại các thủ phủ công nghiệp Biên Hòa, Nhơn Trạch, Long Thành. Bố cục thực chiến giải quyết bài toán lắp mạng cho phòng trọ công nhân, nhà riêng và các doanh nghiệp trong khu công nghiệp."
    },

    # NHÓM 4: BẢNG GIÁ & SO SÁNH GÓI CƯỚC CHUYÊN SÂU (PRICING & COMPARISON HUBS)
    {
        "id": "fpt14",
        "name": "FPT Internet & Truyền Hình",
        "short_name": "FPT Internet",
        "url": "https://fptinternet.vn/",
        "domain": "fptinternet.vn",
        "slug": "fptinternet_vn",
        "industry": "lap-mang-fpt",
        "industry_name": "Lắp Mạng FPT (Google Ads)",
        "category": "Structured Pricing Cards & Visual Grid",
        "category_vn": "Bố Cục Thẻ Card So Sánh Gói Cước Trực Quan",
        "tag": "pricing-comparison",
        "vibe": "Khoa Học & Dễ So Sánh Tốc Độ",
        "location": "Toàn quốc",
        "desc": "Điểm mạnh nổi bật là giao diện dạng lưới thẻ card (pricing cards) so sánh trực quan các gói Giga (300Mbps), Sky (1Gbps/300Mbps), Meta (1Gbps Full) kèm icon thiết bị modem WiFi 6 rõ ràng, giúp khách hàng chọn gói chỉ sau 5 giây."
    },
    {
        "id": "fpt15",
        "name": "Bảng Giá Cước WiFi FPT",
        "short_name": "FPT WiFi",
        "url": "https://fptwifi.com.vn/",
        "domain": "fptwifi.com.vn",
        "slug": "fptwifi_com_vn",
        "industry": "lap-mang-fpt",
        "industry_name": "Lắp Mạng FPT (Google Ads)",
        "category": "Broadband & Mesh WiFi Specialist",
        "category_vn": "Chuyên Sâu Gói Cước Gia Đình & Thiết Bị WiFi Mesh",
        "tag": "pricing-comparison",
        "vibe": "Rõ Ràng & Minh Bạch Cước Phí",
        "location": "Toàn quốc",
        "desc": "Tối ưu cho khách hàng có nhu cầu phủ sóng nhà nhiều tầng, biệt thự hoặc căn hộ rộng với các giải pháp Mesh WiFi hiện đại. Bảng tính cước phí minh bạch, không phí ẩn, hỗ trợ tư vấn phương án kéo dây tối ưu thẩm mỹ."
    },
    {
        "id": "fpt16",
        "name": "Cáp Quang FPT Tốc Độ Cao",
        "short_name": "Cáp Quang FPT Net",
        "url": "https://capquangfpt.net.vn/",
        "domain": "capquangfpt.net.vn",
        "slug": "capquangfpt_net_vn",
        "industry": "lap-mang-fpt",
        "industry_name": "Lắp Mạng FPT (Google Ads)",
        "category": "High-Speed Fiber & Enterprise Solutions",
        "category_vn": "Chuyên Sâu Cáp Quang Doanh Nghiệp & Quán Game",
        "tag": "pricing-comparison",
        "vibe": "Mạnh Mẽ & Cam Kết Băng Thông Quốc Tế",
        "location": "Toàn quốc",
        "desc": "Website chuyên sâu các gói cáp quang FPT băng thông lớn cho doanh nghiệp và phòng máy: Super 250, Super 400, Lux 500, Lux 800. Đầy đủ thông số cam kết tốc độ quốc tế, địa chỉ IP tĩnh và thiết bị cân bằng tải Vigor chuyên dụng."
    },
    {
        "id": "fpt17",
        "name": "Cáp Quang FPT Siêu Tốc",
        "short_name": "Cáp Quang FPT",
        "url": "https://capquangfpt.vn/",
        "domain": "capquangfpt.vn",
        "slug": "capquangfpt_vn",
        "industry": "lap-mang-fpt",
        "industry_name": "Lắp Mạng FPT (Google Ads)",
        "category": "Next-Gen WiFi 6/7 Showcase",
        "category_vn": "Trình Diễn Công Nghệ WiFi 6 & WiFi 7 Tiên Tiến",
        "tag": "pricing-comparison",
        "vibe": "Hiện Đại & Đón Đầu Xu Hướng Công Nghệ",
        "location": "Toàn quốc",
        "desc": "Cập nhật nhanh nhất các gói cước chuẩn công nghệ WiFi 6 và WiFi 7 thế hệ mới của FPT. Cấu trúc bài bản giới thiệu tính năng chống nghẽn mạng, giảm độ trễ khi chơi game và tặng kèm Camera an ninh lưu trữ đám mây."
    },

    # NHÓM 5: TỔNG ĐÀI & PHÂN PHỐI DỊCH VỤ MỞ RỘNG (CALL-TO-ACTION & MULTI-SERVICE)
    {
        "id": "fpt18",
        "name": "Tổng Đài Lắp Mạng FPT",
        "short_name": "Tổng Đài FPT",
        "url": "https://tongdaifpt.com.vn/",
        "domain": "tongdaifpt.com.vn",
        "slug": "tongdaifpt_com_vn",
        "industry": "lap-mang-fpt",
        "industry_name": "Lắp Mạng FPT (Google Ads)",
        "category": "Call-Only & Immediate Hotline Funnel",
        "category_vn": "Phễu Tiếp Nhận Cuộc Gọi Trực Tiếp (Call-Only Ads)",
        "tag": "call-action-funnel",
        "vibe": "Kêu Gọi Gọi Điện & Tiếp Nhận Tức Thì",
        "location": "Toàn quốc",
        "desc": "Mẫu website sinh ra để chạy chiến dịch Google Ads Cuộc gọi (Call-Only Ads) hoặc Quảng cáo tìm kiếm ưu tiên nhấp vào số điện thoại. Hotline và nút Zalo rung lắc liên tục, kích thích khách hàng bấm máy nghe tư vấn ngay trong 30 giây."
    },
    {
        "id": "fpt19",
        "name": "FPT Việt Nam Telecom",
        "short_name": "FPT Vietnam",
        "url": "https://fpt-vietnam.com/",
        "domain": "fpt-vietnam.com",
        "slug": "fpt_vietnam_com",
        "industry": "lap-mang-fpt",
        "industry_name": "Lắp Mạng FPT (Google Ads)",
        "category": "National Commercial Telecom Showcase",
        "category_vn": "Trình Bày Thương Mại Viễn Thông Toàn Diện",
        "tag": "call-action-funnel",
        "vibe": "Đầy Đủ & Quy Trình Lắp Đặt Minh Bạch",
        "location": "Toàn quốc",
        "desc": "Giao diện bài bản theo phong cách thương mại điện tử dịch vụ. Trình bày quy trình 4 bước lắp đặt tại nhà rõ ràng, bảng giải đáp câu hỏi thường gặp (FAQ) chi tiết và các đánh giá hài lòng từ khách hàng thực tế."
    },
    {
        "id": "fpt20",
        "name": "Lắp Mạng FPT Toàn Quốc",
        "short_name": "FPT Toàn Quốc",
        "url": "https://lapmangfpt-toanquoc.com.vn/",
        "domain": "lapmangfpt-toanquoc.com.vn",
        "slug": "lapmangfpt_toanquoc_com_vn",
        "industry": "lap-mang-fpt",
        "industry_name": "Lắp Mạng FPT (Google Ads)",
        "category": "Multi-Region Geo Selector Hub",
        "category_vn": "Cổng Báo Giá Đa Vùng Miền Toàn Quốc",
        "tag": "call-action-funnel",
        "vibe": "Tiện Ích & Tra Cứu Giá Theo Tỉnh Thành",
        "location": "63 Tỉnh Thành Toàn Quốc",
        "desc": "Kênh thông tin toàn diện có bộ lọc bảng giá theo từng tỉnh thành, hỗ trợ khách hàng ngoại tỉnh tra cứu giá cước chính xác tại địa phương mình đang sinh sống mà không sợ bị nhầm lẫn với giá khu vực nội thành."
    }
]

print(f"=== BẮT ĐẦU CHỤP FULL-PAGE 20 WEBSITE DỊCH VỤ LẮP ĐẶT MẠNG FPT ===", flush=True)

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
        
        thumb_name = f"{slug}_thumb.webp"
        full_name = f"{slug}_full.webp"
        fb_name = f"{slug}_fb.png"
        thumb_path = os.path.join(kho_webp_dir, thumb_name)
        full_path = os.path.join(kho_webp_dir, full_name)
        fb_path = os.path.join(kho_webp_dir, fb_name)
        
        # Check if already captured recently and valid (> 10KB)
        if os.path.exists(thumb_path) and os.path.getsize(thumb_path) > 10 * 1024 and os.path.exists(filepath):
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            print(f"  -> File gốc và WebP đã tồn tại: {filename} ({size_mb:.2f} MB), đọc lại thông số...", flush=True)
            thumb_kb = round(os.path.getsize(thumb_path) / 1024, 1)
            full_kb = round(os.path.getsize(full_path) / 1024, 1) if os.path.exists(full_path) else 0
            fb_kb = round(os.path.getsize(fb_path) / 1024, 1) if os.path.exists(fb_path) else 0
            
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

print(f"\n=== HOÀN TẤT CHỤP VÀ NÉN 20 WEBSITE LẮP MẠNG FPT! Đã lưu metadata vào {metadata_file} ===", flush=True)
