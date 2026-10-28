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
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "decor_metadata.json")

os.makedirs(output_dir, exist_ok=True)
os.makedirs(kho_webp_dir, exist_ok=True)
os.makedirs(os.path.dirname(metadata_file), exist_ok=True)

websites = [
    # NHÓM 1: LUXURY & BESPOKE PARTY DECOR
    {
        "id": "dc01",
        "name": "7799 Wedding Storyteller",
        "short_name": "7799 Wedding",
        "url": "https://7799wedding.vn/",
        "domain": "7799wedding.vn",
        "slug": "7799wedding_vn",
        "industry": "decor-su-kien",
        "category": "Luxury & Bespoke Party Decor",
        "category_vn": "Trang Trí Tiệc Cưới & Không Gian Nghệ Thuật",
        "tag": "luxury-bespoke",
        "vibe": "dark-luxury",
        "vibe_name": "Sang trọng & Tinh tế",
        "location": "Hà Nội",
        "desc": "Thương hiệu trang trí sự kiện và tiệc cưới nghệ thuật hàng đầu Hà Nội. Chuyên sâu về nghệ thuật hoa lụa cao cấp, concept decor độc bản và tráp ăn hỏi truyền thống kết hợp hiện đại."
    },
    {
        "id": "dc02",
        "name": "Lutèce Wedding & Party Design",
        "short_name": "Lutèce Design",
        "url": "https://lutece.vn/",
        "domain": "lutece.vn",
        "slug": "lutece_vn",
        "industry": "decor-su-kien",
        "category": "Luxury & Bespoke Party Decor",
        "category_vn": "Thiết Kế Không Gian Yến Tiệc Xa Xỉ",
        "tag": "luxury-bespoke",
        "vibe": "editorial",
        "vibe_name": "Châu Âu & Đẳng cấp",
        "location": "Hà Nội & TP.HCM",
        "desc": "Studio thiết kế không gian tiệc cưới và sự kiện xa xỉ (Luxury Bespoke Design). Phong cách Châu Âu thanh lịch, hoa tươi nghệ thuật nhập khẩu và bài trí bàn tiệc VIP chuẩn Fine Dining."
    },
    {
        "id": "dc03",
        "name": "Phi Điệp Wedding & Event Decor",
        "short_name": "Phi Điệp Decor",
        "url": "https://phidiepwedding.com/",
        "domain": "phidiepwedding.com",
        "slug": "phidiepwedding_com",
        "industry": "decor-su-kien",
        "category": "Luxury & Bespoke Party Decor",
        "category_vn": "Decor Sự Kiện & Tiệc Cưới 5 Sao",
        "tag": "luxury-bespoke",
        "vibe": "corporate",
        "vibe_name": "Quy mô lớn & Vương giả",
        "location": "Toàn quốc",
        "desc": "Đơn vị kỳ cựu hơn 10 năm kinh nghiệm thiết kế đại sảnh tiệc cưới và dạ tiệc hoàng gia tại các khách sạn 5 sao danh tiếng (JW Marriott, Sheraton, Melia, InterContinental)."
    },
    {
        "id": "dc04",
        "name": "MHs Planner & Event Decoration",
        "short_name": "MHs Planner",
        "url": "https://mhswedding.vn/",
        "domain": "mhswedding.vn",
        "slug": "mhswedding_vn",
        "industry": "decor-su-kien",
        "category": "Luxury & Bespoke Party Decor",
        "category_vn": "Tư Vấn Concept & Decor Độc Bản",
        "tag": "luxury-bespoke",
        "vibe": "creative-art",
        "vibe_name": "Sáng tạo & Cá nhân hóa",
        "location": "Hà Nội",
        "desc": "Chuyên gia tư vấn concept và dàn dựng không gian tiệc cưới tư gia, resort và yến tiệc ngoài trời. Thế mạnh về nghệ thuật cắm hoa nghệ thuật đương đại và ánh sáng lãng mạn."
    },

    # NHÓM 2: BIRTHDAY, BABY SHOWER & PRIVATE PARTY
    {
        "id": "dc05",
        "name": "AZ Party — Tổ Chức & Trang Trí Sự Kiện",
        "short_name": "AZ Party",
        "url": "https://azparty.vn/",
        "domain": "azparty.vn",
        "slug": "azparty_vn",
        "industry": "decor-su-kien",
        "category": "Birthday & Private Party",
        "category_vn": "Trang Trí Sinh Nhật & Sự Kiện Trọn Gói",
        "tag": "birthday-party",
        "vibe": "vibrant",
        "vibe_name": "Trẻ trung & Năng động",
        "location": "TP.HCM",
        "desc": "Thương hiệu trang trí sự kiện và sinh nhật, thôi nôi hàng đầu tại Sài Gòn. Cung cấp giải pháp trọn gói từ backdrop 3D, line bóng nghệ thuật đến chú hề, MC và biểu diễn xiếc vui nhộn."
    },
    {
        "id": "dc06",
        "name": "Party Design VN — Thiết Kế Decor Tiệc",
        "short_name": "Party Design",
        "url": "https://partydesign.vn/",
        "domain": "partydesign.vn",
        "slug": "partydesign_vn",
        "industry": "decor-su-kien",
        "category": "Birthday & Private Party",
        "category_vn": "Thiết Kế Backdrop & Concept Tiệc",
        "tag": "birthday-party",
        "vibe": "creative-art",
        "vibe_name": "Hiện đại & Tinh xảo",
        "location": "TP.HCM",
        "desc": "Đơn vị chuyên sâu thiết kế concept sinh nhật, tiệc thôi nôi và decor sự kiện doanh nghiệp. Phong cách tạo hình 3D khối nổi, màu sắc bắt trend Pastel/Boho và phụ kiện tinh tế."
    },
    {
        "id": "dc07",
        "name": "Vua Trang Trí Event",
        "short_name": "Vua Trang Trí",
        "url": "https://vuatrangtri.vn/",
        "domain": "vuatrangtri.vn",
        "slug": "vuatrangtri_vn",
        "industry": "decor-su-kien",
        "category": "Birthday & Private Party",
        "category_vn": "Decor Tiệc Thôi Nôi & Sinh Nhật Trọn Gói",
        "tag": "birthday-party",
        "vibe": "vibrant",
        "vibe_name": "Đa dạng & Tươi vui",
        "location": "TP.HCM",
        "desc": "Hệ thống dịch vụ decor sinh nhật, thôi nôi, mừng thọ và lễ khai trương với kho mẫu thiết kế khổng lồ. Thi công nhanh chóng tại nhà riêng, nhà hàng với mức giá công khai minh bạch."
    },
    {
        "id": "dc08",
        "name": "GU Decorate — Dịch Vụ Trang Trí Tiệc",
        "short_name": "GU Decorate",
        "url": "https://gudecorate.com/",
        "domain": "gudecorate.com",
        "slug": "gudecorate_com",
        "industry": "decor-su-kien",
        "category": "Birthday & Private Party",
        "category_vn": "Decor Bàn Tiệc Gallery & Line Bóng",
        "tag": "birthday-party",
        "vibe": "creative-art",
        "vibe_name": "Bắt trend & Tươi sáng",
        "location": "TP.HCM",
        "desc": "Chuyên setup trọn gói backdrop tiệc sinh nhật người lớn, thôi nôi bé yêu, tiệc kỷ niệm ngày cưới và tiệc công ty. Nổi bật với các mẫu line bóng Chrome ánh kim và hoa tươi phối màu sang trọng."
    },
    {
        "id": "dc09",
        "name": "Sinh Nhật 5 Sao — Dịch Vụ Decor Cao Cấp",
        "short_name": "Sinh Nhật 5 Sao",
        "url": "https://sinhnhat5sao.com/",
        "domain": "sinhnhat5sao.com",
        "slug": "sinhnhat5sao_com",
        "industry": "decor-su-kien",
        "category": "Birthday & Private Party",
        "category_vn": "Trang Trí Sinh Nhật & Tiệc Private",
        "tag": "birthday-party",
        "vibe": "dark-luxury",
        "vibe_name": "Chuẩn 5 Sao & Độc quyền",
        "location": "Hà Nội & TP.HCM",
        "desc": "Dịch vụ tổ chức và trang trí sinh nhật, private party phân khúc cao cấp ở cả hai miền Nam - Bắc. Nhận may đo ý tưởng riêng theo sở thích của chủ nhân bữa tiệc với độ hoàn thiện cao."
    },
    {
        "id": "dc10",
        "name": "Angeline — Event & Birthday Styling",
        "short_name": "Angeline Event",
        "url": "https://angeline.vn/",
        "domain": "angeline.vn",
        "slug": "angeline_vn",
        "industry": "decor-su-kien",
        "category": "Birthday & Private Party",
        "category_vn": "Styling Sự Kiện & Sinh Nhật Nghệ Thuật",
        "tag": "birthday-party",
        "vibe": "editorial",
        "vibe_name": "Nhẹ nhàng & Tinh tế",
        "location": "Hà Nội",
        "desc": "Đơn vị định hình phong cách tiệc cao cấp tại Hà Nội. Khéo léo phối hợp giữa hoa lụa nhập khẩu, bảng tên mica đèn Led và các khối hình nghệ thuật tôn vinh cảm xúc ấm cúng của gia đình."
    },
    {
        "id": "dc11",
        "name": "Minh Triều Party — Dịch Vụ Decor Sự Kiện",
        "short_name": "Minh Triều Party",
        "url": "https://minhtrieuparty.com/",
        "domain": "minhtrieuparty.com",
        "slug": "minhtrieuparty_com",
        "industry": "decor-su-kien",
        "category": "Birthday & Private Party",
        "category_vn": "Decor Tiệc Thôi Nôi & Sinh Nhật Bé",
        "tag": "birthday-party",
        "vibe": "vibrant",
        "vibe_name": "Dễ thương & Hoạt họa",
        "location": "TP.HCM",
        "desc": "Chuyên thiết kế backdrop hoạt hình 3D, chibi ngộ nghĩnh, bàn tiệc cupcake và dịch vụ tổ chức tiệc sinh nhật trọn gói cho bé yêu tại TP.HCM và các tỉnh lân cận."
    },
    {
        "id": "dc12",
        "name": "Minh Hi Party — Trang Trí Tiệc Trọn Gói",
        "short_name": "Minh Hi Party",
        "url": "https://minhhiparty.com/",
        "domain": "minhhiparty.com",
        "slug": "minhhiparty_com",
        "industry": "decor-su-kien",
        "category": "Birthday & Private Party",
        "category_vn": "Trang Trí Tiệc Gia Đình & Sinh Nhật",
        "tag": "birthday-party",
        "vibe": "vibrant",
        "vibe_name": "Ấm áp & Thân thiện",
        "location": "TP.HCM",
        "desc": "Dịch vụ trang trí tiệc thôi nôi, sinh nhật tại nhà hàng và tư gia với chi phí linh hoạt, thiết kế bảng tên neon sign, line bóng ombre mềm mại và phụ kiện trang trí an toàn."
    },

    # NHÓM 3: BALLOON & BACKDROP STYLING
    {
        "id": "dc13",
        "name": "Hoàng Luân Event — Thi Công Backdrop & Bóng Bay",
        "short_name": "Hoàng Luân Event",
        "url": "https://hoangluanevent.com/",
        "domain": "hoangluanevent.com",
        "slug": "hoangluanevent_com",
        "industry": "decor-su-kien",
        "category": "Balloon & Backdrop Styling",
        "category_vn": "Cổng Bong Bóng Nghệ Thuật & Backdrop",
        "tag": "balloon-backdrop",
        "vibe": "corporate",
        "vibe_name": "Chuyên nghiệp & Nhanh chóng",
        "location": "TP.HCM",
        "desc": "Chuyên thi công backdrop formex cán PP, photobooth chụp ảnh, cổng chào bong bóng nghệ thuật cho lễ khai trương, tiệc tất niên Year End Party và sự kiện ngoài trời."
    },
    {
        "id": "dc14",
        "name": "Lucky Balloons — Nghệ Thuật Bóng Bay Thủ Đô",
        "short_name": "Lucky Balloons",
        "url": "https://bongbaysukien.com/",
        "domain": "bongbaysukien.com",
        "slug": "bongbaysukien_com",
        "industry": "decor-su-kien",
        "category": "Balloon & Backdrop Styling",
        "category_vn": "Decor Bóng Bay Nghệ Thuật & Lễ Hội",
        "tag": "balloon-backdrop",
        "vibe": "vibrant",
        "vibe_name": "Sặc sỡ & Rực rỡ",
        "location": "Hà Nội",
        "desc": "Thương hiệu bóng bay sự kiện uy tín hàng đầu Hà Nội. Cung cấp dịch vụ trang trí bóng bay phòng tân hôn, sinh nhật công ty, lễ hội Trung Thu, Giáng Sinh và bóng jumbo in chữ theo yêu cầu."
    },
    {
        "id": "dc15",
        "name": "Cát Decor Đà Nẵng — Trang Trí Tiệc Miền Trung",
        "short_name": "Cát Decor",
        "url": "https://trangtrisinhnhatdanang.com/",
        "domain": "trangtrisinhnhatdanang.com",
        "slug": "trangtrisinhnhatdanang_com",
        "industry": "decor-su-kien",
        "category": "Balloon & Backdrop Styling",
        "category_vn": "Decor Sinh Nhật & Party Đà Nẵng",
        "tag": "balloon-backdrop",
        "vibe": "creative-art",
        "vibe_name": "Nhiệt đới & Năng động",
        "location": "Đà Nẵng",
        "desc": "Đơn vị trang trí sinh nhật và thôi nôi uy tín số 1 Đà Nẵng. Phong cách trang trí mang hơi thở miền biển nhiệt đới, photobooth check-in hiện đại cho các bữa tiệc ngoài trời và resort."
    },
    {
        "id": "dc16",
        "name": "Oha Decor — Dịch Vụ Trang Trí Sự Kiện",
        "short_name": "Oha Decor",
        "url": "https://ohadecor.com/",
        "domain": "ohadecor.com",
        "slug": "ohadecor_com",
        "industry": "decor-su-kien",
        "category": "Balloon & Backdrop Styling",
        "category_vn": "Decor Sự Kiện & Tiệc Ngoài Trời",
        "tag": "balloon-backdrop",
        "vibe": "creative-art",
        "vibe_name": "Sáng tạo & Phóng khoáng",
        "location": "Đà Nẵng",
        "desc": "Cung cấp giải pháp decor sự kiện, tiệc kỷ niệm, sinh nhật người lớn và tiệc bãi biển tại Đà Nẵng - Hội An. Thiết kế phối cảnh 3D trước thi công giúp khách hàng an tâm tuyệt đối."
    },
    {
        "id": "dc17",
        "name": "Anh Đức Wedding & Event Decor",
        "short_name": "Anh Đức Decor",
        "url": "https://anhducwedding.com/",
        "domain": "anhducwedding.com",
        "slug": "anhducwedding_com",
        "industry": "decor-su-kien",
        "category": "Balloon & Backdrop Styling",
        "category_vn": "Decor Tiệc Cưới Bãi Biển & Resort",
        "tag": "balloon-backdrop",
        "vibe": "editorial",
        "vibe_name": "Lãng mạn ven biển",
        "location": "Đà Nẵng",
        "desc": "Thế mạnh về trang trí tiệc cưới bãi biển (Beach Wedding Decor) và sự kiện riêng tư tại các resort danh tiếng Đà Nẵng. Phong cách Boho phóng khoáng, khung vòm gỗ và hoa tươi tự nhiên."
    },

    # NHÓM 4: CORPORATE EVENT & GALA DECOR
    {
        "id": "dc18",
        "name": "Palamun Event — Thiết Kế Không Gian Gala & Hội Nghị",
        "short_name": "Palamun Event",
        "url": "https://palamunevent.com/",
        "domain": "palamunevent.com",
        "slug": "palamunevent_com",
        "industry": "decor-su-kien",
        "category": "Corporate Event & Gala Decor",
        "category_vn": "Thiết Kế Không Gian Gala Dinner",
        "tag": "corporate-gala",
        "vibe": "dark-luxury",
        "vibe_name": "Tập đoàn & Đẳng cấp",
        "location": "TP.HCM",
        "desc": "Agency tổ chức và thiết kế không gian sự kiện chuyên nghiệp tại Sài Gòn. Chuyên sâu về decor sân khấu 3D, sảnh đón khách sang trọng và hiệu ứng ánh sáng cho Gala Dinner, Year End Party."
    },
    {
        "id": "dc19",
        "name": "Will Event — Thiết Kế Thi Công Không Gian Sự Kiện",
        "short_name": "Will Event",
        "url": "https://willevent.vn/",
        "domain": "willevent.vn",
        "slug": "willevent_vn",
        "industry": "decor-su-kien",
        "category": "Corporate Event & Gala Decor",
        "category_vn": "Thiết Kế Sân Khấu & Khu Vực Check-in",
        "tag": "corporate-gala",
        "vibe": "corporate",
        "vibe_name": "Hiện đại & Chuẩn thương hiệu",
        "location": "TP.HCM",
        "desc": "Đơn vị chuyên thiết kế và thi công không gian check-in, photobooth, cổng chào và sân khấu sự kiện trọn gói tại TP.HCM. Tối ưu hóa nhận diện thương hiệu và trải nghiệm thị giác ấn tượng."
    },
    {
        "id": "dc20",
        "name": "Cyber Show — Sự Kiện & Trình Diễn Không Gian",
        "short_name": "Cyber Show",
        "url": "https://cybershow.vn/",
        "domain": "cybershow.vn",
        "slug": "cybershow_vn",
        "industry": "decor-su-kien",
        "category": "Corporate Event & Gala Decor",
        "category_vn": "Thiết Kế Sân Khấu & Sự Kiện Công Nghệ",
        "tag": "corporate-gala",
        "vibe": "corporate",
        "vibe_name": "Công nghệ & Đột phá",
        "location": "TP.HCM",
        "desc": "Thương hiệu hàng đầu về tổ chức sự kiện và thiết kế sân khấu công nghệ cao (Màn hình LED cong, 3D Mapping, ánh sáng biểu diễn) cho các lễ kỷ niệm, khai trương và hội nghị tập đoàn."
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
        # Cũng kiểm tra new_h không vượt quá 15500
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

print(f"=== BẮT ĐẦU CHỤP FULL-PAGE 20 WEBSITE TRANG TRÍ - DECOR TIỆC SỰ KIỆN ===", flush=True)

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
        
        # Check if already captured recently and valid (> 200KB)
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

        # If PNG exists but WebP needs generating (like for angeline.vn)
        if os.path.exists(filepath) and os.path.getsize(filepath) > 200 * 1024:
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            print(f"  -> File PNG đã có sẵn: {filename} ({size_mb:.2f} MB), tiến hành nén với WebP safeguard...", flush=True)
            success = True
        else:
            # Attempt smart clean capture
            try:
                page.goto(item['url'], wait_until="domcontentloaded", timeout=35000)
                time.sleep(2)
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

print(f"\n=== HOÀN TẤT CHỤP VÀ NÉN 20 WEBSITE DECOR! Đã lưu metadata vào {metadata_file} ===", flush=True)
