# -*- coding: utf-8 -*-
"""
Pipeline Tự Động Nén Ảnh WebP 2 Tầng & Đồng Bộ Dữ Liệu WebVault.
Quy chuẩn:
- Tầng 1: Thumbnail width 600px, WebP quality 75 (<80 KB) cho Card & Hover Scroll.
- Tầng 2: Full-Page width 1440px, WebP quality 80 (<800 KB) cho Lightbox Zoom.
"""

import os
import sys
import json
import time
from PIL import Image

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
KHO_WEBP_DIR = os.path.join(BASE_DIR, "Kho_Anh_Webp")
ANH_CHUP_DIR = os.path.join(BASE_DIR, "Anh_Chup_Website")
DB_PATH = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "database.json")
STAGING_JSON = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "approved_selection.json")

os.makedirs(KHO_WEBP_DIR, exist_ok=True)
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

DEFAULT_EVENT_WEBSITES = [
    {
        "id": "01",
        "name": "Square Experiential Communications",
        "short_name": "Square Experiential",
        "url": "https://square-vn.com/",
        "domain": "square-vn.com",
        "industry": "su-kien",
        "industry_name": "Sự kiện & Activation",
        "tag": "creative",
        "vibe": "dark-luxury",
        "vibe_name": "Dark Mode & Sang trọng",
        "category": "Creative & Experiential Agency",
        "location": "TP.HCM & Toàn quốc",
        "source_image": "square-vn.com.png",
        "desc": "Agency hàng đầu về Brand Activation và Experiential Marketing. Giao diện full-bleed tràn viền, hiệu ứng visual storytelling đẳng cấp quốc tế."
    },
    {
        "id": "02",
        "name": "Per-fectiv",
        "short_name": "Per-fectiv",
        "url": "https://per-fectiv.com/",
        "domain": "per-fectiv.com",
        "industry": "su-kien",
        "industry_name": "Sự kiện & Activation",
        "tag": "creative",
        "vibe": "dark-luxury",
        "vibe_name": "Dark Mode & Sang trọng",
        "category": "Luxury Event Agency",
        "location": "TP.HCM",
        "source_image": "per-fectiv.com.png",
        "desc": "Giao diện Dark Mode sang trọng, thời thượng; chuyên các sự kiện trải nghiệm sáng tạo, ra mắt thương hiệu xa xỉ (BMW, Hennessy)."
    },
    {
        "id": "03",
        "name": "Le Bros",
        "short_name": "Le Bros",
        "url": "https://lebros.vn/",
        "domain": "lebros.vn",
        "industry": "su-kien",
        "industry_name": "Sự kiện & Activation",
        "tag": "creative",
        "vibe": "editorial",
        "vibe_name": "Editorial & Tối giản",
        "category": "Editorial & Cultural Events",
        "location": "Hà Nội & TP.HCM",
        "source_image": "lebros.vn.png",
        "desc": "Thuộc Le Group. Thiết kế phong cách tạp chí tối giản (Editorial Minimalist), đậm chất văn hóa nghệ thuật cho sự kiện tầm vóc quốc gia."
    },
    {
        "id": "04",
        "name": "BS Group",
        "short_name": "BS Group",
        "url": "https://bsgroup.com.vn/",
        "domain": "bsgroup.com.vn",
        "industry": "su-kien",
        "industry_name": "Sự kiện & Activation",
        "tag": "creative",
        "vibe": "dark-luxury",
        "vibe_name": "Dark Mode & Sang trọng",
        "category": "Bespoke Events & Production",
        "location": "TP.HCM & Toàn quốc",
        "source_image": "bsgroup.com.vn.png",
        "desc": "Sự kiện may đo độc bản (Bespoke Events). Bố cục phân tầng mạch lạc, video showreel chất lượng cao, stage production chuyên nghiệp."
    },
    {
        "id": "05",
        "name": "Zeit Media",
        "short_name": "Zeit Media",
        "url": "https://zeitmedia.vn/",
        "domain": "zeitmedia.vn",
        "industry": "su-kien",
        "industry_name": "Sự kiện & Activation",
        "tag": "creative",
        "vibe": "creative-art",
        "vibe_name": "Sáng tạo & Đương đại",
        "category": "Creative Art Agency",
        "location": "Hà Nội & TP.HCM",
        "source_image": "zeitmedia.vn.png",
        "desc": "Tinh thần nghệ thuật đương đại 'Creative Above All'. Dàn trang dự án đánh số thứ tự độc đáo, hình ảnh sự kiện sáng tạo nổi bật."
    },
    {
        "id": "06",
        "name": "HoaBinh Events",
        "short_name": "HoaBinh Events",
        "url": "https://hoabinhevents.com/",
        "domain": "hoabinhevents.com",
        "industry": "su-kien",
        "industry_name": "Sự kiện & Activation",
        "tag": "top-seo",
        "vibe": "corporate",
        "vibe_name": "Tập đoàn & Doanh nghiệp lớn",
        "category": "Top 1 SEO MICE & Hội nghị",
        "location": "Toàn quốc & Quốc tế",
        "source_image": "hoabinhevents.com.png",
        "desc": "Ông lớn số 1 về Hội nghị, Hội thảo quốc tế và M.I.C.E. Thống trị hàng trăm từ khóa tìm kiếm Google với cấu trúc danh mục đồ sộ."
    },
    {
        "id": "07",
        "name": "Á Châu Event",
        "short_name": "Á Châu Event",
        "url": "https://sukienachau.com/",
        "domain": "sukienachau.com",
        "industry": "su-kien",
        "industry_name": "Sự kiện & Activation",
        "tag": "top-seo",
        "vibe": "corporate",
        "vibe_name": "Tập đoàn & Doanh nghiệp lớn",
        "category": "Top 1-3 SEO Full-Service",
        "location": "Hà Nội & TP.HCM",
        "source_image": "sukienachau.com.png",
        "desc": "Đơn vị kỳ cựu từ 2008 giữ vững top đầu tìm kiếm Google. Cung cấp gói dịch vụ sự kiện trọn gói từ thiết bị, nhân sự đến kịch bản."
    },
    {
        "id": "08",
        "name": "Vietlink Event",
        "short_name": "Vietlink Event",
        "url": "https://vietlinkevent.vn/",
        "domain": "vietlinkevent.vn",
        "industry": "su-kien",
        "industry_name": "Sự kiện & Activation",
        "tag": "top-seo",
        "vibe": "corporate",
        "vibe_name": "Tập đoàn & Doanh nghiệp lớn",
        "category": "Sự kiện Doanh nghiệp",
        "location": "TP.HCM & Hà Nội",
        "source_image": "vietlinkevent.vn.png",
        "desc": "Top đầu tìm kiếm phía Nam mảng khai trương, khánh thành, hội nghị khách hàng, Year End Party với bố cục nhận báo giá tối ưu."
    },
    {
        "id": "09",
        "name": "Apex Media",
        "short_name": "Apex Media",
        "url": "https://apexevent.vn/",
        "domain": "apexevent.vn",
        "industry": "su-kien",
        "industry_name": "Sự kiện & Activation",
        "tag": "creative",
        "vibe": "corporate",
        "vibe_name": "Tập đoàn & Doanh nghiệp lớn",
        "category": "Strategic Brand Events",
        "location": "TP.HCM",
        "source_image": "apexevent.vn.png",
        "desc": "Thiết kế hiện đại, chỉn chu, truyền tải chiều sâu năng lực chiến lược tổ chức sự kiện đối ngoại và hội nghị thượng đỉnh kinh tế."
    },
    {
        "id": "10",
        "name": "Newday Media",
        "short_name": "Newday Media",
        "url": "https://newdaymedia.com.vn/",
        "domain": "newdaymedia.com.vn",
        "industry": "su-kien",
        "industry_name": "Sự kiện & Activation",
        "tag": "creative",
        "vibe": "creative-art",
        "vibe_name": "Sáng tạo & Đương đại",
        "category": "Stevie Awards Winner",
        "location": "Hà Nội & Toàn quốc",
        "source_image": "newdaymedia.com.vn.png",
        "desc": "Agency sáng tạo đạt giải thưởng danh giá Stevie Awards (Mỹ). Chuyên lễ hội văn hóa di sản, sự kiện công nghệ và đại nhạc hội."
    },
    {
        "id": "11",
        "name": "Cyber Show",
        "short_name": "Cyber Show",
        "url": "https://cybershow.vn/",
        "domain": "cybershow.vn",
        "industry": "su-kien",
        "industry_name": "Sự kiện & Activation",
        "tag": "top-seo",
        "vibe": "vibrant",
        "vibe_name": "Trẻ trung & Năng động",
        "category": "Gala Dinner & YEP",
        "location": "TP.HCM & Miền Nam",
        "source_image": "cybershow.vn.png",
        "desc": "Giao diện tràn đầy năng lượng, tối ưu di động xuất sắc; chuyên tiệc tất niên, gala dinner kết hợp hiệu ứng âm thanh ánh sáng hiện đại."
    },
    {
        "id": "12",
        "name": "YesEvents",
        "short_name": "YesEvents",
        "url": "https://www.yesevents.vn/",
        "domain": "yesevents.vn",
        "industry": "su-kien",
        "industry_name": "Sự kiện & Activation",
        "tag": "top-seo",
        "vibe": "dark-luxury",
        "vibe_name": "Dark Mode & Sang trọng",
        "category": "5-Star Hotels & FDI",
        "location": "TP.HCM & Phú Quốc",
        "source_image": "yesevents.vn.png",
        "desc": "Phong cách thanh lịch, song ngữ Anh - Việt; đối tác chiến lược của các khách sạn 5 sao và resort cao cấp tại TP.HCM và Phú Quốc."
    },
    {
        "id": "13",
        "name": "CAT Event",
        "short_name": "CAT Event",
        "url": "https://cat-event.com.vn/",
        "domain": "cat-event.com.vn",
        "industry": "su-kien",
        "industry_name": "Sự kiện & Activation",
        "tag": "top-seo",
        "vibe": "corporate",
        "vibe_name": "Tập đoàn & Doanh nghiệp lớn",
        "category": "Khánh tiết & Sự kiện lớn",
        "location": "TP.HCM & Toàn quốc",
        "source_image": "cat-event.com.vn.png",
        "desc": "Kinh nghiệm từ 2004, thể hiện hình ảnh vững chãi của doanh nghiệp kỳ cựu chuyên tổ chức sự kiện khánh tiết nhà nước và tập đoàn lớn."
    },
    {
        "id": "14",
        "name": "Hoàng Sa Việt",
        "short_name": "Hoàng Sa Việt",
        "url": "https://hoangsaviet.com/",
        "domain": "hoangsaviet.com",
        "industry": "su-kien",
        "industry_name": "Sự kiện & Activation",
        "tag": "top-seo",
        "vibe": "corporate",
        "vibe_name": "Tập đoàn & Doanh nghiệp lớn",
        "category": "Sản xuất sân khấu & Mega Concert",
        "location": "TP.HCM, HN, Phú Quốc",
        "source_image": "hoangsaviet.com.png",
        "desc": "Sở hữu nhà máy Viettruss lớn nhất miền Nam; trực tiếp tham gia sản xuất concert Anh Trai Say Hi. Hệ sinh thái thiết bị toàn diện."
    },
    {
        "id": "15",
        "name": "Đất Việt Event",
        "short_name": "Đất Việt Event",
        "url": "https://datvietevent.com/",
        "domain": "datvietevent.com",
        "industry": "su-kien",
        "industry_name": "Sự kiện & Activation",
        "tag": "top-seo",
        "vibe": "vibrant",
        "vibe_name": "Trẻ trung & Năng động",
        "category": "Event & Du lịch Doanh nghiệp",
        "location": "TP.HCM & Toàn quốc",
        "source_image": "datvietevent.com.png",
        "desc": "Thuộc Đất Việt Tour. Tông màu cam trắng hiện đại, thông số năng lực minh bạch (500+ sự kiện/năm) cho teambuilding và gala lớn."
    },
    {
        "id": "16",
        "name": "Danang Events",
        "short_name": "Danang Events",
        "url": "https://danangevents.com.vn/",
        "domain": "danangevents.com.vn",
        "industry": "su-kien",
        "industry_name": "Sự kiện & Activation",
        "tag": "regional",
        "vibe": "corporate",
        "vibe_name": "Tập đoàn & Doanh nghiệp lớn",
        "category": "Top 1 Sự kiện Miền Trung",
        "location": "Đà Nẵng & Miền Trung",
        "source_image": "danangevents.com.vn.png",
        "desc": "Dẫn đầu thị phần sự kiện và M.I.C.E tại Đà Nẵng - Hội An - Huế; cấu trúc cẩm nang sự kiện và du lịch kết hợp teambuilding biển chuẩn SEO."
    },
    {
        "id": "17",
        "name": "Sea Event",
        "short_name": "Sea Event",
        "url": "https://seaevent.vn/",
        "domain": "seaevent.vn",
        "industry": "su-kien",
        "industry_name": "Sự kiện & Activation",
        "tag": "regional",
        "vibe": "vibrant",
        "vibe_name": "Trẻ trung & Năng động",
        "category": "Sự kiện Duyên hải Miền Trung",
        "location": "Đà Nẵng & Miền Trung",
        "source_image": "seaevent.vn.png",
        "desc": "Tone xanh biển duyên hải tươi sáng, top 1-2 tìm kiếm sự kiện tại Đà Nẵng, am hiểu văn hóa bản địa và tối ưu chi phí tổ chức."
    },
    {
        "id": "18",
        "name": "AN Media",
        "short_name": "AN Media",
        "url": "https://anmedia.vn/",
        "domain": "anmedia.vn",
        "industry": "su-kien",
        "industry_name": "Sự kiện & Activation",
        "tag": "regional",
        "vibe": "creative-art",
        "vibe_name": "Sáng tạo & Đương đại",
        "category": "Event & Truyền thông KOLs",
        "location": "Hà Nội & Miền Bắc",
        "source_image": "anmedia.vn.png",
        "desc": "Sáng lập bởi ca sĩ / MC Duy Khoa. Kết hợp hoàn hảo giữa tổ chức sự kiện chuyên nghiệp và mạng lưới sản xuất TVC, báo chí, nghệ sĩ."
    },
    {
        "id": "19",
        "name": "Thăng Long Event",
        "short_name": "Thăng Long Event",
        "url": "https://thanglongevent.com/",
        "domain": "thanglongevent.com",
        "industry": "su-kien",
        "industry_name": "Sự kiện & Activation",
        "tag": "regional",
        "vibe": "dark-luxury",
        "vibe_name": "Dark Mode & Sang trọng",
        "category": "Lễ kỷ niệm & Vinh danh",
        "location": "Hà Nội & Toàn quốc",
        "source_image": "thanglongevent.com.png",
        "desc": "Thiết kế nhận diện thương hiệu bài bản bởi Sao Kim Branding; giao diện sang trọng chuyên phục vụ các bộ ban ngành và tập đoàn lớn."
    },
    {
        "id": "20",
        "name": "AzEvent",
        "short_name": "AzEvent",
        "url": "https://azevent.vn/",
        "domain": "azevent.vn",
        "industry": "su-kien",
        "industry_name": "Sự kiện & Activation",
        "tag": "regional",
        "vibe": "corporate",
        "vibe_name": "Tập đoàn & Doanh nghiệp lớn",
        "category": "Hội nghị & Khai trương trọn gói",
        "location": "Hà Nội & Miền Bắc",
        "source_image": "azevent.vn.png",
        "desc": "Bố cục tinh gọn, tốc độ tải nhanh, hiển thị số liệu kinh nghiệm minh bạch, thứ hạng tìm kiếm top đầu thủ đô cho dịch vụ sự kiện."
    }
]

def compress_tri_layer(source_png_path, slug):
    """
    Tạo sẵn 3 phiên bản tối ưu ngay từ đầu:
    1. full.webp (width 1440px, Q80) cho Lightbox phóng to
    2. thumb.webp (width 600px, Q75) cho Card list & hover scroll
    3. fb.png (chuẩn 1080x1920, 9:16 cắt từ đỉnh) để copy dán Facebook/Zalo tức thì (0ms chờ)
    """
    thumb_name = f"{slug}_thumb.webp"
    full_name = f"{slug}_full.webp"
    fb_name = f"{slug}_fb.png"
    thumb_path = os.path.join(KHO_WEBP_DIR, thumb_name)
    full_path = os.path.join(KHO_WEBP_DIR, full_name)
    fb_path = os.path.join(KHO_WEBP_DIR, fb_name)

    if not os.path.exists(source_png_path):
        print(f"[-] Không tìm thấy ảnh gốc: {source_png_path}")
        return None, None, None, 0, 0, 0

    with Image.open(source_png_path) as im:
        im_rgb = im.convert("RGB")
        w, h = im_rgb.size

        # 1. Full-page WebP
        im_rgb.save(full_path, "WEBP", quality=80, method=4)

        # 2. Thumbnail WebP (resize width to 600px)
        new_w = 600
        new_h = int(h * (new_w / w))
        im_thumb = im_rgb.resize((new_w, new_h), Image.Resampling.LANCZOS)
        im_thumb.save(thumb_path, "WEBP", quality=75, method=4)

        # 3. Cắt sẵn chuẩn 1080x1920 (9:16) từ đỉnh trang cho Facebook/Zalo
        slice_h = min(h, int(w * 16 / 9))
        crop = im_rgb.crop((0, 0, w, slice_h))
        im_fb = crop.resize((1080, 1920), Image.Resampling.LANCZOS)
        im_fb.save(fb_path, format="PNG", optimize=True)

    thumb_kb = round(os.path.getsize(thumb_path) / 1024, 1)
    full_kb = round(os.path.getsize(full_path) / 1024, 1)
    fb_kb = round(os.path.getsize(fb_path) / 1024, 1)
    return thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb

def sync_all_default():
    print("[*] Bắt đầu xử lý nén 2 tầng WebP cho toàn bộ 20 mẫu website...")
    total_original_kb = 0
    total_webp_kb = 0
    synced_records = []

    for item in DEFAULT_EVENT_WEBSITES:
        slug = item["domain"].replace(".", "_")
        png_path = os.path.join(ANH_CHUP_DIR, item["source_image"])
        
        orig_kb = round(os.path.getsize(png_path) / 1024, 1) if os.path.exists(png_path) else 0
        total_original_kb += orig_kb

        thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb = compress_tri_layer(png_path, slug)
        total_webp_kb += (thumb_kb + full_kb)

        record = dict(item)
        record["thumb_image"] = f"Kho_Anh_Webp/{thumb_name}"
        record["full_image"] = f"Kho_Anh_Webp/{full_name}"
        record["fb_image"] = f"Kho_Anh_Webp/{fb_name}"
        record["thumb_size_kb"] = thumb_kb
        record["full_size_kb"] = full_kb
        record["fb_size_kb"] = fb_kb
        record["orig_size_kb"] = orig_kb
        record["status"] = "approved"
        synced_records.append(record)

        print(f"  [+] {item['id']}. {item['short_name']:<25} | Gốc: {orig_kb:>6.1f} KB -> Thumb: {thumb_kb:>5.1f} KB, Full: {full_kb:>6.1f} KB, FB: {fb_kb:>6.1f} KB")

    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(synced_records, f, ensure_ascii=False, indent=2)

    reduction_pct = round((1 - (total_webp_kb / total_original_kb)) * 100, 1) if total_original_kb > 0 else 0
    print("\n[OK] ĐỒNG BỘ THÀNH CÔNG!")
    print(f"  - Tổng dung lượng ảnh gốc PNG:  {total_original_kb/1024:>6.2f} MB")
    print(f"  - Tổng dung lượng WebP (2 tầng): {total_webp_kb/1024:>6.2f} MB")
    print(f"  - Tỷ lệ giảm tải dung lượng:     {reduction_pct}%")
    print(f"  - Database lưu tại: {DB_PATH}")

if __name__ == "__main__":
    sync_all_default()
