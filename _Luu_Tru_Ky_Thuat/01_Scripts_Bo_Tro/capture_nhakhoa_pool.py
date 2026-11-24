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
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "nhakhoa_pool_audit.json")

os.makedirs(output_dir, exist_ok=True)
os.makedirs(kho_webp_dir, exist_ok=True)

pool = [
    # --- NHÓM 1: CHUỖI NHA KHOA & CHUYÊN SÂU IMPLANT / NIỀNG RĂNG VIỆT NAM ---
    {
        "name": "Nha Khoa Kim — Hệ Thống Nha Khoa Chuẩn Y Khoa Hàng Đầu Việt Nam",
        "short_name": "Nha Khoa Kim",
        "url": "https://nhakhoakim.com/",
        "domain": "nhakhoakim.com",
        "slug": "nk_nhakhoakim",
        "category": "National Dental Clinic Chain",
        "category_vn": "Nha Khoa Kim — Chuỗi Nha Khoa Quy Mô Lớn & Đặt Lịch Hẹn",
        "tag": "chuoi-nha-khoa-vn",
        "vibe": "Trust Medical UI • Quy Mô Chuỗi • Đặt Lịch & Bảng Giá Rõ",
        "location": "TP.HCM, Hà Nội & Toàn Quốc",
        "desc": "Hình mẫu chuẩn mực cho hệ thống chuỗi nha khoa quy mô lớn tại Việt Nam: cấu trúc dịch vụ mạch lạc (Implant, Bọc sứ, Niềng răng), minh bạch đội ngũ bác sĩ và phễu đặt lịch khám cực mạnh."
    },
    {
        "name": "Nha Khoa Parkway — Chuỗi Nha Khoa Hiện Đại & Niềng Răng Invisalign",
        "short_name": "Nha Khoa Parkway",
        "url": "https://nhakhoaparkway.com/",
        "domain": "nhakhoaparkway.com",
        "slug": "nk_parkway",
        "category": "Modern Orthodontics & Dental Chain",
        "category_vn": "Parkway — Giao Diện Nha Khoa Trẻ Trung, Thân Thiện & Hiện Đại",
        "tag": "chuoi-nha-khoa-vn",
        "vibe": "Friendly Modern • Tông Xanh Tươi • Tối Ưu Niềng Răng & Trẻ Em",
        "location": "Hà Nội, TP.HCM & Toàn Quốc",
        "desc": "Giao diện nha khoa hiện đại, trẻ trung và xóa bỏ cảm giác sợ bệnh viện; làm nổi bật giải pháp niềng răng trong suốt Invisalign, lộ trình điều trị và nút đặt lịch thân thiện."
    },
    {
        "name": "Elite Dental — Trung Tâm Nha Khoa Chuyên Sâu Implant & Chỉnh Nha",
        "short_name": "Elite Dental",
        "url": "https://elitedental.com.vn/",
        "domain": "elitedental.com.vn",
        "slug": "nk_elitedental",
        "category": "Specialist Implant & Orthodontic Center",
        "category_vn": "Elite Dental — Nha Khoa Chuyên Sâu Chuẩn Quốc Tế TP.HCM",
        "tag": "chuoi-nha-khoa-vn",
        "vibe": "Clinical Excellence • Case Study Thực Tế • Tông Xanh Chuyên Gia",
        "location": "TP. Hồ Chí Minh",
        "desc": "Mẫu website nha khoa chuyên sâu chuẩn quốc tế: nhấn mạnh trình độ tiến sĩ/bác sĩ, thư viện ca điều trị Before-After thực tế và trải nghiệm tư vấn tận tâm."
    },
    {
        "name": "Nha Khoa Paris — Chuỗi Nha Khoa Thẩm Mỹ Tiêu Chuẩn Pháp",
        "short_name": "Nha Khoa Paris",
        "url": "https://nhakhoaparis.vn/",
        "domain": "nhakhoaparis.vn",
        "slug": "nk_nhakhoaparis",
        "category": "Cosmetic Dental Chain",
        "category_vn": "Nha Khoa Paris — Chuỗi Thẩm Mỹ Răng Sứ, Implant & Chạy Ads Mạnh",
        "tag": "chuoi-nha-khoa-vn",
        "vibe": "High-Conversion CRO • Ưu Đãi Rõ Ràng • Phễu Tư Vấn Mạnh",
        "location": "Hà Nội, TP.HCM & Toàn Quốc",
        "desc": "Hình mẫu thực chiến về tối ưu chuyển đổi Google Ads & Facebook Ads ngành nha khoa: bố cục chia rõ các gói dịch vụ chủ lực, hình ảnh khách hàng thực tế và form nhận ưu đãi."
    },
    {
        "name": "Dr. Care Implant Clinic — Nha Khoa Chuyên Sâu Trồng Răng Không Đau",
        "short_name": "Dr. Care Implant",
        "url": "https://drcareimplant.com/",
        "domain": "drcareimplant.com",
        "slug": "nk_drcare",
        "category": "Dedicated Implant Clinic",
        "category_vn": "Dr. Care — Chuyên Sâu 1 Dịch Vụ Trồng Răng Implant Cho Trung Niên",
        "tag": "chuoi-nha-khoa-vn",
        "vibe": "Single-Focus CRO • Định Vị Rõ • Chống Sợ Đau & Minh Bạch Giá",
        "location": "TP. Hồ Chí Minh",
        "desc": "Case study mẫu mực về website nha khoa đánh trúng 1 ngách sâu (Trồng răng Implant cho người trung niên): chữ to dễ đọc, đánh thẳng nỗi lo sợ đau và dẫn chứng hàng nghìn ca thành công."
    },
    {
        "name": "Nha Khoa I-Dent — Trung Tâm Trồng Răng Implant & Bọc Răng Sứ",
        "short_name": "Nha Khoa I-Dent",
        "url": "https://nhakhoaident.com/",
        "domain": "nhakhoaident.com",
        "slug": "nk_ident",
        "category": "Implant & Porcelain Crown Center",
        "category_vn": "I-Dent — Trung Tâm Cấy Ghép Implant Chuẩn Pháp & Răng Sứ",
        "tag": "chuoi-nha-khoa-vn",
        "vibe": "Trust Medical Blue • Bảng Giá Minh Bạch • Đánh Giá Khách Hàng",
        "location": "TP. Hồ Chí Minh",
        "desc": "Website trung tâm cấy ghép Implant tối ưu tốt cả SEO lẫn chuyển đổi: làm nổi bật bác sĩ chuyên môn Pháp, quy trình cấy ghép an toàn và bảng giá rõ ràng từng dòng trụ."
    },
    {
        "name": "Lạc Việt Intech — Hệ Thống Chuyên Sâu Implant & Niềng Răng Công Nghệ",
        "short_name": "Lạc Việt Intech",
        "url": "https://lacvietintech.vn/",
        "domain": "lacvietintech.vn",
        "slug": "nk_lacvietintech",
        "category": "Tech-Driven Implant & Braces",
        "category_vn": "Lạc Việt Intech — Nha Khoa Công Nghệ Cao X-Matrix & Safe Tech",
        "tag": "chuoi-nha-khoa-vn",
        "vibe": "Medical Tech • Trình Bày Công Nghệ • Chuỗi Miền Bắc",
        "location": "Hà Nội, Hải Phòng, Nghệ An",
        "desc": "Website nha khoa định vị mạnh về công nghệ điều trị tiên tiến, bố cục rõ ràng giữa 2 mũi nhọn Trồng răng Implant và Niềng răng thẩm mỹ kèm hệ thống bằng chứng khách hàng."
    },
    {
        "name": "Peace Dentistry — Hệ Thống Nha Khoa Chuyên Sâu & Minh Bạch Bác Sĩ",
        "short_name": "Peace Dentistry",
        "url": "https://nhakhoapeace.vn/",
        "domain": "nhakhoapeace.vn",
        "slug": "nk_peace",
        "category": "Doctor-Led Dental System",
        "category_vn": "Peace Dentistry — Uy Tín Đội Ngũ Bác Sĩ & Thư Viện Ca Lâm Sàng",
        "tag": "chuoi-nha-khoa-vn",
        "vibe": "Doctor Authority • Ca Lâm Sàng Thật • Bố Cục Khoa Học",
        "location": "TP.HCM, Biên Hòa & Đà Nẵng",
        "desc": "Mẫu web nha khoa xây dựng niềm tin cực tốt nhờ đặt hồ sơ bác sĩ thật, bằng cấp chuyên khoa và hàng trăm hình ảnh ca điều trị thực tế làm trọng tâm."
    },
    {
        "name": "Up Dental — Nha Khoa Chuyên Sâu 100% Niềng Răng Trả Góp",
        "short_name": "Up Dental",
        "url": "https://updental.vn/",
        "domain": "updental.vn",
        "slug": "nk_updental",
        "category": "Orthodontics Specialist Clinic",
        "category_vn": "Up Dental — Chuyên Sâu Niềng Răng & Chính Sách Trả Góp Rõ Ràng",
        "tag": "chuoi-nha-khoa-vn",
        "vibe": "Youthful Braces UI • Ưu Đãi Trả Góp • Review Học Sinh Sinh Viên",
        "location": "TP. Hồ Chí Minh",
        "desc": "Hình mẫu tuyệt vời cho phòng khám chuyên biệt niềng răng: thông điệp trả góp 1 triệu/tháng nổi bật ngay đầu trang, nhiều câu chuyện tháo niềng thực tế tạo động lực chốt lịch."
    },
    {
        "name": "Nha Khoa Nhân Tâm — Trung Tâm Trồng Răng Implant & Phục Hình Sứ",
        "short_name": "Nha Khoa Nhân Tâm",
        "url": "https://nhakhoanhantam.com/",
        "domain": "nhakhoanhantam.com",
        "slug": "nk_nhantam",
        "category": "Established Implant Dental Center",
        "category_vn": "Nhân Tâm — Nha Khoa Lâu Đời Chuyên Phục Hình & Implant",
        "tag": "chuoi-nha-khoa-vn",
        "vibe": "Trusted Heritage • Đội Ngũ Tiến Sĩ • Đầy Đủ Chuyên Khoa",
        "location": "TP. Hồ Chí Minh",
        "desc": "Website trung tâm nha khoa uy tín lâu năm với tông xanh chuyên nghiệp, trình bày đầy đủ chuyên khoa Implant, răng sứ, niềng răng và các giải pháp điều trị phức tạp."
    },
    {
        "name": "Bệnh Viện Răng Hàm Mặt Worldwide — Bệnh Viện Thẩm Mỹ & Implant 5 Sao",
        "short_name": "BV RHM Worldwide",
        "url": "https://benhvienworldwide.vn/",
        "domain": "benhvienworldwide.vn",
        "slug": "nk_worldwide",
        "category": "5-Star Dental & Maxillofacial Hospital",
        "category_vn": "Bệnh Viện Worldwide — Bệnh Viện RHM Cao Cấp & Du Lịch Nha Khoa",
        "tag": "chuoi-nha-khoa-vn",
        "vibe": "Hospital Luxury • Chuẩn 5 Sao • Khách Việt Kiều & Quốc Tế",
        "location": "Quận 1, TP. Hồ Chí Minh",
        "desc": "Giao diện mang đẳng cấp bệnh viện chuyên khoa Răng Hàm Mặt 5 sao, hướng đến cả khách hàng cao cấp trong nước lẫn khách Việt kiều về làm răng thẩm mỹ và trồng răng."
    },

    # --- NHÓM 2: NHA KHOA THẨM MỸ BOUTIQUE & PHÒNG KHÁM TẠI VIỆT NAM ---
    {
        "name": "Jet Dentist — Nha Khoa Thẩm Mỹ Cao Cấp Phong Cách Luxury",
        "short_name": "Jet Dentist",
        "url": "https://jetdentist.vn/",
        "domain": "jetdentist.vn",
        "slug": "nk_jetdentist",
        "category": "Luxury Aesthetic Dentistry",
        "category_vn": "Jet Dentist — Nha Khoa Thẩm Mỹ Răng Sứ Hạng Sang",
        "tag": "nha-khoa-tham-my-vn",
        "vibe": "Boutique Luxury • Thẩm Mỹ Nụ Cười • Không Gian 5 Sao",
        "location": "Hà Nội & TP. Hồ Chí Minh",
        "desc": "Hình mẫu website nha khoa thẩm mỹ cao cấp: thoát khỏi phong cách phòng khám khô khan, sử dụng ảnh nghệ thuật tinh tế, không gian sang trọng và cảm hứng nụ cười đẹp."
    },
    {
        "name": "Westcoast International — Nha Khoa Chuẩn Quốc Tế Tại Việt Nam",
        "short_name": "Westcoast Dental",
        "url": "https://westcoastinternational.com/",
        "domain": "westcoastinternational.com",
        "slug": "nk_westcoast",
        "category": "International Dental Clinic VN",
        "category_vn": "Westcoast — Nha Khoa Quốc Tế Phục Vụ Expat & Khách Cao Cấp",
        "tag": "nha-khoa-tham-my-vn",
        "vibe": "International Clean • Song Ngữ • Bác Sĩ Nước Ngoài",
        "location": "TP.HCM & Hà Nội",
        "desc": "Website phòng khám nha khoa quốc tế lâu đời tại Việt Nam với bố cục thanh lịch, thông tin dịch vụ rõ ràng, hướng mạnh đến tiêu chuẩn điều trị không đau và khách hàng quốc tế."
    },
    {
        "name": "Nha Khoa Thúy Đức — Phòng Khám Chỉnh Nha & Thẩm Mỹ 20 Năm Hà Nội",
        "short_name": "Nha Khoa Thúy Đức",
        "url": "https://nhakhoathuyduc.com.vn/",
        "domain": "nhakhoathuyduc.com.vn",
        "slug": "nk_thuyduc",
        "category": "Boutique Orthodontics Hanoi",
        "category_vn": "Nha Khoa Thúy Đức — Thương Hiệu Bác Sĩ & Chỉnh Nha Hà Nội",
        "tag": "nha-khoa-tham-my-vn",
        "vibe": "Personal Brand Clinic • 20 Năm Uy Tín • Gần Gũi Sạch Sẽ",
        "location": "Hà Nội",
        "desc": "Mẫu web rất tốt cho phòng khám nha khoa xây dựng theo thương hiệu bác sĩ sáng lập: tạo thiện cảm lớn nhờ câu chuyện nghề, công nghệ niềng răng hiện đại và đánh giá thật."
    },
    {
        "name": "Nha Khoa My Auris — Nha Khoa Thẩm Mỹ Răng Sứ & Công Nghệ Số",
        "short_name": "My Auris",
        "url": "https://myauris.vn/",
        "domain": "myauris.vn",
        "slug": "nk_myauris",
        "category": "Digital Cosmetic Dentistry",
        "category_vn": "My Auris — Nha Khoa Thẩm Mỹ Răng Sứ & Chăm Sóc Nụ Cười",
        "tag": "nha-khoa-tham-my-vn",
        "vibe": "Modern Aesthetic • Bảng Giá & Ưu Đãi • Hình Ảnh Bắt Mắt",
        "location": "TP. Hồ Chí Minh",
        "desc": "Website nha khoa thẩm mỹ có nhịp điệu trình bày hiện đại, làm nổi bật các gói phủ sứ, dán sứ Veneer, trồng răng và hình ảnh khách hàng lột xác nụ cười."
    },
    {
        "name": "Nha Khoa Quốc Tế Việt Pháp — Hệ Thống Nha Khoa Uy Tín Miền Bắc",
        "short_name": "NK Quốc Tế Việt Pháp",
        "url": "https://nhakhoaquoctevietphap.vn/",
        "domain": "nhakhoaquoctevietphap.vn",
        "slug": "nk_vietphap",
        "category": "Multi-Branch Dental Clinic",
        "category_vn": "Việt Pháp — Hệ Thống Nha Khoa Đa Chi Nhánh Chuẩn Chuyển Đổi",
        "tag": "nha-khoa-tham-my-vn",
        "vibe": "Clean Corporate Medical • Hệ Thống Chi Nhánh • Đặt Lịch Nhanh",
        "location": "Hà Nội, Quảng Ninh, Bắc Ninh",
        "desc": "Cấu trúc website chuẩn cho hệ thống nhiều cơ sở tại các tỉnh thành: phân bổ rõ các nhóm dịch vụ răng sứ, Implant, niềng răng và hệ thống cơ sở vật chất."
    },
    {
        "name": "Nha Khoa Trồng Răng Sài Gòn — Tối Ưu Chuyển Đổi Trồng Răng & Răng Sứ",
        "short_name": "NK Trồng Răng SG",
        "url": "https://nhakhoatrongrang.com/",
        "domain": "nhakhoatrongrang.com",
        "slug": "nk_trongrangsg",
        "category": "Implant Lead-Gen Website",
        "category_vn": "Trồng Răng Sài Gòn — Bố Cục Chốt Lịch Google Ads & Bảng Giá",
        "tag": "nha-khoa-tham-my-vn",
        "vibe": "Search Ads CRO • Giá Công Khai • Hình Ảnh Before-After",
        "location": "TP. Hồ Chí Minh",
        "desc": "Mẫu web phòng khám nha khoa tối ưu tốt cho lưu lượng tìm kiếm Google Search: minh bạch chi phí trồng răng Implant, dán sứ và hiển thị rõ các ca điều trị thực tế."
    },
    {
        "name": "Starlight Dental Clinic — Nha Khoa Quốc Tế Cho Gia Đình & Chuyên Gia",
        "short_name": "Starlight Dental",
        "url": "https://starlightdental.net/",
        "domain": "starlightdental.net",
        "slug": "nk_starlight",
        "category": "Expat Family Dental Clinic",
        "category_vn": "Starlight Dental — Phòng Khám Nha Khoa Tiêu Chuẩn Châu Âu",
        "tag": "nha-khoa-tham-my-vn",
        "vibe": "Warm Boutique • Chuyên Nghiệp Tinh Gọn • Khách Quốc Tế",
        "location": "TP. Hồ Chí Minh",
        "desc": "Phòng khám nha khoa tiêu chuẩn quốc tế với thiết kế trang nhã, tập trung trải nghiệm chăm sóc êm ái cho cả gia đình và khách nước ngoài sinh sống tại TP.HCM."
    },

    # --- NHÓM 3: NHA KHOA THẨM MỸ & BOUTIQUE QUỐC TẾ CHUẨN UI/UX ---
    {
        "name": "Grand Street Dental — Biểu Tượng UI/UX Nha Khoa Phong Cách Tạp Chí Mỹ",
        "short_name": "Grand Street Dental",
        "url": "https://www.grandstreetdental.com/",
        "domain": "grandstreetdental.com",
        "slug": "nk_grandstreet",
        "category": "Editorial Boutique Dentistry",
        "category_vn": "Grand Street Dental (New York) — Đỉnh Cao UI/UX Nha Khoa Nghệ Thuật",
        "tag": "quoc-te-nha-khoa",
        "vibe": "Editorial Non-Clinical • Tông Kem Sang • Typography Thời Trang",
        "location": "Brooklyn, New York (Mỹ)",
        "desc": "Một trong những website nha khoa nổi tiếng nhất giới thiết kế UI/UX: phá bỏ hoàn toàn sự lạnh lẽo của y tế bằng tông màu kem ấm, ảnh thời trang và đặt lịch cực tinh tế."
    },
    {
        "name": "Apa Aesthetic — Nha Khoa Thẩm Mỹ Xa Xỉ Hàng Đầu New York & Dubai",
        "short_name": "Apa Aesthetic",
        "url": "https://apaaesthetic.com/",
        "domain": "apaaesthetic.com",
        "slug": "nk_apaaesthetic",
        "category": "Ultra-Luxury Cosmetic Dentistry",
        "category_vn": "Apa Aesthetic (Mỹ/Dubai) — Đỉnh Cao Nha Khoa Thẩm Mỹ Thượng Lưu",
        "tag": "quoc-te-nha-khoa",
        "vibe": "Ultra Luxury Editorial • Minimalist Serif • Định Vị Đẳng Cấp",
        "location": "New York, LA & Dubai",
        "desc": "Chuẩn mực thiết kế web cho nha khoa thẩm mỹ phân khúc siêu sang (Veneer & Smile Makeover): không gian trắng rộng rãi, phông chữ Serif thanh lịch và thần thái thương hiệu đỉnh cao."
    },
    {
        "name": "Premier Arts Dental — Giao Diện Nha Khoa Boutique Ấm Áp & Sang Trọng",
        "short_name": "Premier Arts Dental",
        "url": "https://www.premierartsdental.com/",
        "domain": "premierartsdental.com",
        "slug": "nk_premierarts",
        "category": "Warm Luxury Dental UX",
        "category_vn": "Premier Arts Dental (Mỹ) — Trải Nghiệm Nha Khoa Ấm Áp & Hiện Đại",
        "tag": "quoc-te-nha-khoa",
        "vibe": "Warm Modern Luxury • Ảnh Không Gian Đẹp • CTA Đặt Lịch Nổi Bật",
        "location": "New Jersey, Mỹ",
        "desc": "Thiết kế web nha khoa kết hợp hoàn hảo giữa cảm giác ấm cúng như spa và sự chuyên nghiệp y khoa, với nút đặt lịch nổi bật ngay trên Hero và hình ảnh đội ngũ chân thực."
    },
    {
        "name": "Studio Dental — Nha Khoa Tối Giản Hiện Đại San Francisco",
        "short_name": "Studio Dental",
        "url": "https://www.studiodental.com/",
        "domain": "studiodental.com",
        "slug": "nk_studiodental",
        "category": "Modern Minimalist Dental Studio",
        "category_vn": "Studio Dental (Mỹ) — Tối Giản Hiện Đại & Đặt Lịch Siêu Mượt",
        "tag": "quoc-te-nha-khoa",
        "vibe": "Clean Studio UI • Minh Bạch Bảo Hiểm • Trải Nghiệm Thân Thiện",
        "location": "San Francisco, Mỹ",
        "desc": "Hình mẫu xuất sắc về website phòng khám nha khoa hiện đại cho khách hàng trẻ thành thị: bố cục sạch sẽ, khoảng trắng tinh tế và quy trình đặt hẹn chỉ trong vài giây."
    },
    {
        "name": "Village Dental — Hình Mẫu CRO Đặt Lịch & Social Proof Nha Khoa Mỹ",
        "short_name": "Village Dental",
        "url": "https://www.villagedentaldtc.com/",
        "domain": "villagedentaldtc.com",
        "slug": "nk_villagedental",
        "category": "High-Trust Conversion Dental UX",
        "category_vn": "Village Dental (Mỹ) — Mẫu Mực Tối Ưu Chuyển Đổi & Đánh Giá Google",
        "tag": "quoc-te-nha-khoa",
        "vibe": "Conversion Blueprint • Google Reviews • Thân Thiện Tin Cậy",
        "location": "Colorado, Mỹ",
        "desc": "Case study kinh điển về CRO cho phòng khám nha khoa địa phương: đưa điểm đánh giá khách hàng và nút đặt lịch lên ngay đầu trang, kết hợp giới thiệu dịch vụ cực kỳ dễ quét."
    },
    {
        "name": "Harley Street Dental Studio — Nha Khoa Thẩm Mỹ Cao Cấp London",
        "short_name": "Harley Street Dental",
        "url": "https://www.harleystreetdentalstudio.com/",
        "domain": "harleystreetdentalstudio.com",
        "slug": "nk_harleystreet",
        "category": "London Prestige Cosmetic Clinic",
        "category_vn": "Harley Street (Anh) — Nha Khoa Thẩm Mỹ Danh Tiếng London",
        "tag": "quoc-te-nha-khoa",
        "vibe": "British Prestige • Before/After Sắc Nét • Chuyên Gia Thẩm Mỹ",
        "location": "London, Anh Quốc",
        "desc": "Website phòng khám nha khoa danh tiếng tại phố y khoa Harley Street London, trình bày cực kỳ thuyết phục các ca phục hình thẩm mỹ Veneer, Implant và Invisalign."
    },
    {
        "name": "209 NYC Dental — Phòng Khám Nha Khoa Đa Chuyên Khoa Manhattan",
        "short_name": "209 NYC Dental",
        "url": "https://www.209nycdental.com/",
        "domain": "209nycdental.com",
        "slug": "nk_209nycdental",
        "category": "Urban Multi-Specialty Clinic",
        "category_vn": "209 NYC Dental (New York) — Phòng Khám Đô Thị Hiện Đại & Tiện Lợi",
        "tag": "quoc-te-nha-khoa",
        "vibe": "Urban Clean UX • Mở Cửa 7 Ngày • Bố Cục Thông Minh",
        "location": "Manhattan, New York (Mỹ)",
        "desc": "Mẫu website phòng khám đa chuyên khoa giữa trung tâm New York: bố cục rõ ràng, làm nổi bật lợi thế giờ khám linh hoạt, công nghệ chẩn đoán số và đặt hẹn trực tuyến."
    },
]

results = []
passed_list = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for idx, site in enumerate(pool, 1):
        site["id"] = f"nk{idx:02d}"
        site["industry"] = "nha-khoa"
        site["industry_name"] = "Nha Khoa Thẩm Mỹ & Trồng Răng"
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
                // Close cookies & popups
                const selectors = [
                    'button[aria-label*="Close" i]', 'button[aria-label*="accept" i]',
                    '.onetrust-close-btn-handler', '#onetrust-accept-btn-handler',
                    '#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll',
                    '.didomi-continue-without-agreeing', '#didomi-notice-agree-button',
                    '.cky-btn-accept', '.cookie-accept', '.btn-close-popup',
                    '.popup-close', '.close-modal', '.mfp-close', '.fancybox-close-small',
                    '.elementor-popup-modal .dialog-close-button', '.pum-close',
                    'button[class*="cookie" i]', '.cc-allow', '.cc-dismiss'
                ];
                selectors.forEach(sel => {
                    try { document.querySelectorAll(sel).forEach(btn => { try { btn.click(); } catch(e) {} }); } catch(e) {}
                });
                // Proactively remove floating Shadow DOM chatbots (lesson learned from An Cuong)
                document.querySelectorAll('*').forEach(el => {
                    if (el.shadowRoot) {
                        const tag = (el.tagName || '').toLowerCase();
                        const id = (el.id || '').toLowerCase();
                        if (tag.includes('chat') || tag.includes('bot') || tag.includes('intercom') || tag.includes('widget') || id.includes('chat')) {
                            try { el.remove(); } catch(e) {}
                        }
                    }
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
                        '.modal-backdrop, .popup-overlay, .pum-overlay, [role="dialog"]:not(:has(main)):not(.dialog-off-canvas-main-canvas)'
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

print(f"\n=== TỔNG KẾT QA NGÁCH 6 (NHA KHOA THẨM MỸ & TRỒNG RĂNG): ĐẠT {len(passed_list)}/{len(pool)} MẪU ===")
for r in results:
    print(f"  {r[0]:20s} | {r[1]:32s} | {r[2]:9s} | {r[3]}")
