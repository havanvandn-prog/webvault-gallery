import re

with open("_Luu_Tru_Ky_Thuat/01_Scripts_Bo_Tro/pipeline_sync.py", "r", encoding="utf-8") as f:
    text = f.read()

# Replace compress_dual_layer with compress_tri_layer
old_func = """def compress_dual_layer(source_png_path, slug):
    \"\"\"
    Tạo 2 phiên bản:
    1. full.webp (width 1440px, Q80) cho Lightbox
    2. thumb.webp (width 600px, Q75) cho Card list
    \"\"\"
    thumb_name = f"{slug}_thumb.webp"
    full_name = f"{slug}_full.webp"
    thumb_path = os.path.join(KHO_WEBP_DIR, thumb_name)
    full_path = os.path.join(KHO_WEBP_DIR, full_name)

    if not os.path.exists(source_png_path):
        print(f"[-] Không tìm thấy ảnh gốc: {source_png_path}")
        return None, None, 0, 0

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

    thumb_kb = round(os.path.getsize(thumb_path) / 1024, 1)
    full_kb = round(os.path.getsize(full_path) / 1024, 1)
    return thumb_name, full_name, thumb_kb, full_kb"""

new_func = """def compress_tri_layer(source_png_path, slug):
    \"\"\"
    Tạo sẵn 3 phiên bản tối ưu ngay từ đầu:
    1. full.webp (width 1440px, Q80) cho Lightbox phóng to
    2. thumb.webp (width 600px, Q75) cho Card list & hover scroll
    3. fb.png (chuẩn 1080x1920, 9:16 cắt từ đỉnh) để copy dán Facebook/Zalo tức thì (0ms chờ)
    \"\"\"
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
    return thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb"""

text = text.replace(old_func, new_func)

# Replace sync_all_default calls
old_sync = """        thumb_name, full_name, thumb_kb, full_kb = compress_dual_layer(png_path, slug)
        total_webp_kb += (thumb_kb + full_kb)

        record = dict(item)
        record["thumb_image"] = f"Kho_Anh_Webp/{thumb_name}"
        record["full_image"] = f"Kho_Anh_Webp/{full_name}"
        record["thumb_size_kb"] = thumb_kb
        record["full_size_kb"] = full_kb
        record["orig_size_kb"] = orig_kb
        record["status"] = "approved"
        synced_records.append(record)

        print(f"  [+] {item['id']}. {item['short_name']:<25} | Gốc: {orig_kb:>6.1f} KB -> Thumb: {thumb_kb:>5.1f} KB, Full: {full_kb:>6.1f} KB")"""

new_sync = """        thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb = compress_tri_layer(png_path, slug)
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

        print(f"  [+] {item['id']}. {item['short_name']:<25} | Gốc: {orig_kb:>6.1f} KB -> Thumb: {thumb_kb:>5.1f} KB, Full: {full_kb:>6.1f} KB, FB: {fb_kb:>6.1f} KB")"""

text = text.replace(old_sync, new_sync)

with open("_Luu_Tru_Ky_Thuat/01_Scripts_Bo_Tro/pipeline_sync.py", "w", encoding="utf-8") as f:
    f.write(text)
print("UPDATED PIPELINE")
