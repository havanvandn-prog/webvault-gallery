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
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "vlxd_pool_audit.json")

os.makedirs(output_dir, exist_ok=True)
os.makedirs(kho_webp_dir, exist_ok=True)

pool = [
    # --- NHÓM 1: GẠCH ỐP LÁT, ĐÁ NHÂN TẠO, GỖ & VẬT LIỆU HOÀN THIỆN VIỆT NAM ---
    {
        "name": "Vietceramics — Gạch Ốp Lát Nhập Khẩu & Thiết Bị Phòng Tắm Cao Cấp",
        "short_name": "Vietceramics",
        "url": "https://www.vietceramics.com/",
        "domain": "vietceramics.com",
        "slug": "vlxd_vietceramics",
        "category": "Luxury Tiles & Sanitary Ware",
        "category_vn": "Vietceramics — Gạch Ốp Lát Châu Âu & Thiết Bị Phòng Tắm",
        "tag": "gach-da-vat-lieu-vn",
        "vibe": "Luxury Showroom • Ảnh Không Gian Thực • Catalog Đẳng Cấp",
        "location": "TP.HCM, Hà Nội & Đà Nẵng",
        "desc": "Hình mẫu chuẩn mực cho website showroom gạch ốp lát và thiết bị phòng tắm cao cấp: trình bày bộ sưu tập theo không gian ứng dụng, ảnh sắc nét và trải nghiệm tìm sản phẩm rất tinh tế."
    },
    {
        "name": "Eurotile — Gạch Ốp Lát Kiệt Tác Nghệ Thuật (Viglacera)",
        "short_name": "Eurotile",
        "url": "https://www.eurotile.vn/",
        "domain": "eurotile.vn",
        "slug": "vlxd_eurotile",
        "category": "Artistic Architectural Tiles",
        "category_vn": "Eurotile — Gạch Ốp Lát Nghệ Thuật & Cảm Hứng Kiến Trúc",
        "tag": "gach-da-vat-lieu-vn",
        "vibe": "Editorial Architecture • Bộ Sưu Tập Gạch • Tối Giản Sang Trọng",
        "location": "Toàn Quốc (VN)",
        "desc": "Giao diện mang phong cách tạp chí kiến trúc châu Âu, kể câu chuyện từng bộ sưu tập gạch vân đá/vân gỗ cùng thư viện phối cảnh phòng thực tế cực kỳ cuốn hút."
    },
    {
        "name": "Vicostone — Đá Nhân Tạo Gốc Thạch Anh Cao Cấp Hàng Đầu Thế Giới",
        "short_name": "Vicostone",
        "url": "https://vicostone.com/vi-vn",
        "domain": "vicostone.com",
        "slug": "vlxd_vicostone",
        "category": "Engineered Quartz Surfaces",
        "category_vn": "Vicostone — Đá Thạch Anh Nhân Tạo & Thư Viện Vân Đá",
        "tag": "gach-da-vat-lieu-vn",
        "vibe": "Global Vietnamese Brand • Thư Viện Vân Đá • Xem Phối Cảnh",
        "location": "Hà Nội & Toàn Cầu",
        "desc": "Website thương hiệu đá nhân tạo tầm cỡ quốc tế với bố cục sang trọng, làm nổi bật chi tiết đường vân đá, ứng dụng bàn bếp/ốp tường và hệ thống showroom đại lý."
    },
    {
        "name": "Gỗ An Cường — Vật Liệu, Giải Pháp & Nội Thất Gỗ Công Nghiệp",
        "short_name": "Gỗ An Cường",
        "url": "https://ancuong.com/",
        "domain": "ancuong.com",
        "slug": "vlxd_ancuong",
        "category": "Wood Materials & Interior Solutions",
        "category_vn": "An Cường — Catalog Vật Liệu Gỗ, Laminate, Acrylic & Phụ Kiện",
        "tag": "gach-da-vat-lieu-vn",
        "vibe": "Material Catalog Leader • Hệ Sinh Thái Vật Liệu • Chuẩn Doanh Nghiệp",
        "location": "TP.HCM & Toàn Quốc",
        "desc": "Cổng thông tin mẫu mực của hãng vật liệu gỗ công nghiệp số 1 Việt Nam: phân loại khoa học hàng nghìn mã màu ván gỗ, giải pháp đồng bộ và thư viện ứng dụng cho kiến trúc sư."
    },
    {
        "name": "Caslaquartz — Đá Thạch Anh Nhân Tạo Cao Cấp Chuẩn Quốc Tế",
        "short_name": "Caslaquartz",
        "url": "https://caslaquartz.com/",
        "domain": "caslaquartz.com",
        "slug": "vlxd_caslaquartz",
        "category": "Premium Quartz Slabs",
        "category_vn": "Caslaquartz — Đá Thạch Anh Nhân Tạo & Không Gian Sống",
        "tag": "gach-da-vat-lieu-vn",
        "vibe": "Refined Minimal • Bộ Sưu Tập Đá • Ảnh Công Trình",
        "location": "Hà Nội & Toàn Quốc",
        "desc": "Thiết kế tối giản làm tôn lên vẻ đẹp bề mặt đá thạch anh nhân tạo, kết hợp danh mục phân nhóm màu sắc và nút tra cứu đại lý/nhận báo giá nhanh."
    },
    {
        "name": "Đồng Tâm Group — Gạch Ốp Lát, Ngói Màu, Sơn & Vật Liệu Xây Dựng",
        "short_name": "Đồng Tâm Group",
        "url": "https://dongtam.com.vn/",
        "domain": "dongtam.com.vn",
        "slug": "vlxd_dongtam",
        "category": "Multi-Category Building Materials",
        "category_vn": "Đồng Tâm — Thương Hiệu Quốc Gia Gạch, Ngói & Sơn Nước",
        "tag": "gach-da-vat-lieu-vn",
        "vibe": "Heritage Corporate • Đa Danh Mục VLXD • Trực Quan Rõ Ràng",
        "location": "Long An, TP.HCM & Toàn Quốc",
        "desc": "Website doanh nghiệp vật liệu xây dựng đa ngành lâu đời, cấu trúc danh mục rõ ràng từ gạch bông, gạch porcelain, ngói màu đến thiết bị vệ sinh."
    },
    {
        "name": "Viglacera Tiles — Gạch Ốp Lát & Đá Nung Kết Công Nghệ Xanh",
        "short_name": "Viglacera Tiles",
        "url": "https://viglaceratiles.vn/",
        "domain": "viglaceratiles.vn",
        "slug": "vlxd_viglaceratiles",
        "category": "Porcelain & Sintered Stone Tiles",
        "category_vn": "Viglacera Tiles — Gạch Porcelain & Đá Nung Kết Khổ Lớn",
        "tag": "gach-da-vat-lieu-vn",
        "vibe": "Modern Material Showcase • Công Nghệ Xanh • Danh Mục Gọn",
        "location": "Hà Nội & Toàn Quốc",
        "desc": "Giao diện hiện đại giới thiệu các dòng gạch ốp lát và tấm đá nung kết khổ lớn, nhấn mạnh yếu tố công nghệ xanh và ứng dụng cho công trình dân dụng, thương mại."
    },
    {
        "name": "Vĩnh Tường (Saint-Gobain) — Giải Pháp Trần & Vách Thạch Cao",
        "short_name": "Vĩnh Tường",
        "url": "https://vinhtuong.com/",
        "domain": "vinhtuong.com",
        "slug": "vlxd_vinhtuong",
        "category": "Drywall & Ceiling Systems",
        "category_vn": "Vĩnh Tường — Hệ Giải Pháp Trần, Vách Thạch Cao & Dự Toán",
        "tag": "gach-da-vat-lieu-vn",
        "vibe": "Solution-Driven CRO • Dự Toán Vật Tư • Tìm Thợ & Đại Lý",
        "location": "TP.HCM & Toàn Quốc",
        "desc": "Mẫu web VLXD cực kỳ thực chiến về chuyển đổi: phân chia rõ giải pháp theo nhu cầu (chống ẩm, chống nóng, cách âm), tích hợp công cụ tìm nhà thầu và nhận báo giá thi công."
    },
    {
        "name": "Kosmos Việt Nam — Tổng Kho Sàn Gỗ, Tấm Ốp Lam Sóng & Gỗ Nhựa",
        "short_name": "Kosmos",
        "url": "https://kosmos.vn/",
        "domain": "kosmos.vn",
        "slug": "vlxd_kosmos",
        "category": "Flooring & Wall Panel Distributor",
        "category_vn": "Kosmos — Tổng Kho Sàn Gỗ, Tấm Ốp PVC & Gỗ Nhựa Ngoài Trời",
        "tag": "gach-da-vat-lieu-vn",
        "vibe": "Wholesale Catalog • Chuẩn SEO VLXD • Đa Dạng Mẫu Mã",
        "location": "TP.HCM & Toàn Quốc",
        "desc": "Hình mẫu chuẩn cho website tổng kho phân phối vật liệu trang trí (sàn gỗ, tấm nhựa giả đá, lam sóng, gỗ nhựa ngoài trời) với danh mục trực quan và phễu tuyển đại lý/báo giá mạnh."
    },
    {
        "name": "Topmat Store — Sàn Thương Mại Điện Tử Vật Liệu Xây Dựng & Đá Tự Nhiên",
        "short_name": "Topmat Store",
        "url": "https://topmatstore.vn/",
        "domain": "topmatstore.vn",
        "slug": "vlxd_topmatstore",
        "category": "Building Materials E-Commerce",
        "category_vn": "Topmat — Web Bán Lẻ & Báo Giá VLXD, Đá Tự Nhiên Trực Tuyến",
        "tag": "gach-da-vat-lieu-vn",
        "vibe": "E-Commerce VLXD • Niêm Yết Giá Rõ • Danh Mục Siêu Đầy Đủ",
        "location": "Hà Nội, TP.HCM & Toàn Quốc",
        "desc": "Mẫu website thương mại điện tử bán vật liệu xây dựng trực tuyến cực kỳ hữu ích để tham khảo: có giá tham khảo từng mã đá tự nhiên, gạch trang trí, keo dán gạch và giỏ hàng đặt mua nhanh."
    },
    {
        "name": "Tập Đoàn Hòa Phát — Thép Xây Dựng, Ống Thép & Tôn Mạ",
        "short_name": "Hòa Phát Group",
        "url": "https://www.hoaphat.com.vn/",
        "domain": "hoaphat.com.vn",
        "slug": "vlxd_hoaphat",
        "category": "Steel & Heavy Construction Materials",
        "category_vn": "Hòa Phát — Tập Đoàn Thép Xây Dựng & Vật Liệu Công Nghiệp",
        "tag": "gach-da-vat-lieu-vn",
        "vibe": "Industrial Powerhouse • Tông Xanh Thép • Quy Mô Quốc Gia",
        "location": "Hà Nội & Toàn Quốc",
        "desc": "Giao diện chuẩn tập đoàn sản xuất vật liệu công nghiệp nặng (thép xây dựng, ống thép, tôn mạ), bố cục vững chãi, minh bạch thông số và hệ thống phân phối."
    },

    # --- NHÓM 2: CỬA NHÔM KÍNH, CỬA CUỐN, THIẾT BỊ VỆ SINH & SƠN VIỆT NAM ---
    {
        "name": "Eurowindow — Giải Pháp Tổng Thể Về Cửa, Nhôm Kính & Vách Dựng",
        "short_name": "Eurowindow",
        "url": "https://eurowindow.biz/",
        "domain": "eurowindow.biz",
        "slug": "vlxd_eurowindow",
        "category": "Windows, Doors & Facade Systems",
        "category_vn": "Eurowindow — Cửa Nhôm Kính, Cửa Gỗ & Mặt Dựng Công Trình",
        "tag": "cua-nhom-tbvs-vn",
        "vibe": "Leading Door Brand • Trưng Bày Dự Án • Catalogue Cửa Đầy Đủ",
        "location": "Hà Nội, TP.HCM & Toàn Quốc",
        "desc": "Website chuẩn mực nhất ngành cửa nhôm kính tại Việt Nam: phân loại rõ cửa nhôm, cửa uPVC, cửa gỗ, vách kính lớn kèm dự án thực tế và nút đăng ký tư vấn báo giá."
    },
    {
        "name": "Austdoor — Cửa Cuốn Thông Minh & Giải Pháp Cửa Toàn Diện",
        "short_name": "Austdoor",
        "url": "https://austdoor.com/",
        "domain": "austdoor.com",
        "slug": "vlxd_austdoor",
        "category": "Smart Rolling Doors & Access",
        "category_vn": "Austdoor — Cửa Cuốn Thương Hiệu Quốc Gia & Phụ Kiện Đồng Bộ",
        "tag": "cua-nhom-tbvs-vn",
        "vibe": "Product Showcase • Tính Năng An Toàn • Tìm Đại Lý & Báo Giá",
        "location": "Toàn Quốc (VN)",
        "desc": "Giao diện thương hiệu cửa cuốn dẫn đầu thị trường với cách trình bày công nghệ an toàn trực quan, danh mục sản phẩm rõ ràng và luồng đặt tư vấn lắp đặt nhanh."
    },
    {
        "name": "Nhôm Topal — Hệ Cửa Nhôm Đồng Bộ Tập Đoàn Austdoor",
        "short_name": "Cửa Nhôm Topal",
        "url": "https://topal.vn/",
        "domain": "topal.vn",
        "slug": "vlxd_topal",
        "category": "Synchronized Aluminum Doors",
        "category_vn": "Nhôm Topal — Cửa Nhôm Đồng Bộ Chống Ồn & Kín Nước",
        "tag": "cua-nhom-tbvs-vn",
        "vibe": "Clean Door Brand • Tông Xanh Navy • Trình Bày Hệ Nhôm Rõ",
        "location": "Toàn Quốc (VN)",
        "desc": "Website chuyên biệt cho sản phẩm cửa nhôm định hình đồng bộ, bố cục sạch sẽ, nhấn mạnh ưu điểm kỹ thuật (kín nước, cách âm) và bộ sưu tập công trình nhà phố/biệt thự."
    },
    {
        "name": "Koffmann — Cửa Thép Vân Gỗ & Cửa Chống Cháy Cao Cấp",
        "short_name": "Koffmann",
        "url": "https://koffmann.vn/",
        "domain": "koffmann.vn",
        "slug": "vlxd_koffmann",
        "category": "Wood-Grain Steel Doors",
        "category_vn": "Koffmann — Cửa Thép Vân Gỗ, Cửa Chính & Cửa Chống Cháy",
        "tag": "cua-nhom-tbvs-vn",
        "vibe": "Conversion Door Shop • Lưới Mẫu Cửa Đẹp • Báo Giá Nhanh",
        "location": "Hà Nội & Toàn Quốc",
        "desc": "Hình mẫu thực chiến rất hay cho các doanh nghiệp sản xuất/phân phối cửa nhà ở: phân loại rõ cửa 1 cánh, 2 cánh, 4 cánh, showroom toàn quốc và form nhận báo giá."
    },
    {
        "name": "Xingfa Group — Cửa Nhôm Xingfa Nhập Khẩu Chính Hãng",
        "short_name": "Xingfa Group",
        "url": "https://xingfagroup.vn/",
        "domain": "xingfagroup.vn",
        "slug": "vlxd_xingfagroup",
        "category": "Xingfa Aluminum Door Specialist",
        "category_vn": "Xingfa Group — Thi Công Cửa Nhôm Xingfa & Báo Giá Chi Tiết",
        "tag": "cua-nhom-tbvs-vn",
        "vibe": "SEO Lead Gen • Công Trình Thực Tế • Bảng Giá Minh Bạch",
        "location": "Hà Nội & TP.HCM",
        "desc": "Mẫu website chuyên thi công cửa nhôm kính hướng mạnh vào khách tìm kiếm Google Ads & SEO: tập trung mẫu cửa thực tế, cam kết phụ kiện chính hãng và báo giá nhanh."
    },
    {
        "name": "TOTO Việt Nam — Thiết Bị Vệ Sinh Cao Cấp Nhật Bản",
        "short_name": "TOTO Việt Nam",
        "url": "https://vn.toto.com/",
        "domain": "vn.toto.com",
        "slug": "vlxd_totovn",
        "category": "Japanese Sanitary Ware & Bath",
        "category_vn": "TOTO Việt Nam — Thiết Bị Vệ Sinh, Washlet & Phòng Tắm Cao Cấp",
        "tag": "cua-nhom-tbvs-vn",
        "vibe": "Japanese Minimalism • Trải Nghiệm Phòng Tắm • Catalog Sắc Nét",
        "location": "Toàn Quốc (VN)",
        "desc": "Giao diện tối giản chuẩn Nhật với khoảng thở rộng rãi, trình bày công nghệ phòng tắm cao cấp và danh mục thiết bị vệ sinh cực kỳ trực quan."
    },
    {
        "name": "INAX Việt Nam — Thiết Bị Vệ Sinh & Gạch Kiến Trúc Nhật Bản",
        "short_name": "INAX Việt Nam",
        "url": "https://www.inax.com.vn/",
        "domain": "inax.com.vn",
        "slug": "vlxd_inaxvn",
        "category": "Bath & Architectural Ceramics",
        "category_vn": "INAX — Thiết Bị Phòng Tắm & Gạch Kiến Trúc Ngoại Thất",
        "tag": "cua-nhom-tbvs-vn",
        "vibe": "Clean Blue-White • Gợi Ý Không Gian • Danh Mục Đa Dạng",
        "location": "Toàn Quốc (VN)",
        "desc": "Website thiết bị vệ sinh và gạch kiến trúc cân bằng tốt giữa cảm hứng không gian phòng tắm đẹp và hệ thống tra cứu sản phẩm, showroom chính hãng."
    },
    {
        "name": "Häfele Home — Phụ Kiện Cửa, Khóa Điện Tử & Thiết Bị Hoàn Thiện Đức",
        "short_name": "Häfele Home",
        "url": "https://hafelehome.com.vn/",
        "domain": "hafelehome.com.vn",
        "slug": "vlxd_hafelevn",
        "category": "Architectural Hardware & Home",
        "category_vn": "Häfele — Phụ Kiện Ngành Cửa, Khóa Thông Minh & Thiết Bị Bếp",
        "tag": "cua-nhom-tbvs-vn",
        "vibe": "German E-Commerce • Danh Mục Chuẩn Xác • Thanh Toán Online",
        "location": "TP.HCM, Hà Nội & Toàn Quốc",
        "desc": "Mẫu web bán lẻ vật tư hoàn thiện & phụ kiện cửa chuẩn Đức: giao diện sạch sẽ, hiển thị giá bán rõ ràng, lọc theo nhóm phụ kiện và giỏ hàng hiện đại."
    },
    {
        "name": "Dulux Việt Nam — Sơn Nước Kiến Trúc & Công Cụ Phối Màu",
        "short_name": "Dulux Việt Nam",
        "url": "https://www.dulux.vn/vi",
        "domain": "dulux.vn",
        "slug": "vlxd_duluxvn",
        "category": "Architectural Paints & Color Tools",
        "category_vn": "Dulux — Sơn Nội Ngoại Thất & Bảng Màu Kiến Trúc",
        "tag": "cua-nhom-tbvs-vn",
        "vibe": "Color Inspiration • Trải Nghiệm Phối Màu • Thân Thiện Người Dùng",
        "location": "Toàn Quốc (VN)",
        "desc": "Chuẩn mực trải nghiệm người dùng ngành sơn xây dựng: dẫn dắt khách hàng từ cảm hứng màu sắc, bảng màu tương tác đến chọn đúng dòng sơn chống thấm/nội thất."
    },
    {
        "name": "Jotun Việt Nam — Sơn Trang Trí & Giải Pháp Bảo Vệ Công Trình",
        "short_name": "Jotun Việt Nam",
        "url": "https://www.jotun.com/vn-vi",
        "domain": "jotun.com",
        "slug": "vlxd_jotunvn",
        "category": "Nordic Paint & Coatings",
        "category_vn": "Jotun — Sơn Trang Trí Bắc Âu & Sơn Công Nghiệp",
        "tag": "cua-nhom-tbvs-vn",
        "vibe": "Nordic Editorial • Ảnh Màu Sắc Đẹp • Bố Cục Tối Giản",
        "location": "Toàn Quốc (VN)",
        "desc": "Giao diện mang phong cách Bắc Âu cực kỳ tinh tế, ảnh không gian phối màu sơn sống động và cấu trúc phân chia rõ ràng giữa khách hàng nhà ở và dự án công nghiệp."
    },
    {
        "name": "Nippon Paint Việt Nam — Sơn Trang Trí & Phủ Bảo Vệ Công Trình",
        "short_name": "Nippon Paint",
        "url": "https://nipponpaint.com.vn/",
        "domain": "nipponpaint.com.vn",
        "slug": "vlxd_nipponvn",
        "category": "Paint & Waterproofing Solutions",
        "category_vn": "Nippon Paint — Sơn Nhà Ở, Chống Thấm & Tính Lượng Sơn",
        "tag": "cua-nhom-tbvs-vn",
        "vibe": "Interactive Paint Portal • Công Cụ Tính Sơn • Nhận Diện Mạnh",
        "location": "Toàn Quốc (VN)",
        "desc": "Website ngành sơn nổi bật với màu sắc nhận diện tươi mới, phân nhóm sản phẩm theo bề mặt (nội thất, ngoại thất, chống thấm, sơn gỗ kim loại) và hệ thống đại lý."
    },

    # --- NHÓM 3: VẬT LIỆU KIẾN TRÚC & GẠCH ĐÁ QUỐC TẾ CHUẨN UI/UX ---
    {
        "name": "Caesarstone — Đá Thạch Anh & Bề Mặt Kiến Trúc Chuẩn UI/UX Mỹ",
        "short_name": "Caesarstone",
        "url": "https://www.caesarstoneus.com/",
        "domain": "caesarstoneus.com",
        "slug": "vlxd_caesarstone",
        "category": "Global Quartz & Porcelain Surfaces",
        "category_vn": "Caesarstone (Mỹ) — Đá Bề Mặt Kiến Trúc & Đặt Mẫu Thử",
        "tag": "quoc-te-vlxd",
        "vibe": "Architectural Luxury • Order Sample CTA • Lưới Mẫu Đá Đẹp",
        "location": "Mỹ & Toàn Cầu",
        "desc": "Hình mẫu đỉnh cao cho website bán đá/gạch cao cấp: tập trung trải nghiệm xem vân đá cận cảnh, phối cảnh không gian bếp sang trọng và nút đặt mẫu vật liệu gửi tận nơi."
    },
    {
        "name": "Florim Italy — Gạch Đá Sứ Khổ Lớn Phong Cách Kiến Trúc Ý",
        "short_name": "Florim Italy",
        "url": "https://www.florim.com/en/",
        "domain": "florim.com",
        "slug": "vlxd_florim",
        "category": "Italian Porcelain Slabs",
        "category_vn": "Florim (Ý) — Tấm Đá Sứ Kiến Trúc Khổ Lớn & Thiết Kế Đương Đại",
        "tag": "quoc-te-vlxd",
        "vibe": "Italian High-Design • Không Gian Kiến Trúc • Sang Trọng Tuyệt Đối",
        "location": "Modena, Ý & Toàn Cầu",
        "desc": "Chuẩn mực thiết kế web vật liệu kiến trúc từ Ý: hình ảnh khổ lớn đầy nghệ thuật, bố cục bất đối xứng tinh tế và cách phân loại bộ sưu tập vật liệu cực kỳ đẳng cấp."
    },
    {
        "name": "Mutina Italy — Đỉnh Cao Thẩm Mỹ Gạch Thiết Kế Kiến Trúc Ý",
        "short_name": "Mutina Italy",
        "url": "https://www.mutina.it/en/",
        "domain": "mutina.it",
        "slug": "vlxd_mutina",
        "category": "Designer Architectural Ceramics",
        "category_vn": "Mutina (Ý) — Gạch Nghệ Thuật & Thẩm Mỹ Tối Giản Đỉnh Cao",
        "tag": "quoc-te-vlxd",
        "vibe": "Gallery Minimalism • Typography Tinh Tế • Cảm Hứng Kiến Trúc Sư",
        "location": "Modena, Ý",
        "desc": "Một trong những website ngành gạch đẹp nhất thế giới theo phong cách phòng triển lãm (Gallery): tối giản tuyệt đối, để từng viên gạch và bề mặt vật liệu tự tỏa sáng."
    },
    {
        "name": "Laminam Italy — Tấm Đá Nung Kết Khổ Lớn Cho Kiến Trúc & Nội Thất",
        "short_name": "Laminam Italy",
        "url": "https://www.laminam.com/en/",
        "domain": "laminam.com",
        "slug": "vlxd_laminam",
        "category": "Large Format Sintered Surfaces",
        "category_vn": "Laminam (Ý) — Đá Nung Kết Khổ Lớn Ốp Mặt Tiền & Nội Thất",
        "tag": "quoc-te-vlxd",
        "vibe": "Sleek Material Tech • Ứng Dụng Mặt Dựng & Bếp • Tinh Gọn",
        "location": "Ý & Toàn Cầu",
        "desc": "Giao diện hiện đại làm nổi bật vật liệu đá nung kết siêu mỏng khổ lớn, phân tách mạch lạc giữa ứng dụng kiến trúc mặt tiền, sàn tường và bàn bếp."
    },
    {
        "name": "Marazzi Group — Gạch Ốp Lát Kiến Trúc Ý Chuẩn Lưới Sản Phẩm",
        "short_name": "Marazzi Italy",
        "url": "https://www.marazzigroup.com/",
        "domain": "marazzigroup.com",
        "slug": "vlxd_marazzi",
        "category": "Global Ceramic & Porcelain Leader",
        "category_vn": "Marazzi (Ý) — Gạch Ốp Lát Châu Âu & Thư Viện Phối Cảnh Đỉnh Cao",
        "tag": "quoc-te-vlxd",
        "vibe": "Editorial Catalog • Lọc Hiệu Ứng Bề Mặt • Cân Bằng Thương Mại",
        "location": "Sassuolo, Ý & Toàn Cầu",
        "desc": "Website gạch ốp lát quốc tế cân bằng hoàn hảo giữa nghệ thuật trình bày không gian sống và khả năng tra cứu nhanh theo hiệu ứng (vân đá, vân gỗ, xi măng, terrazzo)."
    },
]

results = []
passed_list = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for idx, site in enumerate(pool, 1):
        site["id"] = f"vl{idx:02d}"
        site["industry"] = "vat-lieu-xay-dung"
        site["industry_name"] = "Vật Liệu Xây Dựng (Gạch, Đá, Cửa, Nhôm Kính)"
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
                    'button[class*="cookie" i]', '.iubenda-cs-accept-btn',
                    '[data-testid="cookie-accept"]', '.cc-allow', '.cc-dismiss'
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
                        '[id*="iubenda" i], [class*="iubenda" i], ' +
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

print(f"\n=== TỔNG KẾT QA NGÁCH 5 (VẬT LIỆU XÂY DỰNG): ĐẠT {len(passed_list)}/{len(pool)} MẪU ===")
for r in results:
    print(f"  {r[0]:22s} | {r[1]:28s} | {r[2]:9s} | {r[3]}")
