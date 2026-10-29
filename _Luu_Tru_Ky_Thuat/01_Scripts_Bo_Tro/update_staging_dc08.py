# -*- coding: utf-8 -*-
import json, re

def update_staging_dc08():
    with open('web_nhap_staging.html', 'r', encoding='utf-8') as f:
        html = f.read()

    old_dc08 = '''  {
    "id": "dc08",
    "name": "GU Decorate — Dịch Vụ Trang Trí Tiệc",
    "short_name": "GU Decorate",
    "url": "https://gudecorate.com/",
    "domain": "gudecorate.com",
    "vibe": "Bắt trend & Tươi sáng",
    "location": "TP.HCM",
    "thumb": "Kho_Anh_Webp/gudecorate_com_thumb.webp",
    "full": "Kho_Anh_Webp/gudecorate_com_full.webp",
    "desc": "Chuyên setup trọn gói backdrop tiệc sinh nhật người lớn, thôi nôi bé yêu, tiệc kỷ niệm ngày cưới và tiệc công ty. Nổi bật với các mẫu line bóng Chrome ánh kim và hoa tươi phối màu sang trọng."
  }'''

    new_dc08 = '''  {
    "id": "dc08",
    "name": "The Planners — Premium Wedding & Event Decor",
    "short_name": "The Planners",
    "url": "https://theplannersvn.com/",
    "domain": "theplannersvn.com",
    "vibe": "Châu Âu & Xa xỉ",
    "location": "Hà Nội & Toàn quốc",
    "thumb": "Kho_Anh_Webp/theplannersvn_com_thumb.webp",
    "full": "Kho_Anh_Webp/theplannersvn_com_full.webp",
    "desc": "Agency hàng đầu về tư vấn concept, thiết kế mỹ thuật và dàn dựng không gian tiệc cưới, sự kiện xa xỉ tại Việt Nam. Từng được vinh danh trên các tạp chí quốc tế danh tiếng WedLuxe, Harper's Bazaar và Elle."
  }'''

    if old_dc08 in html:
        html = html.replace(old_dc08, new_dc08)
    else:
        old_dc08_crlf = old_dc08.replace('\n', '\r\n')
        new_dc08_crlf = new_dc08.replace('\n', '\r\n')
        if old_dc08_crlf in html:
            html = html.replace(old_dc08_crlf, new_dc08_crlf)
        else:
            print("Error: old_dc08 not found")
            return

    with open('web_nhap_staging.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("SUCCESS: Updated dc08 to The Planners in web_nhap_staging.html")

if __name__ == '__main__':
    update_staging_dc08()
