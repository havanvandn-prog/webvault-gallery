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
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "du_lich_metadata.json")

os.makedirs(output_dir, exist_ok=True)
os.makedirs(kho_webp_dir, exist_ok=True)
os.makedirs(os.path.dirname(metadata_file), exist_ok=True)

websites = [
    {
        "id": "dl01",
        "name": "Vietnam Tourism — Cổng Du Lịch Quốc Gia",
        "short_name": "Vietnam.travel",
        "domain": "vietnam.travel",
        "url": "https://vietnam.travel/",
        "industry": "du-lich",
        "industry_name": "Du Lịch & Tour Du Lịch",
        "tag": "national-board",
        "category": "Cổng Du Lịch Quốc Gia",
        "category_vn": "Cổng Du Lịch Quốc Gia",
        "vibe": "editorial",
        "vibe_name": "Editorial & Tạp chí Du lịch",
        "location": "Toàn quốc & Quốc tế",
        "desc": "Cổng thông tin du lịch chính thức của Tổng cục Du lịch Việt Nam. Thiết kế visual storytelling ấn tượng, hình ảnh phong cảnh 4K tuyệt mỹ, tôn vinh văn hóa di sản, ẩm thực và danh lam thắng cảnh Việt Nam vươn tầm thế giới."
    },
    {
        "id": "dl02",
        "name": "Lily's Travel Agency",
        "short_name": "Lily's Travel",
        "domain": "lilystravelagency.com",
        "url": "https://lilystravelagency.com/",
        "industry": "du-lich",
        "industry_name": "Du Lịch & Tour Du Lịch",
        "tag": "tour-operator",
        "category": "Tour Lữ Hành & Trải Nghiệm",
        "category_vn": "Công Ty Lữ Hành & Tour Trải Nghiệm",
        "vibe": "vibrant",
        "vibe_name": "Trẻ trung & Năng động",
        "location": "Hà Nội & Miền Bắc",
        "desc": "Công ty lữ hành hàng đầu đạt chứng nhận xuất sắc TripAdvisor Travelers' Choice. Chuyên các tour khám phá miền Bắc (Hà Giang, Sa Pa, Ninh Bình, Vịnh Hạ Long) và tour trọn gói xuyên Việt cho du khách quốc tế."
    },
    {
        "id": "dl03",
        "name": "Local Vietnam Tours & Travel Guide",
        "short_name": "Local Vietnam",
        "domain": "localvietnam.com",
        "url": "https://localvietnam.com/",
        "industry": "du-lich",
        "industry_name": "Du Lịch & Tour Du Lịch",
        "tag": "boutique-travel",
        "category": "Boutique Tour & Cẩm Nang Bản Địa",
        "category_vn": "Boutique Tour & Cẩm Nang Bản Địa",
        "vibe": "corporate",
        "vibe_name": "Chuyên nghiệp & Bản địa",
        "location": "Toàn quốc & Quốc tế",
        "desc": "Nền tảng du lịch trải nghiệm bản địa chuyên sâu (Authentic Local Experiences) và cẩm nang du lịch toàn diện Việt Nam cho du khách toàn cầu. Bố cục hiện đại, thông tin lịch trình minh bạch và chuẩn SEO quốc tế."
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

print("=== BẮT ĐẦU CHỤP FULL-PAGE 3 WEBSITE NGÀNH DU LỊCH ===", flush=True)

final_metadata = []

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=[
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
            "--disable-blink-features=AutomationControlled"
        ]
    )
    context = browser.new_context(
        viewport={"width": 1440, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        locale="en-US",
        timezone_id="Asia/Ho_Chi_Minh"
    )

    for idx, item in enumerate(websites, start=1):
        filename = f"{item['domain']}.png"
        filepath = os.path.join(output_dir, filename)
        slug = item["domain"].replace(".", "_")
        print(f"\n[{idx}/3] Đang xử lý: {item['name']} -> {item['url']}...", flush=True)
        start_t = time.time()

        # Nếu file đã tồn tại và hợp lệ (> 100KB) thì tái sử dụng hoặc nén lại
        if os.path.exists(filepath) and os.path.getsize(filepath) > 500 * 1024:
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            print(f"  -> File ảnh đã tồn tại hợp lệ: {filename} ({size_mb:.2f} MB), tiến hành nén WebP 3 tầng...", flush=True)
            orig_kb = round(os.path.getsize(filepath) / 1024, 1)
            thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb = compress_tri_layer(filepath, slug)
            record = {
                **item,
                "source_image": filename,
                "thumb": f"Kho_Anh_Webp/{thumb_name}",
                "full": f"Kho_Anh_Webp/{full_name}",
                "fb": f"Kho_Anh_Webp/{fb_name}",
                "thumb_kb": thumb_kb,
                "full_kb": full_kb,
                "fb_kb": fb_kb,
                "orig_kb": orig_kb,
                "status": "SUCCESS"
            }
            final_metadata.append(record)
            continue

        success = False
        res_info = (1440, 900)

        # Mở page riêng cho từng site
        page = context.new_page()
        try:
            # Bypass một số anti-bot đơn giản
            page.set_extra_http_headers({
                "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
                "Sec-Ch-Ua": '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": '"Windows"'
            })

            page.goto(item['url'], wait_until="domcontentloaded", timeout=45000)
            time.sleep(3)
            res_info = capture_smart_clean(page, filepath)
            is_blank, reason = check_for_blank_spaces(filepath)
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            print(f"  -> THÀNH CÔNG (Smart Clean): {filename} ({res_info[0]}x{res_info[1]}, {size_mb:.2f} MB, {time.time()-start_t:.1f}s, Blank: {reason})", flush=True)
            success = True
        except Exception as e:
            print(f"  -> Smart Clean gặp lỗi: {e}, thử Fallback Full-page...", flush=True)
            try:
                page.goto(item['url'], wait_until="load", timeout=35000)
                time.sleep(3)
                page.screenshot(path=filepath, full_page=True)
                size_mb = os.path.getsize(filepath) / (1024 * 1024)
                print(f"  -> Fallback Full-page thành công: {filename} ({size_mb:.2f} MB)", flush=True)
                success = True
            except Exception as e2:
                print(f"  -> THẤT BẠI: {e2}", flush=True)
        finally:
            try:
                page.close()
            except Exception:
                pass

        if success:
            orig_kb = round(os.path.getsize(filepath) / 1024, 1)
            thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb = compress_tri_layer(filepath, slug)
            record = {
                **item,
                "source_image": filename,
                "thumb": f"Kho_Anh_Webp/{thumb_name}",
                "full": f"Kho_Anh_Webp/{full_name}",
                "fb": f"Kho_Anh_Webp/{fb_name}",
                "thumb_kb": thumb_kb,
                "full_kb": full_kb,
                "fb_kb": fb_kb,
                "orig_kb": orig_kb,
                "status": "SUCCESS"
            }
            final_metadata.append(record)
            print(f"  -> Nén WebP 3 tầng hoàn tất: Thumb={thumb_kb}KB, Full={full_kb}KB, FB={fb_kb}KB", flush=True)
        else:
            final_metadata.append({
                **item,
                "source_image": filename,
                "status": "FAILED"
            })

    browser.close()

with open(metadata_file, "w", encoding="utf-8") as f:
    json.dump(final_metadata, f, ensure_ascii=False, indent=2)

print(f"\n=== HOÀN TẤT CHỤP 3 WEBSITE DU LỊCH! Đã lưu metadata vào {metadata_file} ===", flush=True)
