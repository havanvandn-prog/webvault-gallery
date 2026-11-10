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
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "landing_page_lap_mang_metadata.json")

os.makedirs(output_dir, exist_ok=True)
os.makedirs(kho_webp_dir, exist_ok=True)
os.makedirs(os.path.dirname(metadata_file), exist_ok=True)

websites = [
    # NHÓM 1: LANDING PAGE LADIPAGE 1-PAGE THUẦN CHUYỂN ĐỔI (FPT & VIỄN THÔNG VN)
    {
        "id": "lpf01",
        "name": "Khuyến Mãi Lắp Mạng FPT (LadiPage Thực Chiến)",
        "short_name": "LadiPage Mạng FPT",
        "url": "https://www.mangfpt.info.vn/",
        "domain": "mangfpt.info.vn",
        "slug": "lp_mangfpt_info_vn",
        "industry": "landing-page-lap-mang",
        "industry_name": "Landing Page Lắp Mạng",
        "category": "Pure 1-Page LadiPage Google Ads",
        "category_vn": "LadiPage Thuần 1-Trang Chạy Quảng Cáo Lắp Mạng FPT",
        "tag": "ladipage-vn",
        "vibe": "1-Trang Không Menu Thoát • Tối Ưu Chốt Lead",
        "location": "Toàn quốc (LadiPage Live)",
        "desc": "Landing Page dựng trên LadiPage đang chạy quảng cáo thực tế. Triệt tiêu hoàn toàn menu điều hướng (0 link thoát trang), Hero nhấn mạnh gói WiFi 220k + tặng FPT Play cùng 2 form đăng ký và 8 nút gọi hotline trực tiếp."
    },
    {
        "id": "lpf02",
        "name": "Đăng Ký WiFi VNPT — Kiểm Tra Hạ Tầng & Bảng Giá 2 Cột",
        "short_name": "LadiPage WiFi & Check Hạ Tầng",
        "url": "https://dangkywifivnpt.io.vn/",
        "domain": "dangkywifivnpt.io.vn",
        "slug": "lp_dangkywifivnpt",
        "industry": "landing-page-lap-mang",
        "industry_name": "Landing Page Lắp Mạng",
        "category": "Coverage Checker + 2-Column CRO LadiPage",
        "category_vn": "LadiPage Có Ô Kiểm Tra Hạ Tầng & Bảng Giá Cạnh Khuyến Mãi",
        "tag": "ladipage-vn",
        "vibe": "Kiểm Tra Hạ Tầng Ngay Hero • Bố Cục 2 Cột Cực Rõ",
        "location": "Toàn quốc (LadiPage Live)",
        "desc": "Landing page LadiPage rất thông minh để học hỏi cấu trúc CRO: đặt ngay ô 'Kiểm tra hạ tầng cáp quang theo địa chỉ' trên Hero, bên dưới chia 2 cột song song (bảng gói cước bên trái - chính sách khuyến mãi đi kèm bên phải)."
    },
    {
        "id": "lpf03",
        "name": "Mẫu LadiPage Lắp Mạng FPT HCM 24/7 (NVA1070)",
        "short_name": "LadiPage FPT HCM 1070",
        "url": "https://w.tuybutky.com/497.-fpt-wifi-1070",
        "domain": "w.tuybutky.com",
        "slug": "lp_tuybutky_fpt_1070",
        "industry": "landing-page-lap-mang",
        "industry_name": "Landing Page Lắp Mạng",
        "category": "Local Search Ads LadiPage Template",
        "category_vn": "Mẫu LadiPage Lắp Mạng FPT Khu Vực TP.HCM 24/7",
        "tag": "ladipage-vn",
        "vibe": "Bản Địa Hóa Địa Phương • Lắp Trong Ngày",
        "location": "TP.HCM (Mẫu LadiPage NVA1070)",
        "desc": "Mẫu Landing Page LadiPage thực chiến nhắm tệp khách hàng khu vực TP.HCM. Tối ưu cấu trúc thuyết phục theo trình tự: Ưu đãi hòa mạng -> Bảng giá gia đình/doanh nghiệp -> Đánh giá bình luận thực tế -> 2 Form chốt thông tin."
    },
    {
        "id": "lpf04",
        "name": "Mẫu LadiPage Internet & Truyền Hình FPT (NVA1481)",
        "short_name": "LadiPage FPT Net 1481",
        "url": "https://w.tuybutky.com/715.-fpt-internet-1481",
        "domain": "w.tuybutky.com",
        "slug": "lp_tuybutky_fpt_1481",
        "industry": "landing-page-lap-mang",
        "industry_name": "Landing Page Lắp Mạng",
        "category": "Combo Multi-Service LadiPage Template",
        "category_vn": "Mẫu LadiPage Combo Internet, Truyền Hình & Camera FPT",
        "tag": "ladipage-vn",
        "vibe": "Đa Điểm Chạm • Phân Khối Sạch Sẽ Rõ Giá",
        "location": "Toàn quốc (Mẫu LadiPage NVA1481)",
        "desc": "Giao diện Landing Page chuẩn phễu bán chéo Combo Internet + Truyền hình FPT Play + Camera SE. Bố cục đồng hồ đo tốc độ trực quan từng gói cước giúp người dùng chọn nhanh gói phù hợp chỉ trong vài giây."
    },
    {
        "id": "lpf05",
        "name": "Mẫu LadiPage FPT Play Box & Truyền Hình (NVA1063)",
        "short_name": "LadiPage FPT PlayBox 1063",
        "url": "https://w.tuybutky.com/gioi-thieu-fpt-play-box-1063",
        "domain": "w.tuybutky.com",
        "slug": "lp_tuybutky_playbox_1063",
        "industry": "landing-page-lap-mang",
        "industry_name": "Landing Page Lắp Mạng",
        "category": "Fast-Load Product & Combo LadiPage",
        "category_vn": "Mẫu LadiPage Ngắn Gọn Đánh Nhanh Combo Truyền Hình FPT",
        "tag": "ladipage-vn",
        "vibe": "Ngắn Gọn Tức Thì • 4 Điểm Chốt Đặt Hàng",
        "location": "Toàn quốc (Mẫu LadiPage NVA1063)",
        "desc": "Landing page gọn nhẹ (chiều cao chỉ ~3584px) giúp tải cực nhanh trên 4G di động. Phù hợp tham khảo cách so sánh bảng thông số thiết bị + nút đặt mua combo truyền hình/mạng FPT ngay trong 3 cuộn màn hình."
    },
    {
        "id": "lpf06",
        "name": "Mẫu LadiPage Combo Internet & Truyền Hình Viettel",
        "short_name": "LadiPage Combo WiFi",
        "url": "https://showcase.ladi.me/64ed9b10f862bd0012aaf304",
        "domain": "showcase.ladi.me",
        "slug": "lp_ladi_viettel_combo",
        "industry": "landing-page-lap-mang",
        "industry_name": "Landing Page Lắp Mạng",
        "category": "LadiPage Official Showcase Telecom",
        "category_vn": "Mẫu LadiPage Showcase Viễn Thông & Combo WiFi",
        "tag": "ladipage-vn",
        "vibe": "Neo Cuộn Nội Bộ • Thẻ Gói Đỏ Tương Phản Cao",
        "location": "LadiPage Marketplace",
        "desc": "Mẫu thiết kế chính thức trên chợ giao diện LadiPage dành riêng cho ngành viễn thông. Sử dụng thanh điều hướng neo tại chỗ (Gói WiFi / Truyền hình / Ưu điểm / Đăng ký ngay) giữ chân 100% lưu lượng quảng cáo ở lại 1 trang duy nhất."
    },
    {
        "id": "lpf07",
        "name": "LadiPage Bảng Gói Cước Lắp Mạng ViettelCA",
        "short_name": "LadiPage ViettelCA 6-Form",
        "url": "https://viettelca.vn/goi-cuoc-lap-mang-internet-wifi-viettel.html",
        "domain": "viettelca.vn",
        "slug": "lp_viettelca_vn",
        "industry": "landing-page-lap-mang",
        "industry_name": "Landing Page Lắp Mạng",
        "category": "Long-Form High-CRO Telecom LadiPage",
        "category_vn": "LadiPage Chuyên Sâu Phân Tầng Nhu Cầu & 6 Form Chốt Lead",
        "tag": "ladipage-vn",
        "vibe": "Thuyết Phục Toàn Diện • Chặn Mọi Băn Khoăn",
        "location": "Toàn quốc (LadiPage Live)",
        "desc": "Mẫu Landing Page long-form thực chiến dành cho khách hàng cân nhắc kỹ. Tách rành mạch bảng cước Nội thành / Ngoại thành / Doanh nghiệp IP Tĩnh kèm 6 biểu mẫu đăng ký đặt ngay cạnh từng bảng giá."
    },

    # NHÓM 2: LANDING PAGE CHIẾN DỊCH CHÍNH HÃNG FPT & TRANG ĐÍCH CHẠY GOOGLE ADS VN
    {
        "id": "lpf08",
        "name": "FPT Telecom — Landing Page Internet Gia Đình",
        "short_name": "FPT Internet Campaign LP",
        "url": "https://fpt.vn/internet",
        "domain": "fpt.vn",
        "slug": "lp_fpt_internet",
        "industry": "landing-page-lap-mang",
        "industry_name": "Landing Page Lắp Mạng",
        "category": "Official Enterprise Campaign Landing Page",
        "category_vn": "Trang Đích Chiến Dịch Internet WiFi Chính Hãng FPT.vn",
        "tag": "ads-campaign-vn",
        "vibe": "Đẳng Cấp Chính Hãng • Thẻ Gói Cước Trực Quan",
        "location": "FPT Telecom (fpt.vn/internet)",
        "desc": "Trang đích bán hàng chuyên biệt của chính FPT Telecom (tách biệt khỏi trang chủ cổng tập đoàn). Trình bày xuất sắc các gói Giga, Sky, F-Game, Meta cùng ưu đãi tặng Camera AI và Modem Wi-Fi 6 với giao diện phẳng hiện đại."
    },
    {
        "id": "lpf09",
        "name": "FPT Wi-Fi 7 XGS-PON — Landing Page Công Nghệ Mới",
        "short_name": "FPT Wi-Fi 7 XGS-PON LP",
        "url": "https://fpt.vn/internet-wifi-7-xgspon",
        "domain": "fpt.vn",
        "slug": "lp_fpt_wifi7_xgspon",
        "industry": "landing-page-lap-mang",
        "industry_name": "Landing Page Lắp Mạng",
        "category": "Flagship Tech Launch Landing Page",
        "category_vn": "Landing Page Ra Mắt Công Nghệ Wi-Fi 7 & XGS-PON 10Gbps",
        "tag": "ads-campaign-vn",
        "vibe": "Công Nghệ Tiên Phong • Trải Nghiệm Tốc Độ 10Gbps",
        "location": "FPT Telecom Chính Hãng",
        "desc": "Landing page Next.js thế hệ mới của FPT Telecom với cấu trúc kể chuyện công nghệ (Storytelling Landing Page). Có video review tốc độ thực tế và điểm nhấn 10Gbps đối xứng cho nhóm từ khóa gaming/cao cấp."
    },
    {
        "id": "lpf10",
        "name": "FPT Business — Landing Page WiFi Doanh Nghiệp",
        "short_name": "FPT WiFi Doanh Nghiệp LP",
        "url": "https://fpt.vn/internet-doanh-nghiep",
        "domain": "fpt.vn",
        "slug": "lp_fpt_doanh_nghiep",
        "industry": "landing-page-lap-mang",
        "industry_name": "Landing Page Lắp Mạng",
        "category": "B2B Dedicated Search Ads Landing Page",
        "category_vn": "Trang Đích Chạy Quảng Cáo Tệp Doanh Nghiệp & IP Tĩnh",
        "tag": "ads-campaign-vn",
        "vibe": "Chuyên Nghiệp B2B • Cam Kết Băng Thông Quốc Tế",
        "location": "FPT Telecom B2B",
        "desc": "Landing page riêng biệt cho nhóm từ khóa giá trị cao 'lắp mạng cho công ty / quán net / văn phòng'. Làm nổi bật thông số băng thông quốc tế, IP Tĩnh và form đăng ký tư vấn doanh nghiệp ngay cuối trang."
    },
    {
        "id": "lpf11",
        "name": "FPT Play V.VIP — Landing Page Combo Internet & Truyền Hình",
        "short_name": "FPT Play Combo V.VIP LP",
        "url": "https://fpt.vn/truyen-hinh-fpt-play",
        "domain": "fpt.vn",
        "slug": "lp_fpt_play_lp",
        "industry": "landing-page-lap-mang",
        "industry_name": "Landing Page Lắp Mạng",
        "category": "Combo Campaign Landing Page FPT.vn",
        "category_vn": "Landing Page Combo Internet & Truyền Hình Ngoại Hạng Anh",
        "tag": "ads-campaign-vn",
        "vibe": "Ưu Đãi Combo Thể Thao • Tặng Camera + Cloud",
        "location": "FPT Telecom Chính Hãng",
        "desc": "Trang đích chiến dịch chuyên biệt (LDP FPT Play) của FPT Telecom tập trung chốt gói Combo Internet + Truyền hình FPT Play V.VIP (220k–339k/tháng). Tách biệt rõ 2 khối: gói Combo Mạng-TV và gói Truyền hình độc lập."
    },
    {
        "id": "lpf12",
        "name": "FPTNet.vn — Landing Page 1-Trang Đăng Ký Nhanh",
        "short_name": "FPTNet 1-Page",
        "url": "https://fptnet.vn/",
        "domain": "fptnet.vn",
        "slug": "lp_fptnet_vn",
        "industry": "landing-page-lap-mang",
        "industry_name": "Landing Page Lắp Mạng",
        "category": "Compact 1-Page Direct Lead Capture",
        "category_vn": "Landing Page Siêu Gọn 1 Trang Thu Thập Lead Trực Tiếp",
        "tag": "ads-campaign-vn",
        "vibe": "Siêu Gọn 3238px • Tải Tức Thì Trong 1 Giây",
        "location": "Toàn quốc",
        "desc": "Trang đích tối giản với chiều cao gọn gàng (~3238px), bảng chọn khu vực 3 miền Bắc-Trung-Nam đặt ngay trên form đăng ký giúp giữ người dùng chọn tỉnh thành rồi để lại SĐT nhanh nhất."
    },
    {
        "id": "lpf13",
        "name": "FPTHotline — Landing Page Chạy Ads FPT Play VVIP",
        "short_name": "FPTHotline Ads LP",
        "url": "https://fpthotline.net/",
        "domain": "fpthotline.net",
        "slug": "lp_fpthotline_net",
        "industry": "landing-page-lap-mang",
        "industry_name": "Landing Page Lắp Mạng",
        "category": "Google Search Ads BOFU Funnel",
        "category_vn": "Landing Page Phễu Đáy (BOFU) Chạy Ads Tìm Kiếm FPT",
        "tag": "ads-campaign-vn",
        "vibe": "Đánh Trúng Khuyến Mãi • 11 Form/Nút Chuyển Đổi",
        "location": "Toàn quốc",
        "desc": "Trang đích Google Ads thực chiến đánh vào ưu đãi 'Mua 1 Được 3' (Internet + FPT Play VVIP + Camera Cloud). Phối màu cam-trắng thương hiệu FPT sắc nét cùng nút 'Đăng ký ngay' dưới từng gói."
    },
    {
        "id": "lpf14",
        "name": "5GVT — Landing Page Chạy Ads Lắp Mạng Viettel TV360",
        "short_name": "5GVT Ads Landing Page",
        "url": "https://5gvt.vn/lap-mang-viettel/",
        "domain": "5gvt.vn",
        "slug": "lp_5gvt_viettel",
        "industry": "landing-page-lap-mang",
        "industry_name": "Landing Page Lắp Mạng",
        "category": "Paid Search Dedicated Service Landing Page",
        "category_vn": "Trang Đích Con (Subpage LP) Chạy Quảng Cáo Lắp Mạng",
        "tag": "ads-campaign-vn",
        "vibe": "Bố Cục Subpage Ads • Form Đỏ Nổi Bật Sau Mỗi Bảng",
        "location": "Toàn quốc",
        "desc": "Ví dụ điển hình về cấu trúc Subpage Landing Page tách riêng khỏi trang chủ. Trình bày bảng giá chi tiết theo từng phân khúc và đặt liên tiếp 9 hộp thu nhận thông tin đăng ký ngay bên dưới mỗi bảng cước."
    },

    # NHÓM 3: MẪU LANDING PAGE FIBER INTERNET & WI-FI QUỐC TẾ CHUẨN UI/UX (FRAMER / WEBFLOW)
    {
        "id": "lpf15",
        "name": "Opnet ISP — Landing Page Viễn Thông Hiện Đại (Framer)",
        "short_name": "Opnet Framer ISP LP",
        "url": "https://opnet.framer.website/",
        "domain": "opnet.framer.website",
        "slug": "lp_opnet_framer",
        "industry": "landing-page-lap-mang",
        "industry_name": "Landing Page Lắp Mạng",
        "category": "Modern Framer Telecom UI Benchmark",
        "category_vn": "Mẫu Landing Page Framer Ngành Viễn Thông & Internet",
        "tag": "intl-ui-benchmark",
        "vibe": "Thẩm Mỹ Hiện Đại • Typography & Grid Xuất Sắc",
        "location": "Framer Showcase (Quốc tế)",
        "desc": "Mẫu UI/UX đẳng cấp quốc tế xây dựng trên Framer cho các nhà cung cấp dịch vụ Internet. Phối màu tương phản sắc nét, khối trình bày lợi ích doanh nghiệp & cam kết ổn định thuyết phục mạnh mẽ khách hàng cao cấp."
    },
    {
        "id": "lpf16",
        "name": "CBN Fiber WiFi — Landing Page Cáp Quang (Framer)",
        "short_name": "CBN Fiber Framer LP",
        "url": "https://wificbnpalembang.framer.website/",
        "domain": "wificbnpalembang.framer.website",
        "slug": "lp_cbn_fiber_framer",
        "industry": "landing-page-lap-mang",
        "industry_name": "Landing Page Lắp Mạng",
        "category": "Real-World Conversion Framer ISP Page",
        "category_vn": "Landing Page Cáp Quang Thực Tế Xây Trên Framer",
        "tag": "intl-ui-benchmark",
        "vibe": "Sạch Sẽ & Thuần Chuyển Đổi • Menu Neo Tại Chỗ",
        "location": "Quốc tế (Framer Live)",
        "desc": "Landing page lắp đặt WiFi cáp quang thực tế rất đáng học hỏi: thanh trên chỉ có 3 neo cuộn nội bộ (Gói cước - Ưu điểm - Đăng ký ngay), thẻ gói bán chạy ngay vùng đầu trang và nút hành động tương phản cao."
    },
    {
        "id": "lpf17",
        "name": "Tristate Wi-Fi — Landing Page Cáp Quang & Đánh Giá Thực",
        "short_name": "Tristate Wi-Fi Webflow",
        "url": "https://tristate-wifi.webflow.io/",
        "domain": "tristate-wifi.webflow.io",
        "slug": "lp_tristate_wifi",
        "industry": "landing-page-lap-mang",
        "industry_name": "Landing Page Lắp Mạng",
        "category": "Local Fiber ISP Trust-First Landing Page",
        "category_vn": "Landing Page Internet Cáp Quang Tối Ưu Bằng Chứng Tin Cậy",
        "tag": "intl-ui-benchmark",
        "vibe": "Tôn Vinh Đội Ngũ Kỹ Thuật • 100+ Review 5 Sao",
        "location": "Webflow Live (Quốc tế)",
        "desc": "Mẫu Landing Page nhà mạng địa phương cực kỳ đáng học hỏi cho đại lý FPT: đưa ảnh thật đội ngũ kỹ thuật viên + huy hiệu 100+ đánh giá 5 sao lên ngay vùng đầu trang (Above-the-fold) để tăng độ tin cậy trước khi chào gói."
    },
    {
        "id": "lpf18",
        "name": "Zainet Home V1 — Landing Page Bảng Gói Fiber (Webflow)",
        "short_name": "Zainet Home V1 Webflow",
        "url": "https://zainet.webflow.io/home-pages/home-v1",
        "domain": "zainet.webflow.io",
        "slug": "lp_zainet_v1",
        "industry": "landing-page-lap-mang",
        "industry_name": "Landing Page Lắp Mạng",
        "category": "High-Impact Broadband Landing Page Template",
        "category_vn": "Landing Page Dịch Vụ Internet Cáp Quang & TV Hiện Đại",
        "tag": "intl-ui-benchmark",
        "vibe": "Thẻ Giá Dạng Vé Độc Đáo • Thanh Callout Hotline Nổi",
        "location": "Webflow Live (Quốc tế)",
        "desc": "Landing page Home V1 chuẩn mực của Zainet cho ngành Broadband/WiFi: thẻ giá thiết kế dạng vé kèm đồng hồ Mbps bắt mắt, khối gọi hotline nổi bật giữa trang, khu vực video gaming và hộp kiểm tra hạ tầng."
    },
    {
        "id": "lpf19",
        "name": "Novos Fiber — Landing Page Internet Gia Đình (Webflow)",
        "short_name": "Novos Fiber Webflow",
        "url": "https://novos-fiber.webflow.io/",
        "domain": "novos-fiber.webflow.io",
        "slug": "lp_novos_fiber_webflow",
        "industry": "landing-page-lap-mang",
        "industry_name": "Landing Page Lắp Mạng",
        "category": "Clean Consumer Fiber Landing Page",
        "category_vn": "Landing Page Cáp Quang Gia Đình Phong Cách Sáng Hiện Đại",
        "tag": "intl-ui-benchmark",
        "vibe": "Sáng Sủa & Thân Thiện • Thanh So Sánh Tốc Độ Trực Quan",
        "location": "Webflow Live (Quốc tế)",
        "desc": "Landing page cáp quang gia đình với thông điệp đánh trúng tâm lý ngay tiêu đề đầu trang ('Xem phim không giật, lướt web không độ trễ'), 3 thẻ giá làm nổi bật gói khuyên dùng và thanh so sánh tốc độ Fiber vs Cable cực dễ hiểu."
    },
    {
        "id": "lpf20",
        "name": "Broadband 128 — Landing Page Internet & TV (Webflow)",
        "short_name": "Broadband 128 Webflow",
        "url": "https://broadband-and-telecom-128.webflow.io/",
        "domain": "broadband-and-telecom-128.webflow.io",
        "slug": "lp_broadband128_webflow",
        "industry": "landing-page-lap-mang",
        "industry_name": "Landing Page Lắp Mạng",
        "category": "Broadband & Streaming Bundle Template",
        "category_vn": "Mẫu Landing Page Combo Internet & Truyền Hình Streaming",
        "tag": "intl-ui-benchmark",
        "vibe": "Giải Trí & Đa Thiết Bị • Bản Đồ Phủ Sóng Toàn Diện",
        "location": "Webflow Marketplace (Quốc tế)",
        "desc": "Mẫu giao diện Webflow thiết kế riêng cho mô hình bán Combo Cáp Quang + Truyền hình giải trí (rất tương đồng với gói Combo Internet + FPT Play). Trình bày thẻ gói cước tối màu sắc nét và dễ tùy biến trên di động."
    }
]

print("=== XÁC NHẬN & ĐỒNG BỘ 20 LANDING PAGE LẮP MẠNG INTERNET ===", flush=True)

final_metadata = []

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
    )

    for idx, item in enumerate(websites, start=1):
        slug = item["slug"]
        filename = f"{slug}.png"
        filepath = os.path.join(output_dir, filename)
        thumb_name = f"{slug}_thumb.webp"
        full_name = f"{slug}_full.webp"
        fb_name = f"{slug}_fb.png"
        thumb_path = os.path.join(kho_webp_dir, thumb_name)
        full_path = os.path.join(kho_webp_dir, full_name)
        fb_path = os.path.join(kho_webp_dir, fb_name)

        print(f"[{idx}/20] {item['id'].upper()} ({slug}) -> {item['url']}", flush=True)

        if os.path.exists(full_path) and os.path.exists(thumb_path) and os.path.exists(filepath):
            ok, audit_msg = verify_captured_image(full_path)
            if ok:
                size_mb = os.path.getsize(filepath) / (1024 * 1024)
                thumb_kb = round(os.path.getsize(thumb_path) / 1024, 1)
                full_kb = round(os.path.getsize(full_path) / 1024, 1)
                fb_kb = round(os.path.getsize(fb_path) / 1024, 1) if os.path.exists(fb_path) else 0
                print(f"  -> Đạt chuẩn QA: {audit_msg} (Thumb {thumb_kb}KB, Full {full_kb}KB)", flush=True)
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

        # Fallback capture nếu thiếu file nào
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            ignore_https_errors=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        page.goto(item["url"], wait_until="domcontentloaded", timeout=35000)
        time.sleep(2.5)
        page.evaluate("""() => document.querySelectorAll('.ladi-lazyload').forEach(el => el.classList.remove('ladi-lazyload'))""")
        capture_smart_clean(page, filepath, viewport_height=900, scroll_delay=0.22)
        thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb = compress_tri_layer(filepath, slug, kho_webp_dir)
        ok, audit_msg = verify_captured_image(full_path)
        print(f"  -> Captured fallback: {'PASS' if ok else 'WARN'} - {audit_msg}", flush=True)
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
            "status": "SUCCESS" if ok else "WARN"
        })
        context.close()

    browser.close()

with open(metadata_file, "w", encoding="utf-8") as f:
    json.dump(final_metadata, f, ensure_ascii=False, indent=2)

passed = sum(1 for x in final_metadata if x["status"] == "SUCCESS")
print(f"\n=== HOÀN TẤT KIỂM ĐỊNH! PASS: {passed}/20 ===")
