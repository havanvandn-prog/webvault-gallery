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
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "auto_mercedes_candidates.json")

os.makedirs(output_dir, exist_ok=True)
os.makedirs(kho_webp_dir, exist_ok=True)

candidates = [
    # --- NHÓM 1: MERCEDES-BENZ MỚI (12 MẪU TIÊU BIỂU) ---
    {
        "id": "am01",
        "name": "Mercedes-Benz Automobile VN — Báo Giá & Form Hero",
        "short_name": "Mercedes Automobile VN",
        "url": "https://mercedesbenz-automobile.com.vn/",
        "domain": "mercedesbenz-automobile.com.vn",
        "slug": "am_mercedes_automobile",
        "industry": "landing-page-oto-mercedes",
        "industry_name": "Landing Page Ô Tô & Mercedes-Benz (CRO)",
        "category": "Mercedes-Benz New Car Landing Page",
        "category_vn": "Mercedes-Benz Mới — Form Hero & Bảng Giá CRO",
        "tag": "mercedes-cro",
        "vibe": "Form Ngay Above-the-Fold (6 Ô Nhập) • Bảng Giá • Hotline/Zalo Sticky",
        "location": "Việt Nam",
        "desc": "Trang đích bán xe Mercedes-Benz mới chuẩn chạy Google Ads với cụm form nhận báo giá & lái thử hiển thị sớm ngay phần đầu, kèm bảng giá niêm yết từng dòng xe và nút gọi/Zalo nổi cố định."
    },
    {
        "id": "am02",
        "name": "XeMercedes.Net — Báo Giá Lăn Bánh & Dự Toán Trả Góp",
        "short_name": "XeMercedes.Net",
        "url": "https://xemercedes.net/",
        "domain": "xemercedes.net",
        "slug": "am_xemercedes_net",
        "industry": "landing-page-oto-mercedes",
        "industry_name": "Landing Page Ô Tô & Mercedes-Benz (CRO)",
        "category": "Mercedes-Benz Price & Loan Calculator LP",
        "category_vn": "Mercedes-Benz Mới — Dự Toán Lăn Bánh & Trả Góp",
        "tag": "mercedes-cro",
        "vibe": "Custom UI • 11 CTA Đầu Trang • Công Cụ Tính Lăn Bánh & Trả Góp",
        "location": "Việt Nam",
        "desc": "Giao diện thiết kế riêng cho chiến dịch bán Mercedes-Benz mới 2026: cam kết giao xe ngay, 11 nút CTA chuyển đổi ở màn hình đầu, tích hợp bảng giá lăn bánh và dự toán trả góp chi tiết."
    },
    {
        "id": "am03",
        "name": "Mercedes-Benz Đà Nẵng — Bảng Giá & Ưu Đãi Tháng",
        "short_name": "Mercedes Đà Nẵng",
        "url": "https://mercedes-danang.com/",
        "domain": "mercedes-danang.com",
        "slug": "am_mercedes_danang",
        "industry": "landing-page-oto-mercedes",
        "industry_name": "Landing Page Ô Tô & Mercedes-Benz (CRO)",
        "category": "Elementor Mercedes Landing Page",
        "category_vn": "Mercedes-Benz Miền Trung — Elementor CRO",
        "tag": "mercedes-cro",
        "vibe": "Elementor Pro • 10 CTA Đầu Trang • Ưu Đãi Tháng & Trả Góp",
        "location": "Đà Nẵng",
        "desc": "Xây dựng trên Elementor tối ưu chuyển đổi với thông điệp ưu đãi theo tháng ngay H1, lưới sản phẩm kèm giá niêm yết rõ ràng, tính năng dự toán trả góp và nút đặt lịch lái thử trực quan."
    },
    {
        "id": "am04",
        "name": "Giá Xe Mercedes Haxaco — Cổng Báo Giá & Khuyến Mãi",
        "short_name": "Giá Xe Mercedes Haxaco",
        "url": "https://giaxemercedes.com.vn/",
        "domain": "giaxemercedes.com.vn",
        "slug": "am_giaxemercedes_haxaco",
        "industry": "landing-page-oto-mercedes",
        "industry_name": "Landing Page Ô Tô & Mercedes-Benz (CRO)",
        "category": "Custom High-CRO Mercedes Dealer LP",
        "category_vn": "Mercedes-Benz Haxaco — Đa Điểm Chạm Form",
        "tag": "mercedes-cro",
        "vibe": "Custom Theme • 6 Form Thu Lead • Tính Trả Góp & Hotline",
        "location": "TP.HCM & Hà Nội",
        "desc": "Trang chuyên báo giá xe Mercedes chính hãng hệ thống Haxaco: tích hợp 6 biểu mẫu chuyển đổi xuyên suốt trang, công cụ tính lăn bánh/trả góp và điều hướng nhanh theo phân khúc C, E, S, GLC."
    },
    {
        "id": "am05",
        "name": "Mercedes Haxaco Điện Biên Phủ — Showroom Chuẩn 5 Sao",
        "short_name": "Mercedes Haxaco ĐBP",
        "url": "https://mercedes-haxaco.com/",
        "domain": "mercedes-haxaco.com",
        "slug": "am_mercedes_haxaco",
        "industry": "landing-page-oto-mercedes",
        "industry_name": "Landing Page Ô Tô & Mercedes-Benz (CRO)",
        "category": "Mercedes Authorized Dealer LP",
        "category_vn": "Mercedes-Benz Haxaco ĐBP — Giao Diện Riêng",
        "tag": "mercedes-cro",
        "vibe": "Custom Layout • 4 Form Báo Giá • Tính Lãi Suất Trả Góp",
        "location": "TP. Hồ Chí Minh",
        "desc": "Website bán xe Mercedes-Benz mới tại Haxaco Điện Biên Phủ với bố cục tùy biến gọn gàng, 4 điểm thu lead (báo giá, lái thử, trả góp) và khu vực chứng thực showroom chính hãng."
    },
    {
        "id": "am06",
        "name": "Mercedes-Benz An Du — Hệ Thống Đại Lý Miền Bắc",
        "short_name": "Mercedes-Benz An Du",
        "url": "https://mercedesbenz-andu.com.vn/",
        "domain": "mercedesbenz-andu.com.vn",
        "slug": "am_mercedes_andu_comvn",
        "industry": "landing-page-oto-mercedes",
        "industry_name": "Landing Page Ô Tô & Mercedes-Benz (CRO)",
        "category": "Mercedes Dealer Conversion Site",
        "category_vn": "Mercedes-Benz An Du — Ưu Đãi & Báo Giá Nhanh",
        "tag": "mercedes-cro",
        "vibe": "Hero Carousel + 6 CTA • Bảng Giá Trực Quan • 3 Form Báo Giá",
        "location": "Hà Nội & Miền Bắc",
        "desc": "Website bán hàng đại lý An Du tập trung mạnh vào chuyển đổi Google Ads: cụm CTA đa dạng ngay dưới banner đầu, danh mục xe kèm giá niêm yết và banner đăng ký lái thử nổi bật."
    },
    {
        "id": "am07",
        "name": "An Du Mercedes Phạm Hùng — Tư Vấn Xe & Báo Giá",
        "short_name": "An Du Phạm Hùng",
        "url": "https://andu-mercedes.com/",
        "domain": "andu-mercedes.com",
        "slug": "am_andu_mercedes",
        "industry": "landing-page-oto-mercedes",
        "industry_name": "Landing Page Ô Tô & Mercedes-Benz (CRO)",
        "category": "Mercedes Sales Consultant LP",
        "category_vn": "Mercedes An Du Phạm Hùng — Chuẩn Tư Vấn Cá Nhân",
        "tag": "mercedes-cro",
        "vibe": "4 Form Thu Lead • 4 CTA Đầu Trang • Bảng Giá & Dự Toán",
        "location": "Hà Nội",
        "desc": "Trang đích bán xe Mercedes tại An Du Phạm Hùng thiết kế theo phễu tư vấn 1-1: nhấn mạnh ưu đãi đặc quyền, hồ sơ trả góp nhanh và các nút gọi/Zalo gắn cố định trên màn hình."
    },
    {
        "id": "am08",
        "name": "Mercedes Phú Mỹ Hưng — Showroom Quận 7 TP.HCM",
        "short_name": "Mercedes Phú Mỹ Hưng",
        "url": "https://mercedesphumyhung.com.vn/",
        "domain": "mercedesphumyhung.com.vn",
        "slug": "am_mercedes_pmh",
        "industry": "landing-page-oto-mercedes",
        "industry_name": "Landing Page Ô Tô & Mercedes-Benz (CRO)",
        "category": "Luxury Dealer Landing Page",
        "category_vn": "Mercedes Phú Mỹ Hưng — Cao Cấp & Đầy Đủ Section",
        "tag": "mercedes-cro",
        "vibe": "Showroom Quận 7 • 3 Form Chuyển Đổi • Bảng Giá & Lái Thử",
        "location": "Quận 7, TP.HCM",
        "desc": "Đại diện tiêu biểu cho cụm trang đích khu Nam Sài Gòn: hình ảnh xe sang độ phân giải cao, phân chia rành mạch các dòng Sedan/SUV/Maybach kèm CTA nhận giá lăn bánh."
    },
    {
        "id": "am09",
        "name": "Mercedes Vietnam VN — Cổng Thông Tin & Bảng Giá",
        "short_name": "Mercedes Vietnam VN",
        "url": "https://mercedesvietnam.vn/",
        "domain": "mercedesvietnam.vn",
        "slug": "am_mercedesvietnam_vn",
        "industry": "landing-page-oto-mercedes",
        "industry_name": "Landing Page Ô Tô & Mercedes-Benz (CRO)",
        "category": "Mercedes Pricing & Test Drive Hub",
        "category_vn": "Mercedes Vietnam — Phễu Tư Vấn & Đặt Lịch",
        "tag": "mercedes-cro",
        "vibe": "Hero Banner Sang Trọng • 3 Form Thu Lead • Bảng Giá Chi Tiết",
        "location": "Việt Nam",
        "desc": "Mẫu website bán xe Mercedes mới kết hợp giữa trải nghiệm thương hiệu cao cấp và phễu thu lead: bảng giá cập nhật, nút nhận ưu đãi từng dòng xe và khối thông tin showroom."
    },
    {
        "id": "am10",
        "name": "Mercedes-Benz VN — Landing Page Báo Giá & Ưu Đãi",
        "short_name": "Mercedes-Benz VN",
        "url": "https://mercedes-benz-vn.com/",
        "domain": "mercedes-benz-vn.com",
        "slug": "am_mercedes_benz_vn",
        "industry": "landing-page-oto-mercedes",
        "industry_name": "Landing Page Ô Tô & Mercedes-Benz (CRO)",
        "category": "Mercedes Sales Landing Page",
        "category_vn": "Mercedes-Benz VN — Giao Diện Tối Giản Chuyển Đổi",
        "tag": "mercedes-cro",
        "vibe": "Bố Cục Sạch • 3 CTA Đầu Trang • 3 Form Nhận Báo Giá",
        "location": "Việt Nam",
        "desc": "Bố cục tinh gọn với tỷ lệ chuyển đổi cao: hạn chế link điều hướng gây phân tâm, tập trung đưa người dùng từ bảng giá các dòng xe chủ lực xuống form đăng ký nhận báo giá."
    },
    {
        "id": "am11",
        "name": "MercedesVN.VN — Trang Đích Ngắn Gọn 4.300px (Haxaco)",
        "short_name": "MercedesVN.VN",
        "url": "https://mercedesvn.vn/",
        "domain": "mercedesvn.vn",
        "slug": "am_mercedesvn_vn",
        "industry": "landing-page-oto-mercedes",
        "industry_name": "Landing Page Ô Tô & Mercedes-Benz (CRO)",
        "category": "Compact Mercedes Landing Page",
        "category_vn": "MercedesVN.VN — Landing Page Ngắn Gọn Siêu Chuyển Đổi",
        "tag": "mercedes-cro",
        "vibe": "Chiều Dài Gọn 4.376px • 6 Form • 6 CTA Đầu Trang",
        "location": "TP. Hồ Chí Minh",
        "desc": "Mẫu trang đích ngắn gọn hiếm có (chỉ ~4.300px) nhưng tích hợp tới 6 biểu mẫu chuyển đổi và 6 nút CTA ngay màn hình đầu, cực kỳ phù hợp làm mẫu tham khảo chạy Google Ads Search."
    },
    {
        "id": "am12",
        "name": "Mercedes-Benz Láng Hạ — Báo Giá & Lăn Bánh Hà Nội",
        "short_name": "Mercedes Láng Hạ",
        "url": "https://mercedesbenzlangha.com.vn/",
        "domain": "mercedesbenzlangha.com.vn",
        "slug": "am_mercedes_langha",
        "industry": "landing-page-oto-mercedes",
        "industry_name": "Landing Page Ô Tô & Mercedes-Benz (CRO)",
        "category": "Mercedes Hanoi Dealer LP",
        "category_vn": "Mercedes-Benz Láng Hạ — Lăn Bánh & Trả Góp",
        "tag": "mercedes-cro",
        "vibe": "74 Ảnh Thực Tế • Bảng Giá & Dự Toán Trả Góp • 3 CTA Đầu Trang",
        "location": "Hà Nội",
        "desc": "Trang bán hàng Mercedes Láng Hạ giàu hình ảnh thực tế (74 ảnh), trình bày rõ giá xe, chi phí lăn bánh tại Hà Nội, chính sách trả góp và biểu mẫu đăng ký tư vấn."
    },

    # --- NHÓM 2: Ô TÔ HẠNG SANG & PHỔ THÔNG CHUẨN LANDING PAGE GOOGLE ADS (8 MẪU) ---
    {
        "id": "am13",
        "name": "Lexus Thăng Long Hà Nội — Landing Page Gọn 4.000px",
        "short_name": "Lexus Thăng Long",
        "url": "https://lexus-hanoi.vn/",
        "domain": "lexus-hanoi.vn",
        "slug": "am_lexus_hanoi",
        "industry": "landing-page-oto-mercedes",
        "industry_name": "Landing Page Ô Tô & Mercedes-Benz (CRO)",
        "category": "Luxury Auto Elementor Landing Page",
        "category_vn": "Lexus Hà Nội — Elementor Form Ngay Hero",
        "tag": "luxury-auto-lp",
        "vibe": "Elementor • 4 CTA + 3 Input Ngay Hero • Dài 3.987px Chuẩn LP",
        "location": "Hà Nội",
        "desc": "Hình mẫu Landing Page xe sang chuẩn mực: chiều cao chỉ ~3.987px, bố trí sẵn 3 ô nhập liệu và 4 nút CTA ngay màn hình đầu tiên, kết hợp bảng giá và dự toán trả góp."
    },
    {
        "id": "am14",
        "name": "Lexus Trung Tâm Sài Gòn — Landing Page Tinh Gọn 3.000px",
        "short_name": "Lexus Sài Gòn Center",
        "url": "https://lexussaigoncenter.vn/",
        "domain": "lexussaigoncenter.vn",
        "slug": "am_lexus_saigon",
        "industry": "landing-page-oto-mercedes",
        "industry_name": "Landing Page Ô Tô & Mercedes-Benz (CRO)",
        "category": "Compact Luxury Auto Landing Page",
        "category_vn": "Lexus Sài Gòn — Landing Page Tinh Gọn 3.000px",
        "tag": "luxury-auto-lp",
        "vibe": "Siêu Gọn 2.984px • 13 Form Chuyển Đổi • Bảng Giá Xe Sang",
        "location": "TP. Hồ Chí Minh",
        "desc": "Trang đích xe sang cô đọng bậc nhất (chỉ ~2.984px) giúp khách hàng quét nhanh toàn bộ dòng xe Lexus, giá niêm yết và bấm mở form báo giá/lái thử ở mọi điểm chạm."
    },
    {
        "id": "am15",
        "name": "Dana Ford Đà Nẵng — Giao Diện Next.js Hiện Đại",
        "short_name": "Dana Ford (Next.js)",
        "url": "https://danaford.com.vn/",
        "domain": "danaford.com.vn",
        "slug": "am_dana_ford",
        "industry": "landing-page-oto-mercedes",
        "industry_name": "Landing Page Ô Tô & Mercedes-Benz (CRO)",
        "category": "Next.js Modern Auto Conversion LP",
        "category_vn": "Dana Ford — Công Nghệ Next.js Tốc Độ Cao",
        "tag": "auto-cro-lp",
        "vibe": "Next.js SPA • 7 CTA Đầu Trang • Dự Toán Lăn Bánh & Trả Góp",
        "location": "Đà Nẵng",
        "desc": "Website bán ô tô hiếm hoi tại Việt Nam xây dựng trên Next.js cho tốc độ tải tức thì (tốt cho Điểm Chất Lượng Google Ads), sở hữu 7 nút CTA đầu trang và công cụ dự toán trả góp mượt mà."
    },
    {
        "id": "am16",
        "name": "Sài Gòn Ford — Đại Lý Số 1 & Phễu Chuyển Đổi Nhanh",
        "short_name": "Sài Gòn Ford",
        "url": "https://saigonford.com.vn/",
        "domain": "saigonford.com.vn",
        "slug": "am_saigon_ford",
        "industry": "landing-page-oto-mercedes",
        "industry_name": "Landing Page Ô Tô & Mercedes-Benz (CRO)",
        "category": "High-Conversion Auto Dealer LP",
        "category_vn": "Sài Gòn Ford — Custom UI & Phễu Lăn Bánh",
        "tag": "auto-cro-lp",
        "vibe": "Custom CMS • 3 Form • 3 CTA + Input Đầu Trang • 7 Link Hotline",
        "location": "TP. Hồ Chí Minh",
        "desc": "Trang bán ô tô thiết kế riêng tối ưu cho lưu lượng quảng cáo: ô tìm kiếm/chọn xe + CTA nổi bật ngay màn hình đầu, bảng giá lăn bánh từng dòng xe và hệ thống chứng thực đại lý uy tín."
    },
    {
        "id": "am17",
        "name": "VinFast Sài Gòn Minh Đạo — Elementor Full Phễu Ads",
        "short_name": "VinFast Sài Gòn",
        "url": "https://vinfast-saigon.com.vn/",
        "domain": "vinfast-saigon.com.vn",
        "slug": "am_vinfast_saigon",
        "industry": "landing-page-oto-mercedes",
        "industry_name": "Landing Page Ô Tô & Mercedes-Benz (CRO)",
        "category": "Elementor Full-Funnel Auto LP",
        "category_vn": "VinFast Sài Gòn — Đạt 9/9 Tiêu Chí Từ Khóa CRO",
        "tag": "auto-cro-lp",
        "vibe": "Elementor Pro • 9/9 Yếu Tố CRO • Bảng Giá + Trả Góp + Đặt Cọc",
        "location": "TP. Hồ Chí Minh",
        "desc": "Một trong những trang đích ô tô hoàn chỉnh nhất về mặt chuyển đổi: phủ đủ 9/9 yếu tố (báo giá, lăn bánh, lái thử, trả góp, ưu đãi, khuyến mãi, đặt cọc, liên hệ, tư vấn) trên nền Elementor."
    },
    {
        "id": "am18",
        "name": "VinFast TP.HCM Quận 12 — Custom Landing Page Xe Điện",
        "short_name": "VinFast TP.HCM Q12",
        "url": "https://vinfast-tphcm.vn/",
        "domain": "vinfast-tphcm.vn",
        "slug": "am_vinfast_tphcm",
        "industry": "landing-page-oto-mercedes",
        "industry_name": "Landing Page Ô Tô & Mercedes-Benz (CRO)",
        "category": "Custom EV Sales Landing Page",
        "category_vn": "VinFast TP.HCM — Custom UI Giàu Hình Ảnh",
        "tag": "auto-cro-lp",
        "vibe": "Custom UI • 3 Form • Giá Lăn Bánh + Dự Toán Trả Góp + 4 Link Zalo",
        "location": "TP. Hồ Chí Minh",
        "desc": "Giao diện tùy biến nhiều hình ảnh trực quan, phân tầng rõ bảng giá các dòng xe từ VF 3 đến VF 9, tích hợp nút Zalo/Hotline và form đăng ký nhận ưu đãi."
    },
    {
        "id": "am19",
        "name": "BYD Miền Nam — Landing Page Xe Điện Gọn 4.700px",
        "short_name": "BYD Miền Nam",
        "url": "https://bydmiennam.com.vn/",
        "domain": "bydmiennam.com.vn",
        "slug": "am_byd_miennam",
        "industry": "landing-page-oto-mercedes",
        "industry_name": "Landing Page Ô Tô & Mercedes-Benz (CRO)",
        "category": "Compact EV Landing Page",
        "category_vn": "BYD Miền Nam — Form Hero & Cấu Trúc Gọn",
        "tag": "auto-cro-lp",
        "vibe": "Dài 4.700px • 3 Input Ngay Đầu Trang • Bảng Giá & Trả Góp",
        "location": "Miền Nam",
        "desc": "Trang đích bán xe điện BYD với bố cục ngắn gọn 4.700px, đưa ngay cụm 3 ô nhập liệu và CTA lên đầu trang cùng bảng giá niêm yết và tính năng dự toán trả góp."
    },
    {
        "id": "am20",
        "name": "Hyundai Ngọc Phát — Landing Page 8 Form Đa Điểm Chạm",
        "short_name": "Hyundai Ngọc Phát",
        "url": "https://hyundaingocphat.com.vn/",
        "domain": "hyundaingocphat.com.vn",
        "slug": "am_hyundai_ngocphat",
        "industry": "landing-page-oto-mercedes",
        "industry_name": "Landing Page Ô Tô & Mercedes-Benz (CRO)",
        "category": "Multi-Touchpoint Auto Landing Page",
        "category_vn": "Hyundai Ngọc Phát — Landing Page Gọn 4.500px",
        "tag": "auto-cro-lp",
        "vibe": "Dài 4.523px • 8 Form Thu Lead • 2 Input Đầu Trang • 48 Ảnh",
        "location": "Đồng Nai / Miền Nam",
        "desc": "Trang đích bán xe Hyundai rất gọn (4.523px) nhưng bố trí tới 8 điểm chạm biểu mẫu thu lead và ô nhập liệu ngay phần đầu, tối ưu mạnh cho chiến dịch Google Search Ads địa phương."
    }
]

print(f"=== CHỤP & KIỂM ĐỊNH {len(candidates)} LANDING PAGE Ô TÔ & MERCEDES-BENZ ===")
results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for idx, site in enumerate(candidates, 1):
        print(f"\n[{idx:02d}/{len(candidates)}] {site['name']} ({site['url']})...")
        raw_png = os.path.join(output_dir, f"{site['slug']}.png")
        full_webp = os.path.join(kho_webp_dir, f"{site['slug']}_full.webp")

        site["image"] = f"Anh_Chup_Website/{site['slug']}.png"
        site["thumb"] = f"Kho_Anh_Webp/{site['slug']}_thumb.webp"
        site["full"] = f"Kho_Anh_Webp/{site['slug']}_full.webp"
        site["fb"] = f"Kho_Anh_Webp/{site['slug']}_fb.png"

        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            ignore_https_errors=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        setup_page_protection(page)
        try:
            page.goto(site['url'], timeout=45000, wait_until="domcontentloaded")
            time.sleep(3.5)
            # Dismiss cookie/consent/promo popups cleanly before capture
            page.evaluate("""() => {
                const selectors = [
                    'button[aria-label*="Close" i]', 'button[aria-label*="accept" i]',
                    '.onetrust-close-btn-handler', '#onetrust-accept-btn-handler',
                    '.cookie-accept', '.btn-close-popup', '.popup-close', '.close-modal',
                    '.mfp-close', '.fancybox-close-small', '.elementor-popup-modal .dialog-close-button',
                    'button:has-text("Đóng")', 'button:has-text("Accept")'
                ];
                selectors.forEach(sel => {
                    try { document.querySelectorAll(sel).forEach(btn => { try { btn.click(); } catch(e) {} }); } catch(e) {}
                });
            }""")
            time.sleep(0.8)
            capture_smart_clean(page, raw_png, viewport_height=900, scroll_delay=0.3)
            thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb = compress_tri_layer(raw_png, site['slug'], kho_webp_dir)
            valid, msg = verify_captured_image(full_webp)
            print(f"  [+] QA: {'PASS' if valid else 'FAIL'} - {msg}")
            if not valid:
                print("  [!] Self-Healing Vòng 2: Chụp lại với networkidle + delay 0.5s...")
                page.goto(site['url'], timeout=50000, wait_until="networkidle")
                time.sleep(4.0)
                capture_smart_clean(page, raw_png, viewport_height=900, scroll_delay=0.5)
                thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb = compress_tri_layer(raw_png, site['slug'], kho_webp_dir)
                valid, msg = verify_captured_image(full_webp)
                print(f"  [+] QA Vòng 2: {'PASS' if valid else 'FAIL'} - {msg}")

            site["thumb_kb"] = thumb_kb
            site["full_kb"] = full_kb
            site["fb_kb"] = fb_kb
            site["size_mb"] = f"{round(os.path.getsize(raw_png) / (1024*1024), 2)} MB"
            site["audit_msg"] = msg
            site["status"] = "SUCCESS" if valid else "FAIL"
            results.append((site["id"], site["domain"], "PASS" if valid else "FAIL", msg))
        except Exception as e:
            print(f"  [-] Error {site['domain']}: {e}")
            site["status"] = "FAIL"
            site["audit_msg"] = str(e)[:120]
            results.append((site["id"], site["domain"], "FAIL", str(e)[:80]))
        finally:
            context.close()
    browser.close()

with open(metadata_file, "w", encoding="utf-8") as f:
    json.dump(candidates, f, ensure_ascii=False, indent=2)

print("\n=== TỔNG KẾT QA 20 LANDING PAGE Ô TÔ & MERCEDES ===")
for r in results:
    print(f"  {r[0]} | {r[1]:32s} | {r[2]:4s} | {r[3]}")
