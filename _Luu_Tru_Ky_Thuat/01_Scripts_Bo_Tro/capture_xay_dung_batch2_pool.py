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
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "xay_dung_batch2_pool_audit.json")

os.makedirs(output_dir, exist_ok=True)
os.makedirs(kho_webp_dir, exist_ok=True)

pool = [
    # --- NHÓM 1: TỔNG THẦU, HẠ TẦNG & KẾT CẤU THÉP VIỆT NAM (ĐỢT 2) ---
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
        "desc": "Cổng thông tin tập đoàn xây dựng Hòa Bình thể hiện bề dày lịch sử, hệ sinh thái dự án dân dụng - hạ tầng - công nghiệp và hệ thống tin tức doanh nghiệp quy mô."
    },
    {
        "name": "CC1 — Tổng Công Ty Xây Dựng Số 1 (Hạ Tầng, Năng Lượng & EPC)",
        "short_name": "CC1",
        "url": "https://www.cc1.vn/",
        "domain": "cc1.vn",
        "slug": "xd_cc1",
        "category": "EPC & Infrastructure Contractor",
        "category_vn": "Tổng Công Ty Xây Dựng Số 1 — Tổng Thầu EPC & Hạ Tầng",
        "tag": "tong-thau-vn",
        "vibe": "Corporate Bold • Công Trình Trọng Điểm • Hạ Tầng Quốc Gia",
        "location": "TP. Hồ Chí Minh & Toàn Quốc",
        "desc": "Website Tổng Công ty Xây dựng Số 1 (CC1) mang phong thái tổng thầu quốc gia với điểm nhấn vào các đại dự án cầu đường, sân bay, nhà máy điện và công trình dân dụng."
    },
    {
        "name": "Vinaconex — Tổng Công Ty CP Xuất Nhập Khẩu & Xây Dựng Việt Nam",
        "short_name": "Vinaconex",
        "url": "https://vinaconex.com.vn/",
        "domain": "vinaconex.com.vn",
        "slug": "xd_vinaconex",
        "category": "Large-Scale Infrastructure & Civil",
        "category_vn": "Vinaconex — Tập Đoàn Xây Dựng & Hạ Tầng Hàng Đầu",
        "tag": "tong-thau-vn",
        "vibe": "Enterprise Corporate • Hạ Tầng & BĐS • Quan Hệ Cổ Đông",
        "location": "Hà Nội & Toàn Quốc",
        "desc": "Cổng thông tin doanh nghiệp xây dựng đầu ngành phía Bắc với cấu trúc phân tầng rõ ràng giữa xây lắp hạ tầng, đầu tư bất động sản và báo cáo tài chính."
    },
    {
        "name": "Viteccons — Tổng Thầu Thiết Kế & Thi Công Xây Dựng Hiện Đại",
        "short_name": "Viteccons",
        "url": "https://www.viteccons.vn/vi",
        "domain": "viteccons.vn",
        "slug": "xd_viteccons",
        "category": "Modern Design-Build Contractor",
        "category_vn": "Tổng Thầu Viteccons — Giao Diện Hiện Đại & Sắc Nét",
        "tag": "tong-thau-vn",
        "vibe": "Clean Modern • Năng Lực Tổng Thầu • Dự Án Cao Tầng & FDI",
        "location": "TP. Hồ Chí Minh & Toàn Quốc",
        "desc": "Website Viteccons được thiết kế hiện đại, mạch lạc, làm nổi bật năng lực tổng thầu thiết kế & thi công qua các dự án cao ốc, khu nghỉ dưỡng và nhà máy công nghiệp."
    },
    {
        "name": "An Phong Construction — Tổng Thầu Xây Dựng Cao Ốc & Công Nghiệp",
        "short_name": "An Phong",
        "url": "https://www.anphong.vn/",
        "domain": "anphong.vn",
        "slug": "xd_anphong",
        "category": "High-Rise & Industrial Contractor",
        "category_vn": "Xây Dựng An Phong — Tổng Thầu Cao Ốc & Nhà Máy",
        "tag": "tong-thau-vn",
        "vibe": "Structured Corporate • Danh Mục Dự Án Lớn • Chuẩn Mực",
        "location": "TP. Hồ Chí Minh & Toàn Quốc",
        "desc": "Giao diện doanh nghiệp xây dựng lâu năm tại phía Nam, trình bày trực quan danh mục công trình cao tầng, trung tâm thương mại và nhà xưởng tiêu chuẩn cao."
    },
    {
        "name": "Đại Dũng Group (DDC) — Tổng Thầu EPC & Kết Cấu Thép Quốc Tế",
        "short_name": "Đại Dũng (DDC)",
        "url": "https://daidung.com/",
        "domain": "daidung.com",
        "slug": "xd_daidung",
        "category": "Heavy Steel Structure & EPC",
        "category_vn": "Tập Đoàn Đại Dũng — Kết Cấu Thép & Cơ Khí Chế Tạo",
        "tag": "tong-thau-vn",
        "vibe": "Industrial Power • Xuất Khẩu Toàn Cầu • Dự Án Sân Vận Động",
        "location": "TP. Hồ Chí Minh & Toàn Cầu",
        "desc": "Website của tập đoàn Đại Dũng gây ấn tượng mạnh với các dự án kết cấu thép tầm cỡ thế giới (sân vận động World Cup, nhà máy lọc hóa dầu, cầu cảng)."
    },
    {
        "name": "Searefico — Tổng Thầu Cơ Điện (M&E) & Xây Dựng Công Nghiệp",
        "short_name": "Searefico",
        "url": "https://searefico.com/",
        "domain": "searefico.com",
        "slug": "xd_searefico",
        "category": "M&E & Industrial Engineering",
        "category_vn": "Searefico — Tổng Thầu Cơ Điện & Kho Lạnh Công Nghiệp",
        "tag": "tong-thau-vn",
        "vibe": "Tech Engineering • Sắc Xanh Công Nghệ • Hệ Sinh Thái Đa Ngành",
        "location": "TP. Hồ Chí Minh & Toàn Quốc",
        "desc": "Trang chủ Searefico trình bày chuyên nghiệp hệ sinh thái cơ điện lạnh công nghiệp, phòng sạch và bất động sản công nghiệp với bố cục thoáng, dễ theo dõi."
    },
    {
        "name": "Hải Long Construction — Tổng Thầu Nhà Xưởng & Kết Cấu Thép Miền Bắc",
        "short_name": "Hải Long JSC",
        "url": "https://hailongjsc.vn/",
        "domain": "hailongjsc.vn",
        "slug": "xd_hailong",
        "category": "Industrial Factory Contractor",
        "category_vn": "Xây Lắp Hải Long — Nhà Xưởng KCN & Kết Cấu Thép",
        "tag": "tong-thau-vn",
        "vibe": "Industrial Clean • Thế Mạnh KCN • Dự Án FDI Hải Phòng",
        "location": "Hải Phòng & Miền Bắc",
        "desc": "Đại diện tiêu biểu cho nhóm tổng thầu nhà xưởng công nghiệp phía Bắc, làm nổi bật quy mô nhà máy sản xuất kết cấu thép và các dự án FDI lớn."
    },
    {
        "name": "Pebsteel Vietnam — Chuyên Gia Nhà Thép Tiền Chế & Kết Cấu Thép",
        "short_name": "Pebsteel",
        "url": "https://pebsteel.com/vi/",
        "domain": "pebsteel.com",
        "slug": "xd_pebsteel",
        "category": "Pre-Engineered Steel Buildings",
        "category_vn": "Pebsteel — Nhà Thép Tiền Chế Chuẩn Châu Âu",
        "tag": "tong-thau-vn",
        "vibe": "B2B International • Công Nghệ Thép • Thư Viện Giải Pháp",
        "location": "Việt Nam & Đông Nam Á",
        "desc": "Website Pebsteel sở hữu giao diện B2B sắc nét, phân loại khoa học các giải pháp nhà thép tiền chế, nhà cao tầng khung thép và thư viện dự án toàn khu vực."
    },
    {
        "name": "Zamil Steel Vietnam — Nhà Thép Tiền Chế & Kết Cấu Thép Toàn Cầu",
        "short_name": "Zamil Steel",
        "url": "https://www.zamilsteel.com.vn/",
        "domain": "zamilsteel.com.vn",
        "slug": "xd_zamilsteel",
        "category": "Global Steel Building Systems",
        "category_vn": "Zamil Steel — Hệ Thống Nhà Thép Tiền Chế Toàn Cầu",
        "tag": "tong-thau-vn",
        "vibe": "Corporate B2B • Tiêu Chuẩn Quốc Tế • Dữ Liệu Kỹ Thuật",
        "location": "Hà Nội, TP.HCM & Toàn Cầu",
        "desc": "Trang web chính thức tại Việt Nam của thương hiệu nhà thép tiền chế hàng đầu thế giới, thiết kế gọn gàng, tập trung vào giải pháp kỹ thuật và mạng lưới nhà máy."
    },

    # --- NHÓM 2: THIẾT KẾ & THI CÔNG XÂY NHÀ TRỌN GÓI VIỆT NAM (ĐỢT 2) ---
    {
        "name": "XHOME Việt Nam — Hệ Thống Thiết Kế & Thi Công Kiến Trúc Nội Thất",
        "short_name": "XHOME",
        "url": "https://xhome.com.vn/",
        "domain": "xhome.com.vn",
        "slug": "xd_xhome",
        "category": "Nationwide Design & Build Brand",
        "category_vn": "XHOME — Thương Hiệu Thiết Kế Thi Công Quy Mô Toàn Quốc",
        "tag": "xay-nha-tron-goi",
        "vibe": "Brand Authority • Ảnh Công Trình Thực Tế • Phủ Sóng Toàn Quốc",
        "location": "Hà Nội, TP.HCM & Chi Nhánh",
        "desc": "Thương hiệu hàng đầu về thiết kế và thi công kiến trúc - nội thất trọn gói tại Việt Nam, nổi bật với giao diện sang trọng và kho dự án thực tế phong phú."
    },
    {
        "name": "Kiến Trúc Vinavic — Thiết Kế & Thi Công Biệt Thự Trọn Gói",
        "short_name": "Vinavic",
        "url": "https://vinavic.vn/",
        "domain": "vinavic.vn",
        "slug": "xd_vinavic",
        "category": "Villa Architecture & Turnkey",
        "category_vn": "Kiến Trúc Vinavic — Kho Mẫu Biệt Thự & Nhà Phố Đẹp",
        "tag": "xay-nha-tron-goi",
        "vibe": "SEO Catalog • Bộ Lọc Mẫu Nhà • Biệt Thự Cao Cấp",
        "location": "Hà Nội & Toàn Quốc",
        "desc": "Website chuyên sâu thiết kế kiến trúc và thi công biệt thự trọn gói với cấu trúc danh mục tối ưu SEO, dễ dàng tra cứu theo số tầng và phong cách."
    },
    {
        "name": "KataHome — Tư Vấn Thiết Kế & Xây Dựng Biệt Thự, Dinh Thự",
        "short_name": "KataHome",
        "url": "https://katahome.com/",
        "domain": "katahome.com",
        "slug": "xd_katahome",
        "category": "Luxury Residence Architecture",
        "category_vn": "KataHome — Thiết Kế Thi Công Biệt Thự & Lâu Đài",
        "tag": "xay-nha-tron-goi",
        "vibe": "High-Traffic SEO • Thư Viện Công Trình • Tư Vấn Nhanh",
        "location": "Hà Nội & Toàn Quốc",
        "desc": "Mẫu website thiết kế và xây dựng biệt thự có lượng tìm kiếm tự nhiên lớn, trình bày rõ ràng các mẫu nhà theo khu vực và phong cách kiến trúc."
    },
    {
        "name": "Xây Dựng LACO — Nhà Thầu Xây Nhà Phố & Biệt Thự Trọn Gói",
        "short_name": "Xây Dựng LACO",
        "url": "https://xaydunglaco.vn/",
        "domain": "xaydunglaco.vn",
        "slug": "xd_laco",
        "category": "Turnkey Townhouse Contractor",
        "category_vn": "Xây Dựng LACO — Chuẩn Hóa Quy Trình Xây Nhà Phố",
        "tag": "xay-nha-tron-goi",
        "vibe": "Conversion Ready • Đơn Giá Minh Bạch • Video Công Trình",
        "location": "TP. Hồ Chí Minh",
        "desc": "Website nhà thầu dân dụng tại TP.HCM tập trung mạnh vào trải nghiệm chủ nhà: bảng giá xây nhà trọn gói, quy trình nghiệm thu và nhật ký thi công thực tế."
    },
    {
        "name": "Việt Quang Group — Thiết Kế, Xây Dựng & Sửa Chữa Nhà Trọn Gói",
        "short_name": "Việt Quang Group",
        "url": "https://kientrucvietquang.net/",
        "domain": "kientrucvietquang.net",
        "slug": "xd_vietquang",
        "category": "Home Build & Renovation CRO",
        "category_vn": "Việt Quang Group — Xây Mới & Cải Tạo Nhà Trọn Gói",
        "tag": "xay-nha-tron-goi",
        "vibe": "Lead-Gen Focused • Báo Giá Rõ Ràng • Top SEO Phía Nam",
        "location": "TP. Hồ Chí Minh & Miền Nam",
        "desc": "Trang web nhà thầu xây dựng dân dụng tối ưu tốt cho chuyển đổi Google Ads với bảng giá phần thô, hoàn thiện và chính sách bảo hành minh bạch."
    },
    {
        "name": "Việt Architect Group — Mạng Lưới Kiến Trúc Sư & Thi Công Toàn Quốc",
        "short_name": "Việt Architect",
        "url": "https://kientrucsuvietnam.vn/",
        "domain": "kientrucsuvietnam.vn",
        "slug": "xd_vietarchitect",
        "category": "Nationwide Architect Network",
        "category_vn": "Việt Architect Group — Thiết Kế Kiến Trúc & Thi Công",
        "tag": "xay-nha-tron-goi",
        "vibe": "Clean Editorial • Đa Chi Nhánh • Portfolio Đa Dạng",
        "location": "Hà Nội, Đà Nẵng & TP.HCM",
        "desc": "Website hệ thống kiến trúc sư trên toàn quốc, trình bày rõ các dự án biệt thự, nhà phố, khách sạn và văn phòng theo phong cách hiện đại."
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
        "desc": "Website lâu đời có lưu lượng truy cập tự nhiên lớn trong mảng thiết kế thi công nhà phố, biệt thự, tập trung vào kho mẫu thiết kế đa dạng và bảng giá thi công."
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

    # --- NHÓM 3: TỔNG THẦU & XÂY DỰNG QUỐC TẾ CHUẨN UI/UX (ĐỢT 2) ---
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
        "desc": "Website tập đoàn xây dựng hàng đầu Hoa Kỳ với lưới thiết kế bất đối xứng tinh tế, typography hiện đại, trình diễn sân vận động, bệnh viện và tòa nhà chọc trời."
    },
    {
        "name": "DPR Construction — Tổng Thầu Công Trình Công Nghệ Cao & Y Tế Mỹ",
        "short_name": "DPR Construction",
        "url": "https://www.dpr.com/",
        "domain": "dpr.com",
        "slug": "xd_dpr",
        "category": "Technical & Sustainable Builder",
        "category_vn": "DPR Construction (Mỹ) — UI Hiện Đại & Công Trình Kỹ Thuật Cao",
        "tag": "cong-nghiep-quoc-te",
        "vibe": "Bold Red Accent • Tech & Life Sciences • Storytelling Sắc Nét",
        "location": "California, Mỹ & Toàn Cầu",
        "desc": "Website của DPR Construction nổi bật với sắc đỏ đặc trưng, tập trung vào các công trình trung tâm dữ liệu, phòng thí nghiệm và bệnh viện công nghệ cao."
    },
    {
        "name": "PCL Construction — Tập Đoàn Tổng Thầu Dân Dụng & Hạ Tầng Bắc Mỹ",
        "short_name": "PCL Construction",
        "url": "https://www.pcl.com/ca/en",
        "domain": "pcl.com",
        "slug": "xd_pcl",
        "category": "North America Leading Builder",
        "category_vn": "PCL Construction (Canada/Mỹ) — Bố Cục Chuyên Nghiệp & Chuẩn Mực",
        "tag": "cong-nghiep-quoc-te",
        "vibe": "Clean Corporate • Green & Yellow Identity • Megaprojects",
        "location": "Canada, Mỹ & Úc",
        "desc": "Một trong những website tổng thầu có trải nghiệm điều hướng mượt mà nhất Bắc Mỹ, phân tách rõ 3 mảng: Dân dụng, Hạ tầng dân sinh và Công nghiệp nặng."
    },
    {
        "name": "Mortenson — Tổng Thầu Xây Dựng & Năng Lượng Tái Tạo Hàng Đầu Mỹ",
        "short_name": "Mortenson",
        "url": "https://www.mortenson.com/",
        "domain": "mortenson.com",
        "slug": "xd_mortenson",
        "category": "Sports, Healthcare & Renewable Builder",
        "category_vn": "Mortenson (Mỹ) — Sân Vận Động & Hạ Tầng Năng Lượng Xanh",
        "tag": "cong-nghiep-quoc-te",
        "vibe": "Modern Grid • Clean Data Visual • Bold Typography",
        "location": "Minneapolis, Mỹ",
        "desc": "Website Mortenson gây ấn tượng với giao diện tối giản hiện đại, làm nổi bật các siêu dự án sân vận động, trung tâm dữ liệu và điện gió/mặt trời."
    },
    {
        "name": "Lendlease — Tập Đoàn Phát Triển Đô Thị & Xây Dựng Toàn Cầu",
        "short_name": "Lendlease",
        "url": "https://www.lendlease.com/",
        "domain": "lendlease.com",
        "slug": "xd_lendlease",
        "category": "Global Urban Regeneration",
        "category_vn": "Lendlease (Úc) — Phát Triển Đô Thị & Xây Dựng Bền Vững",
        "tag": "cong-nghiep-quoc-te",
        "vibe": "Editorial Architecture • High-End Urban • Global Portfolio",
        "location": "Sydney, Úc & Toàn Cầu",
        "desc": "Giao diện tập đoàn bất động sản & xây dựng đa quốc gia với phong cách tạp chí sang trọng, nhấn mạnh quy hoạch đô thị thông minh và công trình xanh."
    },
    {
        "name": "Swinerton — Tổng Thầu Xây Dựng Thương Mại & Công Trình Xanh Mỹ",
        "short_name": "Swinerton",
        "url": "https://swinerton.com/",
        "domain": "swinerton.com",
        "slug": "xd_swinerton",
        "category": "Commercial & Mass Timber Builder",
        "category_vn": "Swinerton (Mỹ) — Xây Dựng Thương Mại & Kiến Trúc Gỗ Kỹ Thuật",
        "tag": "cong-nghiep-quoc-te",
        "vibe": "Warm Corporate • Mass Timber Showcase • Clean Navigation",
        "location": "California & Toàn Nước Mỹ",
        "desc": "Website Swinerton thể hiện sự kết hợp hài hòa giữa bề dày lịch sử 135+ năm và công nghệ xây dựng hiện đại (Mass Timber, năng lượng tái tạo)."
    },
    {
        "name": "Hensel Phelps — Tổng Thầu Thiết Kế, Xây Dựng & Vận Hành Mỹ",
        "short_name": "Hensel Phelps",
        "url": "https://www.henselphelps.com/",
        "domain": "henselphelps.com",
        "slug": "xd_henselphelps",
        "category": "Plan, Build, Manage Contractor",
        "category_vn": "Hensel Phelps (Mỹ) — Tổng Thầu Khép Kín Plan - Build - Manage",
        "tag": "cong-nghiep-quoc-te",
        "vibe": "Industrial Precision • Blue-Gold Brand • Lifecycle Approach",
        "location": "Colorado, Mỹ",
        "desc": "Website mẫu mực cho mô hình tổng thầu khép kín từ quy hoạch, thi công đến vận hành công trình hàng không, quốc phòng và thương mại."
    }
]

results = []
passed_list = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for idx, site in enumerate(pool, 1):
        site["id"] = f"xd{20+idx:02d}"
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

print(f"\n=== TỔNG KẾT QA ĐỢT 2: ĐẠT {len(passed_list)}/{len(pool)} MẪU ===")
for r in results:
    print(f"  {r[0]:20s} | {r[1]:28s} | {r[2]:9s} | {r[3]}")
