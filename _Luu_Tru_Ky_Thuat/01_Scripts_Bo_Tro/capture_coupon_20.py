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
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "website_coupon_metadata.json")

os.makedirs(output_dir, exist_ok=True)
os.makedirs(kho_webp_dir, exist_ok=True)
os.makedirs(os.path.dirname(metadata_file), exist_ok=True)

websites = [
    # NHÓM 1: MẪU WORDPRESS THEME COUPON & CASHBACK CHUYÊN NGHIỆP
    {
        "id": "cp01",
        "name": "ClipMyDeals — Mẫu Coupon & Cashback WordPress (Layout 1)",
        "short_name": "ClipMyDeals Layout 1",
        "url": "https://demo.clipmydeals.com/1/",
        "domain": "demo.clipmydeals.com",
        "slug": "coupon_clipmydeals_layout1",
        "industry": "website-coupon-ma-giam-gia",
        "industry_name": "Website Dạng Coupon & Săn Deal",
        "category": "WordPress Coupon & Cashback Theme",
        "category_vn": "Theme WordPress Chuyên Dụng Coupon & Hoàn Tiền Tự Động",
        "tag": "wp-coupon-theme",
        "vibe": "Chuẩn WordPress Coupon • Click Lấy Mã + Thanh Tìm Kiếm Cực Đẹp",
        "location": "Quốc tế (Demo ClipMyDeals)",
        "desc": "Theme WordPress số 1 thế giới cho website mã giảm giá và cashback. Tích hợp sẵn cơ chế nạp coupon tự động qua API, nút click sao chép mã (Click-to-Reveal) nhảy sang link affiliate, bộ lọc theo danh mục và thương hiệu hàng đầu."
    },
    {
        "id": "cp02",
        "name": "ClipMyDeals — Mẫu Săn Deal & Voucher Trực Quan (Layout 2)",
        "short_name": "ClipMyDeals Layout 2",
        "url": "https://demo.clipmydeals.com/2/",
        "domain": "demo.clipmydeals.com",
        "slug": "coupon_clipmydeals_layout2",
        "industry": "website-coupon-ma-giam-gia",
        "industry_name": "Website Dạng Coupon & Săn Deal",
        "category": "WordPress Modern Deal & Coupon Theme",
        "category_vn": "Theme WordPress Bố Cục Thẻ Deal Nổi Bật & Slider Khuyến Mãi",
        "tag": "wp-coupon-theme",
        "vibe": "Slider Deal Nóng • Lưới Cửa Hàng Đối Tác Hấp Dẫn",
        "location": "Quốc tế (Demo ClipMyDeals)",
        "desc": "Biến thể layout 2 của ClipMyDeals với banner trượt giới thiệu deal hot nhất trong ngày, lưới logo cửa hàng đối tác (Merchant Grid) và nhãn đếm ngược thời gian hết hạn voucher (Countdown Timer)."
    },
    {
        "id": "cp03",
        "name": "ClipMyDeals — Mẫu Danh Mục Coupon Tối Giản (Layout 3)",
        "short_name": "ClipMyDeals Layout 3",
        "url": "https://demo.clipmydeals.com/3/",
        "domain": "demo.clipmydeals.com",
        "slug": "coupon_clipmydeals_layout3",
        "industry": "website-coupon-ma-giam-gia",
        "industry_name": "Website Dạng Coupon & Săn Deal",
        "category": "WordPress Minimalist Voucher Portal",
        "category_vn": "Cổng Tra Cứu Voucher Tối Giản Tốc Độ Cao",
        "tag": "wp-coupon-theme",
        "vibe": "Gọn Gàng Sạch Sẽ • Phân Loại Cửa Hàng A-Z",
        "location": "Quốc tế (Demo ClipMyDeals)",
        "desc": "Bố cục tối giản tập trung vào tốc độ tải trang trên hosting/VPS. Cung cấp danh bạ tra cứu cửa hàng theo bảng chữ cái A-Z, bảng lọc voucher theo phần trăm giảm giá và bộ lọc loại deal (In-store vs Online)."
    },
    {
        "id": "cp04",
        "name": "ClipMyDeals — Mẫu Săn Voucher Đa Sàn Thương Mại (Layout 4)",
        "short_name": "ClipMyDeals Layout 4",
        "url": "https://demo.clipmydeals.com/4/",
        "domain": "demo.clipmydeals.com",
        "slug": "coupon_clipmydeals_layout4",
        "industry": "website-coupon-ma-giam-gia",
        "industry_name": "Website Dạng Coupon & Săn Deal",
        "category": "Multi-Store Affiliate Voucher Showcase",
        "category_vn": "Cổng Tổng Hợp Voucher Đa Cửa Hàng & Bảng Xếp Hạng Deal",
        "tag": "wp-coupon-theme",
        "vibe": "Đa Cửa Hàng • Thẻ Voucher Nổi Bật Giảm Sâu",
        "location": "Quốc tế (Demo ClipMyDeals)",
        "desc": "Layout chuyên dụng cho website làm affiliate đa ngành hàng (thời trang, công nghệ, du lịch, mẹ bé). Bố cục thẻ coupon phân chia rõ: mã giảm trực tiếp (Code), ưu đãi tự động kích hoạt (Deal) và quà tặng kèm."
    },
    {
        "id": "cp05",
        "name": "REHub Refashion — Theme WordPress Affiliate & Deal Hàng Đầu",
        "short_name": "REHub Refashion Deals",
        "url": "https://refashion.wpsoul.net/",
        "domain": "refashion.wpsoul.net",
        "slug": "coupon_rehub_refashion",
        "industry": "website-coupon-ma-giam-gia",
        "industry_name": "Website Dạng Coupon & Săn Deal",
        "category": "WordPress Affiliate & Deal Framework",
        "category_vn": "Framework WordPress Đỉnh Cao Cho Deal Khuyến Mãi & Thời Trang",
        "tag": "wp-coupon-theme",
        "vibe": "Hiện Đại Cao Cấp • Thẻ Sản Phẩm Kèm Giá Cũ/Mới",
        "location": "Quốc tế (WPSoul REHub)",
        "desc": "Demo Refashion trên nền tảng REHub — theme WordPress affiliate bán chạy nhất ThemeForest. Tối ưu cực mạnh cho deal giảm giá có hiển thị giá gốc gạch ngang, phần trăm giảm nổi bật và nút bấm điều hướng mua ngay."
    },
    {
        "id": "cp06",
        "name": "REHub Recart — Mẫu Danh Sách Coupon & So Sánh Giá",
        "short_name": "REHub Recart Coupons",
        "url": "https://recart.wpsoul.com/",
        "domain": "recart.wpsoul.com",
        "slug": "coupon_rehub_recart",
        "industry": "website-coupon-ma-giam-gia",
        "industry_name": "Website Dạng Coupon & Săn Deal",
        "category": "Price Comparison & Coupon WordPress",
        "category_vn": "Cổng So Sánh Giá Kết Hợp Mã Giảm Giá Đa Kênh",
        "tag": "wp-coupon-theme",
        "vibe": "So Sánh Giá Thông Minh • Bảng Tra Cứu Voucher",
        "location": "Quốc tế (WPSoul REHub)",
        "desc": "Bố cục lai giữa so sánh giá sản phẩm từ nhiều sàn TMĐT và hộp mã giảm giá độc quyền. Giúp khách hàng vừa xem được nơi bán rẻ nhất vừa bấm lấy thêm coupon giảm phụ để chốt đơn."
    },
    {
        "id": "cp07",
        "name": "REHub Repick — Tạp Chí Săn Deal & Đánh Giá Sản Phẩm",
        "short_name": "REHub Repick Curated Deals",
        "url": "https://repick.wpsoul.net/",
        "domain": "repick.wpsoul.net",
        "slug": "coupon_rehub_repick",
        "industry": "website-coupon-ma-giam-gia",
        "industry_name": "Website Dạng Coupon & Săn Deal",
        "category": "Curated Deals & Editorial Coupon Portal",
        "category_vn": "Mẫu Tuyển Chọn Deal Tinh Hoa Kèm Đánh Giá Chuyên Gia",
        "tag": "wp-coupon-theme",
        "vibe": "Tạp Chí Mua Sắm • Bố Cục Thẻ Deal Tinh Tế",
        "location": "Quốc tế (WPSoul REHub)",
        "desc": "Mẫu thiết kế dạng tạp chí tuyển chọn (Editorial Curation), mỗi bài viết review gắn liền với các coupon liên quan. Rất phù hợp cho các bạn làm affiliate xây dựng uy tín cá nhân và cộng đồng trung thành."
    },

    # NHÓM 2: TOP WEBSITE COUPON & SĂN DEAL HÀNG ĐẦU VIỆT NAM
    {
        "id": "cp08",
        "name": "Blog Giảm Giá — Website Săn Mã Giảm Giá Số 1 Việt Nam",
        "short_name": "Blog Giảm Giá VN",
        "url": "https://bloggiamgia.vn/",
        "domain": "bloggiamgia.vn",
        "slug": "coupon_bloggiamgia_vn",
        "industry": "website-coupon-ma-giam-gia",
        "industry_name": "Website Dạng Coupon & Săn Deal",
        "category": "Vietnam Top 1 Coupon & Deals Website",
        "category_vn": "Website Mã Giảm Giá Shopee, Lazada & Sàn TMĐT Hàng Đầu VN",
        "tag": "top-vn-coupon",
        "vibe": "Thực Chiến Số 1 VN • Công Cụ Săn Mã & Khung Giờ Vàng",
        "location": "Toàn quốc (Việt Nam)",
        "desc": "Website mã giảm giá thành công nhất tại Việt Nam. Bố cục tối ưu với banner khung giờ sale (0H-9H-12H-20H), thanh lọc mã theo từng sàn TMĐT (Shopee, Lazada, Tiki), và tích hợp hệ thống bot/tool tự động lấy mã."
    },
    {
        "id": "cp09",
        "name": "Chanh Tươi — Cộng Đồng Review & Mã Giảm Giá Lâu Đời",
        "short_name": "Chanh Tươi Review & Deal",
        "url": "https://chanhtuoi.com/",
        "domain": "chanhtuoi.com",
        "slug": "coupon_chanhtuoi_com",
        "industry": "website-coupon-ma-giam-gia",
        "industry_name": "Website Dạng Coupon & Săn Deal",
        "category": "Consumer Review & Deals Community",
        "category_vn": "Cộng Đồng Đánh Giá Tiêu Dùng & Kho Voucher Khổng Lồ",
        "tag": "top-vn-coupon",
        "vibe": "Cộng Đồng Thảo Luận • Kho Mã Đa Lĩnh Vực",
        "location": "Toàn quốc (Việt Nam)",
        "desc": "Nền tảng cộng đồng người tiêu dùng kết hợp chia sẻ mã giảm giá lớn nhất VN. Có chuyên mục riêng cho từng sàn TMĐT, ngân hàng phát hành thẻ, du lịch, ẩm thực và đánh giá độ uy tín từng gian hàng."
    },
    {
        "id": "cp10",
        "name": "Mã Giảm Giá — Cổng Tổng Hợp Coupon Shopee & Lazada",
        "short_name": "MaGiamGia.com",
        "url": "https://magiamgia.com/",
        "domain": "magiamgia.com",
        "slug": "coupon_magiamgia_com",
        "industry": "website-coupon-ma-giam-gia",
        "industry_name": "Website Dạng Coupon & Săn Deal",
        "category": "Pure Affiliate Voucher Directory",
        "category_vn": "Cổng Tra Cứu Voucher Chuẩn Affiliate Thực Chiến",
        "tag": "top-vn-coupon",
        "vibe": "Giao Diện Thẻ Đơn Giản • Nhấn Nút Sao Chép Mã",
        "location": "Toàn quốc (Việt Nam)",
        "desc": "Website affiliate thuần túy tập trung 100% vào việc tìm và sao chép voucher. Giao diện trực diện không rườm rà: chọn logo sàn -> hiện danh sách mã -> click sao chép mã và mở app sàn TMĐT."
    },
    {
        "id": "cp11",
        "name": "Canh Me — Chuyên Trang Coupon Domain, VPS & Hosting Nổi Tiếng",
        "short_name": "Canh Me Coupon Tech",
        "url": "https://canhme.com/",
        "domain": "canhme.com",
        "slug": "coupon_canhme_com",
        "industry": "website-coupon-ma-giam-gia",
        "industry_name": "Website Dạng Coupon & Săn Deal",
        "category": "Tech & Web Hosting Coupon Blog",
        "category_vn": "Chuyên Trang Săn Deal Tên Miền, VPS, Hosting Lớn Nhất VN",
        "tag": "top-vn-coupon",
        "vibe": "Thân Thuộc Dân Webmaster • Cực Kỳ Đáng Tin Cậy",
        "location": "Toàn quốc (Việt Nam)",
        "desc": "Website săn mã giảm giá công nghệ, hosting, VPS, tên miền huyền thoại trong giới làm web Việt Nam. Thiết kế dạng blog tin tức kết hợp coupon code dạng box nổi bật, tích hợp bình luận hỏi đáp trực tiếp."
    },
    {
        "id": "cp12",
        "name": "Riokupon — Nền Tảng Tra Cứu Voucher Theo Link Sản Phẩm",
        "short_name": "Riokupon VN",
        "url": "https://riokupon.com/vn/",
        "domain": "riokupon.com",
        "slug": "coupon_riokupon_vn",
        "industry": "website-coupon-ma-giam-gia",
        "industry_name": "Website Dạng Coupon & Săn Deal",
        "category": "AI Product Link Coupon Finder",
        "category_vn": "Nền Tảng Tra Cứu Mã Giảm Giá Bằng Link Sản Phẩm",
        "tag": "top-vn-coupon",
        "vibe": "Công Nghệ Trẻ Trung • Dán Link Tìm Mã Ngay",
        "location": "Toàn quốc (Việt Nam)",
        "desc": "Mô hình coupon thế hệ mới: người dùng chỉ cần dán link sản phẩm Shopee/Lazada vào ô tìm kiếm, hệ thống tự động bóc tách và liệt kê tất cả các voucher giảm giá sâu nhất có thể áp dụng."
    },
    {
        "id": "cp13",
        "name": "Mekoupon — Tổng Hợp Voucher & Hoàn Tiền Thông Minh",
        "short_name": "Mekoupon Cashback",
        "url": "https://mekoupon.com/",
        "domain": "mekoupon.com",
        "slug": "coupon_mekoupon_com",
        "industry": "website-coupon-ma-giam-gia",
        "industry_name": "Website Dạng Coupon & Săn Deal",
        "category": "Smart Coupon & Cashback Portal",
        "category_vn": "Cổng Voucher Khung Giờ & Tích Hợp Hoàn Tiền Tiện Lợi",
        "tag": "top-vn-coupon",
        "vibe": "Tươi Sáng • Lọc Deal Theo Giờ Vàng",
        "location": "Toàn quốc (Việt Nam)",
        "desc": "Website tích hợp mô hình săn voucher kết hợp hoàn tiền (Cashback). Giao diện tối ưu theo timeline thời gian thực, hiển thị rõ số lượng mã còn lại và phần trăm hoàn tiền khi mua sắm."
    },
    {
        "id": "cp14",
        "name": "MGG.VN — Nền Tảng Mã Giảm Giá Giao Diện Thẻ Hiện Đại",
        "short_name": "MGG.VN",
        "url": "https://mgg.vn/",
        "domain": "mgg.vn",
        "slug": "coupon_mgg_vn",
        "industry": "website-coupon-ma-giam-gia",
        "industry_name": "Website Dạng Coupon & Săn Deal",
        "category": "Modern Card-Based Coupon Directory",
        "category_vn": "Trang Web Mã Giảm Giá Giao Diện Thẻ Đẹp Mắt",
        "tag": "top-vn-coupon",
        "vibe": "Thẻ Bo Góc Hiện Đại • Danh Mục Sàn Nổi Bật",
        "location": "Toàn quốc (Việt Nam)",
        "desc": "Giao diện thẻ phẳng bo góc (Modern Card UI) rất trực quan. Phân chia rõ ràng các mục: Mã độc quyền, Mã Freeship, Mã thanh toán qua ví (ZaloPay, ShopeePay, Viettel Money)."
    },
    {
        "id": "cp15",
        "name": "Mã Giảm Giá Shopee — Chuyên Trang Săn Sale Shopee",
        "short_name": "MaGiamGiaShopee.vn",
        "url": "https://magiamgiashopee.vn/",
        "domain": "magiamgiashopee.vn",
        "slug": "coupon_magiamgiashopee_vn",
        "industry": "website-coupon-ma-giam-gia",
        "industry_name": "Website Dạng Coupon & Săn Deal",
        "category": "Single-Merchant Deep Coupon Portal",
        "category_vn": "Chuyên Trang Săn Sale & Mã Giảm Giá Độc Quyền Shopee",
        "tag": "top-vn-coupon",
        "vibe": "Tập Trung Chuyên Sâu • Đầy Đủ Mã Ẩn & Freeship",
        "location": "Toàn quốc (Việt Nam)",
        "desc": "Mô hình website coupon ngách (Niche Coupon Site) chuyên sâu cho 1 sàn TMĐT lớn nhất. Khai thác triệt để các loại mã voucher ẩn, mã hoàn xu và banner sự kiện siêu sale hàng tháng."
    },
    {
        "id": "cp16",
        "name": "Voucher Sàn — Cổng Tổng Hợp Deal & Mã Khuyến Mãi",
        "short_name": "Voucher Sàn",
        "url": "https://vouchersan.com/",
        "domain": "vouchersan.com",
        "slug": "coupon_vouchersan_com",
        "industry": "website-coupon-ma-giam-gia",
        "industry_name": "Website Dạng Coupon & Săn Deal",
        "category": "Multi-Platform Coupon Aggregator",
        "category_vn": "Cổng Tổng Hợp Voucher Đa Sàn Thương Mại & Dịch Vụ",
        "tag": "top-vn-coupon",
        "vibe": "Trực Diện Dễ Dùng • Bố Cục Thân Thiện Di Động",
        "location": "Toàn quốc (Việt Nam)",
        "desc": "Thiết kế thân thiện với người dùng di động. Các nút sao chép mã được phóng to, có nhãn phân biệt mã sắp hết hạn và hướng dẫn từng bước nhập mã cho người mới bắt đầu."
    },
    {
        "id": "cp17",
        "name": "Hội Săn Mã — Chia Sẻ Mã Giảm Giá & Flash Sale",
        "short_name": "Hội Săn Mã",
        "url": "https://hoisanma.vn/",
        "domain": "hoisanma.vn",
        "slug": "coupon_hoisanma_vn",
        "industry": "website-coupon-ma-giam-gia",
        "industry_name": "Website Dạng Coupon & Săn Deal",
        "category": "Community Deal Sharing Hub",
        "category_vn": "Kênh Chia Sẻ Mã Giảm Giá & Flash Sale Cộng Đồng",
        "tag": "top-vn-coupon",
        "vibe": "Cập Nhật Liên Tục • Nút Bấm Lấy Mã Nhanh",
        "location": "Toàn quốc (Việt Nam)",
        "desc": "Trang web vận hành theo nhịp độ flash sale liên tục. Người dùng có thể lọc nhanh theo mức giảm từ 10k đến 500k, mã hoàn tiền và voucher miễn phí vận chuyển trên toàn quốc."
    },

    # NHÓM 3: NỀN TẢNG COUPON & SĂN DEAL QUỐC TẾ TIÊU BIỂU
    {
        "id": "cp18",
        "name": "CouponFollow — Cổng Coupon & Voucher Hàng Đầu Thế Giới",
        "short_name": "CouponFollow Global",
        "url": "https://couponfollow.com/",
        "domain": "couponfollow.com",
        "slug": "coupon_couponfollow_com",
        "industry": "website-coupon-ma-giam-gia",
        "industry_name": "Website Dạng Coupon & Săn Deal",
        "category": "Premier Global Coupon Directory",
        "category_vn": "Nền Tảng Tra Cứu Coupon Toàn Cầu Giao Diện Chuẩn Mực",
        "tag": "intl-coupon-benchmark",
        "vibe": "Đẳng Cấp Toàn Cầu • Thanh Tìm Kiếm Cực Nhạy & Store Grid",
        "location": "Quốc tế (USA)",
        "desc": "Một trong những website coupon lớn và uy tín nhất thế giới. Điểm chuẩn mực về UI/UX với thanh tìm kiếm thông minh, thẻ cửa hàng nổi tiếng, tỷ lệ thành công của mã (Success Rate %) và ngày xác minh gần nhất."
    },
    {
        "id": "cp19",
        "name": "Offers.com — Nền Tảng Săn Deal & Tiết Kiệm Mua Sắm Toàn Cầu",
        "short_name": "Offers.com",
        "url": "https://www.offers.com/",
        "domain": "offers.com",
        "slug": "coupon_offers_com",
        "industry": "website-coupon-ma-giam-gia",
        "industry_name": "Website Dạng Coupon & Săn Deal",
        "category": "High-Traffic Deals & Savings Portal",
        "category_vn": "Đế Chế Săn Deal Khuyến Mãi & Mã Giảm Giá Quốc Tế",
        "tag": "intl-coupon-benchmark",
        "vibe": "Bố Cục Chuyên Nghiệp • Phân Tầng Nhu Cầu & Mùa Lễ Hội",
        "location": "Quốc tế (USA)",
        "desc": "Cổng thông tin tiết kiệm mua sắm với hàng chục ngàn mã giảm giá mỗi ngày. Trình bày xuất sắc các chiến dịch theo mùa (Black Friday, Cyber Monday, Back to School) và huy hiệu Verified Codes kiểm tra thủ công."
    },
    {
        "id": "cp20",
        "name": "Picodi Việt Nam — Nền Tảng Hoàn Tiền & Mã Khuyến Mãi Quốc Tế",
        "short_name": "Picodi Việt Nam",
        "url": "https://www.picodi.com/vn/",
        "domain": "picodi.com",
        "slug": "coupon_picodi_vn",
        "industry": "website-coupon-ma-giam-gia",
        "industry_name": "Website Dạng Coupon & Săn Deal",
        "category": "International Localized Cashback & Voucher Portal",
        "category_vn": "Nền Tảng Hoàn Tiền & Coupon Quốc Tế Bản Địa Hóa Tại VN",
        "tag": "intl-coupon-benchmark",
        "vibe": "Bản Địa Hóa Xuất Sắc • Tích Hợp Hoàn Tiền Tiện Dụng",
        "location": "Việt Nam & Quốc tế (Picodi)",
        "desc": "Phiên bản tiếng Việt của tập đoàn Picodi toàn cầu. Kết hợp hoàn hảo giữa mã giảm giá của các thương hiệu quốc tế (Nike, Adidas, Agoda, Booking) và các sàn nội địa (Shopee, Lazada, Tiki) kèm tỷ lệ hoàn tiền thật."
    }
]

print("=== BẮT ĐẦU CHỤP 20 WEBSITE DẠNG COUPON & SĂN DEAL ===", flush=True)

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

        print(f"\n[{idx}/20] {item['id'].upper()} ({slug}) -> {item['url']}", flush=True)

        if os.path.exists(full_path) and os.path.exists(thumb_path) and os.path.exists(filepath):
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

        try:
            page.goto(item["url"], wait_until="domcontentloaded", timeout=40000)
            time.sleep(2.5)

            # Đóng các popup modal / banner nếu có
            page.evaluate("""() => {
                const selectors = [
                    '.modal', '.popup', '#onesignal-slidedown-dialog',
                    '.cookie-notice', '#cookie-notice', '.fancybox-overlay'
                ];
                selectors.forEach(s => {
                    document.querySelectorAll(s).forEach(el => el.style.display = 'none');
                });
            }""")

            capture_smart_clean(page, filepath, viewport_height=900, scroll_delay=0.20)
            thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb = compress_tri_layer(filepath, slug, kho_webp_dir)
            ok, audit_msg = verify_captured_image(full_path)
            print(f"  -> Đã chụp & nén: {'PASS' if ok else 'WARN'} - {audit_msg} (Thumb {thumb_kb}KB, Full {full_kb}KB)", flush=True)

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
        except Exception as e:
            print(f"  -> LỖI CHỤP: {e}", flush=True)
            final_metadata.append({
                **item,
                "status": "ERROR",
                "error": str(e)
            })
        finally:
            context.close()

    browser.close()

with open(metadata_file, "w", encoding="utf-8") as f:
    json.dump(final_metadata, f, ensure_ascii=False, indent=2)

passed = sum(1 for x in final_metadata if x.get("status") == "SUCCESS")
print(f"\n=== HOÀN TẤT CHỤP! ĐẠT CHUẨN: {passed}/20 ===", flush=True)
