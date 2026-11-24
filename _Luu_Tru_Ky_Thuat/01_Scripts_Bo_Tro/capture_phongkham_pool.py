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
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "phongkham_pool_audit.json")

os.makedirs(output_dir, exist_ok=True)
os.makedirs(kho_webp_dir, exist_ok=True)

pool = [
    # --- NHÓM 1: HỆ THỐNG BỆNH VIỆN TƯ NHÂN & PHÒNG KHÁM ĐA KHOA VIỆT NAM ---
    {
        "name": "Vinmec — Hệ Thống Y Tế & Bệnh Viện Đa Khoa Quốc Tế Hàng Đầu VN",
        "short_name": "Vinmec Healthcare",
        "url": "https://www.vinmec.com/vie/",
        "domain": "vinmec.com",
        "slug": "pk_vinmec",
        "category": "International Hospital System",
        "category_vn": "Vinmec — Hệ Thống Y Tế Quốc Tế, Tìm Bác Sĩ & Đặt Hẹn",
        "tag": "da-khoa-benh-vien-vn",
        "vibe": "Clean Enterprise Medical • Tìm Bác Sĩ Nhanh • Độ Tin Cậy Cao",
        "location": "Hà Nội, TP.HCM & Toàn Quốc",
        "desc": "Chuẩn mực hàng đầu cho cổng thông tin bệnh viện và phòng khám đa khoa tại Việt Nam: thanh tìm kiếm bác sĩ/chuyên khoa ngay trên Hero, bố cục thoáng sạch và nút đặt lịch khám cực kỳ rõ ràng."
    },
    {
        "name": "Bệnh Viện Đa Khoa Tâm Anh — Hệ Thống Bệnh Viện Chuyên Sâu",
        "short_name": "BVĐK Tâm Anh",
        "url": "https://tamanhhospital.vn/",
        "domain": "tamanhhospital.vn",
        "slug": "pk_tamanh",
        "category": "Specialist Private Hospital",
        "category_vn": "Tâm Anh — Bệnh Viện Đa Khoa Chuẩn SEO & Hồ Sơ Chuyên Gia",
        "tag": "da-khoa-benh-vien-vn",
        "vibe": "Authority Medical • Đội Ngũ Giáo Sư Bác Sĩ • Thiết Bị Hiện Đại",
        "location": "Hà Nội & TP. Hồ Chí Minh",
        "desc": "Website hệ thống bệnh viện dẫn đầu về nội dung chuyên sâu và độ uy tín bác sĩ: trình bày mạch lạc các chuyên khoa mũi nhọn, trang thiết bị hiện đại và đặt lịch khám trực tuyến."
    },
    {
        "name": "Bệnh Viện Đa Khoa Hồng Ngọc — Chăm Sóc Sức Khỏe Chuẩn Quốc Tế",
        "short_name": "BVĐK Hồng Ngọc",
        "url": "https://hongngochospital.vn/",
        "domain": "hongngochospital.vn",
        "slug": "pk_hongngoc",
        "category": "Full-Service Private Hospital",
        "category_vn": "Hồng Ngọc — Bệnh Viện Đa Khoa & Phòng Khám Tiêu Chuẩn 5 Sao",
        "tag": "da-khoa-benh-vien-vn",
        "vibe": "Warm Hospital UI • Gói Khám Tổng Quát • Đặt Hẹn Mượt",
        "location": "Hà Nội",
        "desc": "Giao diện bệnh viện - phòng khám thân thiện, làm nổi bật các gói khám sức khỏe tổng quát, thai sản trọn gói và tìm kiếm bác sĩ theo từng cơ sở."
    },
    {
        "name": "Thu Cúc TCI — Hệ Thống Y Tế & Phòng Khám Đa Khoa Quốc Tế",
        "short_name": "Thu Cúc TCI",
        "url": "https://benhvienthucuc.vn/",
        "domain": "benhvienthucuc.vn",
        "slug": "pk_thucucmed",
        "category": "Multi-Branch Medical Clinic",
        "category_vn": "Thu Cúc TCI — Gói Khám Sức Khỏe, Tầm Soát & Đặt Lịch Nhanh",
        "tag": "da-khoa-benh-vien-vn",
        "vibe": "Conversion Medical • Tầm Soát Ung Thư • Bảng Gói Khám Rõ",
        "location": "Hà Nội",
        "desc": "Hình mẫu tối ưu chuyển đổi cho phòng khám đa khoa chạy Google Ads: phân loại rõ gói khám tổng quát, tầm soát ung thư, nội soi tiêu hóa kèm form đăng ký nhận ưu đãi."
    },
    {
        "name": "MEDLATEC — Hệ Thống Y Tế & Lấy Mẫu Xét Nghiệm Tận Nơi",
        "short_name": "MEDLATEC",
        "url": "https://medlatec.vn/",
        "domain": "medlatec.vn",
        "slug": "pk_medlatec",
        "category": "Diagnostics & Home Lab Testing",
        "category_vn": "MEDLATEC — Phòng Khám & Dịch Vụ Xét Nghiệm Tại Nhà Toàn Quốc",
        "tag": "da-khoa-benh-vien-vn",
        "vibe": "Lab & Clinic Portal • Đặt Lấy Mẫu Tại Nhà • Tra Kết Quả Online",
        "location": "Toàn Quốc (VN)",
        "desc": "Mẫu website cực kỳ hữu ích cho phòng khám và trung tâm xét nghiệm: đưa 2 tính năng cốt lõi (Đặt lịch lấy mẫu tận nơi + Tra cứu kết quả online) lên ngay vị trí trung tâm."
    },
    {
        "name": "Victoria Healthcare — Hệ Thống Phòng Khám Đa Khoa Tiêu Chuẩn Mỹ",
        "short_name": "Victoria Healthcare",
        "url": "https://www.victoriavn.com/",
        "domain": "victoriavn.com",
        "slug": "pk_victoria",
        "category": "American-Standard Outpatient Clinic",
        "category_vn": "Victoria Healthcare — Phòng Khám Đa Khoa Gia Đình & Nhi Khoa",
        "tag": "da-khoa-benh-vien-vn",
        "vibe": "Family Clinic Clean • Y Học Chứng Cứ • Khám Tổng Quát",
        "location": "TP. Hồ Chí Minh",
        "desc": "Thiết kế sáng sủa, sạch sẽ rất hợp cho mô hình phòng khám đa khoa tư nhân quy mô vừa và chuỗi phòng khám gia đình với danh mục gói khám sức khỏe trực quan."
    },
    {
        "name": "Bệnh Viện FV — Bệnh Viện Quốc Tế Chuẩn JCI Tại TP.HCM",
        "short_name": "FV Hospital",
        "url": "https://www.fvhospital.com/",
        "domain": "fvhospital.com",
        "slug": "pk_fvhospital",
        "category": "JCI-Accredited Hospital",
        "category_vn": "Bệnh Viện FV — Chuẩn Bệnh Viện Quốc Tế & Quy Trình Minh Bạch",
        "tag": "da-khoa-benh-vien-vn",
        "vibe": "International Medical • Đa Ngôn Ngữ • Cấu Trúc Mạch Lạc",
        "location": "TP. Hồ Chí Minh",
        "desc": "Website bệnh viện chuẩn quốc tế với cấu trúc điều hướng cực kỳ khoa học giúp bệnh nhân tìm nhanh chuyên khoa, chi phí khám chữa bệnh và đặt hẹn trực tuyến."
    },
    {
        "name": "Tập Đoàn Y Khoa Hoàn Mỹ — Hệ Thống Bệnh Viện & Phòng Khám Toàn Quốc",
        "short_name": "Hoàn Mỹ Medical",
        "url": "https://hoanmy.com/",
        "domain": "hoanmy.com",
        "slug": "pk_hoanmy",
        "category": "National Private Healthcare Network",
        "category_vn": "Hoàn Mỹ — Giao Diện Y Tế Hiện Đại, Ấm Áp & Dễ Tra Cứu",
        "tag": "da-khoa-benh-vien-vn",
        "vibe": "Modern Healthcare UI • Tông Xanh Ấm • Tìm Cơ Sở & Bác Sĩ",
        "location": "Toàn Quốc (VN)",
        "desc": "Giao diện y tế được tái thiết kế rất hiện đại và nhân văn: khoảng trắng thoáng đãng, phông chữ rõ ràng, dễ tra cứu mạng lưới bệnh viện/phòng khám và gói khám."
    },
    {
        "name": "Bernard Healthcare — Trung Tâm Y Khoa Chuyên Sâu & Tầm Soát Nhật Bản",
        "short_name": "Bernard Healthcare",
        "url": "https://bernard.vn/",
        "domain": "bernard.vn",
        "slug": "pk_bernard",
        "category": "Executive Health Screening Clinic",
        "category_vn": "Bernard — Phòng Khám Chuyên Sâu Tầm Soát Ung Thư & Đột Quỵ",
        "tag": "da-khoa-benh-vien-vn",
        "vibe": "Premium Boutique Clinic • Mô Hình Ningen Dock • Sang Trọng",
        "location": "TP. Hồ Chí Minh",
        "desc": "Hình mẫu đỉnh cao cho phòng khám cao cấp chuyên tầm soát sức khỏe (Executive Screening): thiết kế sang trọng, nhấn mạnh công nghệ MRI/CT và hội chẩn chuyên gia Nhật."
    },
    {
        "name": "Diag — Hệ Thống Phòng Khám & Trung Tâm Xét Nghiệm Y Khoa Hiện Đại",
        "short_name": "Diag Medical",
        "url": "https://diag.vn/",
        "domain": "diag.vn",
        "slug": "pk_diag",
        "category": "Modern Lab & Diagnostic Chain",
        "category_vn": "Diag — Chuỗi Xét Nghiệm & Khám Bệnh UI Hiện Đại Bậc Nhất VN",
        "tag": "da-khoa-benh-vien-vn",
        "vibe": "Startup HealthTech UI • Bảng Giá Xét Nghiệm Rõ • Đặt Lịch 1 Chạm",
        "location": "TP.HCM & Miền Nam",
        "desc": "Một trong những website y tế có UI/UX hiện đại và thân thiện nhất Việt Nam: hiển thị rõ giá từng gói xét nghiệm, cho phép chọn điểm lấy mẫu và đặt lịch online cực mượt."
    },
    {
        "name": "Family Medical Practice — Phòng Khám Đa Khoa Quốc Tế Đầu Tiên Tại VN",
        "short_name": "Family Medical",
        "url": "https://www.vietnammedicalpractice.com/",
        "domain": "vietnammedicalpractice.com",
        "slug": "pk_fmp",
        "category": "Expat International Clinic",
        "category_vn": "Family Medical Practice — Phòng Khám Quốc Tế & Cấp Cứu *9999",
        "tag": "da-khoa-benh-vien-vn",
        "vibe": "International Clinic • Đa Ngôn Ngữ • Rõ Ràng Từng Cơ Sở",
        "location": "TP.HCM, Hà Nội & Đà Nẵng",
        "desc": "Website phòng khám quốc tế phục vụ chuyên gia nước ngoài và gia đình Việt, nổi bật với nút cấp cứu nhanh, thông tin bác sĩ quốc tế và lịch khám rõ ràng."
    },
    {
        "name": "Raffles Medical Việt Nam — Hệ Thống Phòng Khám Quốc Tế Singapore",
        "short_name": "Raffles Medical",
        "url": "https://rafflesmedical.vn/",
        "domain": "rafflesmedical.vn",
        "slug": "pk_rafflesvn",
        "category": "Singapore Standard Clinic",
        "category_vn": "Raffles Medical — Phòng Khám Chuẩn Singapore & Khám Visa",
        "tag": "da-khoa-benh-vien-vn",
        "vibe": "Clean Singapore Medical • Dịch Vụ Rõ • Bảo Hiểm Trực Tiếp",
        "location": "TP.HCM, Hà Nội & Vũng Tàu",
        "desc": "Thiết kế gọn gàng chuẩn Singapore, tách bạch rõ khám đa khoa, khám sức khỏe doanh nghiệp, khám visa định cư và danh sách bảo hiểm bảo lãnh trực tiếp."
    },

    # --- NHÓM 2: PHÒNG KHÁM CHUYÊN KHOA (XƯƠNG KHỚP, MẮT) & NỀN TẢNG ĐẶT LỊCH VN ---
    {
        "name": "Phòng Khám ACC — Chuyên Khoa Trị Liệu Thần Kinh Cột Sống & Vật Lý Trị Liệu",
        "short_name": "Phòng Khám ACC",
        "url": "https://acc.vn/",
        "domain": "acc.vn",
        "slug": "pk_accvn",
        "category": "Chiropractic & Physiotherapy Clinic",
        "category_vn": "ACC Chiropractic — Chuyên Khoa Cơ Xương Khớp & Vật Lý Trị Liệu",
        "tag": "chuyen-khoa-dat-lich-vn",
        "vibe": "Specialist Clinic CRO • Không Phẫu Thuật • Đặt Hẹn Nhanh",
        "location": "TP.HCM, Hà Nội & Đà Nẵng",
        "desc": "Hình mẫu chuẩn cho phòng khám chuyên khoa cơ xương khớp & vật lý trị liệu: giải thích rõ bệnh lý thoát vị đĩa đệm/đau lưng, phác đồ không dùng thuốc và form đặt lịch ngay."
    },
    {
        "name": "iCCARE Chiropractic — Phòng Khám Xương Khớp Cột Sống Chuẩn Mỹ",
        "short_name": "iCCARE Chiropractic",
        "url": "https://iccare.com.vn/",
        "domain": "iccare.com.vn",
        "slug": "pk_iccare",
        "category": "Spine & Sports Injury Clinic",
        "category_vn": "iCCARE — Phòng Khám Trị Liệu Cột Sống & Phục Hồi Chức Năng",
        "tag": "chuyen-khoa-dat-lich-vn",
        "vibe": "Clean Specialist • Bác Sĩ Nước Ngoài • Video Khách Hàng Thật",
        "location": "Hà Nội",
        "desc": "Website phòng khám chuyên khoa trị liệu cột sống có bố cục rất sạch và thuyết phục, nổi bật với đội ngũ bác sĩ Mỹ, máy móc phục hồi và phản hồi thực tế."
    },
    {
        "name": "Bệnh Viện Mắt Quốc Tế Việt - Nga — Chuyên Khoa Nhãn Khoa & Xóa Cận",
        "short_name": "Mắt Việt - Nga",
        "url": "https://matvietnga.com/",
        "domain": "matvietnga.com",
        "slug": "pk_matvietnga",
        "category": "Ophthalmology & Laser Eye Hospital",
        "category_vn": "Mắt Quốc Tế Việt-Nga — Chuyên Khoa Mắt, Xóa Cận SMILE & Đục Thủy Tinh Thể",
        "tag": "chuyen-khoa-dat-lich-vn",
        "vibe": "Eye Specialist CRO • Phẫu Thuật Xóa Cận • Chuyên Gia Châu Âu",
        "location": "Hà Nội, TP.HCM & Hải Phòng",
        "desc": "Mẫu website chuyên khoa Mắt tối ưu tốt cho nhu cầu tìm kiếm dịch vụ xóa cận và điều trị tật khúc xạ, làm nổi bật công nghệ phẫu thuật và bác sĩ chuyên gia."
    },
    {
        "name": "BookingCare — Nền Tảng Đặt Lịch Khám Chuyên Khoa Hàng Đầu Việt Nam",
        "short_name": "BookingCare",
        "url": "https://bookingcare.vn/",
        "domain": "bookingcare.vn",
        "slug": "pk_bookingcare",
        "category": "Medical Appointment Marketplace",
        "category_vn": "BookingCare — Sàn Đặt Lịch Khám Bác Sĩ & Phòng Khám Chuyên Khoa",
        "tag": "chuyen-khoa-dat-lich-vn",
        "vibe": "Health Booking UX • Tìm Theo Chuyên Khoa • Lọc Bác Sĩ Nhanh",
        "location": "Toàn Quốc (VN)",
        "desc": "Chuẩn mực UX đặt lịch khám bệnh trực tuyến tại Việt Nam: thanh tìm kiếm theo triệu chứng/bác sĩ, biểu tượng chuyên khoa trực quan và luồng chọn khung giờ khám rõ ràng."
    },
    {
        "name": "Medpro — Nền Tảng Đặt Khám Nhanh 500+ Bệnh Viện & Phòng Khám",
        "short_name": "Medpro",
        "url": "https://medpro.vn/",
        "domain": "medpro.vn",
        "slug": "pk_medpro",
        "category": "Digital Healthcare Booking Platform",
        "category_vn": "Medpro — Web & App Đặt Lịch Khám Bệnh Không Chờ Đợi",
        "tag": "chuyen-khoa-dat-lich-vn",
        "vibe": "Modern HealthTech • Giao Diện Sáng Mượt • Đa Dịch Vụ Y Tế",
        "location": "Toàn Quốc (VN)",
        "desc": "Giao diện đặt lịch y tế hiện đại với màu xanh tươi sáng, trình bày rõ các dịch vụ đặt khám tại viện, tư vấn video từ xa, xét nghiệm và chăm sóc tại nhà."
    },
    {
        "name": "Hello Bacsi — Cổng Thông Tin Sức Khỏe & Đặt Lịch Bác Sĩ Hàng Đầu",
        "short_name": "Hello Bacsi",
        "url": "https://hellobacsi.com/",
        "domain": "hellobacsi.com",
        "slug": "pk_hellobacsi",
        "category": "Health Content & Clinic Directory",
        "category_vn": "Hello Bacsi — Cổng Kiến Thức Y Khoa Chuẩn SEO & Công Cụ Sức Khỏe",
        "tag": "chuyen-khoa-dat-lich-vn",
        "vibe": "SEO Health Portal • Công Cụ Tính BMI/Thai Kỳ • Cực Sạch",
        "location": "Toàn Quốc (VN)",
        "desc": "Hình mẫu chuẩn mực về website nội dung y tế & SEO sức khỏe: phân nhóm chuyên mục dễ quét, tích hợp các công cụ kiểm tra sức khỏe tự động và liên kết đặt khám."
    },

    # --- NHÓM 3: PHÒNG KHÁM HIỆN ĐẠI & Y TẾ QUỐC TẾ CHUẨN UI/UX ---
    {
        "name": "One Medical — Chuẩn Mực Vàng UI/UX Phòng Khám Đa Khoa Hiện Đại Mỹ",
        "short_name": "One Medical",
        "url": "https://www.onemedical.com/",
        "domain": "onemedical.com",
        "slug": "pk_onemedical",
        "category": "Modern Primary Care Chain",
        "category_vn": "One Medical (Mỹ) — Chuẩn Mực UI/UX Phòng Khám Hiện Đại & Thân Thiện",
        "tag": "quoc-te-y-te",
        "vibe": "Warm Modern Care • Xanh Rừng & Kem • Xóa Bỏ Cảm Giác Bệnh Viện",
        "location": "Mỹ (Amazon Health)",
        "desc": "Biểu tượng toàn cầu về thiết kế website phòng khám thế hệ mới: dùng tông xanh rừng dịu mắt và ảnh đời thường ấm áp, nhấn mạnh khám trong ngày và chăm sóc 24/7 qua app."
    },
    {
        "name": "Parsley Health — Phòng Khám Y Học Chức Năng & Chăm Sóc Toàn Diện",
        "short_name": "Parsley Health",
        "url": "https://www.parsleyhealth.com/",
        "domain": "parsleyhealth.com",
        "slug": "pk_parsleyhealth",
        "category": "Functional & Holistic Medicine Clinic",
        "category_vn": "Parsley Health (Mỹ) — Phòng Khám Y Học Chức Năng Phong Cách Editorial",
        "tag": "quoc-te-y-te",
        "vibe": "Editorial Wellness Clinic • Tinh Tế Nhẹ Nhàng • Gói Thành Viên",
        "location": "New York & Los Angeles, Mỹ",
        "desc": "Thiết kế web y khoa mang đậm hơi thở lifestyle cao cấp: trình bày thuyết phục phương pháp điều trị tận gốc (y học chức năng + dinh dưỡng) và lộ trình hội viên sức khỏe."
    },
    {
        "name": "Tia — Phòng Khám Chăm Sóc Sức Khỏe Toàn Diện Cho Phụ Nữ",
        "short_name": "Tia Health",
        "url": "https://asktia.com/",
        "domain": "asktia.com",
        "slug": "pk_asktia",
        "category": "Modern Women's Health Clinic",
        "category_vn": "Tia (Mỹ) — Phòng Khám Sức Khỏe Phụ Nữ & Sản Phụ Khoa Đẳng Cấp UI",
        "tag": "quoc-te-y-te",
        "vibe": "Boutique Women's Health • Bảng Màu Ấm Độc Bản • Cực Thân Thiện",
        "location": "New York, LA & San Francisco",
        "desc": "Hình mẫu xuất sắc nhất cho phòng khám Sản Phụ Khoa & chăm sóc sức khỏe nữ giới: phá vỡ hoàn toàn khuôn mẫu phòng khám truyền thống bằng thẩm mỹ hiện đại, ấm áp và thấu hiểu."
    },
    {
        "name": "Spring Fertility — Trung Tâm Hỗ Trợ Sinh Sản & IVF Hàng Đầu Mỹ",
        "short_name": "Spring Fertility",
        "url": "https://springfertility.com/",
        "domain": "springfertility.com",
        "slug": "pk_springfertility",
        "category": "Fertility & IVF Specialist Clinic",
        "category_vn": "Spring Fertility (Mỹ) — Phòng Khám Sản & Hiếm Muộn Ấm Áp, Tin Cậy",
        "tag": "quoc-te-y-te",
        "vibe": "Empathetic Medical UI • Số Liệu Thành Công Rõ • Đặt Lịch Tư Vấn",
        "location": "San Francisco & New York, Mỹ",
        "desc": "Website phòng khám chuyên khoa hiếm muộn/IVF được đánh giá cực cao về cảm xúc và niềm tin: kết hợp tỷ lệ thành công minh bạch với hình ảnh ấm áp, gần gũi."
    },
    {
        "name": "Cleveland Clinic — Trung Tâm Y Tế Hàng Đầu Thế Giới Chuẩn UX",
        "short_name": "Cleveland Clinic",
        "url": "https://my.clevelandclinic.org/",
        "domain": "my.clevelandclinic.org",
        "slug": "pk_cleveland",
        "category": "World-Class Medical Center",
        "category_vn": "Cleveland Clinic (Mỹ) — Chuẩn Kiến Trúc Thông Tin Bệnh Viện Toàn Cầu",
        "tag": "quoc-te-y-te",
        "vibe": "Global Medical Benchmark • Tìm Bác Sĩ & Cơ Sở • Cực Kỳ Rõ Ràng",
        "location": "Ohio, Mỹ & Toàn Cầu",
        "desc": "Chuẩn mực thế giới về cách tổ chức hàng nghìn chuyên khoa và bác sĩ thành một trang chủ gọn gàng, cực kỳ dễ dùng cho mọi độ tuổi bệnh nhân."
    },
    {
        "name": "Nuffield Health — Hệ Thống Bệnh Viện Tư Nhân & Vật Lý Trị Liệu Anh Quốc",
        "short_name": "Nuffield Health",
        "url": "https://www.nuffieldhealth.com/",
        "domain": "nuffieldhealth.com",
        "slug": "pk_nuffield",
        "category": "UK Private Hospitals & Physiotherapy",
        "category_vn": "Nuffield Health (Anh) — Bệnh Viện, Vật Lý Trị Liệu & Sức Khỏe Tinh Thần",
        "tag": "quoc-te-y-te",
        "vibe": "British Clean Green • Hệ Sinh Thái Sức Khỏe • Tìm Nhanh Dịch Vụ",
        "location": "Vương Quốc Anh",
        "desc": "Hệ thống y tế tư nhân lớn tại Anh kết hợp bệnh viện, phòng vật lý trị liệu và chăm sóc sức khỏe tinh thần với thanh tìm kiếm theo triệu chứng/vị trí cực kỳ trực quan."
    },
    {
        "name": "OneWelbeck — Trung Tâm Khám Chuyên Khoa Tư Nhân Hạng Sang London",
        "short_name": "OneWelbeck London",
        "url": "https://onewelbeck.com/",
        "domain": "onewelbeck.com",
        "slug": "pk_onewelbeck",
        "category": "Luxury Specialist Medical Centre",
        "category_vn": "OneWelbeck (London) — Trung Tâm Chuyên Khoa Cao Cấp Phong Cách Tối Giản",
        "tag": "quoc-te-y-te",
        "vibe": "Luxury Private Clinic • Xanh Đậm Tinh Tế • Trải Nghiệm Bệnh Nhân 5 Sao",
        "location": "London, Anh Quốc",
        "desc": "Hình mẫu đỉnh cao cho trung tâm khám chuyên khoa tư nhân cao cấp: giao diện tinh gọn chuẩn kiến trúc hiện đại, tập trung vào 14 chuyên khoa sâu và đội ngũ bác sĩ đầu ngành."
    },
]

results = []
passed_list = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for idx, site in enumerate(pool, 1):
        site["id"] = f"pk{idx:02d}"
        site["industry"] = "phong-kham-y-te"
        site["industry_name"] = "Phòng Khám Chuyên Khoa & Y Tế"
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
                    '.elementor-popup-modal .dialog-close-button', '.pum-close',
                    'button[class*="cookie" i]', '.cc-allow', '.cc-dismiss',
                    '[aria-label="Close dialog"]'
                ];
                selectors.forEach(sel => {
                    try { document.querySelectorAll(sel).forEach(btn => { try { btn.click(); } catch(e) {} }); } catch(e) {}
                });
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

print(f"\n=== TỔNG KẾT QA NGÁCH 8 (PHÒNG KHÁM CHUYÊN KHOA & Y TẾ): ĐẠT {len(passed_list)}/{len(pool)} MẪU ===")
for r in results:
    print(f"  {r[0]:20s} | {r[1]:30s} | {r[2]:9s} | {r[3]}")
