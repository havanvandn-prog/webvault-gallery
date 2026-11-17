# -*- coding: utf-8 -*-
import json
import os
import sys
import subprocess

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
nt_meta_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "noi_that_metadata.json")
staging_json_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "staging_all_candidates.json")
build_script_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "01_Scripts_Bo_Tro", "build_multi_staging.py")
anh_dir = os.path.join(BASE_DIR, "Anh_Chup_Website")
webp_dir = os.path.join(BASE_DIR, "Kho_Anh_Webp")

skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)
from capture_engine import verify_captured_image

with open(nt_meta_path, "r", encoding="utf-8") as f:
    nt_data = json.load(f)

# Cập nhật nt14 -> Baya Việt Nam & nt20 -> HAY
for item in nt_data:
    if item["id"] == "nt14":
        item.update({
            "name": "Nội Thất Baya — Nội Thất & Gia Dụng Hiện Đại",
            "short_name": "Baya",
            "url": "https://baya.vn/",
            "domain": "baya.vn",
            "slug": "noi_that_baya",
            "industry": "noi-that",
            "industry_name": "Nội Thất & Kiến Trúc Không Gian",
            "category": "Modern Home Furniture & Living E-Commerce",
            "category_vn": "Showroom & Bán Lẻ Nội Thất Gia Đình Hiện Đại",
            "tag": "showroom-ecommerce",
            "vibe": "Tươi Sáng Gần Gũi • Phân Danh Mục Không Gian • Phối Cảnh Căn Hộ",
            "location": "TP.HCM & Hà Nội",
            "desc": "Thương hiệu nội thất và gia dụng quen thuộc cho căn hộ Việt Nam (tiền thân Uma). Giao diện sạch sẽ, phân luồng rõ ràng theo từng phòng (Khách, Ngủ, Ăn, Làm việc) kết hợp cẩm nang trang trí nhà cửa thực tiễn.",
            "image": "Anh_Chup_Website/noi_that_baya.png",
            "thumb": "Kho_Anh_Webp/noi_that_baya_thumb.webp",
            "full": "Kho_Anh_Webp/noi_that_baya_full.webp",
            "fb": "Kho_Anh_Webp/noi_that_baya_fb.png"
        })
    elif item["id"] == "nt20":
        item.update({
            "name": "HAY — Scandinavian Contemporary Design",
            "short_name": "HAY",
            "url": "https://www.hay.com/",
            "domain": "hay.com",
            "slug": "noi_that_hay",
            "industry": "noi-that",
            "industry_name": "Nội Thất & Kiến Trúc Không Gian",
            "category": "Danish Contemporary Furniture & Objects",
            "category_vn": "Thương Hiệu Nội Thất & Decor Đương Đại Đan Mạch",
            "tag": "global-luxury",
            "vibe": "Scandinavian Đương Đại • Khoảng Thở Nghệ Thuật • Sắc Màu Tinh Tế",
            "location": "Đan Mạch & Toàn cầu",
            "desc": "Thương hiệu thiết kế nội thất Đan Mạch nổi tiếng toàn cầu (thuộc tập đoàn MillerKnoll). Website tối giản chuẩn tạp chí nghệ thuật Bắc Âu, tôn vinh hình khối sản phẩm, màu sắc hài hòa và thư viện tài liệu cho kiến trúc sư.",
            "image": "Anh_Chup_Website/noi_that_hay.png",
            "thumb": "Kho_Anh_Webp/noi_that_hay_thumb.webp",
            "full": "Kho_Anh_Webp/noi_that_hay_full.webp",
            "fb": "Kho_Anh_Webp/noi_that_hay_fb.png"
        })

# Cập nhật kích thước & QA message cho toàn bộ 20 mẫu
for item in nt_data:
    slug = item["slug"]
    raw_png = os.path.join(anh_dir, f"{slug}.png")
    full_webp = os.path.join(webp_dir, f"{slug}_full.webp")
    thumb_webp = os.path.join(webp_dir, f"{slug}_thumb.webp")
    fb_png = os.path.join(webp_dir, f"{slug}_fb.png")

    valid, msg = verify_captured_image(full_webp)
    assert valid, f"Mẫu {item['id']} ({slug}) không đạt QA: {msg}"

    item["thumb_kb"] = round(os.path.getsize(thumb_webp) / 1024, 1)
    item["full_kb"] = round(os.path.getsize(full_webp) / 1024, 1)
    item["fb_kb"] = round(os.path.getsize(fb_png) / 1024, 1)
    item["size_mb"] = f"{round(os.path.getsize(raw_png) / (1024*1024), 2)} MB"
    item["audit_msg"] = msg
    item["status"] = "SUCCESS"

with open(nt_meta_path, "w", encoding="utf-8") as f:
    json.dump(nt_data, f, ensure_ascii=False, indent=2)
print(f"[+] Đã xác thực 20/20 mẫu Nội thất PASS 100% và lưu vào noi_that_metadata.json!")

# Dọn dẹp file ảnh thử nghiệm không dùng
unused_slugs = ["noi_that_makemyhome", "noi_that_vincentvanduysen", "noi_that_dergo", "noi_that_molteni"]
for us in unused_slugs:
    for p in [
        os.path.join(anh_dir, f"{us}.png"),
        os.path.join(webp_dir, f"{us}_full.webp"),
        os.path.join(webp_dir, f"{us}_thumb.webp"),
        os.path.join(webp_dir, f"{us}_fb.png"),
    ]:
        if os.path.exists(p):
            os.remove(p)
            print(f"  [cleanup] Đã xóa file dự phòng không dùng: {os.path.basename(p)}")

# Gộp vào staging_all_candidates.json
with open(staging_json_path, "r", encoding="utf-8") as f:
    existing = json.load(f)

existing_filtered = [item for item in existing if item.get("industry") != "noi-that"]
merged = nt_data + existing_filtered

with open(staging_json_path, "w", encoding="utf-8") as f:
    json.dump(merged, f, ensure_ascii=False, indent=2)

print(f"[+] Đã gộp {len(nt_data)} mẫu Nội thất vào staging_all_candidates.json (Tổng: {len(merged)} mẫu)")

# Cập nhật build_multi_staging.py
with open(build_script_path, "r", encoding="utf-8") as f:
    text = f.read()

if 'data-industry="noi-that"' not in text:
    old_tabs = """      <button class="staging-tab-btn" data-industry="all" onclick="filterStagingTopic('all')">
        <span>⚡</span> Tất Cả Nháp <span class="tab-badge" id="badgeAll">261</span>
      </button>
      <button class="staging-tab-btn active" data-industry="phong-thuy" onclick="filterStagingTopic('phong-thuy')">"""

    new_tabs = f"""      <button class="staging-tab-btn" data-industry="all" onclick="filterStagingTopic('all')">
        <span>⚡</span> Tất Cả Nháp <span class="tab-badge" id="badgeAll">{len(merged)}</span>
      </button>
      <button class="staging-tab-btn active" data-industry="noi-that" onclick="filterStagingTopic('noi-that')">
        <span>🛋️</span> Nội Thất <span class="tab-badge" id="badgeNoiThat">{len(nt_data)}</span>
      </button>
      <button class="staging-tab-btn" data-industry="phong-thuy" onclick="filterStagingTopic('phong-thuy')">"""

    assert old_tabs in text, "Không tìm thấy old_tabs trong build_multi_staging.py"
    text = text.replace(old_tabs, new_tabs, 1)

    old_topic = "let currentTopic = 'phong-thuy';"
    new_topic = "let currentTopic = 'noi-that';"
    assert old_topic in text, "Không tìm thấy old_topic"
    text = text.replace(old_topic, new_topic, 1)

    old_param = "const indParam = params.get('industry') || params.get('topic') || 'phong-thuy';"
    new_param = "const indParam = params.get('industry') || params.get('topic') || 'noi-that';"
    assert old_param in text, "Không tìm thấy old_param"
    text = text.replace(old_param, new_param, 1)

    old_map = "const topicMapName = {"
    new_map = """const topicMapName = {
      'noi-that': 'Nội Thất & Kiến Trúc Không Gian (Studio Luxury, Thi Công Trọn Gói & Showroom E-Commerce)',"""
    assert old_map in text, "Không tìm thấy old_map"
    text = text.replace(old_map, new_map, 1)

    old_badge = "if (document.getElementById('badgePhongThuy'))"
    new_badge = """if (document.getElementById('badgeNoiThat')) document.getElementById('badgeNoiThat').textContent = CANDIDATES.filter(c => c.industry === 'noi-that').length;
    if (document.getElementById('badgePhongThuy'))"""
    assert old_badge in text, "Không tìm thấy old_badge"
    text = text.replace(old_badge, new_badge, 1)

    with open(build_script_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("[+] Đã cập nhật build_multi_staging.py với tab Nội Thất!")
else:
    print("[i] build_multi_staging.py đã có tab noi-that từ trước.")

# Chạy build_multi_staging.py để xuất web_nhap_staging.html
res = subprocess.run([sys.executable, build_script_path], capture_output=True, text=True, encoding="utf-8")
print("[+] Build output:", res.stdout.strip())
if res.returncode != 0:
    print("[-] Build error:", res.stderr)
    sys.exit(1)
