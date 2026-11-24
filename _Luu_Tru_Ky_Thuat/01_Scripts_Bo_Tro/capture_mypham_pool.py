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
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "mypham_pool_audit.json")

os.makedirs(output_dir, exist_ok=True)
os.makedirs(kho_webp_dir, exist_ok=True)

pool = [
    # --- NHÓM 1: THƯƠNG HIỆU MỸ PHẨM & CHUỖI SKINCARE VIỆT NAM (9) ---
    {
        "name": "Cocoon Vietnam — Mỹ Phẩm Thuần Chay Việt Nam Chuẩn UI/UX Đỉnh Cao",
        "short_name": "Cocoon Vietnam",
        "url": "https://cocoonvietnam.com/",
        "domain": "cocoonvietnam.com",
        "slug": "mp_cocoon",
        "category": "Local Vegan Skincare Brand",
        "category_vn": "Cocoon — Mỹ Phẩm Thuần Chay Việt Nam Phong Cách Tối Giản Sang Trọng",
        "tag": "my-pham-vn",
        "vibe": "Vietnamese Editorial • Tông Kem Nâu Đẹp • Storytelling Đỉnh",
        "location": "TP.HCM & Toàn Quốc",
        "desc": "Hình mẫu đẹp nhất trong các thương hiệu mỹ phẩm Việt Nam: tông màu đất-kem ấm áp, kể chuyện nguyên liệu thiên nhiên (bí đao, cà phê Đắk Lắk) đầy cảm xúc và trải nghiệm mua hàng cực mượt."
    },
    {
        "name": "Cỏ Mềm HomeLab — Mỹ Phẩm Thiên Nhiên Lành & Thật Việt Nam",
        "short_name": "Cỏ Mềm HomeLab",
        "url": "https://comem.vn/",
        "domain": "comem.vn",
        "slug": "mp_comem",
        "category": "Natural Cosmetics D2C VN",
        "category_vn": "Cỏ Mềm — Thương Hiệu Mỹ Phẩm Thiên Nhiên D2C & Bán Lẻ Mạnh",
        "tag": "my-pham-vn",
        "vibe": "Botanical Green • E-Commerce D2C • Combo & Quà Tặng Rõ",
        "location": "Hà Nội & Toàn Quốc",
        "desc": "Website D2C mỹ phẩm thiên nhiên rất thành công tại Việt Nam: tông xanh lá dịu mắt, hiển thị rõ sản phẩm bán chạy, combo tiết kiệm và nút thêm giỏ hàng trực tiếp."
    },
    {
        "name": "Hasaki.vn — Siêu Thị Mỹ Phẩm Chính Hãng & Bán Lẻ Lớn Nhất VN",
        "short_name": "Hasaki Beauty",
        "url": "https://hasaki.vn/",
        "domain": "hasaki.vn",
        "slug": "mp_hasaki",
        "category": "Mega Beauty Retail E-Commerce",
        "category_vn": "Hasaki — Chuỗi Bán Lẻ Mỹ Phẩm & Flash Sale Quy Mô Lớn",
        "tag": "my-pham-vn",
        "vibe": "High-Volume E-Com • Flash Deals • Tìm Kiếm Đa Thương Hiệu",
        "location": "TP.HCM, Hà Nội & Toàn Quốc",
        "desc": "Chuẩn mực giao diện siêu thị bán lẻ mỹ phẩm quy mô lớn: phân loại cực chi tiết theo thương hiệu, vấn đề da, Flash Sale đếm ngược và giao hàng nhanh 2H."
    },
    {
        "name": "Beauty Box — Chuỗi Bán Lẻ Mỹ Phẩm Hàn Quốc & Quốc Tế Hiện Đại",
        "short_name": "Beauty Box",
        "url": "https://beautybox.com.vn/",
        "domain": "beautybox.com.vn",
        "slug": "mp_beautybox",
        "category": "Modern Multi-Brand Beauty Store",
        "category_vn": "Beauty Box — Cửa Hàng Mỹ Phẩm Đa Thương Hiệu UI Sạch Trẻ Trung",
        "tag": "my-pham-vn",
        "vibe": "Clean Retail UI • Thẻ Sản Phẩm Đẹp • Bộ Lọc Trực Quan",
        "location": "TP.HCM & Hà Nội",
        "desc": "Website bán lẻ mỹ phẩm đa thương hiệu có thiết kế sạch sẽ, hiện đại hơn các sàn rao bán truyền thống, làm nổi bật sản phẩm mới, đánh giá sao và ưu đãi thành viên."
    },
    {
        "name": "Lemonade Cosmetics — Thương Hiệu Trang Điểm Hiện Đại Việt Nam",
        "short_name": "Lemonade Cosmetics",
        "url": "https://www.lemonade.vn/",
        "domain": "lemonade.vn",
        "slug": "mp_lemonade",
        "category": "Local Makeup D2C Brand",
        "category_vn": "Lemonade — Mỹ Phẩm Trang Điểm Cho Phụ Nữ Việt Chuẩn D2C",
        "tag": "my-pham-vn",
        "vibe": "Youthful Makeup D2C • Bảng Màu Son/Phấn • Ảnh Lookbook Sắc Nét",
        "location": "TP. Hồ Chí Minh",
        "desc": "Mẫu web thương hiệu trang điểm nội địa trẻ trung: ảnh sản phẩm sắc nét, chọn nhanh bảng màu son/cushion ngay trên thẻ và tối ưu đặt mua nhanh trên di động."
    },
    {
        "name": "Ofélia Cosmetics — Thương Hiệu Mỹ Phẩm Trẻ Trung Phong Cách Gen Z",
        "short_name": "Ofélia Cosmetics",
        "url": "https://ofelia.vn/",
        "domain": "ofelia.vn",
        "slug": "mp_ofelia",
        "category": "Trendy Indie Beauty Brand",
        "category_vn": "Ofélia — Mỹ Phẩm Trang Điểm Cá Tính & Lookbook Hiện Đại",
        "tag": "my-pham-vn",
        "vibe": "Indie Beauty Chic • Bộ Sưu Tập Bắt Mắt • E-Com Tối Giản",
        "location": "TP. Hồ Chí Minh",
        "desc": "Giao diện mỹ phẩm indie Việt Nam rất có gu, lấy hình ảnh bộ sưu tập và swatch màu làm trung tâm giúp khách hàng dễ bị thu hút ngay khi vào trang."
    },
    {
        "name": "Paula's Choice Việt Nam — Dược Mỹ Phẩm Khoa Học & Tư Vấn Làn Da",
        "short_name": "Paula's Choice VN",
        "url": "https://paulaschoice.vn/",
        "domain": "paulaschoice.vn",
        "slug": "mp_paulaschoicevn",
        "category": "Clinical Skincare E-Commerce",
        "category_vn": "Paula's Choice — Dược Mỹ Phẩm Chuyên Sâu Theo Hoạt Chất & Vấn Đề Da",
        "tag": "my-pham-vn",
        "vibe": "Science-Backed Skincare • Phân Loại Hoạt Chất • Bán Lẻ Chuẩn CRO",
        "location": "Hà Nội & TP.HCM",
        "desc": "Hình mẫu chuẩn cho website dược mỹ phẩm: phân loại rõ theo hoạt chất (BHA, Retinol, Niacinamide) và tình trạng da (mụn, lão hóa) kèm bảng giá minh bạch."
    },
    {
        "name": "La Roche-Posay Việt Nam — Dược Mỹ Phẩm Chăm Sóc Da Nhạy Cảm",
        "short_name": "La Roche-Posay VN",
        "url": "https://www.larocheposay.vn/",
        "domain": "larocheposay.vn",
        "slug": "mp_larocheposayvn",
        "category": "Dermatological Skincare Brand",
        "category_vn": "La Roche-Posay — Dược Mỹ Phẩm Chuẩn Bác Sĩ Da Liễu Khuyên Dùng",
        "tag": "my-pham-vn",
        "vibe": "Clean Clinical Blue • Niềm Tin Da Liễu • Tư Vấn Chu Trình Da",
        "location": "Toàn Quốc (VN)",
        "desc": "Website dược mỹ phẩm quốc tế tại Việt Nam với tông trắng-xanh y khoa cực kỳ sạch sẽ, dẫn dắt người dùng tìm đúng dòng sản phẩm cho da mụn và da nhạy cảm."
    },
    {
        "name": "Innisfree Việt Nam — Mỹ Phẩm Thiên Nhiên Đảo Jeju Chính Hãng",
        "short_name": "Innisfree VN",
        "url": "https://www.innisfree.vn/",
        "domain": "innisfree.vn",
        "slug": "mp_innisfreevn",
        "category": "K-Beauty Natural Skincare",
        "category_vn": "Innisfree — Thương Hiệu Skincare Thiên Nhiên Hàn Quốc Sạch Mát",
        "tag": "my-pham-vn",
        "vibe": "Fresh K-Beauty • Tông Xanh Tự Nhiên • Lưới Sản Phẩm Thoáng",
        "location": "Toàn Quốc (VN)",
        "desc": "Giao diện K-Beauty tươi mới, tinh gọn sau đợt tái định vị thương hiệu, tập trung hình ảnh sản phẩm cận cảnh và trải nghiệm mua sắm dễ chịu."
    },

    # --- NHÓM 2: THỰC PHẨM CHỨC NĂNG, VITAMIN & CHĂM SÓC SỨC KHỎE VIỆT NAM (7) ---
    {
        "name": "DHC Việt Nam — Thực Phẩm Chức Năng & Viên Uống Làm Đẹp Nhật Bản",
        "short_name": "DHC Việt Nam",
        "url": "https://dhcvietnam.com.vn/",
        "domain": "dhcvietnam.com.vn",
        "slug": "mp_dhcvietnam",
        "category": "Japanese Beauty Supplements",
        "category_vn": "DHC Việt Nam — Viên Uống Vitamin, Collagen & Bán Lẻ TPCN Nhật",
        "tag": "tpcn-suc-khoe-vn",
        "vibe": "Clean Japanese E-Com • Vitamin & Collagen • Phễu Chốt Đơn Mạnh",
        "location": "Hà Nội, TP.HCM & Toàn Quốc",
        "desc": "Hình mẫu bán lẻ Thực phẩm chức năng cực kỳ hiệu quả tại Việt Nam: phân nhóm rõ viên uống trắng da, vitamin C, rau củ, collagen với giá niêm yết và combo ưu đãi hấp dẫn."
    },
    {
        "name": "Doppelherz Việt Nam — Thực Phẩm Bảo Vệ Sức Khỏe Số 1 Tại Đức",
        "short_name": "Doppelherz VN",
        "url": "https://doppelherz.vn/",
        "domain": "doppelherz.vn",
        "slug": "mp_doppelherz",
        "category": "German Vitamins & Supplements",
        "category_vn": "Doppelherz — TPCN Chuẩn Đức Theo Độ Tuổi & Nhóm Sức Khỏe",
        "tag": "tpcn-suc-khoe-vn",
        "vibe": "Trust German Pharma • Phân Loại Nhu Cầu • Uy Tín Khoa Học",
        "location": "Toàn Quốc (VN)",
        "desc": "Website thực phẩm bảo vệ sức khỏe chuẩn châu Âu, tổ chức sản phẩm rất thông minh theo từng đối tượng (trẻ em, phụ nữ, tim mạch, xương khớp) và chứng nhận chất lượng Đức."
    },
    {
        "name": "Blackmores Việt Nam — Vitamin & Thực Phẩm Chức Năng Hàng Đầu Úc",
        "short_name": "Blackmores VN",
        "url": "https://www.blackmores.com.vn/",
        "domain": "blackmores.com.vn",
        "slug": "mp_blackmoresvn",
        "category": "Australian Health Supplements",
        "category_vn": "Blackmores — Thương Hiệu Vitamin & Dinh Dưỡng Tự Nhiên Chuẩn Úc",
        "tag": "tpcn-suc-khoe-vn",
        "vibe": "Natural Wellness • Tông Xanh Tươi • Tư Vấn Vitamin Minh Bạch",
        "location": "Toàn Quốc (VN)",
        "desc": "Giao diện sáng sủa, giàu sức sống của hãng thực phẩm chức năng số 1 nước Úc, cân bằng giữa giới thiệu sản phẩm vitamin/dầu cá và kiến thức chăm sóc sức khỏe chủ động."
    },
    {
        "name": "Hector — Nước Uống Đông Trùng Hạ Thảo & Collagen Việt Nam",
        "short_name": "Hector Wellness",
        "url": "https://dongtrunghathaohector.com/",
        "domain": "dongtrunghathaohector.com",
        "slug": "mp_hector",
        "category": "Local Functional Drink & Health",
        "category_vn": "Hector — Thực Phẩm Bảo Vệ Sức Khỏe Đông Trùng Hạ Thảo D2C",
        "tag": "tpcn-suc-khoe-vn",
        "vibe": "Modern Local Health • Quà Tặng Sức Khỏe • Bố Cục Sang Gọn",
        "location": "TP.HCM & Toàn Quốc",
        "desc": "Mẫu website cực hay cho các doanh nghiệp Việt làm thực phẩm bảo vệ sức khỏe (đông trùng hạ thảo, nước uống collagen, yến sào): hiện đại, sang trọng và tối ưu mua làm quà biếu."
    },
    {
        "name": "Pharmacity — Hệ Thống Bán Lẻ Thực Phẩm Chức Năng & Dược Mỹ Phẩm",
        "short_name": "Pharmacity",
        "url": "https://www.pharmacity.vn/",
        "domain": "pharmacity.vn",
        "slug": "mp_pharmacity",
        "category": "Health & Supplement Retail Chain",
        "category_vn": "Pharmacity — Sàn TMĐT Thực Phẩm Chức Năng, Vitamin & Chăm Sóc Cá Nhân",
        "tag": "tpcn-suc-khoe-vn",
        "vibe": "Modern Pharma E-Com • Lọc Nhóm Bệnh/Vitamin • Giao Nhanh",
        "location": "Toàn Quốc (VN)",
        "desc": "Giao diện thương mại điện tử dược phẩm & thực phẩm chức năng rất mượt và thân thiện, dễ tìm kiếm theo công dụng vitamin, chăm sóc sắc đẹp và tư vấn dược sĩ trực tuyến."
    },
    {
        "name": "Nhà Thuốc Long Châu — Hệ Thống Bán Lẻ TPCN & Dược Phẩm Số 1 VN",
        "short_name": "Long Châu FPT",
        "url": "https://nhathuoclongchau.com.vn/",
        "domain": "nhathuoclongchau.com.vn",
        "slug": "mp_longchau",
        "category": "Top 1 Pharma & Supplement E-Com",
        "category_vn": "Long Châu — Chuỗi Bán Lẻ TPCN & Dược Mỹ Phẩm Tối Ưu Chuyển Đổi",
        "tag": "tpcn-suc-khoe-vn",
        "vibe": "High-Conversion Pharma • Danh Mục Thông Minh • Giá Niêm Yết Rõ",
        "location": "Toàn Quốc (VN)",
        "desc": "Chuẩn mực hàng đầu về TMĐT ngành sức khỏe tại Việt Nam: thanh tìm kiếm siêu nhanh, phân tầng rõ thực phẩm chức năng, dược mỹ phẩm, thiết bị y tế và giá bán minh bạch."
    },
    {
        "name": "WheyStore — Thực Phẩm Bổ Sung Thể Hình, Protein & Vitamin",
        "short_name": "WheyStore",
        "url": "https://www.wheystore.vn/",
        "domain": "wheystore.vn",
        "slug": "mp_wheystore",
        "category": "Sports Nutrition & Supplements",
        "category_vn": "WheyStore — Web Bán Thực Phẩm Bổ Sung, Whey & Vitamin Tối Ưu SEO",
        "tag": "tpcn-suc-khoe-vn",
        "vibe": "Sports Supplement E-Com • Bảng Giá & Combo • Chốt Đơn Nhanh",
        "location": "Hà Nội, TP.HCM & Đà Nẵng",
        "desc": "Mẫu web bán lẻ thực phẩm bổ sung thể thao và vitamin rất thực chiến với bộ lọc theo mục tiêu (tăng cơ, giảm mỡ, vitamin tổng hợp), giá rõ ràng và khuyến mãi nổi bật."
    },

    # --- NHÓM 3: D2C MỸ PHẨM & THỰC PHẨM CHỨC NĂNG QUỐC TẾ CHUẨN UI/UX (10) ---
    {
        "name": "Rhode Skin — Biểu Tượng Tối Giản Mỹ Phẩm D2C Của Hailey Bieber",
        "short_name": "Rhode Skin",
        "url": "https://www.rhodeskin.com/",
        "domain": "rhodeskin.com",
        "slug": "mp_rhodeskin",
        "category": "Minimalist Luxury Skincare D2C",
        "category_vn": "Rhode Skin (Mỹ) — Đỉnh Cao Tối Giản Mỹ Phẩm D2C & Cảm Xúc Hình Ảnh",
        "tag": "quoc-te-d2c",
        "vibe": "Ultra-Minimal Editorial • Ảnh Texture Da Đỉnh • Tập Trung Ít SKU",
        "location": "Los Angeles, Mỹ",
        "desc": "Một trong những website mỹ phẩm được săn đón và học hỏi thiết kế nhiều nhất thế giới: bảng màu trung tính tinh khiết, ít sản phẩm nhưng mỗi sản phẩm đều được trình bày như tác phẩm nghệ thuật."
    },
    {
        "name": "Glossier — Huyền Thoại UI/UX Thương Hiệu Mỹ Phẩm D2C Toàn Cầu",
        "short_name": "Glossier",
        "url": "https://www.glossier.com/",
        "domain": "glossier.com",
        "slug": "mp_glossier",
        "category": "Iconic D2C Beauty Brand",
        "category_vn": "Glossier (Mỹ) — Chuẩn Mực UI/UX Mỹ Phẩm D2C & Mua Nhanh 1 Chạm",
        "tag": "quoc-te-d2c",
        "vibe": "Iconic Clean D2C • Quick-Add Swatch • Phong Cách Tự Nhiên",
        "location": "New York, Mỹ",
        "desc": "Tượng đài thiết kế web mỹ phẩm D2C: bố cục tinh sạch, cho phép chọn tông màu và thêm ngay vào giỏ hàng từ trang chủ mà không cần chuyển nhiều bước."
    },
    {
        "name": "Summer Fridays — Skincare & Dưỡng Môi D2C Phong Cách California",
        "short_name": "Summer Fridays",
        "url": "https://summerfridays.com/",
        "domain": "summerfridays.com",
        "slug": "mp_summerfridays",
        "category": "Warm Aesthetic Skincare D2C",
        "category_vn": "Summer Fridays (Mỹ) — Skincare Tông Kem Ấm & Trải Nghiệm Mua Hàng Mượt",
        "tag": "quoc-te-d2c",
        "vibe": "Warm Pastel Chic • Lưới Sản Phẩm Sạch • Best-Seller Nổi Bật",
        "location": "California, Mỹ",
        "desc": "Giao diện skincare mang sắc thái ấm áp, dễ chịu như nắng chiều California, làm nổi bật sản phẩm bán chạy, kết cấu chất kem và đánh giá thực tế từ khách hàng."
    },
    {
        "name": "The Ordinary — Dược Mỹ Phẩm Tối Giản Khoa Học & Minh Bạch Hoạt Chất",
        "short_name": "The Ordinary",
        "url": "https://theordinary.com/en-us",
        "domain": "theordinary.com",
        "slug": "mp_theordinary",
        "category": "Clinical Minimalist Skincare",
        "category_vn": "The Ordinary (Canada) — Tối Giản Đen-Trắng Chuẩn Phòng Lab",
        "tag": "quoc-te-d2c",
        "vibe": "Lab Minimalism • Đen-Trắng Sắc Nét • Xây Dựng Chu Trình Da",
        "location": "Toronto, Canada & Toàn Cầu",
        "desc": "Hình mẫu hoàn hảo cho dòng mỹ phẩm tập trung vào thành phần khoa học: giao diện trắng-đen chuẩn phòng thí nghiệm, loại bỏ mọi chi tiết rườm rà để tập trung vào công thức và giá."
    },
    {
        "name": "Rare Beauty — Thương Hiệu Mỹ Phẩm Hiện Đại & Nhân Văn Của Selena Gomez",
        "short_name": "Rare Beauty",
        "url": "https://www.rarebeauty.com/",
        "domain": "rarebeauty.com",
        "slug": "mp_rarebeauty",
        "category": "Modern Inclusive Makeup D2C",
        "category_vn": "Rare Beauty (Mỹ) — Mỹ Phẩm Trang Điểm Hiện Đại & Ảnh Đa Sắc Da",
        "tag": "quoc-te-d2c",
        "vibe": "Editorial Warmth • Trình Bày Tông Màu Mượt • Câu Chuyện Thương Hiệu",
        "location": "California, Mỹ",
        "desc": "Website mỹ phẩm có tỷ lệ chuyển đổi cực cao nhờ hình ảnh chân thực trên nhiều tông da, lưới sản phẩm gọn đẹp và cách lồng ghép câu chuyện thương hiệu đầy cảm hứng."
    },
    {
        "name": "Glow Recipe — Skincare Chiết Xuất Trái Cây Tươi Trẻ & Bắt Mắt",
        "short_name": "Glow Recipe",
        "url": "https://www.glowrecipe.com/",
        "domain": "glowrecipe.com",
        "slug": "mp_glowrecipe",
        "category": "Fruit-Forward Skincare D2C",
        "category_vn": "Glow Recipe (Mỹ) — Skincare Màu Sắc Tươi Mát & Bắt Mắt Giới Trẻ",
        "tag": "quoc-te-d2c",
        "vibe": "Vibrant Pastel • Ảnh Trái Cây & Chất Kem • Quiz Chọn Sản Phẩm",
        "location": "New York, Mỹ",
        "desc": "Mẫu thiết kế xuất sắc cho các thương hiệu mỹ phẩm hướng tới giới trẻ thích màu sắc pastel tươi tắn, hình ảnh nguyên liệu trái cây sống động và công cụ chọn chu trình dưỡng da."
    },
    {
        "name": "Seed — Đỉnh Cao UI/UX Thực Phẩm Chức Năng & Men Vi Sinh Khoa Học",
        "short_name": "Seed Health",
        "url": "https://seed.com/",
        "domain": "seed.com",
        "slug": "mp_seed",
        "category": "Science-First Probiotic D2C",
        "category_vn": "Seed (Mỹ) — Đỉnh Cao Thiết Kế Web Thực Phẩm Chức Năng Khoa Học",
        "tag": "quoc-te-d2c",
        "vibe": "Design Award Winner • Xanh Rêu Sang Trọng • Khoa Học Minh Bạch",
        "location": "Los Angeles, Mỹ",
        "desc": "Được xem là một trong những website thực phẩm chức năng đẹp nhất lịch sử thiết kế web: tông xanh rêu quyền lực, minh họa khoa học trực quan và mô hình bán theo gói định kỳ cực thuyết phục."
    },
    {
        "name": "Ritual — Thương Hiệu Vitamin & TPCN Minh Bạch Thành Phần Hàng Đầu Mỹ",
        "short_name": "Ritual Vitamins",
        "url": "https://ritual.com/",
        "domain": "ritual.com",
        "slug": "mp_ritual",
        "category": "Traceable Vitamins Subscription",
        "category_vn": "Ritual (Mỹ) — Chuẩn Mực UX Bán Vitamin & Truy Xuất Nguồn Gốc",
        "tag": "quoc-te-d2c",
        "vibe": "Yellow-Navy Signature • Minh Bạch Thành Phần • Subscription UX",
        "location": "Los Angeles, Mỹ",
        "desc": "Hình mẫu chuẩn mực nhất cho website bán viên uống Vitamin & TPCN hiện đại: dùng hình ảnh viên nang trong suốt, giải thích rõ nguồn gốc từng dưỡng chất và phân loại theo nhóm tuổi/giới tính."
    },
    {
        "name": "AG1 (Athletic Greens) — Siêu Phẩm Landing Page Bán 1 Sản Phẩm TPCN",
        "short_name": "AG1 Nutrition",
        "url": "https://drinkag1.com/",
        "domain": "drinkag1.com",
        "slug": "mp_drinkag1",
        "category": "Single-Product Supplement Funnel",
        "category_vn": "AG1 (Mỹ) — Mẫu Mực Chốt Đơn 1 Sản Phẩm Thực Phẩm Bổ Sung Toàn Cầu",
        "tag": "quoc-te-d2c",
        "vibe": "1-Product CRO King • Xanh Đậm Uy Tín • Bằng Chứng Lâm Sàng",
        "location": "Mỹ & Toàn Cầu",
        "desc": "Case study vĩ đại nhất thế giới về website bán 1 sản phẩm thực phẩm bổ sung (Single-SKU): dẫn dắt chặt chẽ từ lợi ích 75 dưỡng chất, kiểm nghiệm lâm sàng đến gói đăng ký định kỳ."
    },
    {
        "name": "HUM Nutrition — Thực Phẩm Chức Năng Làm Đẹp Da Tóc & Quiz Cá Nhân Hóa",
        "short_name": "HUM Nutrition",
        "url": "https://www.humnutrition.com/",
        "domain": "humnutrition.com",
        "slug": "mp_humnutrition",
        "category": "Beauty-From-Within Supplements",
        "category_vn": "HUM Nutrition (Mỹ) — TPCN Làm Đẹp Da/Tóc/Dáng & Phễu Quiz Chọn Gói",
        "tag": "quoc-te-d2c",
        "vibe": "Bright Modern Wellness • Quiz Cá Nhân Hóa • Gợi Ý Combo Đẹp Da",
        "location": "Los Angeles, Mỹ",
        "desc": "Giao diện rực rỡ, hiện đại dành riêng cho mảng thực phẩm chức năng làm đẹp từ bên trong (da, tóc, vóc dáng) với điểm nhấn là bài Quiz 3 phút gợi ý đúng hộp vitamin."
    },
]

results = []
passed_list = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for idx, site in enumerate(pool, 1):
        site["id"] = f"mp{idx:02d}"
        site["industry"] = "my-pham-tpcn"
        site["industry_name"] = "Mỹ Phẩm & Thực Phẩm Chức Năng"
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
                    '.klaviyo-close-form', '[aria-label="Close dialog"]',
                    'button[data-testid="close-button"]', '.needsclick[aria-label*="Close" i]'
                ];
                selectors.forEach(sel => {
                    try { document.querySelectorAll(sel).forEach(btn => { try { btn.click(); } catch(e) {} }); } catch(e) {}
                });
                // Remove Shadow DOM chat/marketing widgets (Klaviyo, Attentive, Gorgias, etc.)
                document.querySelectorAll('*').forEach(el => {
                    if (el.shadowRoot) {
                        const tag = (el.tagName || '').toLowerCase();
                        const id = (el.id || '').toLowerCase();
                        if (tag.includes('chat') || tag.includes('bot') || tag.includes('intercom') || tag.includes('widget') || id.includes('chat') || tag.includes('attentive') || tag.includes('gorgias')) {
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
                        '[id*="klaviyo" i], [class*="klaviyo" i], [id*="attentive" i], ' +
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

print(f"\n=== TỔNG KẾT QA NGÁCH 10 (MỸ PHẨM & THỰC PHẨM CHỨC NĂNG): ĐẠT {len(passed_list)}/{len(pool)} MẪU ===")
for r in results:
    print(f"  {r[0]:20s} | {r[1]:28s} | {r[2]:9s} | {r[3]}")
