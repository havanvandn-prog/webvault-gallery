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
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "spa_pool_audit.json")

os.makedirs(output_dir, exist_ok=True)
os.makedirs(kho_webp_dir, exist_ok=True)

pool = [
    # --- NHÓM 1: BỆNH VIỆN THẨM MỸ, CLINIC DA LIỄU & CHUỖI THẨM MỸ VIỆN VIỆT NAM ---
    {
        "name": "Rohto Aohal Clinic — Phòng Khám Da Liễu & Thẩm Mỹ Chuẩn Nhật Bản",
        "short_name": "Rohto Aohal Clinic",
        "url": "https://rohtoaohalclinic.com.vn/",
        "domain": "rohtoaohalclinic.com.vn",
        "slug": "spa_rohtoaohal",
        "category": "Japanese Dermatology & Aesthetic Clinic",
        "category_vn": "Rohto Aohal — Phòng Khám Da Liễu & Trẻ Hóa Da Chuẩn Nhật",
        "tag": "clinic-tmv-vn",
        "vibe": "Japanese Clean Clinic • Tin Cậy Y Khoa • Liệu Trình Rõ Ràng",
        "location": "TP.HCM & Hà Nội",
        "desc": "Hình mẫu chuẩn mực cho website clinic da liễu thẩm mỹ chuẩn Nhật: giao diện thanh lịch, phân loại khoa học các liệu trình laser/trị nám/trẻ hóa và đặt lịch hẹn rất gọn gàng."
    },
    {
        "name": "Ruco International Clinic — Viện Trẻ Hóa Công Nghệ Cao Hạng Sang",
        "short_name": "Ruco International",
        "url": "https://rucointernational.vn/",
        "domain": "rucointernational.vn",
        "slug": "spa_ruco",
        "category": "Luxury Anti-Aging & MedSpa",
        "category_vn": "Ruco Clinic — Viện Trẻ Hóa Da & Công Nghệ Cao Đẳng Cấp 5 Sao",
        "tag": "clinic-tmv-vn",
        "vibe": "Luxury MedSpa • Công Nghệ Ultherapy/Thermage • Tông Sang Trọng",
        "location": "TP. Hồ Chí Minh",
        "desc": "Website viện thẩm mỹ phân khúc cao cấp với phong thái sang trọng, làm nổi bật các phác đồ trẻ hóa không xâm lấn, không gian 5 sao và danh sách khách hàng nghệ sĩ."
    },
    {
        "name": "Pensilia — Hệ Thống Phòng Khám Da Liễu Thẩm Mỹ Chuẩn Y Khoa",
        "short_name": "Pensilia Clinic",
        "url": "https://pensilia.com/",
        "domain": "pensilia.com",
        "slug": "spa_pensilia",
        "category": "Doctor-Led Skin & Aesthetic Clinic",
        "category_vn": "Pensilia — Phòng Khám Da Liễu Trị Nám, Trẻ Hóa & Bác Sĩ Chuyên Khoa",
        "tag": "clinic-tmv-vn",
        "vibe": "Doctor Authority • Chuẩn Y Khoa • Tối Ưu SEO & Tư Vấn",
        "location": "TP.HCM, Biên Hòa & Vũng Tàu",
        "desc": "Mẫu web phòng khám da liễu thẩm mỹ xây dựng niềm tin cực mạnh nhờ nhấn mạnh đội ngũ bác sĩ chuyên khoa, công nghệ FDA và hệ thống bài tư vấn bệnh lý da bài bản."
    },
    {
        "name": "Lavender By Chang — Viện Thẩm Mỹ Công Nghệ Cao & Tắm Trắng",
        "short_name": "Lavender By Chang",
        "url": "https://www.lavenderbychang.com/",
        "domain": "lavenderbychang.com",
        "slug": "spa_lavender",
        "category": "High-Tech Luxury Beauty Institute",
        "category_vn": "Lavender By Chang — Viện Thẩm Mỹ Hạng Sang & Phễu Ưu Đãi",
        "tag": "clinic-tmv-vn",
        "vibe": "High-Fashion Beauty • Trắng Da & Giảm Béo • Chuyển Đổi Mạnh",
        "location": "TP.HCM & Hà Nội",
        "desc": "Giao diện viện thẩm mỹ cao cấp đậm chất thời trang, sử dụng hình ảnh đại sứ thương hiệu sắc nét cùng hệ thống giới thiệu dịch vụ trẻ hóa, trắng da và giảm béo bắt mắt."
    },
    {
        "name": "Bệnh Viện Thẩm Mỹ Kangnam — Hệ Thống Thẩm Mỹ Chuẩn Hàn Quốc",
        "short_name": "BVTM Kangnam",
        "url": "https://benhvienthammykangnam.vn/",
        "domain": "benhvienthammykangnam.vn",
        "slug": "spa_kangnam",
        "category": "Leading Aesthetic Hospital Chain",
        "category_vn": "Kangnam — Bệnh Viện Thẩm Mỹ Quy Mô Lớn & Chạy Ads Mạnh Nhất",
        "tag": "clinic-tmv-vn",
        "vibe": "High-Conversion Portal • Before/After Thật • Phễu Chốt Lịch",
        "location": "Hà Nội, TP.HCM & Toàn Quốc",
        "desc": "Case study kinh điển về website bệnh viện thẩm mỹ tối ưu chuyển đổi tại Việt Nam: phân nhóm rõ mũi, mắt, hàm mặt, vóc dáng kèm kho ảnh Before-After đồ sộ."
    },
    {
        "name": "Bệnh Viện Thẩm Mỹ Thu Cúc — Hệ Thống Thẩm Mỹ Toàn Diện",
        "short_name": "BVTM Thu Cúc",
        "url": "https://thammythucuc.vn/",
        "domain": "thammythucuc.vn",
        "slug": "spa_thucuc",
        "category": "National Aesthetic Hospital",
        "category_vn": "Thu Cúc Beauty — Bệnh Viện Thẩm Mỹ Lâu Đời & Đa Chuyên Khoa",
        "tag": "clinic-tmv-vn",
        "vibe": "Trusted Aesthetic Brand • Danh Mục Đầy Đủ • Bảng Giá & Ưu Đãi",
        "location": "Hà Nội, TP.HCM & Toàn Quốc",
        "desc": "Website hệ thống thẩm mỹ lâu đời với cấu trúc cực kỳ khoa học, cân bằng giữa dịch vụ đại phẫu, thẩm mỹ công nghệ cao và chăm sóc da spa."
    },
    {
        "name": "Thẩm Mỹ Viện Ngọc Dung — Hệ Thống Làm Đẹp 18 Chi Nhánh Toàn Quốc",
        "short_name": "TMV Ngọc Dung",
        "url": "https://thammyvienngocdung.com/",
        "domain": "thammyvienngocdung.com",
        "slug": "spa_ngocdung",
        "category": "Multi-Branch Beauty Salon Chain",
        "category_vn": "TMV Ngọc Dung — Phun Xăm, Điều Trị Da & Hệ Thống 18 Chi Nhánh",
        "tag": "clinic-tmv-vn",
        "vibe": "Warm Gold Luxury • Phun Xăm & Laser • Đặt Lịch Nhanh",
        "location": "TP.HCM & Toàn Quốc",
        "desc": "Giao diện sang trọng tông vàng đồng - trắng đặc trưng, tối ưu phễu đăng ký ưu đãi cho các dịch vụ chủ lực như phun xăm thẩm mỹ, laser trị thâm nám và giảm mỡ."
    },
    {
        "name": "Thẩm Mỹ Viện Seoul Center — Chuỗi Làm Đẹp Công Nghệ Hiện Đại",
        "short_name": "Seoul Center",
        "url": "https://seoulcenter.vn/",
        "domain": "seoulcenter.vn",
        "slug": "spa_seoulcenter",
        "category": "Modern Korean-Style Beauty Chain",
        "category_vn": "Seoul Center — Chuỗi Spa & Thẩm Mỹ Viện Phủ Sóng Toàn Quốc",
        "tag": "clinic-tmv-vn",
        "vibe": "Promo-Driven CRO • Hệ Thống Chi Nhánh • Ảnh Hiện Đại",
        "location": "Toàn Quốc (VN)",
        "desc": "Mẫu web chuỗi thẩm mỹ viện tốc độ mở rộng mạnh, tập trung trình bày dịch vụ chăm sóc da, điêu khắc, làm đẹp công nghệ cao và nút đặt hẹn theo chi nhánh gần nhất."
    },
    {
        "name": "Bệnh Viện Thẩm Mỹ Gangwhoo — Bệnh Viện Thẩm Mỹ Chuẩn Hàn TP.HCM",
        "short_name": "BVTM Gangwhoo",
        "url": "https://benhvienthammygangwhoo.vn/",
        "domain": "benhvienthammygangwhoo.vn",
        "slug": "spa_gangwhoo",
        "category": "Korean-Standard Plastic Surgery Hospital",
        "category_vn": "Gangwhoo — Bệnh Viện Thẩm Mỹ Công Nghệ Nội Soi & Khách Quốc Tế",
        "tag": "clinic-tmv-vn",
        "vibe": "Prestige Purple-Gold • Thiết Bị Hiện Đại • Khách Việt Kiều",
        "location": "TP. Hồ Chí Minh",
        "desc": "Website bệnh viện thẩm mỹ chú trọng hình ảnh phòng mổ hiện đại, đội ngũ bác sĩ Việt-Hàn và danh mục dịch vụ rõ ràng hướng tới cả khách trong nước lẫn Việt kiều."
    },
    {
        "name": "O2 SKIN — Phòng Khám Da Liễu Chuyên Sâu Điều Trị Mụn Chuẩn Y Khoa",
        "short_name": "O2 SKIN",
        "url": "https://o2skin.vn/",
        "domain": "o2skin.vn",
        "slug": "spa_o2skin",
        "category": "Acne Treatment Medical Clinic",
        "category_vn": "O2 SKIN — Phòng Khám Chuyên Trị Mụn, Sẹo Rỗ & Phác Đồ Rõ Ràng",
        "tag": "clinic-tmv-vn",
        "vibe": "Medical Clean Blue • Minh Bạch Bảng Giá • Ca Trị Mụn Thật",
        "location": "TP.HCM & Cần Thơ",
        "desc": "Hình mẫu xuất sắc về phòng khám da liễu chuyên 1 ngách sâu (Trị mụn & Sẹo rỗ): tông xanh y khoa sạch sẽ, công khai bảng giá, quy trình chuẩn và hàng nghìn ca khỏi mụn."
    },
    {
        "name": "Saigon Smile Medical — Viện Giảm Béo & Trẻ Hóa Công Nghệ Cao",
        "short_name": "Saigon Smile",
        "url": "https://saigonsmilespa.com.vn/",
        "domain": "saigonsmilespa.com.vn",
        "slug": "spa_saigonsmile",
        "category": "Slimming & Rejuvenation Clinic",
        "category_vn": "Saigon Smile — Chuyên Sâu Giảm Béo & Trẻ Hóa Da Không Xâm Lấn",
        "tag": "clinic-tmv-vn",
        "vibe": "Medical Aesthetic • Chuyên Sâu 2 Dịch Vụ • Khách Sao Việt",
        "location": "Hà Nội & TP.HCM",
        "desc": "Website viện chăm sóc sắc đẹp lâu năm định vị rõ vào giảm béo và trẻ hóa công nghệ cao, bố cục mạch lạc và có nhiều câu chuyện khách hàng thuyết phục."
    },
    {
        "name": "Lux Beauty Center — Viện Thẩm Mỹ Công Nghệ Cao & Trẻ Hóa Da",
        "short_name": "Lux Beauty Center",
        "url": "https://luxclinic.vn/",
        "domain": "luxclinic.vn",
        "slug": "spa_luxclinic",
        "category": "Boutique High-Tech Skin Clinic",
        "category_vn": "Lux Beauty Center — Clinic Da Liễu Boutique & Trẻ Hóa Nâng Cơ",
        "tag": "clinic-tmv-vn",
        "vibe": "Boutique Clinic • Bác Sĩ Sáng Lập • Giao Diện Sang Nhẹ",
        "location": "TP. Hồ Chí Minh",
        "desc": "Mẫu website đẹp cho mô hình Aesthetic Clinic boutique xây dựng quanh bác sĩ chuyên môn: bố cục thoáng, hình ảnh nhẹ nhàng sang trọng và rõ ràng từng phác đồ trẻ hóa."
    },

    # --- NHÓM 2: DAY SPA, MASSAGE THƯ GIÃN & BOUTIQUE SPA VIỆT NAM ---
    {
        "name": "La Spa — Hệ Thống Spa Thư Giãn 5 Sao Thuộc Tập Đoàn EHG",
        "short_name": "La Spa",
        "url": "https://laspas.vn/",
        "domain": "laspas.vn",
        "slug": "spa_laspa",
        "category": "5-Star Boutique Hospitality Spa",
        "category_vn": "La Spa — Spa Thư Giãn Chuẩn Khách Sạn 5 Sao & Đặt Lịch Nhanh",
        "tag": "day-spa-vn",
        "vibe": "Zen Luxury • Menu Liệu Trình Tinh Tế • Không Gian An Yên",
        "location": "Hà Nội, TP.HCM & Hội An",
        "desc": "Hình mẫu đẹp bậc nhất mảng Day Spa & Massage cao cấp tại Việt Nam: tông màu trầm ấm thư thái, menu liệu trình trình bày như khách sạn 5 sao và nút đặt lịch nổi bật."
    },
    {
        "name": "Sen Tài Thu — Hệ Thống Chăm Sóc Sức Khỏe & Trị Liệu Cổ Truyền",
        "short_name": "Sen Tài Thu",
        "url": "https://sentaithu.com.vn/",
        "domain": "sentaithu.com.vn",
        "slug": "spa_sentaithu",
        "category": "Traditional Wellness & Therapy Spa",
        "category_vn": "Sen Tài Thu — Massage Trị Liệu, Bấm Huyệt & Dưỡng Sinh Đông Y",
        "tag": "day-spa-vn",
        "vibe": "Vietnamese Heritage Wellness • Dưỡng Sinh Cổ Truyền • Sang Ấm",
        "location": "Hà Nội & Toàn Quốc",
        "desc": "Website thương hiệu spa trị liệu & dưỡng sinh Đông y hàng đầu Việt Nam: bản sắc văn hóa rõ nét, gói trị liệu minh bạch và hệ thống đặt lịch theo từng cơ sở."
    },
    {
        "name": "Herbal Spa — Top Spa Chăm Sóc Da & Massage Thảo Mộc Đà Nẵng",
        "short_name": "Herbal Spa",
        "url": "https://herbalspa.vn/",
        "domain": "herbalspa.vn",
        "slug": "spa_herbalspa",
        "category": "Botanical & Tourism Day Spa",
        "category_vn": "Herbal Spa — Spa Thảo Mộc Đà Nẵng/Hội An Chuẩn Khách Du Lịch",
        "tag": "day-spa-vn",
        "vibe": "Natural Herbal • Đa Ngôn Ngữ • Menu Giá Rõ & Booking Ngay",
        "location": "Đà Nẵng & Hội An",
        "desc": "Mẫu website cực kỳ thực chiến cho spa phục vụ cả khách Việt và khách du lịch quốc tế: bảng giá gói massage rõ ràng, review TripAdvisor uy tín và nút đặt lịch tức thì."
    },
    {
        "name": "Charm Spa Grand — Hệ Thống Spa & Massage Thư Giãn Cao Cấp",
        "short_name": "Charm Spa Grand",
        "url": "https://charmspagrand.com/",
        "domain": "charmspagrand.com",
        "slug": "spa_charmspa",
        "category": "Luxury Massage & Wellness Spa",
        "category_vn": "Charm Spa Grand — Không Gian Spa Sang Trọng & Liệu Trình Trọn Gói",
        "tag": "day-spa-vn",
        "vibe": "Warm Boutique Spa • Ảnh Không Gian Đẹp • Đặt Hẹn Dễ Dàng",
        "location": "Đà Nẵng, Nha Trang & Đà Lạt",
        "desc": "Giao diện spa thư giãn mang cảm giác ấm cúng, trình bày trực quan các gói trị liệu đá nóng, thảo dược, chăm sóc da mặt cùng hình ảnh không gian sang trọng."
    },
    {
        "name": "L'Apothiquaire Artisan Beauté — Spa Hữu Cơ Phong Cách Pháp Sài Gòn",
        "short_name": "L'Apothiquaire",
        "url": "https://lapothiquaire.com/",
        "domain": "lapothiquaire.com",
        "slug": "spa_lapothiquaire",
        "category": "French Organic Artisan Spa",
        "category_vn": "L'Apothiquaire — Spa Hữu Cơ & Mỹ Phẩm Thiên Nhiên Phong Cách Pháp",
        "tag": "day-spa-vn",
        "vibe": "French Heritage • Minimal Organic • Kết Hợp Bán Mỹ Phẩm",
        "location": "TP. Hồ Chí Minh",
        "desc": "Thương hiệu spa boutique phong cách Pháp nổi tiếng tại Sài Gòn, kết hợp tinh tế giữa giới thiệu không gian trị liệu cổ điển và cửa hàng mỹ phẩm hữu cơ."
    },

    # --- NHÓM 3: LUXURY SPA, MEDSPA & SKINCARE CLINIC QUỐC TẾ CHUẨN UI/UX ---
    {
        "name": "Heyday Skincare — Chuỗi Chăm Sóc Da Mặt Hiện Đại Hàng Đầu Mỹ",
        "short_name": "Heyday Skincare",
        "url": "https://www.heydayskincare.com/",
        "domain": "heydayskincare.com",
        "slug": "spa_heydayskincare",
        "category": "Modern Facial Shop Chain",
        "category_vn": "Heyday (Mỹ) — Chuẩn UI/UX Chuỗi Skincare & Gói Hội Viên Hiện Đại",
        "tag": "quoc-te-spa",
        "vibe": "Editorial Skincare • Tông Kem Ấm • Booking & Membership Mượt",
        "location": "New York & Toàn Nước Mỹ",
        "desc": "Hình mẫu UI/UX hàng đầu cho mô hình Facial Spa hiện đại: màu sắc ấm áp thân thiện, giải thích quy trình chăm sóc da 50 phút cực dễ hiểu và luồng đặt lịch/thẻ thành viên siêu mượt."
    },
    {
        "name": "Skin Laundry — Chuỗi Laser Facial & Trẻ Hóa Da Công Nghệ Mỹ",
        "short_name": "Skin Laundry",
        "url": "https://www.skinlaundry.com/",
        "domain": "skinlaundry.com",
        "slug": "spa_skinlaundry",
        "category": "Tech-Forward Laser Facial Clinic",
        "category_vn": "Skin Laundry (Mỹ) — Clinic Laser Facial Tối Giản & Trẻ Trung",
        "tag": "quoc-te-spa",
        "vibe": "Minimalist MedSpa • Laser 15 Phút • Ảnh Da Thật Sắc Nét",
        "location": "Mỹ, Anh & Châu Á",
        "desc": "Thiết kế web cực kỳ sắc sảo cho chuỗi clinic laser trẻ hóa da: tối giản hiện đại, tập trung chứng minh hiệu quả trên làn da thật và nút trải nghiệm buổi đầu giá ưu đãi."
    },
    {
        "name": "Ever/Body — Chuỗi Thẩm Mỹ Da Liễu Công Nghệ Cao New York",
        "short_name": "Ever/Body",
        "url": "https://everbody.com/",
        "domain": "everbody.com",
        "slug": "spa_everbody",
        "category": "Cosmetic Dermatology MedSpa",
        "category_vn": "Ever/Body (New York) — MedSpa Da Liễu Cao Cấp & Đẹp Từng Pixel",
        "tag": "quoc-te-spa",
        "vibe": "High-End MedSpa • Serif + Neutral • Phác Đồ Minh Bạch",
        "location": "New York & Washington D.C.",
        "desc": "Một trong những website MedSpa đẹp nhất nước Mỹ: kết hợp hoàn hảo thẩm mỹ thời trang cao cấp với độ tin cậy y khoa, trình bày dịch vụ Botox/Laser/Facial cực kỳ rõ ràng."
    },
    {
        "name": "Silver Mirror — Facial Bar Chăm Sóc Da Chuyên Sâu New York",
        "short_name": "Silver Mirror",
        "url": "https://silvermirror.com/",
        "domain": "silvermirror.com",
        "slug": "spa_silvermirror",
        "category": "Specialized Facial Bar",
        "category_vn": "Silver Mirror (Mỹ) — Mô Hình Facial Bar Trẻ Trung & Chốt Lịch Nhanh",
        "tag": "quoc-te-spa",
        "vibe": "Clean Pastel UI • Menu 30/50 Phút • Trải Nghiệm Tối Ưu",
        "location": "New York, Miami & D.C.",
        "desc": "Mẫu website tuyệt vời cho spa chuyên chăm sóc da mặt: phân tách gói 30 phút và 50 phút trực quan, khoảng trắng rộng rãi và nút Book Now luôn rõ ràng."
    },
    {
        "name": "Glowbar — Chuỗi Chăm Sóc Da 30 Phút Chuyên Biệt & Tối Giản",
        "short_name": "Glowbar",
        "url": "https://www.glowbar.com/",
        "domain": "glowbar.com",
        "slug": "spa_glowbar",
        "category": "Express Skincare Membership Studio",
        "category_vn": "Glowbar (Mỹ) — Spa Da Mặt 30 Phút & Mô Hình Hội Viên Định Kỳ",
        "tag": "quoc-te-spa",
        "vibe": "Fresh Brand Identity • 1 Mức Giá Duy Nhất • Dễ Hiểu 100%",
        "location": "New York & Bờ Đông Mỹ",
        "desc": "Ví dụ kinh điển về tối giản thông điệp bán hàng ngành spa: một liệu trình thiết kế riêng 30 phút, một mức giá minh bạch và bố cục hình ảnh tràn đầy sức sống."
    },
    {
        "name": "Formula Fig — Spa Công Nghệ Cao Kết Hợp Quầy Skincare Đương Đại",
        "short_name": "Formula Fig",
        "url": "https://formulafig.com/",
        "domain": "formulafig.com",
        "slug": "spa_formulafig",
        "category": "Avant-Garde Skincare & Tech Bar",
        "category_vn": "Formula Fig (Canada/Mỹ) — UI/UX Độc Bản & Spa Công Nghệ Tương Lai",
        "tag": "quoc-te-spa",
        "vibe": "Editorial Design Award • Bảng Màu Xanh-Kem Độc Đáo • Cực Gu",
        "location": "Vancouver, Toronto & LA",
        "desc": "Website spa mang gu thiết kế cực kỳ cá tính và hiện đại, kết hợp hoàn hảo giữa đặt lịch liệu trình công nghệ cao và cửa hàng sản phẩm dưỡng da tuyển chọn."
    },
    {
        "name": "Bathhouse — Không Gian Tắm Khoáng, Sauna & Massage Đương Đại New York",
        "short_name": "Bathhouse",
        "url": "https://www.abathhouse.com/",
        "domain": "abathhouse.com",
        "slug": "spa_bathhouse",
        "category": "Modern Bathhouse & Wellness Club",
        "category_vn": "Bathhouse (New York) — Spa Tắm Khoáng & Xông Hơi Phong Cách Đương Đại",
        "tag": "quoc-te-spa",
        "vibe": "Architectural Dark/Warm • Trải Nghiệm Không Gian • Đặt Vé Online",
        "location": "Brooklyn & Manhattan, Mỹ",
        "desc": "Hình mẫu đỉnh cao cho các mô hình tổ hợp tắm khoáng Onsen, xông hơi Jjimjilbang và massage cao cấp: nghệ thuật nhiếp ảnh kiến trúc đẹp xuất sắc."
    },
    {
        "name": "Burke Williams — Hệ Thống Day Spa Hạng Sang Kinh Điển California",
        "short_name": "Burke Williams",
        "url": "https://www.burkewilliams.com/",
        "domain": "burkewilliams.com",
        "slug": "spa_burkewilliams",
        "category": "Classic Luxury Day Spa",
        "category_vn": "Burke Williams (Mỹ) — Day Spa Sang Trọng & Thẻ Quà Tặng Cao Cấp",
        "tag": "quoc-te-spa",
        "vibe": "Timeless Spa Luxury • Không Gian Nghỉ Dưỡng • Gift Card CRO",
        "location": "California, Mỹ",
        "desc": "Website Day Spa kinh điển của California, tập trung truyền tải cảm giác thư giãn trọn vẹn của không gian spa nghỉ dưỡng cùng hệ thống bán gói trị liệu & thẻ quà tặng."
    },
    {
        "name": "Canyon Ranch — Khu Nghỉ Dưỡng Wellness & Spa Sức Khỏe Toàn Diện",
        "short_name": "Canyon Ranch",
        "url": "https://www.canyonranch.com/",
        "domain": "canyonranch.com",
        "slug": "spa_canyonranch",
        "category": "Luxury Wellness & Longevity Resort",
        "category_vn": "Canyon Ranch (Mỹ) — Đỉnh Cao Wellness Spa & Chăm Sóc Sức Khỏe",
        "tag": "quoc-te-spa",
        "vibe": "Serene Earth-Tone • Editorial Storytelling • Cao Cấp Thanh Lịch",
        "location": "Arizona & Massachusetts, Mỹ",
        "desc": "Chuẩn mực thiết kế cho phân khúc Wellness Spa & trị liệu sức khỏe cao cấp với tông màu đất dịu mắt, nhịp điệu kể chuyện thanh thản và trải nghiệm đặt lịch chuẩn 5 sao."
    },
]

results = []
passed_list = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for idx, site in enumerate(pool, 1):
        site["id"] = f"sp{idx:02d}"
        site["industry"] = "spa-tham-my-vien"
        site["industry_name"] = "Spa, Thẩm Mỹ Viện & Clinic"
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
                    '.klaviyo-close-form', '[aria-label="Close dialog"]'
                ];
                selectors.forEach(sel => {
                    try { document.querySelectorAll(sel).forEach(btn => { try { btn.click(); } catch(e) {} }); } catch(e) {}
                });
                // Remove Shadow DOM chat/marketing widgets proactively
                document.querySelectorAll('*').forEach(el => {
                    if (el.shadowRoot) {
                        const tag = (el.tagName || '').toLowerCase();
                        const id = (el.id || '').toLowerCase();
                        if (tag.includes('chat') || tag.includes('bot') || tag.includes('intercom') || tag.includes('widget') || id.includes('chat') || tag.includes('attentive')) {
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

print(f"\n=== TỔNG KẾT QA NGÁCH 7 (SPA, THẨM MỸ VIỆN & CLINIC): ĐẠT {len(passed_list)}/{len(pool)} MẪU ===")
for r in results:
    print(f"  {r[0]:20s} | {r[1]:30s} | {r[2]:9s} | {r[3]}")
