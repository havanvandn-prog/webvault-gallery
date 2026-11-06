# -*- coding: utf-8 -*-
file_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts\capture_engine.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace overly broad lightbox selector with precise modal selectors
old_str = """        [class*="dialog"], [id*="dialog"],
        [class*="lightbox"], [id*="lightbox"],
        [class*="banner-ads"], [class*="adv-popup"],"""

new_str = """        [class*="dialog"], [id*="dialog"],
        .mfp-wrap, .mfp-bg, .mfp-container, .fancybox-container, div.lightbox-modal,
        [class*="banner-ads"], [class*="adv-popup"],"""

norm_content = content.replace("\r\n", "\n")
norm_old = old_str.replace("\r\n", "\n")
norm_new = new_str.replace("\r\n", "\n")

if norm_old in norm_content:
    norm_content = norm_content.replace(norm_old, norm_new)
    print("Fixed lightbox selector successfully.")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(norm_content)
else:
    print("Warning: old_str not found.")
