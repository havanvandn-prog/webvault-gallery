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
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "khach_san_candidates.json")

os.makedirs(output_dir, exist_ok=True)
os.makedirs(kho_webp_dir, exist_ok=True)

pool = [
    # --- NHÓM 1: KHÁCH SẠN LUXURY & BOUTIQUE HÀNG ĐẦU VIỆT NAM (13 MẪU) ---
    {
        "name": "Sofitel Legend Metropole Hanoi — Di Sản 5 Sao Huyền Thoại",
        "short_name": "Sofitel Metropole Hanoi",
        "url": "https://www.sofitel-legend-metropole-hanoi.com/",
        "domain": "sofitel-legend-metropole-hanoi.com",
        "slug": "ks_metropole_hanoi",
        "category": "Heritage Luxury Hotel",
        "category_vn": "Khách Sạn Di Sản Pháp Cổ — Đặt Phòng Trực Tiếp",
        "tag": "luxury-heritage",
        "vibe": "Heritage Luxury • Kiến Trúc Pháp Cổ • Thanh Booking Đầu Trang",
        "location": "Hà Nội",
        "desc": "Website khách sạn di sản 5 sao lâu đời bậc nhất Hà Nội với bố cục sang trọng, hình ảnh nghệ thuật kích thước lớn và thanh đặt phòng trực tiếp (Direct Booking) ngay trên màn hình đầu."
    },
    {
        "name": "Peridot Grand Luxury Boutique Hotel — Boutique Cao Cấp Phố Cổ",
        "short_name": "Peridot Grand Hanoi",
        "url": "https://peridotgrandhotel.com/",
        "domain": "peridotgrandhotel.com",
        "slug": "ks_peridot_grand",
        "category": "Luxury Boutique Hotel",
        "category_vn": "Boutique Hotel Đương Đại — Phố Cổ Hà Nội",
        "tag": "boutique-luxury",
        "vibe": "Boutique Luxury • Hồ Bơi Vô Cực & Sky Bar • Form Đặt Phòng Nổi",
        "location": "Hà Nội",
        "desc": "Giao diện khách sạn boutique 5 sao tại trung tâm Hoàn Kiếm nổi bật với tông màu vàng kim-đen quyền quý, trình diễn trực quan hệ thống phòng, nhà hàng, spa và thanh book phòng nhanh."
    },
    {
        "name": "The Reverie Saigon — Khách Sạn Xa Xỉ Chuẩn Leading Hotels",
        "short_name": "The Reverie Saigon",
        "url": "https://www.thereveriesaigon.com/",
        "domain": "thereveriesaigon.com",
        "slug": "ks_reverie_saigon",
        "category": "Ultra-Luxury City Hotel",
        "category_vn": "Khách Sạn 6 Sao Xa Hoa — Trung Tâm Quận 1",
        "tag": "luxury-heritage",
        "vibe": "Ultra Luxury • Nội Thất Ý Độc Bản • Storytelling Toàn Cảnh",
        "location": "TP. Hồ Chí Minh",
        "desc": "Website khách sạn sang trọng bậc nhất Sài Gòn trực thuộc Leading Hotels of the World, gây ấn tượng bằng hình ảnh toàn cảnh đại lộ Nguyễn Huệ, bộ sưu tập suite xa hoa và trải nghiệm ẩm thực."
    },
    {
        "name": "Hôtel des Arts Saigon (MGallery) — Nghệ Thuật Đông Dương",
        "short_name": "Hôtel des Arts Saigon",
        "url": "https://www.hoteldesartssaigon.com/",
        "domain": "hoteldesartssaigon.com",
        "slug": "ks_hotel_des_arts",
        "category": "Indochine Art Boutique Hotel",
        "category_vn": "Boutique Nghệ Thuật Đông Dương — MGallery",
        "tag": "boutique-luxury",
        "vibe": "Indochine Art • Typography Cổ Điển • Rooftop Pool & Bar",
        "location": "TP. Hồ Chí Minh",
        "desc": "Trang web khách sạn boutique nghệ thuật mang phong cách Đông Dương thập niên 1930, kết hợp khéo léo giữa phông chữ editorial thanh lịch, bộ sưu tập tranh nghệ thuật và CTA đặt phòng rõ nét."
    },
    {
        "name": "Hôtel de la Coupole Sapa — kiệt tác Bill Bensley giữa mây ngàn",
        "short_name": "Hôtel de la Coupole Sapa",
        "url": "https://www.hoteldelacoupole.com/",
        "domain": "hoteldelacoupole.com",
        "slug": "ks_hotel_de_la_coupole",
        "category": "High-Fashion Mountain Hotel",
        "category_vn": "Khách Sạn Nghệ Thuật Sapa — Thiết Kế Bill Bensley",
        "tag": "boutique-luxury",
        "vibe": "Haute Couture • Màu Sắc Nghệ Thuật • Trải Nghiệm Sapa",
        "location": "Sapa, Lào Cai",
        "desc": "Giao diện khách sạn 5 sao tại Sapa lấy cảm hứng từ thời trang cao cấp Pháp và văn hóa vùng cao, sử dụng bố cục tạp chí giàu màu sắc và hệ thống đặt phòng/ẩm thực trực quan."
    },
    {
        "name": "Regent Phú Quốc — Khu Nghỉ Dưỡng & Khách Sạn All-Suites",
        "short_name": "Regent Phú Quốc",
        "url": "https://phuquoc.regenthotels.com/",
        "domain": "phuquoc.regenthotels.com",
        "slug": "ks_regent_phu_quoc",
        "category": "Ultra-Luxury Resort Hotel",
        "category_vn": "Khu Nghỉ Dưỡng All-Suites 5 Sao+ — Phú Quốc",
        "tag": "resort-hotel",
        "vibe": "Minimalist Luxury • Biệt Thự & Suite Biển • Thanh Đặt Phòng Sticky",
        "location": "Phú Quốc",
        "desc": "Website chuẩn quốc tế của thương hiệu Regent tại Bãi Trường Phú Quốc: thiết kế tối giản tĩnh tại, tỷ lệ ảnh-chữ cân bằng hoàn hảo và phễu đặt phòng biệt thự biển mượt mà."
    },
    {
        "name": "Azerai Resorts — Chuỗi Khách Sạn & Resort Tối Giản Tinh Tế",
        "short_name": "Azerai Resorts",
        "url": "https://azerai.com/",
        "domain": "azerai.com",
        "slug": "ks_azerai_resorts",
        "category": "Minimalist Boutique Collection",
        "category_vn": "Chuỗi Boutique Di Sản Huế, Cần Thơ & Kê Gà",
        "tag": "boutique-luxury",
        "vibe": "Quiet Luxury • Adrian Zecha • Minimalist Editorial Grid",
        "location": "Huế / Cần Thơ / Bình Thuận",
        "desc": "Website của chuỗi boutique resort do huyền thoại Adrian Zecha sáng lập (Azerai La Residence Huế, Cần Thơ, Kê Gà Bay), chuẩn mực về phong cách Quiet Luxury với nhiều khoảng thở."
    },
    {
        "name": "An Lâm Retreats — Khách Sạn & Retreat Sinh Thái Biệt Lập",
        "short_name": "An Lâm Retreats",
        "url": "https://anlam.com/",
        "domain": "anlam.com",
        "slug": "ks_an_lam_retreats",
        "category": "Eco Luxury Retreat",
        "category_vn": "Retreat Nghỉ Dưỡng Sinh Thái — Ninh Vân & Sài Gòn",
        "tag": "resort-hotel",
        "vibe": "Nature Sanctuary • Tông Đất Ấm • Storytelling Biệt Lập",
        "location": "Nha Trang & TP.HCM",
        "desc": "Giao diện mang hơi thở thiên nhiên bản địa kết hợp nghỉ dưỡng cao cấp tại vịnh Ninh Vân và sông Sài Gòn, chú trọng trải nghiệm chăm sóc sức khỏe và đặt kỳ nghỉ trọn gói."
    },
    {
        "name": "Wink Hotels — Chuỗi Khách Sạn Lifestyle Hiện Đại Việt Nam",
        "short_name": "Wink Hotels",
        "url": "https://wink-hotels.com/",
        "domain": "wink-hotels.com",
        "slug": "ks_wink_hotels",
        "category": "Modern Lifestyle Hotel Chain",
        "category_vn": "Chuỗi Khách Sạn Hiện Đại 24h Stay — Đa Thành Phố",
        "tag": "modern-chain",
        "vibe": "Bold Youthful UI • 24h Stay Concept • Booking Engine Tối Ưu",
        "location": "TP.HCM / Đà Nẵng / Cần Thơ / Tuy Hòa",
        "desc": "Website chuỗi khách sạn thế hệ mới tại Việt Nam với ngôn ngữ thị giác trẻ trung, tương phản mạnh, nhấn mạnh đặc quyền lưu trú đủ 24 giờ và quy trình đặt phòng trực tuyến siêu nhanh."
    },
    {
        "name": "Fusion Hotel Group — Chuỗi Khách Sạn All-Spa Inclusive",
        "short_name": "Fusion Hotel Group",
        "url": "https://fusionhotelgroup.com/",
        "domain": "fusionhotelgroup.com",
        "slug": "ks_fusion_hotel_group",
        "category": "Wellness & Hotel Group",
        "category_vn": "Tập Đoàn Khách Sạn & Nghỉ Dưỡng Wellness Hàng Đầu VN",
        "tag": "modern-chain",
        "vibe": "Multi-Property Hub • Wellness Lifestyle • Bộ Lọc Điểm Đến",
        "location": "Toàn Quốc & Thái Lan",
        "desc": "Cổng thông tin tập đoàn quản lý hàng loạt thương hiệu khách sạn nổi tiếng (Fusion Resort, Maia, Fusion Suites, Alba) với bộ lọc điểm đến trực quan và bảng đặt phòng đa cơ sở."
    },
    {
        "name": "La Siesta Hotels & Resorts — Top Khách Sạn Boutique Phố Cổ",
        "short_name": "La Siesta Hotels",
        "url": "https://lasiestahotels.com/",
        "domain": "lasiestahotels.com",
        "slug": "ks_la_siesta_hotels",
        "category": "Boutique Hospitality Group",
        "category_vn": "Hệ Thống Khách Sạn Boutique Top TripAdvisor",
        "tag": "modern-chain",
        "vibe": "Warm Indochine • Đa Cơ Sở Hà Nội & Hội An • Ưu Đãi Trực Tiếp",
        "location": "Hà Nội & Hội An",
        "desc": "Website của chuỗi khách sạn boutique Việt Nam thường xuyên đứng top thế giới trên TripAdvisor, thiết kế ấm áp thân thiện với hệ thống chọn cơ sở và gói ưu đãi đặt trực tiếp rõ ràng."
    },
    {
        "name": "Silk Path Hotels & Resorts — Chuỗi Khách Sạn 4–5 Sao Quốc Nội",
        "short_name": "Silk Path Hotels",
        "url": "https://silkpathhotel.com/",
        "domain": "silkpathhotel.com",
        "slug": "ks_silk_path",
        "category": "Vietnamese Hotel Chain",
        "category_vn": "Chuỗi Khách Sạn Hà Nội, Huế & Sapa",
        "tag": "modern-chain",
        "vibe": "Classic Elegance • Booking Bar Đầu Trang • Gói Combo Nghỉ Dưỡng",
        "location": "Hà Nội / Huế / Sapa",
        "desc": "Trang web chuỗi khách sạn mang dấu ấn di sản và hiện đại tại các thành phố du lịch lớn, cấu trúc phân tầng dịch vụ phòng, hội nghị MICE và ẩm thực rất khoa học."
    },
    {
        "name": "Silverland Hospitality — Chuỗi Boutique Hotel Trung Tâm Sài Gòn",
        "short_name": "Silverland Hotels",
        "url": "https://silverlandhotels.com/",
        "domain": "silverlandhotels.com",
        "slug": "ks_silverland_hotels",
        "category": "Urban Boutique Collection",
        "category_vn": "Hệ Thống 8 Khách Sạn Boutique Quận 1",
        "tag": "boutique-luxury",
        "vibe": "Urban Boutique • Bản Đồ Hệ Thống • Direct Booking Perk",
        "location": "Quận 1, TP.HCM",
        "desc": "Website quy tụ chuỗi khách sạn boutique đặc sắc ngay trung tâm Quận 1 (Silverland Sakyo, Jolie, Ben Thanh...), làm nổi bật nét kiến trúc riêng từng cơ sở và đặc quyền trà chiều."
    },
    # --- NHÓM 2: KHÁCH SẠN & BOUTIQUE HOTEL QUỐC TẾ ĐẠT GIẢI UI/UX (7 MẪU + BACKUPS) ---
    {
        "name": "Aman Resorts — Chuẩn Mực Tối Giản Xa Xỉ Toàn Cầu",
        "short_name": "Aman Resorts",
        "url": "https://www.aman.com/",
        "domain": "aman.com",
        "slug": "ks_aman_resorts",
        "category": "Global Ultra-Luxury Sanctuary",
        "category_vn": "Tượng Đài Minimalist Luxury Toàn Cầu",
        "tag": "international-awwwards",
        "vibe": "Ultra Minimalist • Editorial Serif • Không Gian Thở Tuyệt Đối",
        "location": "Quốc tế (có Amanoi VN)",
        "desc": "Website chuẩn mực cho phân khúc siêu sang thế giới: sử dụng typography serif tinh tế, nền kem/trắng thanh thoát, ảnh nhiếp ảnh kiến trúc toàn khung và trải nghiệm khám phá điểm đến."
    },
    {
        "name": "Rosewood Hotels & Resorts — Bố Cục Tạp Chí Sang Trọng",
        "short_name": "Rosewood Hotels",
        "url": "https://www.rosewoodhotels.com/en/default",
        "domain": "rosewoodhotels.com",
        "slug": "ks_rosewood_hotels",
        "category": "Luxury Editorial Hospitality",
        "category_vn": "Chuỗi Khách Sạn Xa Xỉ Phong Cách Tạp Chí",
        "tag": "international-awwwards",
        "vibe": "Sense of Place • Editorial Grid • Đa Điểm Đến Toàn Cầu",
        "location": "Quốc tế",
        "desc": "Giao diện mang triết lý 'A Sense of Place' với lưới ảnh bất đối xứng, câu chuyện văn hóa bản địa sâu sắc và thanh tìm kiếm đặt phòng tinh gọn chuẩn thương hiệu xa xỉ."
    },
    {
        "name": "Ett Hem Stockholm — Khách Sạn Boutique Như Ngôi Nhà Riêng",
        "short_name": "Ett Hem Stockholm",
        "url": "https://www.etthem.se/",
        "domain": "etthem.se",
        "slug": "ks_ett_hem",
        "category": "Scandinavian Boutique Hotel",
        "category_vn": "Boutique Bắc Âu Ấm Áp — Thiết Kế Ilse Crawford",
        "tag": "international-awwwards",
        "vibe": "Scandinavian Warmth • Intimate Storytelling • Tối Giản Tinh Tế",
        "location": "Stockholm, Thụy Điển",
        "desc": "Hình mẫu kinh điển trong giới thiết kế web boutique hotel: xóa bỏ cảm giác khô khan của bảng giá, thay bằng nhịp cuộn chậm rãi, chất liệu ấm áp như một tư gia riêng."
    },
    {
        "name": "Constance Hotels & Resorts — Chuỗi Resort Đạt Giải Awwwards",
        "short_name": "Constance Hotels",
        "url": "https://www.constancehotels.com/en/",
        "domain": "constancehotels.com",
        "slug": "ks_constance_hotels",
        "category": "Awwwards Hospitality Winner",
        "category_vn": "Khách Sạn Đạt Giải Awwwards Mobile & UI/UX",
        "tag": "international-awwwards",
        "vibe": "Awwwards Honoree • Cân Bằng Cảm Xúc & Booking Engine",
        "location": "Ấn Độ Dương",
        "desc": "Website từng được vinh danh trên Awwwards nhờ khả năng kết hợp hoàn hảo giữa kể chuyện du lịch nghỉ dưỡng đầy cảm xúc với công cụ kiểm tra phòng trống chuyển đổi cao."
    },
    {
        "name": "7132 Hotel Vals — Kiến Trúc Tối Giản & Dark Luxury Thụy Sĩ",
        "short_name": "7132 Hotel Switzerland",
        "url": "https://7132.com/en",
        "domain": "7132.com",
        "slug": "ks_7132_hotel",
        "category": "Architectural Dark Luxury Hotel",
        "category_vn": "Khách Sạn Kiến Trúc Đá Tối Giản — Thụy Sĩ",
        "tag": "international-awwwards",
        "vibe": "Dark Architectural • Thermal Baths • Typography Đậm Chất Tạp Chí",
        "location": "Vals, Thụy Sĩ",
        "desc": "Website khách sạn gắn liền với công trình suối khoáng nổi tiếng của KTS Peter Zumthor, nổi bật với tông màu trầm tương phản cao, khoảng trắng lớn và bố cục kiến trúc cực kỳ sắc nét."
    },
    {
        "name": "Our Habitas — Khách Sạn Trải Nghiệm & Bền Vững Toàn Cầu",
        "short_name": "Our Habitas",
        "url": "https://www.ourhabitas.com/",
        "domain": "ourhabitas.com",
        "slug": "ks_our_habitas",
        "category": "Experiential Sustainable Hotel",
        "category_vn": "Thương Hiệu Khách Sạn Trải Nghiệm & Cộng Đồng",
        "tag": "international-awwwards",
        "vibe": "Earthy Aesthetic • Video Immersion • Wellness & Music",
        "location": "Quốc tế (Tulum, AlUla...)",
        "desc": "Giao diện khách sạn phong cách du mục bền vững với gam màu đất hữu cơ, bố cục mô-đun hiện đại làm nổi bật giá trị kết nối thiên nhiên, nghệ thuật và trải nghiệm cộng đồng."
    },
    {
        "name": "Badrutt's Palace St. Moritz — Khách Sạn Di Sản Hoàng Gia",
        "short_name": "Badrutt's Palace",
        "url": "https://badruttspalace.com/en/winter/",
        "domain": "badruttspalace.com",
        "slug": "ks_badrutts_palace",
        "category": "Iconic Alpine Heritage Hotel",
        "category_vn": "Cung Điện Nghỉ Dưỡng Huyền Thoại Dãy Alps",
        "tag": "international-awwwards",
        "vibe": "Grand Heritage • Interactive Room Preview • Concierge Digital",
        "location": "St. Moritz, Thụy Sĩ",
        "desc": "Chuẩn mực chuyển đổi số cho các khách sạn di sản lâu đời: giữ trọn vẻ uy nghi quý tộc kết hợp cùng điều hướng hiện đại, trình xem phòng tương tác và đặt bàn/phòng trực tuyến."
    },
    # --- BACKUP CANDIDATES ---
    {
        "name": "P'apiu Resort Hà Giang — Khu Nghỉ Dưỡng Độc Bản Cho Cặp Đôi",
        "short_name": "P'apiu Resort",
        "url": "https://papiu.vn/",
        "domain": "papiu.vn",
        "slug": "ks_papiu_resort",
        "category": "Bespoke Mountain Retreat",
        "category_vn": "Nghỉ Dưỡng Độc Bản Trên Núi — Hà Giang",
        "tag": "resort-hotel",
        "vibe": "Bespoke Storytelling • Văn Hóa Bản Địa • Chỉ 5 Căn Độc Quyền",
        "location": "Hà Giang",
        "desc": "Website giới thiệu khu nghỉ dưỡng riêng tư độc đáo tại Hà Giang với câu chuyện kiến trúc bản địa, các trải nghiệm cá nhân hóa và hệ thống tư vấn đặt phòng trực tiếp."
    },
    {
        "name": "Topas Ecolodge Sapa — Khu Nghỉ Dưỡng Sinh Thái Top National Geographic",
        "short_name": "Topas Ecolodge",
        "url": "https://topasecolodge.com/",
        "domain": "topasecolodge.com",
        "slug": "ks_topas_ecolodge",
        "category": "Sustainable Mountain Ecolodge",
        "category_vn": "Ecolodge Hồ Bơi Vô Cực Giữa Ruộng Bậc Thang",
        "tag": "resort-hotel",
        "vibe": "Eco Resort • Ảnh Flycam Toàn Cảnh • Đặt Bungalow Trực Tiếp",
        "location": "Sapa, Lào Cai",
        "desc": "Trang chủ khu nghỉ dưỡng sinh thái nổi tiếng thế giới tại Sapa, khai thác tối đa hình ảnh hồ bơi vô cực giữa núi rừng và luồng đặt phòng bungalow thân thiện với du khách quốc tế."
    },
    {
        "name": "Le Barn Hotel Paris — Boutique Đồng Quê Phong Cách Pháp",
        "short_name": "Le Barn Hotel",
        "url": "https://lebarnhotel.com/en/",
        "domain": "lebarnhotel.com",
        "slug": "ks_le_barn_hotel",
        "category": "French Countryside Boutique",
        "category_vn": "Khách Sạn Đồng Quê Thanh Lịch Ngoại Ô Paris",
        "tag": "international-awwwards",
        "vibe": "Countryside Chic • Slow Living • Pastel & Editorial Font",
        "location": "Paris, Pháp",
        "desc": "Website khách sạn đồng quê cách Paris 45 phút mang phong cách nhẹ nhàng, tinh tế với bảng màu thiên nhiên dịu mắt và cách kể chuyện hoạt động ngoài trời rất cuốn hút."
    }
]

print(f"=== CHỤP & KIỂM ĐỊNH POOL {len(pool)} WEBSITE KHÁCH SẠN (CHỌN ĐỦ 20 MẪU PASS 100%) ===")
approved_20 = []
results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for idx, site in enumerate(pool, 1):
        if len(approved_20) >= 20:
            print("\n[✓] Đã thu thập đủ 20 mẫu PASS 100%! Dừng vòng lặp pool.")
            break

        ks_num = len(approved_20) + 1
        site_id = f"ks{ks_num:02d}"
        site["id"] = site_id
        site["industry"] = "khach-san"
        site["industry_name"] = "Khách Sạn & Khu Nghỉ Dưỡng"

        print(f"\n[Pool {idx:02d}/{len(pool)} -> Target {site_id}] {site['name']} ({site['url']})...")
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
            page.goto(site['url'], timeout=45000, wait_until="domcontentloaded")
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
                    'button:has-text("Accept")', 'button:has-text("Agree")',
                    'button:has-text("Đóng")', 'button:has-text("Đồng ý")'
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
                page.goto(site['url'], timeout=55000, wait_until="networkidle")
                time.sleep(4.5)
                page.evaluate("""() => {
                    document.querySelectorAll('[id*="cookie" i], [class*="cookie" i], [id*="consent" i], [class*="consent" i], [class*="onetrust" i], [id*="onetrust" i], .modal-backdrop, .popup-overlay').forEach(el => {
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
                approved_20.append(site)
                results.append((site_id, site["domain"], "PASS", msg))
            else:
                # Dọn dẹp file lỗi để giữ kho sạch
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
    json.dump(approved_20, f, ensure_ascii=False, indent=2)

print(f"\n=== TỔNG KẾT QA: ĐẠT {len(approved_20)}/20 MẪU KHÁCH SẠN ===")
for r in results:
    print(f"  {r[0]:24s} | {r[1]:32s} | {r[2]:9s} | {r[3]}")
