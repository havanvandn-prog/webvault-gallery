# -*- coding: utf-8 -*-
import os
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
index_path = os.path.join(BASE_DIR, "index.html")

with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Sidebar Navigation
old_nav_section = """    <!-- TIER 1: NGÀNH NGHỀ -->
    <div class="sidebar-section">
      <div class="sidebar-title">Ngành Nghề & Lĩnh Vực</div>
      <ul class="nav-list">
        <li class="nav-item active" onclick="setIndustry('all', this)">
          <span>Tất Cả Danh Mục</span>
          <span class="nav-count" id="countAll">20</span>
        </li>
        <li class="nav-item" onclick="setIndustry('su-kien', this)">
          <span>Sự Kiện & Activation</span>
          <span class="nav-count">20</span>
        </li>
        <li class="nav-item" style="opacity: 0.45; cursor: not-allowed;" title="Sắp nạp dữ liệu">
          <span>Bất Động Sản</span>
          <span class="nav-count">Sắp có</span>
        </li>"""

new_nav_section = """    <!-- TIER 1: NGÀNH NGHỀ -->
    <div class="sidebar-section">
      <div class="sidebar-title">Ngành Nghề & Lĩnh Vực</div>
      <ul class="nav-list">
        <li class="nav-item active" onclick="setIndustry('all', this)">
          <span>Tất Cả Danh Mục</span>
          <span class="nav-count" id="countAll">23</span>
        </li>
        <li class="nav-item" onclick="setIndustry('su-kien', this)">
          <span>Sự Kiện & Activation</span>
          <span class="nav-count">20</span>
        </li>
        <li class="nav-item" onclick="setIndustry('du-lich', this)">
          <span>Du Lịch & Tour Du Lịch</span>
          <span class="nav-count">3</span>
        </li>
        <li class="nav-item" style="opacity: 0.45; cursor: not-allowed;" title="Sắp nạp dữ liệu">
          <span>Bất Động Sản</span>
          <span class="nav-count">Sắp có</span>
        </li>"""

if old_nav_section in content:
    content = content.replace(old_nav_section, new_nav_section)
    print("[+] Da cap nhat TIER 1 Nganh nghe!")
else:
    # Normalize line breaks
    content_norm = content.replace("\r\n", "\n")
    old_nav_norm = old_nav_section.replace("\r\n", "\n")
    new_nav_norm = new_nav_section.replace("\r\n", "\n")
    if old_nav_norm in content_norm:
        content_norm = content_norm.replace(old_nav_norm, new_nav_norm)
        content = content_norm
        print("[+] Da cap nhat TIER 1 Nganh nghe (LF)!")

# 2. Update Vibe counts
content = content.replace(
    '<span>Editorial & Tối giản</span>\n          <span class="nav-count">1</span>',
    '<span>Editorial & Tối giản</span>\n          <span class="nav-count">2</span>'
).replace(
    '<span>Editorial & Tối giản</span>\r\n          <span class="nav-count">1</span>',
    '<span>Editorial & Tối giản</span>\r\n          <span class="nav-count">2</span>'
)

content = content.replace(
    '<span>Tập đoàn & Uy tín</span>\n          <span class="nav-count">7</span>',
    '<span>Tập đoàn & Uy tín</span>\n          <span class="nav-count">8</span>'
).replace(
    '<span>Tập đoàn & Uy tín</span>\r\n          <span class="nav-count">7</span>',
    '<span>Tập đoàn & Uy tín</span>\r\n          <span class="nav-count">8</span>'
)

content = content.replace(
    '<span>Trẻ trung & Năng động</span>\n          <span class="nav-count">4</span>',
    '<span>Trẻ trung & Năng động</span>\n          <span class="nav-count">5</span>'
).replace(
    '<span>Trẻ trung & Năng động</span>\r\n          <span class="nav-count">4</span>',
    '<span>Trẻ trung & Năng động</span>\r\n          <span class="nav-count">5</span>'
)

# 3. Update Location counts
content = content.replace(
    '<span>Hà Nội</span>\n          <span class="nav-count">8</span>',
    '<span>Hà Nội</span>\n          <span class="nav-count">9</span>'
).replace(
    '<span>Hà Nội</span>\r\n          <span class="nav-count">8</span>',
    '<span>Hà Nội</span>\r\n          <span class="nav-count">9</span>'
)

# 4. Insert 3 travel websites into WEBSITES_DATA
travel_items_js = """,
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
    }
  ];"""

# Replace the closing of WEBSITES_DATA
old_end_data_lf = '        "fb_kb": 1249.1\n    }\n  ];'
old_end_data_crlf = '        "fb_kb": 1249.1\r\n    }\r\n  ];'

if old_end_data_crlf in content:
    content = content.replace(old_end_data_crlf, '        "fb_kb": 1249.1\r\n    }' + travel_items_js.replace('\n', '\r\n'))
    print("[+] Da nap 3 website du lich vao WEBSITES_DATA (CRLF)!")
elif old_end_data_lf in content:
    content = content.replace(old_end_data_lf, '        "fb_kb": 1249.1\n    }' + travel_items_js)
    print("[+] Da nap 3 website du lich vao WEBSITES_DATA (LF)!")
else:
    print("[-] Kiem tra closing cua WEBSITES_DATA...")

# Quick link in header
old_actions = """        <a href="web_nhap_staging.html" class="btn btn-secondary">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path></svg>
          Trạm Kiểm Duyệt Nháp
        </a>"""

new_actions = """        <a href="preview_mau_website_du_lich.html" class="btn btn-secondary" style="border-color: #0284c7; color: #38bdf8;">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"></polygon></svg>
          Bộ Mẫu Du Lịch
        </a>

        <a href="web_nhap_staging.html" class="btn btn-secondary">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path></svg>
          Trạm Kiểm Duyệt Nháp
        </a>"""

content_norm = content.replace("\r\n", "\n")
old_actions_norm = old_actions.replace("\r\n", "\n")
new_actions_norm = new_actions.replace("\r\n", "\n")
if old_actions_norm in content_norm:
    content_norm = content_norm.replace(old_actions_norm, new_actions_norm)
    content = content_norm
    print("[+] Da them link Bo Mau Du Lich vao Top Header!")

with open(index_path, "w", encoding="utf-8") as f:
    f.write(content)

print("[SUCCESS] Da cap nhat index.html thanh cong!")
