import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

candidates = [
    # NHÓM 1: LUXURY & SIÊU XA XỈ (HAUTE HORLOGERIE & PRE-OWNED)
    {
        "id": "dh01",
        "name": "Gia Bảo Luxury",
        "short_name": "Gia Bảo Luxury",
        "url": "https://giabaoluxury.com/",
        "domain": "giabaoluxury.com",
        "category": "Haute Horlogerie & Super Luxury",
        "category_vn": "Đồng Hồ Xa Xỉ & Haute Horlogerie",
        "tag": "luxury-watches",
        "vibe": "dark-luxury",
        "vibe_name": "Đẳng cấp & Xa xỉ",
        "location": "Hà Nội & TP.HCM",
        "desc": "Điểm đến hàng đầu cho giới mộ điệu đồng hồ xa xỉ Thụy Sĩ. Chuyên phân phối, thẩm định và giao dịch các kiệt tác thời gian từ Patek Philippe, Rolex, Audemars Piguet, Richard Mille."
    },
    {
        "id": "dh02",
        "name": "Boss Luxury Watch",
        "short_name": "Boss Luxury",
        "url": "https://bossluxurywatch.vn/",
        "domain": "bossluxurywatch.vn",
        "category": "Haute Horlogerie & Super Luxury",
        "category_vn": "Showroom Đồng Hồ Thượng Lưu",
        "tag": "luxury-watches",
        "vibe": "dark-luxury",
        "vibe_name": "Thượng lưu & Quyền lực",
        "location": "Hà Nội & TP.HCM",
        "desc": "Không gian mua sắm đồng hồ và trang sức xa xỉ uy tín với bộ sưu tập Rolex, Hublot, Patek Philippe phiên bản giới hạn dành cho giới thượng lưu và doanh nhân thành đạt."
    },
    {
        "id": "dh03",
        "name": "Empire Luxury",
        "short_name": "Empire Luxury",
        "url": "https://empireluxury.vn/",
        "domain": "empireluxury.vn",
        "category": "Haute Horlogerie & Super Luxury",
        "category_vn": "Đồng Hồ & Phong Cách Sống Thượng Lưu",
        "tag": "luxury-watches",
        "vibe": "minimal-dark",
        "vibe_name": "Hiện đại & Tinh xảo",
        "location": "TP.HCM",
        "desc": "Showroom phong cách sống thượng lưu tại trung tâm TP.HCM, quy tụ các tuyệt phẩm đồng hồ cơ khí đỉnh cao thế giới cùng dịch vụ tư vấn cá nhân hóa tiêu chuẩn 5 sao."
    },
    {
        "id": "dh04",
        "name": "Authentic Luxury",
        "short_name": "Authentic Luxury",
        "url": "https://authenticluxury.vn/",
        "domain": "authenticluxury.vn",
        "category": "Haute Horlogerie & Super Luxury",
        "category_vn": "Sàn Giao Dịch Đồng Hồ Authentic",
        "tag": "luxury-watches",
        "vibe": "dark-luxury",
        "vibe_name": "Sang trọng & Chuẩn mực",
        "location": "Hà Nội",
        "desc": "Hệ thống chuyên sâu về đồng hồ Rolex, Hublot, Patek Philippe chính hãng với quy trình kiểm định nghiêm ngặt, minh bạch tình trạng và chính sách bảo hành hậu mãi vượt trội."
    },
    {
        "id": "dh05",
        "name": "24Kara Authentic Watches",
        "short_name": "24Kara",
        "url": "https://24kara.com/",
        "domain": "24kara.com",
        "category": "Haute Horlogerie & Super Luxury",
        "category_vn": "Đồng Hồ Chính Hãng & Đồ Hiệu Xa Xỉ",
        "tag": "luxury-watches",
        "vibe": "editorial",
        "vibe_name": "Cổ điển & Giá trị di sản",
        "location": "Hà Nội & TP.HCM",
        "desc": "Chuỗi cửa hàng đồng hồ chính hãng và phụ kiện xa xỉ, nổi tiếng với kho sản phẩm đa dạng từ phân khúc cao cấp Thụy Sĩ đến các mẫu vintage sưu tầm hiếm có."
    },
    {
        "id": "dh06",
        "name": "Kỳ Lân Luxury",
        "short_name": "Kỳ Lân Luxury",
        "url": "https://kylanluxury.com/",
        "domain": "kylanluxury.com",
        "category": "Haute Horlogerie & Super Luxury",
        "category_vn": "Chế Tác Bespoke & Vàng Khối",
        "tag": "luxury-watches",
        "vibe": "dark-luxury",
        "vibe_name": "Độc bản & Vàng khối",
        "location": "TP.HCM",
        "desc": "Thương hiệu chế tác và phân phối các dòng đồng hồ siêu sang nạm kim cương, vàng khối nguyên bản, kết hợp điện thoại Vertu và trang sức cao cấp độc bản."
    },
    {
        "id": "dh07",
        "name": "Tam Sơn Luxury",
        "short_name": "Tam Sơn Luxury",
        "url": "https://tamsonvn.com/",
        "domain": "tamsonvn.com",
        "category": "Haute Horlogerie & Super Luxury",
        "category_vn": "Tập Đoàn Phân Phối Thương Hiệu Xa Xỉ",
        "tag": "luxury-watches",
        "vibe": "editorial",
        "vibe_name": "Quý phái & Di sản quốc tế",
        "location": "Toàn quốc",
        "desc": "Thành viên tập đoàn Openasia, đại diện phân phối chính thức các thương hiệu xa xỉ bậc nhất thế giới tại Việt Nam gồm Patek Philippe, Chopard, Hermès và Vacheron Constantin."
    },

    # NHÓM 2: HỆ THỐNG BÁN LẺ & ĐẠI LÝ ỦY QUYỀN HÀNG ĐẦU (TOP SEO & AUTHORIZED RETAILERS)
    {
        "id": "dh08",
        "name": "Galle Watch",
        "short_name": "Galle Watch",
        "url": "https://galle.vn/",
        "domain": "galle.vn",
        "category": "Authorized Retail Chains",
        "category_vn": "Chuỗi Bán Lẻ Đồng Hồ Chính Hãng",
        "tag": "authorized-retail",
        "vibe": "clean-white",
        "vibe_name": "Chuyên nghiệp & Minh bạch",
        "location": "Toàn quốc",
        "desc": "Hệ thống phân phối đồng hồ chính hãng quy mô hàng đầu Việt Nam với hơn 30 thương hiệu danh tiếng: Frederique Constant, Longines, Rado, Tissot, Certina, Seiko, Orient."
    },
    {
        "id": "dh09",
        "name": "Xwatch",
        "short_name": "Xwatch",
        "url": "https://xwatch.vn/",
        "domain": "xwatch.vn",
        "category": "Authorized Retail Chains",
        "category_vn": "Hệ Thống Đồng Hồ Thật & Bảo Hiểm",
        "tag": "authorized-retail",
        "vibe": "vibrant-modern",
        "vibe_name": "Năng động & Tin cậy",
        "location": "Toàn quốc",
        "desc": "Đơn vị tiên phong chống hàng giả tại Việt Nam với triết lý 'Đồng hồ thật - Giá trị thật' cùng gói bảo hiểm cả lỗi người dùng trong 5 năm độc quyền thị trường."
    },
    {
        "id": "dh10",
        "name": "Đồng Hồ Duy Anh",
        "short_name": "Đồng Hồ Duy Anh",
        "url": "https://donghoduyanh.com/",
        "domain": "donghoduyanh.com",
        "category": "Authorized Retail Chains",
        "category_vn": "Đại Lý Ủy Quyền Thụy Sĩ Lâu Đời",
        "tag": "authorized-retail",
        "vibe": "editorial",
        "vibe_name": "Cổ điển & Uy tín lâu đời",
        "location": "Hà Nội & TP.HCM",
        "desc": "Hơn 60 năm kinh nghiệm trong ngành chế tác và phân phối đồng hồ. Đại lý ủy quyền chính thức của Longines, Tissot, Mido, Hamilton, Seiko với trung tâm bảo hành chuẩn Thụy Sĩ."
    },
    {
        "id": "dh11",
        "name": "Đồng Hồ Tân Tân",
        "short_name": "Đồng Hồ Tân Tân",
        "url": "https://donghotantan.vn/",
        "domain": "donghotantan.vn",
        "category": "Authorized Retail Chains",
        "category_vn": "Biểu Tượng Bán Lẻ Đồng Hồ Miền Nam",
        "tag": "authorized-retail",
        "vibe": "clean-white",
        "vibe_name": "Bền bỉ & Chuẩn xác",
        "location": "TP.HCM",
        "desc": "Thành lập từ năm 1985, Tân Tân là biểu tượng bán lẻ đồng hồ uy tín bậc nhất miền Nam và là trung tâm bảo hành ủy quyền chính thức của Citizen và Movado Group tại Việt Nam."
    },
    {
        "id": "dh12",
        "name": "WatchStore",
        "short_name": "WatchStore",
        "url": "https://www.watchstore.vn/",
        "domain": "watchstore.vn",
        "category": "Authorized Retail Chains",
        "category_vn": "Thương Mại Điện Tử Đồng Hồ Hiện Đại",
        "tag": "authorized-retail",
        "vibe": "vibrant-modern",
        "vibe_name": "Hiện đại & Tối ưu chuyển đổi",
        "location": "Hà Nội, Đà Nẵng & TP.HCM",
        "desc": "Chuỗi bán lẻ đồng hồ thế hệ mới phát triển thần tốc với trải nghiệm mua sắm đa kênh (Omnichannel), giao diện UI/UX tối ưu chuyển đổi, cam kết chính hãng 100% đền gấp 20 lần."
    },
    {
        "id": "dh13",
        "name": "Đồng Hồ Chính Hãng",
        "short_name": "Đồng Hồ Chính Hãng",
        "url": "https://donghochinhhang.com/",
        "domain": "donghochinhhang.com",
        "category": "Authorized Retail Chains",
        "category_vn": "Showroom Cao Cấp Tại Trung Tâm Thương Mại",
        "tag": "authorized-retail",
        "vibe": "clean-white",
        "vibe_name": "Thanh lịch & Chuẩn mực TTTM",
        "location": "Hà Nội",
        "desc": "Hệ thống gian hàng cao cấp đặt tại các trung tâm thương mại sang trọng bậc nhất thủ đô (Tràng Tiền Plaza, Vincom Center Bà Triệu), chuyên phân phối Longines, Tissot, Movado."
    },
    {
        "id": "dh14",
        "name": "Đồng Hồ Thụy Sỹ",
        "short_name": "Đồng Hồ Thụy Sỹ",
        "url": "https://donghothuysy.vn/",
        "domain": "donghothuysy.vn",
        "category": "Authorized Retail Chains",
        "category_vn": "Chuyên Trang Đồng Hồ Swiss Made Cao Cấp",
        "tag": "authorized-retail",
        "vibe": "editorial",
        "vibe_name": "Tinh hoa cơ khí Swiss Made",
        "location": "Toàn quốc",
        "desc": "Chuyên trang độc quyền hội tụ các tuyệt tác Swiss Made đỉnh cao do Galle phân phối, cung cấp kiến thức cơ khí chuyên sâu và không gian tuyển chọn đồng hồ Thụy Sỹ chuẩn mực."
    },
    {
        "id": "dh15",
        "name": "Luxshopping",
        "short_name": "Luxshopping",
        "url": "https://luxshopping.vn/",
        "domain": "luxshopping.vn",
        "category": "Authorized Retail Chains",
        "category_vn": "Đồng Hồ Nhập Khẩu Mỹ & Châu Âu",
        "tag": "authorized-retail",
        "vibe": "clean-white",
        "vibe_name": "Thời thượng & Đa dạng",
        "location": "TP.HCM",
        "desc": "Kênh mua sắm đồng hồ và trang sức nhập khẩu chính hãng từ Mỹ và Thụy Sĩ, nổi tiếng với dịch vụ đặt hàng theo yêu cầu các mẫu đồng hồ cao cấp từ Longines, Omega, Tag Heuer."
    },
    {
        "id": "dh16",
        "name": "Thế Giới Thời Gian",
        "short_name": "Thế Giới Thời Gian",
        "url": "https://thegioithoigian.vn/",
        "domain": "thegioithoigian.vn",
        "category": "Authorized Retail Chains",
        "category_vn": "Đồng Hồ Thời Trang & Phong Cách Sống",
        "tag": "authorized-retail",
        "vibe": "clean-white",
        "vibe_name": "Thanh lịch & Dễ tiếp cận",
        "location": "Toàn quốc",
        "desc": "Chuỗi bán lẻ đồng hồ chính hãng tập trung vào các thương hiệu thời trang quốc tế được yêu thích như Casio, Citizen, Daniel Wellington, Claude Bernard với mức giá hợp lý."
    },

    # NHÓM 3: THƯƠNG HIỆU VIỆT NAM & THIẾT KẾ ĐỘC BẢN (LOCAL BRANDS & DTC)
    {
        "id": "dh17",
        "name": "ViWat Watch",
        "short_name": "ViWat Watch",
        "url": "https://viwat.vn/",
        "domain": "viwat.vn",
        "category": "Vietnamese Watchmaker & DTC",
        "category_vn": "Đồng Hồ Tối Giản Di Sản Việt Nam",
        "tag": "local-dtc",
        "vibe": "minimal-dark",
        "vibe_name": "Tối giản & Văn hóa Việt",
        "location": "TP.HCM",
        "desc": "Thương hiệu đồng hồ Việt Nam lấy cảm hứng từ biểu tượng di sản các thành phố (Sài Gòn, Hà Nội, Bến Thành). Thiết kế tối giản, tinh tế, khẳng định niềm tự hào sáng tạo Việt."
    },

    # NHÓM 4: TẬP ĐOÀN ĐẠI DIỆN SIÊU THƯƠNG HIỆU & QUỐC TẾ (GLOBAL BENCHMARKS & CONGLOMERATES)
    {
        "id": "dh18",
        "name": "S&S Group",
        "short_name": "S&S Group",
        "url": "https://ssgroup.net/",
        "domain": "ssgroup.net",
        "category": "Luxury Conglomerate & Global",
        "category_vn": "Tập Đoàn Đại Diện Siêu Thương Hiệu Xa Xỉ",
        "tag": "luxury-watches",
        "vibe": "dark-luxury",
        "vibe_name": "Siêu xa xỉ & Đẳng cấp thế giới",
        "location": "Hà Nội & TP.HCM",
        "desc": "Tập đoàn phân phối độc quyền tại Việt Nam các đỉnh cao cơ khí thế giới: Richard Mille, Audemars Piguet, Hublot, MB&F, Bovet và siêu xe Rolls-Royce, McLaren."
    },
    {
        "id": "dh19",
        "name": "Hodinkee",
        "short_name": "Hodinkee",
        "url": "https://www.hodinkee.com/",
        "domain": "hodinkee.com",
        "category": "Luxury Conglomerate & Global",
        "category_vn": "Tạp Chí & Sàn Thương Mại Đồng Hồ Toàn Cầu",
        "tag": "global-benchmarks",
        "vibe": "editorial",
        "vibe_name": "Báo chí nghệ thuật & Đẳng cấp toàn cầu",
        "location": "New York, USA",
        "desc": "Tạp chí và nền tảng thương mại đồng hồ uy tín số 1 thế giới. Mẫu mực về thiết kế UI/UX dạng Editorial, nghệ thuật nhiếp ảnh đồng hồ macro và trải nghiệm mua sắm xa xỉ chuẩn mực."
    },
    {
        "id": "dh20",
        "name": "The 1916 Company",
        "short_name": "The 1916 Company",
        "url": "https://www.the1916company.com/",
        "domain": "the1916company.com",
        "category": "Luxury Conglomerate & Global",
        "category_vn": "Nền Tảng Đồng Hồ Xa Xỉ Hàng Đầu Thế Giới",
        "tag": "global-benchmarks",
        "vibe": "dark-luxury",
        "vibe_name": "Toàn cầu & Bộ sưu tập vô giá",
        "location": "Toàn cầu",
        "desc": "Liên minh đồng hồ cao cấp hàng đầu thế giới (hợp nhất từ WatchBox, Govberg, Radcliffe và Hyde Park). Nền tảng giao dịch đồng hồ xa xỉ và sưu tầm đỉnh cao với mạng lưới Lounge toàn cầu."
    }
]

print(f"Testing {len(candidates)} candidate websites with Playwright...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    success_count = 0
    for c in candidates:
        try:
            resp = page.goto(c["url"], timeout=18000, wait_until="domcontentloaded")
            status = resp.status if resp else "NO_RESP"
            print(f"[OK {status}] {c['id']} - {c['name']} -> {page.title()[:40]}")
            success_count += 1
        except Exception as e:
            print(f"[ERR] {c['id']} - {c['name']} -> {e}")
    browser.close()

print(f"Completed! {success_count}/{len(candidates)} loaded successfully.")
