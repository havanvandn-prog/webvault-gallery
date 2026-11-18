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
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "anhngu_dep_candidates.json")

os.makedirs(output_dir, exist_ok=True)
os.makedirs(kho_webp_dir, exist_ok=True)
os.makedirs(os.path.dirname(metadata_file), exist_ok=True)

pool = [
    # --- NHÓM 1: HỌC VIỆN & TRƯỜNG ANH NGỮ QUỐC TẾ (BỐ CỤC EDITORIAL HIỆN ĐẠI) ---
    {
        "name": "EF Education First — Học Viện Ngôn Ngữ & Du Học Toàn Cầu",
        "short_name": "EF Education First",
        "url": "https://www.ef.com/wwen/",
        "domain": "ef.com",
        "slug": "anhngu_dep_ef",
        "category": "Global Editorial Language Academy",
        "category_vn": "Học Viện Anh Ngữ Quốc Tế — Thiết Kế Editorial Đẳng Cấp",
        "tag": "quoc-te-editorial",
        "vibe": "Editorial Toàn Cầu • Typography Sắc Nét • Storytelling Trực Quan",
        "location": "Quốc tế (Toàn cầu)",
        "desc": "Website chuẩn mực quốc tế của tập đoàn giáo dục EF với bố cục tạp chí hiện đại, khoảng thở rộng rãi, phân tầng chương trình học theo độ tuổi rõ nét và điều hướng tối giản."
    },
    {
        "name": "EC English — Chuỗi Trường Anh Ngữ Quốc Tế Hiện Đại",
        "short_name": "EC English",
        "url": "https://ecenglish.com/en/",
        "domain": "ecenglish.com",
        "slug": "anhngu_dep_ecenglish",
        "category": "Modern International English School",
        "category_vn": "Trường Anh Ngữ Quốc Tế — Giao Diện Trẻ Trung & Năng Động",
        "tag": "quoc-te-editorial",
        "vibe": "Hiện Đại • Thẻ Khóa Học Sạch Sẽ • Tối Ưu Chọn Điểm Đến",
        "location": "Anh, Mỹ, Canada, Malta",
        "desc": "Giao diện trường Anh ngữ quốc tế nổi bật với bảng màu tương phản sạch sẽ, bộ lọc chọn thành phố và khóa học trực quan, kết hợp ảnh sinh viên thực tế giàu cảm xúc."
    },
    {
        "name": "Bayswater Education — Học Viện Tiếng Anh Boutique Đương Đại",
        "short_name": "Bayswater Education",
        "url": "https://www.bayswater.ac/en",
        "domain": "bayswater.ac",
        "slug": "anhngu_dep_bayswater",
        "category": "Boutique International College",
        "category_vn": "Học Viện Tiếng Anh Boutique — Bố Cục Tươi Mới & Sáng Tạo",
        "tag": "quoc-te-editorial",
        "vibe": "Boutique Sáng Tạo • Bố Cục Bento Card • Màu Sắc Đương Đại",
        "location": "London, Paris, Toronto",
        "desc": "Thiết kế web đậm chất boutique với các khối bo góc mềm mại, lưới card chương trình đào tạo bắt mắt và trải nghiệm thị giác cân bằng giữa thẩm mỹ và chuyển đổi."
    },
    {
        "name": "Oxford International English — Trường Anh Ngữ Học Thuật Anh Quốc",
        "short_name": "Oxford International",
        "url": "https://www.oxfordinternationalenglish.com/",
        "domain": "oxfordinternationalenglish.com",
        "slug": "anhngu_dep_oxford_intl",
        "category": "British Academic English School",
        "category_vn": "Trường Anh Ngữ Anh Quốc — Bố Cục Chuẩn Học Thuật",
        "tag": "quoc-te-editorial",
        "vibe": "Chuẩn Anh Quốc • Xanh Navy Uy Tín • Phân Cấp Thông Tin Rõ",
        "location": "Vương quốc Anh & Bắc Mỹ",
        "desc": "Website mang phong cách học thuật Anh Quốc hiện đại, trình bày mạch lạc lộ trình tiếng Anh tổng quát, học thuật và luyện thi IELTS cùng hệ thống cơ sở vật chất."
    },
    {
        "name": "Wimbledon School of English — Trường Anh Ngữ Top #1 Vương Quốc Anh",
        "short_name": "Wimbledon School",
        "url": "https://wimbledon-school.ac.uk/",
        "domain": "wimbledon-school.ac.uk",
        "slug": "anhngu_dep_wimbledon",
        "category": "Top-Ranked UK English School",
        "category_vn": "Trường Anh Ngữ Danh Tiếng London — Giao Diện Thanh Lịch",
        "tag": "quoc-te-editorial",
        "vibe": "Thanh Lịch London • Lưới Ảnh Sạch Đẹp • Trust Badges Rõ Nét",
        "location": "London, Anh Quốc",
        "desc": "Mẫu website trường tiếng Anh lâu đời tại London được làm mới hiện đại, nổi bật với huy hiệu chứng nhận chất lượng British Council và hành trình đăng ký khóa học tinh gọn."
    },
    {
        "name": "Stafford House International — Hệ Thống Đào Tạo Anh Ngữ Quốc Tế",
        "short_name": "Stafford House",
        "url": "https://www.staffordhouse.com/",
        "domain": "staffordhouse.com",
        "slug": "anhngu_dep_staffordhouse",
        "category": "Multi-Campus English Academy",
        "category_vn": "Học Viện Anh Ngữ Đa Cơ Sở — Trình Bày Trực Quan",
        "tag": "quoc-te-editorial",
        "vibe": "Tươi Sáng • Cấu Trúc Modular • Thẻ Khóa Học Hiện Đại",
        "location": "Anh & Mỹ",
        "desc": "Bố cục dạng module rõ ràng giúp học viên quốc tế nhanh chóng chọn khóa tiếng Anh giao tiếp, kinh doanh hoặc luyện thi theo từng thành phố."
    },
    {
        "name": "Kings Education — Học Viện Tiếng Anh & Dự Bị Đại Học",
        "short_name": "Kings Education",
        "url": "https://www.kingseducation.com/",
        "domain": "kingseducation.com",
        "slug": "anhngu_dep_kings",
        "category": "University Pathway & English Hub",
        "category_vn": "Học Viện Tiếng Anh Học Thuật — Bố Cục Tạp Chí Cao Cấp",
        "tag": "quoc-te-editorial",
        "vibe": "Editorial Cao Cấp • Khoảng Trắng Tinh Tế • Chuyển Đổi Tư Vấn",
        "location": "Anh & Mỹ",
        "desc": "Website thiết kế chỉn chu với hệ thống typography rõ ràng, khối số liệu thành tích thuyết phục và hình ảnh đời sống học đường chân thực."
    },
    {
        "name": "Berlitz — Hệ Thống Đào Tạo Ngoại Ngữ Toàn Cầu Cho Người Đi Làm",
        "short_name": "Berlitz",
        "url": "https://www.berlitz.com/",
        "domain": "berlitz.com",
        "slug": "anhngu_dep_berlitz",
        "category": "Executive & Global Language Training",
        "category_vn": "Trung Tâm Ngoại Ngữ Doanh Nhân — Giao Diện Chuẩn SaaS",
        "tag": "quoc-te-editorial",
        "vibe": "Doanh Nhân • Xanh Hiện Đại • Phễu Chọn Khóa Học Nhanh",
        "location": "Toàn cầu (70+ quốc gia)",
        "desc": "Thương hiệu đào tạo ngoại ngữ 145 năm với giao diện web thế hệ mới gọn gàng, điều hướng thông minh theo nhu cầu cá nhân, trẻ em và doanh nghiệp."
    },

    # --- NHÓM 2: EDTECH & TRƯỜNG TIẾNG ANH CÔNG NGHỆ CAO (UI/UX HIỆN ĐẠI) ---
    {
        "name": "Speak — Nền Tảng Luyện Nói Tiếng Anh AI Chuẩn Silicon Valley",
        "short_name": "Speak",
        "url": "https://www.speak.com/",
        "domain": "speak.com",
        "slug": "anhngu_dep_speak",
        "category": "AI Spoken English Platform",
        "category_vn": "Học Viện Luyện Giao Tiếp AI — UI/UX Đẳng Cấp Silicon Valley",
        "tag": "edtech-hien-dai",
        "vibe": "Silicon Valley UI • Typography Cỡ Lớn • Mockup Ứng Dụng Sắc Nét",
        "location": "Quốc tế (Mỹ & Toàn cầu)",
        "desc": "Giao diện mang chuẩn thiết kế sản phẩm công nghệ hàng đầu với font chữ đậm nét, bố cục bất đối xứng tinh tế và trình diễn giao diện hội thoại AI cực kỳ mượt mà."
    },
    {
        "name": "Lingoda — Trường Tiếng Anh Trực Tuyến Chuẩn Châu Âu",
        "short_name": "Lingoda",
        "url": "https://www.lingoda.com/en/",
        "domain": "lingoda.com",
        "slug": "anhngu_dep_lingoda",
        "category": "European Online Language School",
        "category_vn": "Trường Tiếng Anh Online — Bố Cục SaaS Sạch & Chuyển Đổi Cao",
        "tag": "edtech-hien-dai",
        "vibe": "SaaS Giáo Dục • Bảng Cấp Độ CEFR Trực Quan • CTA Học Thử Rõ Ràng",
        "location": "Châu Âu & Toàn cầu",
        "desc": "Mẫu mực về bố cục trường học trực tuyến: trình bày lộ trình CEFR A1-C2 trực quan, thẻ gói học linh hoạt, lịch lớp 24/7 và đánh giá học viên xác thực."
    },
    {
        "name": "Cambly — Học Tiếng Anh 1-1 Với Giáo Viên Bản Xứ",
        "short_name": "Cambly",
        "url": "https://www.cambly.com/english",
        "domain": "cambly.com",
        "slug": "anhngu_dep_cambly",
        "category": "1-on-1 Native English Tutoring",
        "category_vn": "Nền Tảng Gia Sư Tiếng Anh Bản Xứ — Giao Diện Thân Thiện",
        "tag": "edtech-hien-dai",
        "vibe": "Vàng Ấm Thân Thiện • Thẻ Giáo Viên Trực Quan • Bố Cục Thoáng Đãng",
        "location": "Toàn cầu",
        "desc": "Thiết kế gần gũi, dễ quét thông tin với tông màu vàng-trắng đặc trưng, lưới thẻ hồ sơ gia sư bản xứ và luồng đăng ký học thử cực kỳ ít bước."
    },
    {
        "name": "Novakid — Trường Tiếng Anh Trực Tuyến Cho Trẻ Em",
        "short_name": "Novakid",
        "url": "https://www.novakidenglish.com/",
        "domain": "novakidenglish.com",
        "slug": "anhngu_dep_novakid",
        "category": "Gamified Kids English School",
        "category_vn": "Trường Anh Ngữ Thiếu Nhi — Minh Họa Sáng Tạo & Bố Cục Vui Nhộn",
        "tag": "edtech-hien-dai",
        "vibe": "Tím Năng Động • Minh Họa 3D Trẻ Em • Lộ Trình Theo Độ Tuổi",
        "location": "Quốc tế",
        "desc": "Bố cục trường tiếng Anh thiếu nhi đẹp mắt kết hợp nhân vật minh họa sinh động, phân chia cấp độ học theo lứa tuổi rõ ràng và form đặt lịch học thử miễn phí."
    },
    {
        "name": "Busuu — Cộng Đồng & Hệ Thống Học Tiếng Anh Chuẩn Quốc Tế",
        "short_name": "Busuu",
        "url": "https://www.busuu.com/",
        "domain": "busuu.com",
        "slug": "anhngu_dep_busuu",
        "category": "Interactive Language Learning Hub",
        "category_vn": "Nền Tảng Học Ngoại Ngữ Hiện Đại — Bố Cục Tối Giản Tinh Gọn",
        "tag": "edtech-hien-dai",
        "vibe": "Tối Giản Hiện Đại • Xanh Dương Sạch Sẽ • Card Tính Năng Cân Đối",
        "location": "Châu Âu & Toàn cầu",
        "desc": "Giao diện web hiện đại với khoảng trắng hợp lý, phân tách rõ ràng lộ trình tự học, chứng chỉ và cộng đồng sửa bài bản ngữ."
    },
    {
        "name": "Prep Edu — Nền Tảng Học & Luyện Thi Tiếng Anh AI Hàng Đầu Việt Nam",
        "short_name": "Prep Edu",
        "url": "https://prepedu.com/vi/",
        "domain": "prepedu.com",
        "slug": "anhngu_dep_prepedu",
        "category": "Vietnam AI English EdTech",
        "category_vn": "EdTech Tiếng Anh Việt Nam — Giao Diện Công Nghệ & Tương Tác Đẹp",
        "tag": "edtech-hien-dai",
        "vibe": "EdTech Việt Nam • Xanh Công Nghệ • Phòng Luyện Ảo AI Trực Quan",
        "location": "Việt Nam",
        "desc": "Một trong những website giáo dục tiếng Anh có UI/UX đẹp nhất Việt Nam: phối màu xanh dương hiện đại, phân tách rõ IELTS/TOEIC/Giao tiếp và minh họa phòng luyện Speaking-Writing AI."
    },
    {
        "name": "ELSA Speak Việt Nam — Gia Sư AI Luyện Phát Âm & Giao Tiếp",
        "short_name": "ELSA Speak",
        "url": "https://vn.elsaspeak.com/",
        "domain": "vn.elsaspeak.com",
        "slug": "anhngu_dep_elsaspeak",
        "category": "AI Pronunciation & Speaking Platform",
        "category_vn": "Nền Tảng Luyện Nói Tiếng Anh AI — Landing Page Chuyển Đổi Đẹp",
        "tag": "edtech-hien-dai",
        "vibe": "Gradient Tech • Bố Cục Chuyển Đổi CRO • Showcase Tính Năng App",
        "location": "Việt Nam & Toàn cầu",
        "desc": "Website thiết kế theo phong cách Tech-Startup toàn cầu với khối hero thu hút, bảng so sánh gói học minh bạch, bằng chứng hiệu quả học tập và CTA rõ nét."
    },

    # --- NHÓM 3: TRUNG TÂM TIẾNG ANH VIỆT NAM GIAO DIỆN MỚI & BỐ CỤC ĐẸP ---
    {
        "name": "TalkFirst — Trung Tâm Anh Ngữ Giao Tiếp & IELTS Không Gian Hiện Đại",
        "short_name": "TalkFirst",
        "url": "https://talkfirst.vn/",
        "domain": "talkfirst.vn",
        "slug": "anhngu_dep_talkfirst",
        "category": "Modern Lifestyle English Academy",
        "category_vn": "Trung Tâm Tiếng Anh Sài Gòn — Giao Diện Sang Trọng & Hình Ảnh Thật",
        "tag": "trung-tam-vn-dep",
        "vibe": "Hiện Đại Cao Cấp • Ảnh Lớp Học Thực Tế • Tông Màu Đậm Chất Sáng Tạo",
        "location": "TP. Hồ Chí Minh",
        "desc": "Trung tâm tiếng Anh tại TP.HCM sở hữu website đầu tư bài bản về mặt thị giác, ảnh không gian học tập chuẩn coworking sắc nét và bố cục khóa học dễ quét."
    },
    {
        "name": "Simple English — Hệ Thống Anh Ngữ Giao Tiếp & Luyện Thi IELTS",
        "short_name": "Simple English",
        "url": "https://simpleenglish.com.vn/",
        "domain": "simpleenglish.com.vn",
        "slug": "anhngu_dep_simpleenglish",
        "category": "Clean Communication & IELTS Center",
        "category_vn": "Trung Tâm Anh Ngữ TP.HCM — Bố Cục Tối Giản & Thân Thiện",
        "tag": "trung-tam-vn-dep",
        "vibe": "Sạch Sẽ Thân Thiện • Bố Cục Khối Rõ Ràng • Chứng Thực Học Viên",
        "location": "TP. Hồ Chí Minh",
        "desc": "Website có bố cục gọn gàng, nhịp điệu section dễ đọc, trình bày thuyết phục phương pháp RESTA, profile giảng viên và phản hồi thực tế từ học viên."
    },
    {
        "name": "Summit Education — Học Viện Tiếng Anh Học Thuật, IELTS & SAT",
        "short_name": "Summit Education",
        "url": "https://summit.edu.vn/",
        "domain": "summit.edu.vn",
        "slug": "anhngu_dep_summit",
        "category": "Academic IELTS & SAT Center",
        "category_vn": "Trung Tâm Anh Ngữ Học Thuật — Bố Cục Uy Tín & Chặt Chẽ",
        "tag": "trung-tam-vn-dep",
        "vibe": "Học Thuật Uy Tín • Bảng Thành Tích Điểm Cao • Cấu Trúc Mạch Lạc",
        "location": "Hà Nội, TP.HCM & Đà Nẵng",
        "desc": "Giao diện thể hiện rõ vị thế học thuật cao cấp với bảng vàng thành tích IELTS/SAT, hệ thống khóa học phân cấp từ THCS đến du học và nút đăng ký tư vấn nổi bật."
    },
    {
        "name": "Monkey English — Hệ Sinh Thái Tiếng Anh Trẻ Em Số 1 Việt Nam",
        "short_name": "Monkey English",
        "url": "https://monkey.edu.vn/",
        "domain": "monkey.edu.vn",
        "slug": "anhngu_dep_monkey",
        "category": "Kids English Learning Ecosystem",
        "category_vn": "Tiếng Anh Trẻ Em — Giao Diện Sinh Động & Thân Thiện Phụ Huynh",
        "tag": "trung-tam-vn-dep",
        "vibe": "Xanh Tươi Vui Nhộn • Card Sản Phẩm Rõ Ràng • Dễ Chuyển Đổi",
        "location": "Việt Nam",
        "desc": "Website tiếng Anh thiếu nhi thiết kế rực rỡ mà vẫn giữ được sự ngăn nắp, phân tách rõ từng chương trình theo độ tuổi và tích hợp đánh giá từ phụ huynh."
    },
    {
        "name": "Kyna English — Học Tiếng Anh Online 1 Kèm 1 Cho Trẻ Em & Thiếu Niên",
        "short_name": "Kyna English",
        "url": "https://kynaenglish.vn/",
        "domain": "kynaenglish.vn",
        "slug": "anhngu_dep_kynaenglish",
        "category": "1-on-1 Online Youth English Center",
        "category_vn": "Anh Ngữ Trực Tuyến 1-1 — Bố Cục Lộ Trình Chuẩn Cambridge",
        "tag": "trung-tam-vn-dep",
        "vibe": "Hiện Đại Thân Thiện • Lộ Trình Cambridge Trực Quan • Form Học Thử",
        "location": "Việt Nam (Trực tuyến)",
        "desc": "Bố cục trang đích tối ưu cho phụ huynh tìm lớp tiếng Anh 1 kèm 1: minh họa lộ trình Starters-Movers-Flyers, đội ngũ giáo viên và form đăng ký học thử ngay đầu trang."
    },
]

backups = [
    {
        "name": "EIV Education — Đào Tạo Tiếng Anh 100% Giáo Viên Bản Ngữ",
        "short_name": "EIV Education",
        "url": "https://eiv.edu.vn/",
        "domain": "eiv.edu.vn",
        "slug": "anhngu_dep_eiv",
        "category": "Native Teacher Corporate & 1-1 English",
        "category_vn": "Trung Tâm Tiếng Anh Bản Ngữ — Doanh Nghiệp & Kèm Riêng",
        "tag": "trung-tam-vn-dep",
        "vibe": "Doanh Nghiệp Chuyên Nghiệp • Bố Cục Gọn Sạch • Dịch Vụ 1-1",
        "location": "Hà Nội, TP.HCM & Đà Nẵng",
        "desc": "Website cung cấp giải pháp đào tạo tiếng Anh doanh nghiệp và gia sư bản ngữ 1-1 với bố cục rõ ràng, làm nổi bật đối tác lớn và quy trình tuyển chọn giáo viên."
    },
    {
        "name": "Positively Languages (Kaplan) — Học Tiếng Anh Quốc Tế Trải Nghiệm",
        "short_name": "Positively Languages",
        "url": "https://positivelylanguages.com/",
        "domain": "positivelylanguages.com",
        "slug": "anhngu_dep_positively",
        "category": "Global Language Travel School",
        "category_vn": "Trường Ngôn Ngữ Quốc Tế — Thiết Kế Tươi Mới Hiện Đại",
        "tag": "quoc-te-editorial",
        "vibe": "Trẻ Trung Quốc Tế • Hình Ảnh Ấn Tượng • Điều Hướng Rõ Ràng",
        "location": "Anh, Mỹ, Canada, Úc",
        "desc": "Giao diện hiện đại cho chương trình học tiếng Anh kết hợp trải nghiệm văn hóa tại các thành phố lớn trên thế giới."
    },
    {
        "name": "British Council LearnEnglish — Cổng Học Tiếng Anh Hội Đồng Anh",
        "short_name": "British Council",
        "url": "https://learnenglish.britishcouncil.org/",
        "domain": "learnenglish.britishcouncil.org",
        "slug": "anhngu_dep_bc_learn",
        "category": "Global British English Authority",
        "category_vn": "Tổ Chức Anh Ngữ Hoàng Gia — Giao Diện Chuẩn Mực & Tin Cậy",
        "tag": "quoc-te-editorial",
        "vibe": "Chuẩn Quốc Tế • Xanh Tím Đậm Uy Tín • Phân Tầng Kỹ Năng Rõ",
        "location": "Toàn cầu",
        "desc": "Cổng học tiếng Anh chính thức của Hội đồng Anh với hệ thống điều hướng chuẩn mực, phân tầng theo trình độ A1-C1 và kỹ năng rõ nét."
    },
    {
        "name": "LSI Education — Trường Anh Ngữ Quốc Tế Lâu Đời",
        "short_name": "LSI Education",
        "url": "https://www.lsi.edu/en/",
        "domain": "lsi.edu",
        "slug": "anhngu_dep_lsi",
        "category": "International English School Network",
        "category_vn": "Mạng Lưới Trường Anh Ngữ Quốc Tế — Giao Diện Gọn Đẹp",
        "tag": "quoc-te-editorial",
        "vibe": "Sạch Sẽ Hiện Đại • Bộ Lọc Điểm Đến • Tin Cậy Quốc Tế",
        "location": "Anh, Mỹ, Canada, Úc",
        "desc": "Thiết kế web trường tiếng Anh đa quốc gia gọn gàng, tối ưu trải nghiệm chọn khóa học và thành phố du học tiếng Anh."
    },
]

def dismiss_cookies_and_overlays(page):
    try:
        page.evaluate("""() => {
            const cookieSelectors = [
                '#onetrust-accept-btn-handler',
                '.onetrust-close-btn-handler',
                '#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll',
                'button[id*="accept-cookie" i]',
                'button[class*="cookie" i][class*="accept" i]',
                'button[aria-label*="accept" i]',
                'button[aria-label*="close" i]'
            ];
            for (const sel of cookieSelectors) {
                const btn = document.querySelector(sel);
                if (btn) { try { btn.click(); } catch(e) {} }
            }
            document.querySelectorAll('#onetrust-consent-sdk, #CybotCookiebotDialog, .cookie-banner, [id*="cookie-banner"], [class*="cookie-consent"]').forEach(el => {
                el.style.setProperty('display', 'none', 'important');
            });
        }""")
    except Exception:
        pass

def process_item(page, item, idx):
    slug = item["slug"]
    png_path = os.path.join(output_dir, f"{slug}.png")
    print(f"\n[{idx}] Đang xử lý: {item['short_name']} ({item['url']})")

    for attempt in range(2):
        delay = 0.16 if attempt == 0 else 0.30
        try:
            setup_page_protection(page)
            page.goto(item["url"], timeout=45000, wait_until="domcontentloaded")
            try:
                page.wait_for_load_state("networkidle", timeout=10000)
            except Exception:
                pass
            time.sleep(2.5 if attempt == 0 else 4.0)
            dismiss_cookies_and_overlays(page)
            time.sleep(0.5)

            w, h = capture_smart_clean(page, png_path, viewport_height=900, scroll_delay=delay)
            print(f"    -> Đã chụp: {w}x{h}px (Lần {attempt+1})")

            thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb = compress_tri_layer(png_path, slug, kho_webp_dir)
            full_webp_path = os.path.join(kho_webp_dir, full_name)
            ok, msg = verify_captured_image(full_webp_path)
            print(f"    -> Kiểm định: [{'PASS' if ok else 'FAIL'}] {msg}")

            if ok:
                item["id"] = f"eng{idx:02d}"
                item["industry"] = "trung-tam-tieng-anh-dep"
                item["industry_name"] = "Trung Tâm Tiếng Anh (Bố Cục Đẹp)"
                item["image"] = f"Anh_Chup_Website/{slug}.png"
                item["thumb"] = f"Kho_Anh_Webp/{thumb_name}"
                item["full"] = f"Kho_Anh_Webp/{full_name}"
                item["fb"] = f"Kho_Anh_Webp/{fb_name}"
                item["thumb_kb"] = thumb_kb
                item["full_kb"] = full_kb
                item["fb_kb"] = fb_kb
                item["size_mb"] = f"{round(os.path.getsize(png_path)/(1024*1024), 2)} MB"
                item["audit_msg"] = msg
                item["status"] = "SUCCESS"
                return True
        except Exception as e:
            print(f"    -> Lỗi lần {attempt+1}: {str(e)[:120]}")

    item["status"] = "FAILED"
    return False

def main():
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            ignore_https_errors=True
        )
        page = context.new_page()

        success_count = 0
        for item in pool:
            if success_count >= 20:
                break
            ok = process_item(page, item, success_count + 1)
            if ok:
                results.append(item)
                success_count += 1

        if success_count < 20:
            for b_item in backups:
                if success_count >= 20:
                    break
                ok = process_item(page, b_item, success_count + 1)
                if ok:
                    results.append(b_item)
                    success_count += 1

        browser.close()

    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n=== HOÀN TẤT: {len(results)}/20 mẫu đạt chuẩn kiểm định! ===")

if __name__ == "__main__":
    main()
