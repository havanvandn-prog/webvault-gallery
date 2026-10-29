# -*- coding: utf-8 -*-
import os, sys
from PIL import Image

def test_crop_and_compress():
    kho_dir = 'Kho_Anh_Webp'
    source_dir = 'Anh_Chup_Website'
    
    samples = [
        ('angeline.vn.png', 'angeline_vn'),
        ('hoangluanevent.com.png', 'hoangluanevent_com'),
        ('trangtrisinhnhatdanang.com.png', 'trangtrisinhnhatdanang_com')
    ]
    
    for png_name, slug in samples:
        png_path = os.path.join(source_dir, png_name)
        full_webp = os.path.join(kho_dir, f"{slug}_full.webp")
        thumb_webp = os.path.join(kho_dir, f"{slug}_thumb.webp")
        
        im = Image.open(png_path).convert('RGB')
        w, h = im.size
        print(f"Original {png_name}: {w}x{h}")
        
        # 1. Full-page WebP: KHÓA CHẶT WIDTH 1440px, crop nếu h > 15500
        target_h = min(h, 15500)
        im_full = im.crop((0, 0, 1440, target_h))
        im_full.save(full_webp, 'WEBP', quality=82, method=4)
        
        # 2. Thumb WebP: width 600px, tỷ lệ theo target_h
        thumb_h = int(target_h * (600.0 / 1440.0))
        im_thumb = im_full.resize((600, thumb_h), Image.Resampling.LANCZOS)
        im_thumb.save(thumb_webp, 'WEBP', quality=75, method=4)
        
        fw, fh = im_full.size
        tw, th = im_thumb.size
        print(f" -> Full WebP: {fw}x{fh} ({os.path.getsize(full_webp)//1024} KB)")
        print(f" -> Thumb WebP: {tw}x{th} ({os.path.getsize(thumb_webp)//1024} KB)")

if __name__ == '__main__':
    test_crop_and_compress()
