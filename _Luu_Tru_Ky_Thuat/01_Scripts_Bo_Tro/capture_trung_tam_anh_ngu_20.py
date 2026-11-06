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
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "trung_tam_anh_ngu_metadata.json")

os.makedirs(output_dir, exist_ok=True)
os.makedirs(kho_webp_dir, exist_ok=True)
os.makedirs(os.path.dirname(metadata_file), exist_ok=True)

websites = [
    # =========================================================================
    # NHÓM 1: HỆ THỐNG ANH NGỮ QUỐC TẾ & CHUỖI TRUNG TÂM LỚN TOÀN QUỐC
    # =========================================================================
    {
        "id": "anhngu01",
        "name": "Anh Văn Hội Việt Mỹ (VUS)",
        "short_name": "VUS",
        "url": "https://vus.edu.vn/",
        "domain": "vus.edu.vn",
        "slug": "vus_edu_vn",
        "industry": "trung-tam-anh-ngu",
        "industry_name": "Trung Tâm Anh Ngữ",
        "category": "Top-Tier National English Education System",
        "category_vn": "Hệ Thống Trung Tâm Anh Ngữ Chuẩn Quốc Tế Quy Mô Lớn Nhất Việt Nam",
        "tag": "he-thong-quoc-te",
        "vibe": "corporate-international-blue",
        "vibe_name": "Hiện Đại, Đẳng Cấp & Chuẩn Quốc Tế",
        "location": "Toàn quốc (TP.HCM, Hà Nội, Đà Nẵng, Bình Dương, Cần Thơ...)",
        "desc": "Hệ thống Anh ngữ chuẩn NEAS quốc tế với mạng lưới hơn 80 cơ sở. Giao diện trực quan, kiến trúc thông tin phân tầng rõ ràng theo từng độ tuổi (SmartKids, SuperKids, Young Leaders, IELTS), tích hợp lịch khai giảng và hệ sinh thái học tập OEA."
    },
    {
        "id": "anhngu02",
        "name": "ILA Vietnam",
        "short_name": "ILA",
        "url": "https://ila.edu.vn/",
        "domain": "ila.edu.vn",
        "slug": "ila_edu_vn",
        "industry": "trung-tam-anh-ngu",
        "industry_name": "Trung Tâm Anh Ngữ",
        "category": "Leading 100% Native English Education Network",
        "category_vn": "Tổ Chức Giáo Dục & Đào Tạo Anh Ngữ 100% Giáo Viên Bản Xứ",
        "tag": "he-thong-quoc-te",
        "vibe": "clean-premium-educational",
        "vibe_name": "Sang Trọng, Tinh Tế & Giáo Dục Tương Lai",
        "location": "Toàn quốc (Hơn 60 trung tâm tại các thành phố lớn)",
        "desc": "Chuỗi trung tâm cao cấp tiên phong phương pháp học tập thế kỷ 21. Bố cục website chuẩn quốc tế với hình ảnh lớp học thực tế sắc nét, bộ lọc khóa học thông minh, lời chứng thực từ phụ huynh và chuyển đổi tư vấn học phí liền mạch."
    },
    {
        "id": "anhngu03",
        "name": "Apollo English",
        "short_name": "Apollo English",
        "url": "https://apollo.edu.vn/",
        "domain": "apollo.edu.vn",
        "slug": "apollo_edu_vn",
        "industry": "trung-tam-anh-ngu",
        "industry_name": "Trung Tâm Anh Ngữ",
        "category": "Pioneer Young Learners English Academy",
        "category_vn": "Tổ Chức Anh Ngữ Trẻ Em Chuẩn Quốc Tế Đầu Tiên Tại Việt Nam",
        "tag": "he-thong-quoc-te",
        "vibe": "vibrant-friendly-kids",
        "vibe_name": "Tươi Sáng, Năng Động & Thân Thiện Gia Đình",
        "location": "Toàn quốc (Hà Nội, TP.HCM, Hải Phòng, Đà Nẵng...)",
        "desc": "Thương hiệu hơn 30 năm kinh nghiệm thuộc hệ sinh thái International House. Website thiết kế thân thiện với phụ huynh, tối ưu hóa điểm chạm đăng ký học thử miễn phí, minh họa phương pháp độc quyền Apollo Active và lộ trình phát triển toàn diện của trẻ."
    },
    {
        "id": "anhngu04",
        "name": "YOLA (Tri Thức Trẻ)",
        "short_name": "YOLA",
        "url": "https://yola.vn/",
        "domain": "yola.vn",
        "slug": "yola_vn",
        "industry": "trung-tam-anh-ngu",
        "industry_name": "Trung Tâm Anh Ngữ",
        "category": "Academic English & Test Preparation Hub",
        "category_vn": "Tổ Chức Giáo Dục Tiếng Anh Học Thuật & Khai Phóng Tiềm Năng",
        "tag": "he-thong-quoc-te",
        "vibe": "inspirational-youth",
        "vibe_name": "Truyền Cảm Hứng, Trẻ Trung & Đậm Tính Học Thuật",
        "location": "Hà Nội & TP.HCM",
        "desc": "Trung tâm chuyên đào tạo tiếng Anh học thuật, IELTS, SAT và chuẩn bị du học. Giao diện hiện đại nổi bật với bảng vàng thành tích điểm cao của học viên, biểu mẫu đăng ký kiểm tra trình độ xếp lớp nhanh và thông tin học bổng hấp dẫn."
    },
    {
        "id": "anhngu05",
        "name": "Wall Street English Việt Nam",
        "short_name": "Wall Street English",
        "url": "https://wallstreetenglish.edu.vn/",
        "domain": "wallstreetenglish.edu.vn",
        "slug": "wallstreetenglish_edu_vn",
        "industry": "trung-tam-anh-ngu",
        "industry_name": "Trung Tâm Anh Ngữ",
        "category": "Global Adult & Executive English Academy",
        "category_vn": "Trung Tâm Anh Ngữ Dành Riêng Cho Người Lớn & Người Đi Làm Toàn Cầu",
        "tag": "he-thong-quoc-te",
        "vibe": "executive-corporate-blue",
        "vibe_name": "Chuyên Nghiệp, Doanh Nhân & Đề Cao Hiệu Quả",
        "location": "TP.HCM & Hà Nội",
        "desc": "Mô hình học tiếng Anh chuẩn quốc tế cho người bận rộn với thời gian biểu linh hoạt 100%. Giao diện định hướng chuyển đổi cao (CRO) với form kiểm tra trình độ nhận lộ trình cá nhân hóa, nhấn mạnh môi trường giao tiếp 100% tiếng Anh."
    },
    {
        "id": "anhngu06",
        "name": "Ocean Edu Vietnam",
        "short_name": "Ocean Edu",
        "url": "https://ocean.edu.vn/",
        "domain": "ocean.edu.vn",
        "slug": "ocean_edu_vn",
        "industry": "trung-tam-anh-ngu",
        "industry_name": "Trung Tâm Anh Ngữ",
        "category": "Nationwide International English System",
        "category_vn": "Hệ Thống Anh Ngữ Quốc Tế Quy Mô Lớn Nhất Miền Bắc & Toàn Quốc",
        "tag": "he-thong-quoc-te",
        "vibe": "energetic-cyan-community",
        "vibe_name": "Sôi Động, Lan Tỏa & Phủ Khắp Toàn Quốc",
        "location": "Toàn quốc (Hơn 150 chi nhánh khắp các tỉnh thành)",
        "desc": "Chuỗi trung tâm giáo dục tiếng Anh chuẩn Cambridge với mạng lưới rộng khắp cả nước. Website bố cục phong phú về hoạt động ngoại khóa, hệ thống định vị cơ sở toàn quốc và các chương trình ưu đãi học bổng trực quan."
    },
    {
        "id": "anhngu07",
        "name": "GLN English Center",
        "short_name": "GLN English",
        "url": "https://gln.edu.vn/",
        "domain": "gln.edu.vn",
        "slug": "gln_edu_vn",
        "industry": "trung-tam-anh-ngu",
        "industry_name": "Trung Tâm Anh Ngữ",
        "category": "Luxury Space IELTS & Kids English Center",
        "category_vn": "Trung Tâm Anh Ngữ Không Gian Đẳng Cấp & Luyện Thi IELTS Hàng Đầu",
        "tag": "he-thong-quoc-te",
        "vibe": "luxury-creative-space",
        "vibe_name": "Sang Trọng, Độc Đáo & Không Gian Sáng Tạo",
        "location": "Hà Nội (Keangnam Landmark & Tràng Thi)",
        "desc": "Nổi tiếng với không gian học tập chuẩn 5 sao mô phỏng các kỳ quan thế giới tại các tòa tháp hạng A ở Hà Nội. Website thể hiện đẳng cấp thương hiệu với hình ảnh cơ sở vật chất sang trọng, bảng thành tích hàng ngàn học viên đạt 7.5 - 8.5 IELTS."
    },

    # =========================================================================
    # NHÓM 2: HỌC VIỆN LUYỆN THI IELTS HỌC THUẬT & CHUYÊN SÂU
    # =========================================================================
    {
        "id": "anhngu08",
        "name": "DOL English (IELTS Đình Lực)",
        "short_name": "DOL English",
        "url": "https://www.dolenglish.vn/",
        "domain": "dolenglish.vn",
        "slug": "dolenglish_vn",
        "industry": "trung-tam-anh-ngu",
        "industry_name": "Trung Tâm Anh Ngữ",
        "category": "EdTech & Linearthinking IELTS Academy",
        "category_vn": "Học Viện Tiếng Anh Tư Duy Linearthinking & Ứng Dụng Công Nghệ AI",
        "tag": "luyen-thi-ielts",
        "vibe": "modern-tech-edtech",
        "vibe_name": "Hiện Đại, Đột Phá & Công Nghệ Cao",
        "location": "Toàn quốc (TP.HCM, Hà Nội, Đà Nẵng, Cần Thơ, Hải Phòng)",
        "desc": "Đơn vị tiên phong sáng tạo phương pháp Linearthinking giúp học viên bứt phá điểm số IELTS, TOEIC và SAT. Giao diện đậm chất EdTech với thư viện tự học phong phú, tích hợp nền tảng thi thử online và định vị thương hiệu học tập thông minh."
    },
    {
        "id": "anhngu09",
        "name": "The IELTS Workshop (TIW)",
        "short_name": "The IELTS Workshop",
        "url": "https://theieltsworkshop.com/",
        "domain": "theieltsworkshop.com",
        "slug": "theieltsworkshop_com",
        "industry": "trung-tam-anh-ngu",
        "industry_name": "Trung Tâm Anh Ngữ",
        "category": "Celebrity-Led Elite IELTS Preparation Hub",
        "category_vn": "Trung Tâm Luyện Thi IELTS Hàng Đầu Sáng Lập Bởi Thầy Đặng Trần Tùng",
        "tag": "luyen-thi-ielts",
        "vibe": "friendly-academic-orange",
        "vibe_name": "Nhiệt Huyết, Gần Gũi & Uy Tín Vững Chắc",
        "location": "Hà Nội, TP.HCM & Online Toàn quốc",
        "desc": "Học viện luyện thi IELTS được bảo chứng chuyên môn bởi thầy Đặng Trần Tùng (4 lần đạt 9.0 IELTS). Bố cục trang chia rõ lộ trình từ 0 đến 7.5+ IELTS, thư viện tài liệu luyện thi phong phú, lịch thi thử định kỳ và đội ngũ giáo viên 8.0+ minh bạch."
    },
    {
        "id": "anhngu10",
        "name": "ZIM Academy",
        "short_name": "ZIM Academy",
        "url": "https://zim.vn/",
        "domain": "zim.vn",
        "slug": "zim_vn",
        "industry": "trung-tam-anh-ngu",
        "industry_name": "Trung Tâm Anh Ngữ",
        "category": "Personalized Academic English & Test Prep",
        "category_vn": "Trường Anh Ngữ Học Thuật & Đào Tạo Chứng Chỉ Quốc Tế Cá Nhân Hóa",
        "tag": "luyen-thi-ielts",
        "vibe": "minimalist-clean-scholarly",
        "vibe_name": "Tối Giản, Khoa Học & Mẫu Mực Học Thuật",
        "location": "Hà Nội, TP.HCM, Đà Nẵng",
        "desc": "Hệ thống đào tạo IELTS, TOEIC và tiếng Anh học thuật nổi tiếng với kho xuất bản giáo trình chuyên sâu. Giao diện thiết kế theo phong cách tối giản thanh lịch, công cụ tra cứu ngữ pháp/từ vựng tiện lợi, và form đánh giá năng lực cá nhân hóa theo từng mục tiêu điểm."
    },
    {
        "id": "anhngu11",
        "name": "IELTS Fighter (Chiến Binh IELTS)",
        "short_name": "IELTS Fighter",
        "url": "https://ielts-fighter.com/",
        "domain": "ielts-fighter.com",
        "slug": "ielts_fighter_com",
        "industry": "trung-tam-anh-ngu",
        "industry_name": "Trung Tâm Anh Ngữ",
        "category": "Popular Nationwide IELTS Training Network",
        "category_vn": "Hệ Thống Luyện Thi IELTS Phổ Biến Nhất Cho Học Sinh & Sinh Viên",
        "tag": "luyen-thi-ielts",
        "vibe": "energetic-red-motivational",
        "vibe_name": "Nhiệt Huyết, Thực Chiến & Bứt Phá Điểm Số",
        "location": "Toàn quốc (Hơn 60 cơ sở trên toàn quốc)",
        "desc": "Thuộc hệ sinh thái IMAP Việt Nam, chuyên đào tạo IELTS mục tiêu 7.0+ theo phương pháp RIPL độc quyền. Trang web có lưu lượng truy cập khổng lồ nhờ kho bài giảng miễn phí, bộ đề dự đoán sát thực tế và form đăng ký kiểm tra năng lực trực quan."
    },
    {
        "id": "anhngu12",
        "name": "Anh Ngữ RES (RES English)",
        "short_name": "RES English",
        "url": "https://res.edu.vn/",
        "domain": "res.edu.vn",
        "slug": "res_edu_vn",
        "industry": "trung-tam-anh-ngu",
        "industry_name": "Trung Tâm Anh Ngữ",
        "category": "Cambridge & IELTS Specialized English System",
        "category_vn": "Hệ Thống Anh Ngữ Quốc Tế Chuyên Luyện Thi IELTS & Tiếng Anh Trẻ Em",
        "tag": "luyen-thi-ielts",
        "vibe": "established-educational-navy",
        "vibe_name": "Quy Mô Lớn, Truyền Thống & Vững Chãi",
        "location": "Toàn quốc (Hơn 40 chi nhánh tại các thành phố lớn)",
        "desc": "Đối tác xuất sắc nhiều năm liền của Hội đồng Úc IDP. Bố cục giới thiệu toàn diện các khóa học từ tiếng Anh 4 kỹ năng mầm non đến khóa luyện thi IELTS cấp tốc, bảng thành tích giải thưởng và hệ thống cơ sở vật chất hiện đại."
    },
    {
        "id": "anhngu13",
        "name": "Vietop English",
        "short_name": "Vietop",
        "url": "https://vietop.edu.vn/",
        "domain": "vietop.edu.vn",
        "slug": "vietop_edu_vn",
        "industry": "trung-tam-anh-ngu",
        "industry_name": "Trung Tâm Anh Ngữ",
        "category": "Intensive Boutique IELTS Training Center",
        "category_vn": "Trung Tâm Luyện Thi IELTS Chuyên Sâu & Cam Kết Điểm Số Bằng Hợp Đồng",
        "tag": "luyen-thi-ielts",
        "vibe": "boutique-professional-green",
        "vibe_name": "Tận Tâm, Chuyên Sâu & Cam Kết Vàng",
        "location": "TP.HCM",
        "desc": "Hệ thống trung tâm luyện thi IELTS trọng điểm tại TP.HCM nổi tiếng với chính sách học lại miễn phí đến khi đạt điểm mục tiêu. Giao diện hiện đại, rõ ràng về thời lượng khóa học, chia sẻ đề thi thật hàng tuần và đội ngũ giảng viên chuyên môn cao."
    },
    {
        "id": "anhngu14",
        "name": "KTDC Group",
        "short_name": "KTDC Group",
        "url": "https://ktdcgroup.vn/",
        "domain": "ktdcgroup.vn",
        "slug": "ktdcgroup_vn",
        "industry": "trung-tam-anh-ngu",
        "industry_name": "Trung Tâm Anh Ngữ",
        "category": "Native Expert IELTS & Business English Training",
        "category_vn": "Trung Tâm IELTS & Kỹ Năng Doanh Nghiệp Với 100% Chuyên Gia Bản Xứ",
        "tag": "luyen-thi-ielts",
        "vibe": "elite-western-academic",
        "vibe_name": "Chuẩn Bản Xứ, Đẳng Cấp & Chuyên Sâu",
        "location": "TP.HCM",
        "desc": "Đơn vị đào tạo IELTS và kỹ năng mềm tiếng Anh danh tiếng với 100% giảng viên bản ngữ có bằng cấp sư phạm quốc tế. Thiết kế website mang phong cách tối giản phương Tây, làm nổi bật profile từng chuyên gia và phương pháp kèm cặp kỹ năng phát âm chuẩn."
    },
    {
        "id": "anhngu15",
        "name": "WESET English Center",
        "short_name": "WESET",
        "url": "https://weset.edu.vn/",
        "domain": "weset.edu.vn",
        "slug": "weset_edu_vn",
        "industry": "trung-tam-anh-ngu",
        "industry_name": "Trung Tâm Anh Ngữ",
        "category": "Root-Based Methodology IELTS & Communication Hub",
        "category_vn": "Trung Tâm Đào Tạo IELTS Theo Phương Pháp Dựa Trên Cội Rễ Ngôn Ngữ",
        "tag": "luyen-thi-ielts",
        "vibe": "fresh-youth-academic",
        "vibe_name": "Trẻ Trung, Sáng Tạo & Đề Cao Bản Chất Ngôn Ngữ",
        "location": "TP.HCM",
        "desc": "Trung tâm Anh ngữ tiên phong phương pháp Root-Based Learning: học tiếng Anh từ gốc rễ tư duy ngôn ngữ để tự tin ứng dụng trong đời sống và kỳ thi. Website bố cục thoáng đãng, dễ theo dõi tiến độ các khóa học và đăng ký nhận lộ trình học tập miễn phí."
    },

    # =========================================================================
    # NHÓM 3: TIẾNG ANH GIAO TIẾP THỰC CHIẾN & NỀN TẢNG HỌC HIỆN ĐẠI
    # =========================================================================
    {
        "id": "anhngu16",
        "name": "Langmaster English",
        "short_name": "Langmaster",
        "url": "https://langmaster.edu.vn/",
        "domain": "langmaster.edu.vn",
        "slug": "langmaster_edu_vn",
        "industry": "trung-tam-anh-ngu",
        "industry_name": "Trung Tâm Anh Ngữ",
        "category": "Mindset & Spoken English Communication Ecosystem",
        "category_vn": "Tổ Chức Giáo Dục Tiếng Anh Giao Tiếp & Huấn Luyện Tư Duy Số 1",
        "tag": "giao-tiep-edtech",
        "vibe": "energetic-growth-mindset",
        "vibe_name": "Năng Lượng Đỉnh Cao, Thực Chiến & Bứt Phá Giới Hạn",
        "location": "Hà Nội & Online Toàn quốc",
        "desc": "Hệ thống đào tạo tiếng Anh giao tiếp kết hợp ứng dụng phương pháp NLP (Lập trình ngôn ngữ tư duy). Giao diện tối ưu trải nghiệm người dùng với các bài test trình độ tương tác, câu chuyện chuyển hóa thực tế của học viên và lộ trình chinh phục phản xạ giao tiếp tự nhiên."
    },
    {
        "id": "anhngu17",
        "name": "Jaxtina English Center",
        "short_name": "Jaxtina",
        "url": "https://jaxtina.com/",
        "domain": "jaxtina.com",
        "slug": "jaxtina_com",
        "industry": "trung-tam-anh-ngu",
        "industry_name": "Trung Tâm Anh Ngữ",
        "category": "Comprehensive 4-Skills English Training Center",
        "category_vn": "Hệ Thống Trung Tâm Anh Ngữ Tiên Phong Đào Tạo Toàn Diện 4 Kỹ Năng",
        "tag": "giao-tiep-edtech",
        "vibe": "modern-yellow-accent",
        "vibe_name": "Trẻ Trung, Năng Động & Rõ Ràng Lộ Trình",
        "location": "Hà Nội, TP.HCM & Đà Nẵng",
        "desc": "Hệ thống tiên phong đào tạo đồng đều 4 kỹ năng Nghe - Nói - Đọc - Viết cho sinh viên và người đi làm. Website tối ưu tỷ lệ chuyển đổi với giao diện hiện đại, công cụ xếp lớp nhanh chóng và cam kết đầu ra bằng hợp đồng minh bạch."
    },
    {
        "id": "anhngu18",
        "name": "Aten English School",
        "short_name": "Aten English",
        "url": "https://aten.edu.vn/",
        "domain": "aten.edu.vn",
        "slug": "aten_edu_vn",
        "industry": "trung-tam-anh-ngu",
        "industry_name": "Trung Tâm Anh Ngữ",
        "category": "Exclusive Communication Coaching & 1-on-1 English",
        "category_vn": "Hệ Thống Chuyên Sâu Tiếng Anh Giao Tiếp & Huấn Luyện Phát Âm Chuẩn",
        "tag": "giao-tiep-edtech",
        "vibe": "clean-friendly-pink",
        "vibe_name": "Ấm Áp, Tận Tụy & Cá Nhân Hóa Từng Học Viên",
        "location": "Toàn quốc (Hà Nội, TP.HCM, Đà Nẵng...)",
        "desc": "Trung tâm chuyên sâu về giao tiếp với mô hình kèm cặp 3 kèm 1 và đào tạo trọn đời. Bố cục website tinh gọn, tập trung tháo gỡ tâm lý sợ nói tiếng Anh của người mới bắt đầu và cung cấp các buổi học thử định hướng chuẩn phản xạ."
    },
    {
        "id": "anhngu19",
        "name": "NativeX (Topica Native)",
        "short_name": "NativeX",
        "url": "https://nativex.edu.vn/",
        "domain": "nativex.edu.vn",
        "slug": "nativex_edu_vn",
        "industry": "trung-tam-anh-ngu",
        "industry_name": "Trung Tâm Anh Ngữ",
        "category": "Next-Gen Online English Learning Platform",
        "category_vn": "Nền Tảng Học Tiếng Anh Online Toàn Diện Cho Người Đi Làm Bận Rộn",
        "tag": "giao-tiep-edtech",
        "vibe": "modern-saas-fintech",
        "vibe_name": "Công Nghệ Mới, Linh Hoạt & Đậm Chất SaaS",
        "location": "Toàn quốc (100% Trực tuyến)",
        "desc": "Nền tảng học tiếng Anh trực tuyến thế hệ mới với lớp học nén 45 phút, giảng viên bản xứ và thời gian biểu linh hoạt. Thiết kế UI/UX theo phong cách ứng dụng công nghệ hiện đại, điều hướng mượt mà, tối ưu hóa điểm chạm đăng ký trải nghiệm lớp học trực tiếp."
    },
    {
        "id": "anhngu20",
        "name": "Pasal English",
        "short_name": "Pasal",
        "url": "https://pasal.edu.vn/",
        "domain": "pasal.edu.vn",
        "slug": "pasal_edu_vn",
        "industry": "trung-tam-anh-ngu",
        "industry_name": "Trung Tâm Anh Ngữ",
        "category": "Exclusive Global Method Communication Center",
        "category_vn": "Tổ Chức Chuyên Sâu Giao Tiếp Độc Quyền Phương Pháp Effortless English",
        "tag": "giao-tiep-edtech",
        "vibe": "energetic-orange-enthusiasm",
        "vibe_name": "Năng Động, Tự Nhiên & Đầy Cảm Hứng",
        "location": "Hà Nội, TP.HCM & Online",
        "desc": "Đơn vị độc quyền tại Việt Nam hợp tác cùng TS A.J Hoge (cha đẻ Effortless English) và chuyên gia Paul Gruber (Pronunciation Workshop). Bố cục website trình bày trực quan lộ trình phản xạ phát âm, cung cấp nhiều bài học mẫu và kích thích động lực học tập."
    }
]

print(f"=== BẮT ĐẦU CHỤP VÀ NÉN ẢNH CHO {len(websites)} WEBSITE TRUNG TÂM ANH NGỮ ===")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    for idx, site in enumerate(websites, 1):
        print(f"\n[{idx:02d}/{len(websites)}] Đang xử lý: {site['name']} ({site['url']})...")
        
        raw_png = os.path.join(output_dir, f"{site['domain']}.png")
        full_webp = os.path.join(kho_webp_dir, f"{site['slug']}_full.webp")
        thumb_webp = os.path.join(kho_webp_dir, f"{site['slug']}_thumb.webp")
        fb_png = os.path.join(kho_webp_dir, f"{site['slug']}_fb.png")
        
        # Kiểm tra nếu đã có ảnh đầy đủ và đạt chuẩn thì có thể tái sử dụng
        if os.path.exists(full_webp) and os.path.exists(thumb_webp) and os.path.exists(fb_png):
            valid, msg = verify_captured_image(full_webp)
            if valid:
                print(f"  -> Đã có ảnh đạt chuẩn: {full_webp} ({msg}). Bỏ qua chụp lại.")
                continue
        
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        
        try:
            # Điều hướng với timeout 35s
            page.goto(site['url'], timeout=35000, wait_until="domcontentloaded")
            time.sleep(1.5)
            
            # Chụp clean không viền thừa bằng capture_smart_clean
            capture_smart_clean(page, raw_png, viewport_height=900, scroll_delay=0.18)
            
            if not os.path.exists(raw_png) or os.path.getsize(raw_png) == 0:
                print(f"  [-] Lỗi: Không thể chụp ảnh cho {site['domain']}")
                continue
                
            # Nén 3 tầng WebP
            thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb = compress_tri_layer(raw_png, site['slug'], kho_webp_dir)
            
            # Cổng tự động kiểm định chất lượng (Post-Capture QA)
            valid, msg = verify_captured_image(full_webp)
            print(f"  [+] QA Audit {site['domain']}: {'PASS' if valid else 'FAIL'} - {msg}")
            
            if not valid:
                print(f"  [!] Cảnh báo: Tự động chụp lại với độ trễ cao hơn...")
                time.sleep(2.0)
                capture_smart_clean(page, raw_png, viewport_height=900, scroll_delay=0.28)
                compress_tri_layer(raw_png, site['slug'], kho_webp_dir)
                valid2, msg2 = verify_captured_image(full_webp)
                print(f"  [+] QA Audit Vòng 2 {site['domain']}: {'PASS' if valid2 else 'FAIL'} - {msg2}")
                
        except Exception as e:
            print(f"  [-] Lỗi trong quá trình chụp {site['domain']}: {e}")
        finally:
            page.close()
            
    browser.close()

# Lưu metadata JSON
with open(metadata_file, "w", encoding="utf-8") as f:
    json.dump(websites, f, ensure_ascii=False, indent=2)

print(f"\n[+] Đã lưu {len(websites)} metadata website vào: {metadata_file}")
print("[+] Hoàn tất toàn bộ quy trình chụp và nén ảnh!")
