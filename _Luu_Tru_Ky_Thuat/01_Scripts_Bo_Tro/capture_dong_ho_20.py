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
from capture_engine import capture_smart_clean, check_for_blank_spaces
from playwright.sync_api import sync_playwright

output_dir = os.path.join(BASE_DIR, "Anh_Chup_Website")
kho_webp_dir = os.path.join(BASE_DIR, "Kho_Anh_Webp")
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "dong_ho_metadata.json")

os.makedirs(output_dir, exist_ok=True)
os.makedirs(kho_webp_dir, exist_ok=True)
os.makedirs(os.path.dirname(metadata_file), exist_ok=True)

websites = [
    # NHÓM 1: LUXURY & SIÊU XA XỈ (HAUTE HORLOGERIE & PRE-OWNED)
    {
        "id": "dh01",
        "name": "Gia Bảo Luxury",
        "short_name": "Gia Bảo Luxury",
        "url": "https://giabaoluxury.com/",
        "domain": "giabaoluxury.com",
        "slug": "giabaoluxury_com",
        "industry": "ban-dong-ho",
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
        "slug": "bossluxurywatch_vn",
        "industry": "ban-dong-ho",
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
        "slug": "empireluxury_vn",
        "industry": "ban-dong-ho",
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
        "slug": "authenticluxury_vn",
        "industry": "ban-dong-ho",
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
        "slug": "24kara_com",
        "industry": "ban-dong-ho",
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
        "slug": "kylanluxury_com",
        "industry": "ban-dong-ho",
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
        "slug": "tamsonvn_com",
        "industry": "ban-dong-ho",
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
        "slug": "galle_vn",
        "industry": "ban-dong-ho",
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
        "name": "Đăng Quang Watch",
        "short_name": "Đăng Quang Watch",
        "url": "https://www.dangquangwatch.vn/",
        "domain": "dangquangwatch.vn",
        "slug": "dangquangwatch_vn",
        "industry": "ban-dong-ho",
        "category": "Authorized Retail Chains",
        "category_vn": "Chuỗi Showroom Phủ Khắp Toàn Quốc",
        "tag": "authorized-retail",
        "vibe": "clean-white",
        "vibe_name": "Quy mô lớn & Bảo hành 10 năm",
        "location": "Toàn quốc",
        "desc": "Hệ thống bán lẻ đồng hồ và kính mắt quy mô cả nước, phân phối chính hãng Epos Swiss, Atlantic Swiss, Bruno Sohnle, Diamond D, Citizen với chính sách bảo hành lên tới 10 năm."
    },
    {
        "id": "dh10",
        "name": "Đồng Hồ Duy Anh",
        "short_name": "Đồng Hồ Duy Anh",
        "url": "https://donghoduyanh.com/",
        "domain": "donghoduyanh.com",
        "slug": "donghoduyanh_com",
        "industry": "ban-dong-ho",
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
        "slug": "donghotantan_vn",
        "industry": "ban-dong-ho",
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
        "slug": "watchstore_vn",
        "industry": "ban-dong-ho",
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
        "slug": "donghochinhhang_com",
        "industry": "ban-dong-ho",
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
        "slug": "donghothuysy_vn",
        "industry": "ban-dong-ho",
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
        "name": "Đồng Hồ Thành Phát",
        "short_name": "Đồng Hồ Thành Phát",
        "url": "https://donghothanhphat.vn/",
        "domain": "donghothanhphat.vn",
        "slug": "donghothanhphat_vn",
        "industry": "ban-dong-ho",
        "category": "Authorized Retail Chains",
        "category_vn": "Boutique Thụy Sĩ Tại Takashimaya",
        "tag": "authorized-retail",
        "vibe": "clean-white",
        "vibe_name": "Sang trọng & Tinh hoa Thụy Sĩ",
        "location": "TP.HCM",
        "desc": "Nhà bán lẻ đồng hồ Thụy Sĩ cao cấp lâu năm tại Sài Gòn, sở hữu chuỗi boutique sang trọng tại TTTM Takashimaya Saigon Centre, đại lý ủy quyền Longines, Rado, Hamilton, Tissot."
    },
    {
        "id": "dh16",
        "name": "Luxshopping",
        "short_name": "Luxshopping",
        "url": "https://luxshopping.vn/",
        "domain": "luxshopping.vn",
        "slug": "luxshopping_vn",
        "industry": "ban-dong-ho",
        "category": "Authorized Retail Chains",
        "category_vn": "Đồng Hồ Nhập Khẩu Mỹ & Châu Âu",
        "tag": "authorized-retail",
        "vibe": "clean-white",
        "vibe_name": "Thời thượng & Đa dạng",
        "location": "TP.HCM",
        "desc": "Kênh mua sắm đồng hồ và trang sức nhập khẩu chính hãng từ Mỹ và Thụy Sĩ, nổi tiếng với dịch vụ đặt hàng theo yêu cầu các mẫu đồng hồ cao cấp từ Longines, Omega, Tag Heuer."
    },
    {
        "id": "dh17",
        "name": "Thế Giới Thời Gian",
        "short_name": "Thế Giới Thời Gian",
        "url": "https://thegioithoigian.vn/",
        "domain": "thegioithoigian.vn",
        "slug": "thegioithoigian_vn",
        "industry": "ban-dong-ho",
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
        "id": "dh18",
        "name": "ViWat Watch",
        "short_name": "ViWat Watch",
        "url": "https://viwat.vn/",
        "domain": "viwat.vn",
        "slug": "viwat_vn",
        "industry": "ban-dong-ho",
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
        "id": "dh19",
        "name": "S&S Group",
        "short_name": "S&S Group",
        "url": "https://ssgroup.net/",
        "domain": "ssgroup.net",
        "slug": "ssgroup_net",
        "industry": "ban-dong-ho",
        "category": "Luxury Conglomerate & Global",
        "category_vn": "Tập Đoàn Đại Diện Siêu Thương Hiệu Xa Xỉ",
        "tag": "luxury-watches",
        "vibe": "dark-luxury",
        "vibe_name": "Siêu xa xỉ & Đẳng cấp thế giới",
        "location": "Hà Nội & TP.HCM",
        "desc": "Tập đoàn phân phối độc quyền tại Việt Nam các đỉnh cao cơ khí thế giới: Richard Mille, Audemars Piguet, Hublot, MB&F, Bovet và siêu xe Rolls-Royce, McLaren."
    },
    {
        "id": "dh20",
        "name": "Hodinkee",
        "short_name": "Hodinkee",
        "url": "https://www.hodinkee.com/",
        "domain": "hodinkee.com",
        "slug": "hodinkee_com",
        "industry": "ban-dong-ho",
        "category": "Luxury Conglomerate & Global",
        "category_vn": "Tạp Chí & Sàn Thương Mại Đồng Hồ Toàn Cầu",
        "tag": "global-benchmarks",
        "vibe": "editorial",
        "vibe_name": "Báo chí nghệ thuật & Đẳng cấp toàn cầu",
        "location": "New York, USA",
        "desc": "Tạp chí và nền tảng thương mại đồng hồ uy tín số 1 thế giới. Mẫu mực về thiết kế UI/UX dạng Editorial, nghệ thuật nhiếp ảnh đồng hồ macro và trải nghiệm mua sắm xa xỉ chuẩn mực."
    }
]

def compress_tri_layer(source_png_path, slug):
    thumb_name = f"{slug}_thumb.webp"
    full_name = f"{slug}_full.webp"
    fb_name = f"{slug}_fb.png"
    thumb_path = os.path.join(kho_webp_dir, thumb_name)
    full_path = os.path.join(kho_webp_dir, full_name)
    fb_path = os.path.join(kho_webp_dir, fb_name)

    if not os.path.exists(source_png_path):
        print(f"[-] Không tìm thấy ảnh gốc: {source_png_path}")
        return None, None, None, 0, 0, 0

    with Image.open(source_png_path) as im:
        im_rgb = im.convert("RGB")
        w, h = im_rgb.size

        # 1. Full-page WebP (Giới hạn tối đa của WebP là 16383px)
        if h > 15500:
            scale = 15500.0 / h
            new_w = int(w * scale)
            im_full = im_rgb.resize((new_w, 15500), Image.Resampling.LANCZOS)
        else:
            im_full = im_rgb
        im_full.save(full_path, "WEBP", quality=80, method=4)

        # 2. Thumbnail WebP (resize width to 600px)
        new_w = 600
        new_h = int(h * (new_w / w))
        if new_h > 15500:
            new_h = 15500
        im_thumb = im_rgb.resize((new_w, new_h), Image.Resampling.LANCZOS)
        im_thumb.save(thumb_path, "WEBP", quality=75, method=4)

        # 3. Cắt sẵn chuẩn 1080x1920 (9:16) từ đỉnh trang cho Facebook/Zalo Lead Card
        slice_h = min(h, int(w * 16 / 9))
        crop = im_rgb.crop((0, 0, w, slice_h))
        im_fb = crop.resize((1080, 1920), Image.Resampling.LANCZOS)
        im_fb.save(fb_path, format="PNG", optimize=True)

    thumb_kb = round(os.path.getsize(thumb_path) / 1024, 1)
    full_kb = round(os.path.getsize(full_path) / 1024, 1)
    fb_kb = round(os.path.getsize(fb_path) / 1024, 1)
    return thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb

print(f"=== BẮT ĐẦU CHỤP FULL-PAGE 20 WEBSITE BÁN ĐỒNG HỒ CHÍNH HÃNG & XA XỈ ===", flush=True)

final_metadata = []

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
    )
    context = browser.new_context(
        viewport={"width": 1440, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
    page = context.new_page()

    for idx, item in enumerate(websites, start=1):
        filename = f"{item['domain']}.png"
        filepath = os.path.join(output_dir, filename)
        slug = item["slug"]
        print(f"\n[{idx}/20] ({item['category_vn']}) Đang xử lý: {item['name']} -> {item['url']}...", flush=True)
        start_t = time.time()
        
        success = False
        res_info = (1440, 900)
        
        # Check if already captured recently and valid (> 100KB)
        thumb_name = f"{slug}_thumb.webp"
        thumb_path = os.path.join(kho_webp_dir, thumb_name)
        if os.path.exists(thumb_path) and os.path.getsize(thumb_path) > 10 * 1024 and os.path.exists(filepath):
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            print(f"  -> File gốc và WebP đã tồn tại hoàn chỉnh: {filename} ({size_mb:.2f} MB), đọc lại thông số...", flush=True)
            full_name = f"{slug}_full.webp"
            fb_name = f"{slug}_fb.png"
            full_path = os.path.join(kho_webp_dir, full_name)
            fb_path = os.path.join(kho_webp_dir, fb_name)
            thumb_kb = round(os.path.getsize(thumb_path) / 1024, 1)
            full_kb = round(os.path.getsize(full_path) / 1024, 1) if os.path.exists(full_path) else 0
            fb_kb = round(os.path.getsize(fb_path) / 1024, 1) if os.path.exists(fb_path) else 0
            final_metadata.append({
                **item,
                "image": f"Anh_Chup_Website/{filename}",
                "thumb": f"Kho_Anh_Webp/{thumb_name}",
                "full": f"Kho_Anh_Webp/{full_name}",
                "fb": f"Kho_Anh_Webp/{fb_name}",
                "thumb_kb": thumb_kb,
                "full_kb": full_kb,
                "fb_kb": fb_kb,
                "size_mb": f"{size_mb:.2f} MB",
                "status": "SUCCESS"
            })
            continue

        # Attempt smart clean capture
        try:
            page.goto(item['url'], wait_until="domcontentloaded", timeout=35000)
            time.sleep(2.5)
            res_info = capture_smart_clean(page, filepath)
            is_blank, reason = check_for_blank_spaces(filepath)
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            print(f"  -> Smart Clean thành công: {filename} ({res_info[0]}x{res_info[1]}, {size_mb:.2f} MB, {time.time()-start_t:.1f}s, Blank: {reason})", flush=True)
            success = True
        except Exception as e:
            print(f"  -> Smart Clean gặp lỗi: {e}, chuyển sang Fallback Full-page...", flush=True)
            try:
                page.goto(item['url'], wait_until="load", timeout=30000)
                time.sleep(2)
                page.screenshot(path=filepath, full_page=True)
                size_mb = os.path.getsize(filepath) / (1024 * 1024)
                print(f"  -> Fallback Full-page thành công: {filename} ({size_mb:.2f} MB)", flush=True)
                success = True
            except Exception as e2:
                print(f"  -> THẤT BẠI: {e2}", flush=True)

        if success and os.path.exists(filepath):
            thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb = compress_tri_layer(filepath, slug)
            final_metadata.append({
                **item,
                "image": f"Anh_Chup_Website/{filename}",
                "thumb": f"Kho_Anh_Webp/{thumb_name}",
                "full": f"Kho_Anh_Webp/{full_name}",
                "fb": f"Kho_Anh_Webp/{fb_name}",
                "thumb_kb": thumb_kb,
                "full_kb": full_kb,
                "fb_kb": fb_kb,
                "size_mb": f"{os.path.getsize(filepath)/(1024*1024):.2f} MB",
                "status": "SUCCESS"
            })
            print(f"  -> Đã nén: Thumb {thumb_kb} KB, Full {full_kb} KB, FB {fb_kb} KB", flush=True)
        else:
            final_metadata.append({
                **item,
                "image": f"Anh_Chup_Website/{filename}",
                "thumb": "",
                "full": "",
                "fb": "",
                "thumb_kb": 0,
                "full_kb": 0,
                "fb_kb": 0,
                "size_mb": "N/A",
                "status": "FAILED"
            })

    browser.close()

with open(metadata_file, "w", encoding="utf-8") as f:
    json.dump(final_metadata, f, ensure_ascii=False, indent=2)

print(f"\n=== HOÀN TẤT CHỤP VÀ NÉN 20 WEBSITE ĐỒNG HỒ! Đã lưu metadata vào {metadata_file} ===", flush=True)
