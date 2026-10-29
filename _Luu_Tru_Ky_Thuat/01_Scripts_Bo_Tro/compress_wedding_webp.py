# -*- coding: utf-8 -*-
import os, sys, json
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
kho_webp_dir = os.path.join(BASE_DIR, "Kho_Anh_Webp")
wedding_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "wedding_metadata.json")

with open(wedding_file, "r", encoding="utf-8") as f:
    items = json.load(f)

print(f"Compressing {len(items)} wedding websites...")

for it in items:
    png_path = os.path.join(BASE_DIR, it["image"])
    slug = it["domain"].replace(".", "_")
    thumb_name = f"{slug}_thumb.webp"
    full_name = f"{slug}_full.webp"
    fb_name = f"{slug}_fb.png"
    thumb_path = os.path.join(kho_webp_dir, thumb_name)
    full_path = os.path.join(kho_webp_dir, full_name)
    fb_path = os.path.join(kho_webp_dir, fb_name)
    
    if os.path.exists(thumb_path) and os.path.getsize(thumb_path) > 10 * 1024:
        it["thumb"] = f"Kho_Anh_Webp/{thumb_name}"
        it["full"] = f"Kho_Anh_Webp/{full_name}"
        it["fb"] = f"Kho_Anh_Webp/{fb_name}"
        continue

    if os.path.exists(png_path):
        with Image.open(png_path) as im:
            im_rgb = im.convert("RGB")
            w, h = im_rgb.size
            if h > 15500:
                scale = 15500.0 / h
                new_w = int(w * scale)
                im_full = im_rgb.resize((new_w, 15500), Image.Resampling.LANCZOS)
            else:
                im_full = im_rgb
            im_full.save(full_path, "WEBP", quality=80, method=4)

            new_w = 600
            new_h = min(15500, int(h * (new_w / w)))
            im_thumb = im_rgb.resize((new_w, new_h), Image.Resampling.LANCZOS)
            im_thumb.save(thumb_path, "WEBP", quality=75, method=4)

            slice_h = min(h, int(w * 16 / 9))
            crop = im_rgb.crop((0, 0, w, slice_h))
            im_fb = crop.resize((1080, 1920), Image.Resampling.LANCZOS)
            im_fb.save(fb_path, format="PNG", optimize=True)

        it["thumb"] = f"Kho_Anh_Webp/{thumb_name}"
        it["full"] = f"Kho_Anh_Webp/{full_name}"
        it["fb"] = f"Kho_Anh_Webp/{fb_name}"
        print(f"  [+] Compressed {slug}")

with open(wedding_file, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

print("Wedding compression complete!")
