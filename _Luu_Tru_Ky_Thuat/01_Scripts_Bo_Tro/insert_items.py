# -*- coding: utf-8 -*-
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

travel_items_js = """
    {
        "id": "21",
        "name": "Vietnam Tourism — Cổng Du Lịch Quốc Gia",
        "short_name": "Vietnam Tourism",
        "url": "https://vietnam.travel/",
        "domain": "vietnam.travel",
        "industry": "du-lich",
        "tag": "national-board",
        "vibe": "editorial",
        "vibe_name": "Editorial & Tạp chí Du lịch",
        "location": "Toàn quốc & Quốc tế",
        "desc": "Cổng thông tin du lịch chính thức của Tổng cục Du lịch Việt Nam. Thiết kế visual storytelling ấn tượng, hình ảnh phong cảnh 4K tuyệt mỹ, tôn vinh văn hóa di sản, ẩm thực và danh lam thắng cảnh Việt Nam vươn tầm thế giới.",
        "thumb": "Kho_Anh_Webp/vietnam_travel_thumb.webp",
        "full": "Kho_Anh_Webp/vietnam_travel_full.webp",
        "fb": "Kho_Anh_Webp/vietnam_travel_fb.png",
        "thumb_kb": 143.7,
        "full_kb": 691.1,
        "fb_kb": 1262.1
    },
    {
        "id": "22",
        "name": "Lily's Travel Agency",
        "short_name": "Lily's Travel",
        "url": "https://lilystravelagency.com/",
        "domain": "lilystravelagency.com",
        "industry": "du-lich",
        "tag": "tour-operator",
        "vibe": "vibrant",
        "vibe_name": "Trẻ trung & Năng động",
        "location": "Hà Nội & Miền Bắc",
        "desc": "Công ty lữ hành hàng đầu đạt chứng nhận xuất sắc TripAdvisor Travelers' Choice. Chuyên các tour khám phá miền Bắc (Hà Giang, Sa Pa, Ninh Bình, Vịnh Hạ Long) và tour trọn gói xuyên Việt cho du khách quốc tế.",
        "thumb": "Kho_Anh_Webp/lilystravelagency_com_thumb.webp",
        "full": "Kho_Anh_Webp/lilystravelagency_com_full.webp",
        "fb": "Kho_Anh_Webp/lilystravelagency_com_fb.png",
        "thumb_kb": 94.3,
        "full_kb": 395.2,
        "fb_kb": 1460.9
    },
    {
        "id": "23",
        "name": "Local Vietnam Tours & Travel Guide",
        "short_name": "Local Vietnam",
        "url": "https://localvietnam.com/",
        "domain": "localvietnam.com",
        "industry": "du-lich",
        "tag": "boutique-travel",
        "vibe": "corporate",
        "vibe_name": "Chuyên nghiệp & Bản địa",
        "location": "Toàn quốc & Quốc tế",
        "desc": "Nền tảng du lịch trải nghiệm bản địa chuyên sâu (Authentic Local Experiences) và cẩm nang du lịch toàn diện Việt Nam cho du khách toàn cầu. Bố cục hiện đại, thông tin lịch trình minh bạch và chuẩn SEO quốc tế.",
        "thumb": "Kho_Anh_Webp/localvietnam_com_thumb.webp",
        "full": "Kho_Anh_Webp/localvietnam_com_full.webp",
        "fb": "Kho_Anh_Webp/localvietnam_com_fb.png",
        "thumb_kb": 262.6,
        "full_kb": 1047.3,
        "fb_kb": 1964.1
    }"""

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = '        "fb_kb": 1249.1\n    }\n];'
target_crlf = '        "fb_kb": 1249.1\r\n    }\r\n];'

if target_crlf in text:
    replacement = '        "fb_kb": 1249.1\r\n    },' + travel_items_js.replace('\n', '\r\n') + '\r\n];'
    text = text.replace(target_crlf, replacement)
    print('[+] Inserted with CRLF')
elif target in text:
    replacement = '        "fb_kb": 1249.1\n    },' + travel_items_js + '\n];'
    text = text.replace(target, replacement)
    print('[+] Inserted with LF')
else:
    print('[-] Target not found')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('[+] Hoàn tất cập nhật WEBSITES_DATA trong index.html!')
