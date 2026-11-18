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
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "banh_mi_quoc_te_pool_audit.json")

os.makedirs(output_dir, exist_ok=True)
os.makedirs(kho_webp_dir, exist_ok=True)

pool = [
    # --- NHÓM 1: TIỆM BÁNH MÌ & ẨM THỰC VIỆT PHỤC VỤ KHÁCH QUỐC TẾ TẠI VIỆT NAM ---
    {
        "name": "Bánh Mì Mẹ Ỉn — Tiệm Bánh Mì Sài Gòn Cho Du Khách Quốc Tế",
        "short_name": "Bánh Mì Mẹ Ỉn",
        "url": "https://banhmi.mein.vn/",
        "domain": "banhmi.mein.vn",
        "slug": "bmqt_mein_saigon",
        "category": "Tourist-First Saigon Banh Mi",
        "category_vn": "Tiệm Bánh Mì Chợ Bến Thành — Thiết Kế Cho Du Khách",
        "tag": "vietnam-expat",
        "vibe": "Boutique Saigon • Song Ngữ Anh-Việt • Ảnh Món Ăn Sắc Nét",
        "location": "Quận 1, TP. Hồ Chí Minh",
        "desc": "Thương hiệu Bánh Mì Mẹ Ỉn ngay trung tâm Chợ Bến Thành phục vụ lượng lớn du khách quốc tế. Giao diện nổi bật với gam màu ấm cổ điển, hình ảnh bánh mì nhân đầy đặn, trình bày menu tiếng Anh rõ ràng kèm giá và câu chuyện ẩm thực."
    },
    {
        "name": "Vietnom Local Eatery — Bếp Việt Đương Đại Tại Đà Nẵng & Hội An",
        "short_name": "Vietnom Local Eatery",
        "url": "https://vietnom.kitchen/en",
        "domain": "vietnom.kitchen",
        "slug": "bmqt_vietnom_kitchen",
        "category": "Modern Vietnamese Local Eatery",
        "category_vn": "Tiệm Ăn Việt Hiện Đại — Đà Nẵng & Hội An",
        "tag": "vietnam-expat",
        "vibe": "Modern Bistro • Editorial Typography • Thực Đơn Chuẩn Expat",
        "location": "Đà Nẵng & Hội An",
        "desc": "Không gian ẩm thực Việt đương đại rất được cộng đồng expat và du khách nước ngoài yêu thích tại miền Trung. Website sở hữu bố cục hiện đại, phông chữ tinh tế, kể chuyện nguyên liệu địa phương và nút đặt bàn/xem menu mượt mà."
    },
    {
        "name": "Anan Saigon — Michelin Street Food & Bánh Mì 100 USD",
        "short_name": "Anan Saigon",
        "url": "https://anansaigon.com/",
        "domain": "anansaigon.com",
        "slug": "bmqt_anan_saigon",
        "category": "Michelin Modern Vietnamese",
        "category_vn": "Ẩm Thực Đường Phố Cao Cấp 1 Sao Michelin",
        "tag": "vietnam-expat",
        "vibe": "Fine Street Food • Dark Editorial • Đặt Bàn Quốc Tế",
        "location": "Chợ Cũ Tôn Thất Đạm, Q.1, TP.HCM",
        "desc": "Nhà hàng 1 sao Michelin nổi tiếng thế giới với phiên bản Bánh Mì 100 USD trứ danh. Website tiếng Anh chuẩn quốc tế với phong cách tối giản sang trọng, ảnh nghệ thuật và quy trình đặt bàn cho khách nước ngoài."
    },
    # --- NHÓM 2: TIỆM BÁNH MÌ BOUTIQUE TẠI CHÂU ÂU, ÚC, NHẬT & SINGAPORE ---
    {
        "name": "Nonette Banh Mi & Donuts — Tiệm Bánh Mì Nghệ Thuật Tại Paris",
        "short_name": "Nonette Paris",
        "url": "https://www.nonettebanhmi.com/",
        "domain": "nonettebanhmi.com",
        "slug": "bmqt_nonette_paris",
        "category": "Artisanal Banh Mi & Cafe",
        "category_vn": "Bánh Mì Thủ Công & Cà Phê Nghệ Thuật — Paris",
        "tag": "europe-au-asia",
        "vibe": "Parisian Chic • Bố Cục Tạp Chí • Màu Sắc Độc Bản",
        "location": "Paris, Pháp",
        "desc": "Quầy bánh mì và bánh ngọt thủ công đình đám tại Paris do đội ngũ The Hood sáng lập. Website gây ấn tượng mạnh nhờ phong cách editorial táo bạo, bố cục bất đối xứng gọn gàng và hình ảnh bánh mì kẹp thịt nguội chuẩn vị."
    },
    {
        "name": "BAMMI — Chuỗi Bánh Mì Đường Phố Đương Đại Tại Melbourne",
        "short_name": "BAMMI Melbourne",
        "url": "https://bammivietnam.com.au/",
        "domain": "bammivietnam.com.au",
        "slug": "bmqt_bammi_melbourne",
        "category": "Contemporary Australian Banh Mi",
        "category_vn": "Bánh Mì Việt Phong Cách Melbourne Hiện Đại",
        "tag": "europe-au-asia",
        "vibe": "Bold Branding • Visual Menu • Catering & Order Online",
        "location": "Melbourne, Úc",
        "desc": "Thương hiệu bánh mì nổi tiếng tại Melbourne chinh phục thực khách quốc tế bằng nhận diện thương hiệu trẻ trung, màu sắc nổi bật, menu hiển thị trực quan từng loại nhân và luồng đặt tiệc catering chuyên nghiệp."
    },
    {
        "name": "Banh Mi Bao — Tiệm Bánh Mì & Bao Thủ Công Tại Sydney",
        "short_name": "Banh Mi Bao Sydney",
        "url": "https://www.banhmibao.com.au/",
        "domain": "banhmibao.com.au",
        "slug": "bmqt_banh_mi_bao_sydney",
        "category": "Artisan Street Food Sydney",
        "category_vn": "Tiệm Bánh Mì & Bánh Bao Hiện Đại — Sydney",
        "tag": "europe-au-asia",
        "vibe": "Modern Streetwear Vibe • Macro Photography • Pick-up Nhanh",
        "location": "Sydney, Úc",
        "desc": "Giao diện tiệm ăn uống bánh mì tại Sydney được thiết kế hiện đại với ảnh cận cảnh lớp vỏ giòn rụm, phân tầng menu dễ hiểu cho người nước ngoài kèm chế độ đặt hàng mang đi nhanh chóng."
    },
    {
        "name": "Luke's Bánh Mì — Thương Hiệu Bánh Mì Lò Nướng Tươi Melbourne",
        "short_name": "Luke's Bánh Mì",
        "url": "https://www.lukesbanhmi.au/",
        "domain": "lukesbanhmi.au",
        "slug": "bmqt_lukes_banhmi",
        "category": "Fresh Baked Banh Mi",
        "category_vn": "Tiệm Bánh Mì Lò Nướng Mỗi Giờ — Melbourne",
        "tag": "europe-au-asia",
        "vibe": "Clean Grid • Warm Bakery Tone • App & Loyalty",
        "location": "Melbourne, Úc",
        "desc": "Website tiệm bánh mì nổi bật tại Úc nhờ bố cục sạch sẽ, tông màu ấm áp gợi cảm giác bánh mới ra lò, tích hợp rõ hệ thống chi nhánh, thực đơn dinh dưỡng và đặt hàng trực tuyến."
    },
    {
        "name": "Roll'd Vietnamese — Chuỗi Bánh Mì & Gỏi Cuốn Lớn Nhất Nước Úc",
        "short_name": "Roll'd Vietnamese",
        "url": "https://rolld.com.au/",
        "domain": "rolld.com.au",
        "slug": "bmqt_rolld_au",
        "category": "National Vietnamese Fast-Casual",
        "category_vn": "Chuỗi Ẩm Thực Bánh Mì Việt Chuẩn Quốc Tế — Úc",
        "tag": "europe-au-asia",
        "vibe": "High-Conversion Fast Casual • Tương Phản Mạnh • Store Locator",
        "location": "Toàn quốc Úc (Melbourne, Sydney, Perth...)",
        "desc": "Chuỗi ẩm thực đường phố Việt Nam thành công bậc nhất tại Úc. Website là hình mẫu về UX ngành F&B: phân loại món rõ nét, ảnh chụp studio sắc nét, thẻ dinh dưỡng (Vegan/GF) và đặt đơn lấy tại quầy."
    },
    {
        "name": "The Banh Mi House — Tiệm Bánh Mì Gia Truyền Chuẩn Úc",
        "short_name": "The Banh Mi House",
        "url": "https://www.thebanhmihouse.com.au/",
        "domain": "thebanhmihouse.com.au",
        "slug": "bmqt_the_banh_mi_house",
        "category": "Modern Heritage Banh Mi",
        "category_vn": "Tiệm Bánh Mì Hiện Đại & Catering — Úc",
        "tag": "europe-au-asia",
        "vibe": "Clean Editorial • Storytelling Gia Đình • Đặt Tiệc Công Ty",
        "location": "Úc",
        "desc": "Trang web tiệm bánh mì có bố cục cân đối, kết hợp khéo léo câu chuyện gia đình làm bánh thủ công với danh mục món ăn và gói đặt tiệc cho dân văn phòng nước ngoài."
    },
    {
        "name": "Bun Banh Mi — Tiệm Bánh Mì Phong Cách Trẻ Tại Perth",
        "short_name": "Bun Banh Mi Perth",
        "url": "https://bunbanhmi.com.au/",
        "domain": "bunbanhmi.com.au",
        "slug": "bmqt_bun_banh_mi",
        "category": "Modern Casual Banh Mi",
        "category_vn": "Tiệm Bánh Mì & Bún Thịt Nướng — Perth",
        "tag": "europe-au-asia",
        "vibe": "Playful Modern • Color Blocking • Menu Dễ Chọn",
        "location": "Perth, Úc",
        "desc": "Giao diện tiệm ăn uống bánh mì tại Tây Úc với màu sắc tươi sáng, phông chữ dễ đọc và bố cục chia khối rõ ràng giữa bánh mì giòn, bún thịt nướng và thức uống Việt."
    },
    {
        "name": "Mister Banh Mi — Bếp Bánh Mì Đường Phố Tại Perth",
        "short_name": "Mister Banh Mi",
        "url": "https://misterbanhmi.com.au/",
        "domain": "misterbanhmi.com.au",
        "slug": "bmqt_mister_banh_mi",
        "category": "Neighborhood Banh Mi Shop",
        "category_vn": "Quán Bánh Mì Khu Phố Hiện Đại — Perth",
        "tag": "europe-au-asia",
        "vibe": "Warm Street Tone • Order CTA Nổi Bật • Thân Thiện Mobile",
        "location": "Perth, Úc",
        "desc": "Website gọn gàng, tối ưu trải nghiệm đặt món nhanh cho khách địa phương và quốc tế với phần giới thiệu nguyên liệu tươi mới mỗi ngày."
    },
    {
        "name": "Destination Roll — Chuỗi Bánh Mì Văn Phòng Tại Sydney & Perth",
        "short_name": "Destination Roll",
        "url": "https://destinationroll.co/",
        "domain": "destinationroll.co",
        "slug": "bmqt_destination_roll",
        "category": "Modern Corporate & Casual Banh Mi",
        "category_vn": "Chuỗi Bánh Mì & Catering Hiện Đại — Sydney/Perth",
        "tag": "europe-au-asia",
        "vibe": "Minimalist Fast-Casual • Bố Cục Lưới • Corporate Catering",
        "location": "Sydney & Perth, Úc",
        "desc": "Thiết kế tối giản chuẩn quốc tế, nhấn mạnh yếu tố sạch sẽ, nhanh gọn cho khách văn phòng nước ngoài muốn đặt bánh mì và hộp tiệc trưa."
    },
    {
        "name": "Banemi Paris — Tiệm Bánh Mì Việt Hiện Đại Tại Paris",
        "short_name": "Banemi Paris",
        "url": "https://www.banemi.fr/",
        "domain": "banemi.fr",
        "slug": "bmqt_banemi_paris",
        "category": "Parisian Modern Banh Mi",
        "category_vn": "Bistro Bánh Mì Phong Cách Pháp — Paris",
        "tag": "europe-au-asia",
        "vibe": "French Bistro Aesthetic • Pastel & Warm Cream • Tinh Tế",
        "location": "Paris, Pháp",
        "desc": "Thương hiệu bánh mì tại Paris mang giao diện thanh lịch kiểu Pháp, sử dụng bảng màu nhẹ nhàng, bố cục tạp chí và ảnh chụp món ăn tinh tế."
    },
    {
        "name": "An Banh Mi — Tiệm Bánh Mì Thủ Công Tại Berlin",
        "short_name": "An Banh Mi Berlin",
        "url": "https://www.anbanhmi.de/",
        "domain": "anbanhmi.de",
        "slug": "bmqt_an_banh_mi_berlin",
        "category": "Artisanal Banh Mi Berlin",
        "category_vn": "Tiệm Bánh Mì Việt Hiện Đại — Berlin, Đức",
        "tag": "europe-au-asia",
        "vibe": "European Minimalist • Clean Menu • Street Craft",
        "location": "Berlin, Đức",
        "desc": "Giao diện website tiệm bánh mì tại Berlin theo phong cách tối giản châu Âu, tập trung vào ảnh thật món ăn, giờ mở cửa và bản đồ cửa hàng."
    },
    {
        "name": "Banh Mi 73 — Quán Bánh Mì & Cà Phê Việt Tại Berlin",
        "short_name": "Banh Mi 73 Berlin",
        "url": "https://www.banhmi73.de/",
        "domain": "banhmi73.de",
        "slug": "bmqt_banhmi_73_berlin",
        "category": "Berlin Urban Banh Mi",
        "category_vn": "Quán Bánh Mì & Trà Sữa/Cà Phê — Berlin",
        "tag": "europe-au-asia",
        "vibe": "Urban Chic • Dark/Light Contrast • Thực Đơn Chi Tiết",
        "location": "Berlin, Đức",
        "desc": "Trang web ẩm thực Việt tại Đức trình bày thực đơn bánh mì, bún và cà phê Việt Nam trực quan, dễ đọc cho thực khách châu Âu."
    },
    {
        "name": "Banh Mi King — Tiệm Bánh Mì Nổi Tiếng Tại Amsterdam",
        "short_name": "Banh Mi King Amsterdam",
        "url": "https://banhmiking.nl/",
        "domain": "banhmiking.nl",
        "slug": "bmqt_banhmi_king_nl",
        "category": "European Street Banh Mi",
        "category_vn": "Tiệm Bánh Mì Đường Phố — Amsterdam, Hà Lan",
        "tag": "europe-au-asia",
        "vibe": "Bold Typography • Bố Cục Mạch Lạc • Giao Hàng Nhanh",
        "location": "Amsterdam, Hà Lan",
        "desc": "Website tiệm bánh mì được du khách và dân bản địa tại Amsterdam yêu thích nhờ giao diện rõ ràng, nút đặt hàng nổi bật và hình ảnh món ăn bắt mắt."
    },
    {
        "name": "Bánh Mì Xin Chào — Thương Hiệu Bánh Mì Việt Hàng Đầu Tại Tokyo",
        "short_name": "Bánh Mì Xin Chào Tokyo",
        "url": "https://banhmixinchao.co.jp/ja",
        "domain": "banhmixinchao.co.jp",
        "slug": "bmqt_xinchao_tokyo",
        "category": "Japanese-Market Vietnamese Banh Mi",
        "category_vn": "Chuỗi Bánh Mì Việt Chuẩn Nhật — Tokyo",
        "tag": "europe-au-asia",
        "vibe": "Japanese Warm Craft • Storytelling Việt-Nhật • Menu Rõ Ràng",
        "location": "Tokyo, Nhật Bản",
        "desc": "Thương hiệu Bánh Mì Xin Chào nổi tiếng tại Nhật Bản với hệ thống nhiều chi nhánh. Giao diện mang nét ấm áp chỉn chu kiểu Nhật kết hợp tinh thần đường phố Việt Nam."
    },
    {
        "name": "Joo Chiat Caphe — Bánh Mì & Cà Phê Phin Phong Cách Hội An Tại Singapore",
        "short_name": "Joo Chiat Caphe",
        "url": "https://joochiatcaphe.com/",
        "domain": "joochiatcaphe.com",
        "slug": "bmqt_joo_chiat_caphe",
        "category": "Heritage Cafe & Banh Mi Singapore",
        "category_vn": "Cafe Cà Phê Phin & Bánh Mì Di Sản — Singapore",
        "tag": "europe-au-asia",
        "vibe": "Heritage Yellow & Teal • Indochine Boutique • Menu Song Ngữ",
        "location": "Joo Chiat, Singapore",
        "desc": "Tiệm bánh mì và cà phê phin nằm giữa khu phố di sản Joo Chiat, Singapore. Website sở hữu bảng màu vàng Hội An thanh lịch, bố cục storytelling rất có gu."
    },
    {
        "name": "The Viet Roti — Bánh Mì Chuẩn Halal & Cà Phê Hiện Đại Tại Singapore",
        "short_name": "The Viet Roti Singapore",
        "url": "https://www.thevietroti.com/",
        "domain": "thevietroti.com",
        "slug": "bmqt_the_viet_roti",
        "category": "Halal-Friendly Modern Banh Mi",
        "category_vn": "Tiệm Bánh Mì Thủ Công & Cà Phê — Singapore",
        "tag": "europe-au-asia",
        "vibe": "Clean Contemporary • Nhấn Mạnh Nguyên Liệu • Pick-up/Delivery",
        "location": "Singapore",
        "desc": "Thương hiệu bánh mì hiện đại phục vụ thực khách đa văn hóa tại Singapore với giao diện sáng sủa, làm nổi bật bánh nướng mới và thực đơn dễ tùy biến."
    },
    {
        "name": "Banh Mi Kitchen — Chuỗi Bánh Mì Hiện Đại Phong Cách Take-Away",
        "short_name": "Banh Mi Kitchen",
        "url": "https://banhmikitchen.ph/",
        "domain": "banhmikitchen.ph",
        "slug": "bmqt_banh_mi_kitchen",
        "category": "Trendy Fast-Casual Banh Mi",
        "category_vn": "Chuỗi Bánh Mì Kiosk & Take-Away Hiện Đại",
        "tag": "europe-au-asia",
        "vibe": "Modern Pop Palette • Graphic Icons • Franchise & Menu",
        "location": "Manila, Philippines",
        "desc": "Mô hình chuỗi bánh mì take-away thiết kế trẻ trung, sử dụng minh họa đồ họa bắt mắt, ảnh chụp cận cảnh và hệ thống đặt hàng/nhượng quyền bài bản."
    },
    {
        "name": "Bánh Mì Kêu — Tiệm Bánh Mì & Món Việt Phong Cách Urban Tại London",
        "short_name": "Bánh Mì Kêu London",
        "url": "https://banhmikeu.co.uk/",
        "domain": "banhmikeu.co.uk",
        "slug": "bmqt_banhmi_keu_london",
        "category": "London Urban Vietnamese Deli",
        "category_vn": "Deli Bánh Mì Việt Nổi Tiếng — Soho & Shoreditch, London",
        "tag": "europe-au-asia",
        "vibe": "London Urban Chic • High-Contrast • Multi-Location Menu",
        "location": "London, Anh",
        "desc": "Thương hiệu bánh mì đình đám tại trung tâm London (Soho, Shoreditch, City). Website tối ưu cho khách quốc tế với điều hướng chi nhánh rõ nét và bố cục mạnh mẽ."
    },
    # --- NHÓM 3: THƯƠNG HIỆU BÁNH MÌ ĐƯƠNG ĐẠI TẠI MỸ & CANADA ---
    {
        "name": "Bun Mee — Chuỗi Bánh Mì Gourmet Nổi Tiếng San Francisco & NYC",
        "short_name": "Bun Mee",
        "url": "https://bunmee.co/",
        "domain": "bunmee.co",
        "slug": "bmqt_bun_mee_sf",
        "category": "Gourmet Vietnamese Sandwich Chain",
        "category_vn": "Chuỗi Bánh Mì Gourmet — San Francisco & New York",
        "tag": "north-america",
        "vibe": "Editorial Food Photography • Brand Storytelling • Order Flow Chuẩn",
        "location": "San Francisco & New York, Mỹ",
        "desc": "Một trong những website tiệm bánh mì đẹp và chỉn chu nhất tại Mỹ: ảnh chụp sản phẩm chuẩn tạp chí, phối màu hiện đại, tách bạch rõ phần đặt món và câu chuyện thương hiệu."
    },
    {
        "name": "Bánh NYC — Quán Ăn Việt & Bánh Mì Phong Cách Boutique Tại New York",
        "short_name": "Bánh NYC",
        "url": "https://www.banhny.com/",
        "domain": "banhny.com",
        "slug": "bmqt_banh_nyc",
        "category": "NYC Boutique Vietnamese Eatery",
        "category_vn": "Quán Ăn Việt & Bánh Mì Boutique — Upper West Side, NYC",
        "tag": "north-america",
        "vibe": "Warm Editorial • Typography Đẹp • Đặt Bàn & Thực Đơn Rõ",
        "location": "New York City, Mỹ",
        "desc": "Nhà hàng Việt hiện đại được giới thiệu trên nhiều tạp chí ẩm thực New York. Trang web mang cảm giác ấm cúng, bố cục rõ ràng từ câu chuyện bếp trưởng đến thực đơn bánh mì."
    },
    {
        "name": "Bánh Anh Em — Tiệm Bánh Mì Lò Than & Bánh Tươi Tại Seattle",
        "short_name": "Bánh Anh Em",
        "url": "https://www.banhanhem.com/",
        "domain": "banhanhem.com",
        "slug": "bmqt_banh_anh_em",
        "category": "Craft Charcoal Banh Mi Seattle",
        "category_vn": "Tiệm Bánh Mì Nướng Than & Bánh Tươi — Seattle",
        "tag": "north-america",
        "vibe": "Craft Bakery • Dark/Warm Aesthetic • Menu Nguyên Liệu Thủ Công",
        "location": "Seattle, Mỹ",
        "desc": "Thương hiệu bánh mì thủ công tại Seattle tự nướng vỏ bánh mỗi sáng và nướng thịt bằng than hoa. Website gây thiện cảm bởi bố cục tinh gọn và mô tả món ăn đầy hấp dẫn."
    },
    {
        "name": "Num Pang Kitchen — Thương Hiệu Bánh Mì & Sandwich Đông Nam Á Tại NYC",
        "short_name": "Num Pang NYC",
        "url": "https://www.eatnumpang.com/",
        "domain": "eatnumpang.com",
        "slug": "bmqt_num_pang_nyc",
        "category": "Iconic NYC Sandwich Brand",
        "category_vn": "Chuỗi Bánh Mì Kẹp Đông Nam Á Đình Đám — New York",
        "tag": "north-america",
        "vibe": "Bold Fast-Casual • Color Contrast • Catering & Delivery",
        "location": "New York City, Mỹ",
        "desc": "Thương hiệu bánh mì lấy cảm hứng từ ẩm thực Đông Dương rất thành công tại Manhattan. Giao diện mạnh mẽ, hình ảnh bắt mắt và phễu đặt hàng doanh nghiệp chuyên nghiệp."
    },
    {
        "name": "Paris Banh Mi Cafe Bakery — Chuỗi Tiệm Bánh Ngọt & Bánh Mì Pháp-Việt Tại Mỹ",
        "short_name": "Paris Banh Mi USA",
        "url": "https://www.parisbanhmi.com/",
        "domain": "parisbanhmi.com",
        "slug": "bmqt_paris_banh_mi_usa",
        "category": "French-Vietnamese Bakery Chain",
        "category_vn": "Chuỗi Tiệm Bánh Mì & Trà Sữa Pháp-Việt — Toàn Quốc Mỹ",
        "tag": "north-america",
        "vibe": "Luxury Bakery • Gold & Cream • Franchise & Menu Showcase",
        "location": "Nhiều bang tại Mỹ",
        "desc": "Chuỗi cửa hàng bánh mì kết hợp bakery kiểu Pháp phát triển nhanh tại Mỹ. Website nổi bật với phong cách sang trọng, hình ảnh bánh mì và bánh ngọt được trưng bày bài bản."
    },
    {
        "name": "Banh Mi & Ti — Tiệm Bánh Mì Việt Hiện Đại Tại Mỹ",
        "short_name": "Banh Mi & Ti",
        "url": "https://www.banhmiandti.com/",
        "domain": "banhmiandti.com",
        "slug": "bmqt_banh_mi_and_ti",
        "category": "Modern Vietnamese Sandwich & Tea",
        "category_vn": "Tiệm Bánh Mì & Trà Việt Đương Đại — Mỹ",
        "tag": "north-america",
        "vibe": "Clean Minimalist • Fresh Green Accent • Order Online",
        "location": "Mỹ",
        "desc": "Website thiết kế gọn nhẹ, hiện đại với điểm nhấn màu xanh lá tươi mát, trình bày danh sách bánh mì và thức uống rõ ràng cho thực khách bản xứ."
    },
    {
        "name": "Banh Mi Boys — Thương Hiệu Bánh Mì & Bao Biểu Tượng Tại Toronto",
        "short_name": "Banh Mi Boys Toronto",
        "url": "https://banhmiboys.com/",
        "domain": "banhmiboys.com",
        "slug": "bmqt_banh_mi_boys",
        "category": "Iconic Toronto Street Food",
        "category_vn": "Tiệm Bánh Mì & Bao Phong Cách Streetwear — Toronto",
        "tag": "north-america",
        "vibe": "Streetwear Bold • High Energy • Cult Brand",
        "location": "Toronto, Canada",
        "desc": "Thương hiệu bánh mì đình đám bậc nhất Canada với phong cách trẻ trung, cá tính, giao diện đậm chất đường phố hiện đại."
    },
    {
        "name": "Mr. Banh Mi — Tiệm Bánh Mì Vỏ Giòn Sài Gòn Tại Brooklyn, NYC",
        "short_name": "Mr. Banh Mi NYC",
        "url": "https://mrbanhminyc.com/",
        "domain": "mrbanhminyc.com",
        "slug": "bmqt_mr_banh_mi_nyc",
        "category": "Brooklyn Craft Banh Mi",
        "category_vn": "Tiệm Bánh Mì Tự Nướng Công Thức Sài Gòn — Brooklyn",
        "tag": "north-america",
        "vibe": "Crisp Bakery • Clean Sections • Pickup Brooklyn",
        "location": "Brooklyn, New York",
        "desc": "Tiệm bánh mì được yêu thích tại Brooklyn nhờ tự nướng baguette theo công thức Sài Gòn, trang web sáng sủa, trực diện và dễ đặt món."
    },
    {
        "name": "Ba Le Sandwiches — Thương Hiệu Bánh Mì Huyền Thoại Tại Chicago",
        "short_name": "Ba Le Chicago",
        "url": "https://www.balesandwich.com/",
        "domain": "balesandwich.com",
        "slug": "bmqt_bale_chicago",
        "category": "Historic Artisan Banh Mi Chicago",
        "category_vn": "Tiệm Bánh Mì Lịch Sử Phố Argyle — Chicago",
        "tag": "north-america",
        "vibe": "Heritage Craft • Authentic Story • Bakery & Deli",
        "location": "Chicago, Mỹ",
        "desc": "Biểu tượng bánh mì Việt tại Chicago nổi tiếng với ổ bánh tự nướng vỏ giòn tan, trang web truyền tải trọn vẹn câu chuyện di sản và thực đơn truyền thống."
    },
    {
        "name": "Bánh Mì Ông Mười — Tiệm Bánh Mì Tươi Mỗi Sáng Tại Chicago",
        "short_name": "Bánh Mì Ông Mười",
        "url": "https://banhmiongmuoi.com/",
        "domain": "banhmiongmuoi.com",
        "slug": "bmqt_ong_muoi_chicago",
        "category": "Fresh Morning Bake Banh Mi",
        "category_vn": "Tiệm Bánh Mì Nướng Sáng — Chicago",
        "tag": "north-america",
        "vibe": "Warm Neighborhood • Clean Visuals • Takeout Ready",
        "location": "Chicago, Mỹ",
        "desc": "Tiệm bánh mì hướng tới khách bản địa Mỹ với điểm nhấn rau đồ chua đóng gói riêng giữ độ giòn, giao diện đơn giản thân thiện."
    },
    {
        "name": "Lotus Banh Mi — Chuỗi Quán Bánh Mì & Phở Hiện Đại Tại Chicago",
        "short_name": "Lotus Banh Mi",
        "url": "https://lotusbanhmi.com/",
        "domain": "lotusbanhmi.com",
        "slug": "bmqt_lotus_banhmi",
        "category": "Modern Vietnamese Cafe Chicago",
        "category_vn": "Chuỗi Bánh Mì, Phở & Cơm Việt — Chicago",
        "tag": "north-america",
        "vibe": "Clean Card Grid • Multi-Location • Online Ordering",
        "location": "Chicago, Mỹ",
        "desc": "Website chuẩn mực cho tiệm ăn Việt đa món tại Mỹ với bố cục thẻ menu rõ ràng, hỗ trợ khách nước ngoài chọn món và đặt hàng nhanh."
    },
    {
        "name": "The Best Baguette — Tiệm Bánh Mì Việt Phong Cách Pháp Tại Portland",
        "short_name": "The Best Baguette",
        "url": "https://www.thebestbaguette.com/",
        "domain": "thebestbaguette.com",
        "slug": "bmqt_best_baguette",
        "category": "Portland Artisan Banh Mi",
        "category_vn": "Tiệm Bánh Mì Baguette Thủ Công — Portland",
        "tag": "north-america",
        "vibe": "Warm Bakery • Clean Menu • Pacific Northwest Vibe",
        "location": "Portland, Oregon, Mỹ",
        "desc": "Tiệm bánh mì nổi tiếng tại Portland kết hợp kỹ thuật làm bánh mì Pháp với nhân Việt truyền thống, trang web thân thiện và dễ duyệt thực đơn."
    }
]

print(f"=== CHỤP & KIỂM ĐỊNH POOL {len(pool)} WEBSITE TIỆM BÁNH MÌ QUỐC TẾ ===")
passed_list = []
results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for idx, site in enumerate(pool, 1):
        site["industry"] = "banh-mi-quoc-te"
        site["industry_name"] = "Tiệm Bánh Mì Cho Người Nước Ngoài"

        print(f"\n[Pool {idx:02d}/{len(pool)}] {site['name']} ({site['url']})...")
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
                    'button:has-text("Accept")', 'button:has-text("Agree")',
                    'button:has-text("Close")', 'button:has-text("Got it")',
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
                page.goto(site['url'], timeout=50000, wait_until="networkidle")
                time.sleep(4.0)
                page.evaluate("""() => {
                    document.querySelectorAll('[id*="cookie" i], [class*="cookie" i], [id*="consent" i], [class*="consent" i], [class*="onetrust" i], [id*="onetrust" i], .modal-backdrop, .popup-overlay, [role="dialog"]').forEach(el => {
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

print(f"\n=== TỔNG KẾT QA: ĐẠT {len(passed_list)}/{len(pool)} MẪU ===")
for r in results:
    print(f"  {r[0]:28s} | {r[1]:28s} | {r[2]:9s} | {r[3]}")
