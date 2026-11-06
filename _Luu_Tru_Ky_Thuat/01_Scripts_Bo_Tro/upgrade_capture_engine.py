# -*- coding: utf-8 -*-
import os
import sys

file_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts\capture_engine.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update selectors in setup_page_protection
old_sel = """        #introLux, .introAgency, [class*="splash-screen"], [class*="preloader-overlay"],
        [class*="site-intro"], [id*="site-intro"], [class*="welcome-overlay"], [id*="welcome-overlay"] {"""

new_sel = """        #introLux, .introAgency, [class*="splash-screen"], [class*="preloader-overlay"],
        [class*="site-intro"], [id*="site-intro"], [class*="welcome-overlay"], [id*="welcome-overlay"],
        #hv3-gate, .hv3-hero-sticky, .hv3-journey-sticky, #maydoAppointmentModal, .maydo-modal-backdrop,
        .lead-form-popup, .dialog-container {"""

# 2. Update check_for_blank_spaces
old_blank = """def check_for_blank_spaces(image_path, chunk_size=1000, white_threshold=98.0):
    \"\"\"Kiểm tra ảnh có bị khoảng trắng bất thường >1000px hay không.\"\"\"
    img = Image.open(image_path).convert('RGB')
    arr = np.array(img)
    h, w, _ = arr.shape
    for y in range(0, h - chunk_size, 500):
        chunk = arr[y:y+chunk_size, :, :]
        white_mask = (chunk[:,:,0] > 245) & (chunk[:,:,1] > 245) & (chunk[:,:,2] > 245)
        if (white_mask.mean() * 100) > white_threshold:
            return True, f"Khoảng trắng bất thường tại Y={y}-{y+chunk_size}"
    return False, "OK\""""

new_blank = """def check_for_blank_spaces(image_path, chunk_size=1000, white_threshold=98.0, min_std=3.0):
    \"\"\"Kiểm tra ảnh có bị khoảng trắng bất thường >1000px hay không (tự loại trừ phần thiết kế nền trắng có nội dung).\"\"\"
    img = Image.open(image_path).convert('RGB')
    arr = np.array(img)
    h, w, _ = arr.shape
    for y in range(0, h - chunk_size, 500):
        chunk = arr[y:y+chunk_size, :, :]
        white_mask = (chunk[:,:,0] > 245) & (chunk[:,:,1] > 245) & (chunk[:,:,2] > 245)
        # Chỉ báo lỗi nếu tỷ lệ trắng vượt ngưỡng VÀ độ lệch chuẩn cực thấp (< min_std: không có chữ/ảnh)
        if (white_mask.mean() * 100) > white_threshold and np.std(chunk) < min_std:
            return True, f"Khoảng trắng bất thường tại Y={y}-{y+chunk_size}"
    return False, "OK\""""

# Normalize newlines for replacement
norm_content = content.replace("\r\n", "\n")
norm_old_sel = old_sel.replace("\r\n", "\n")
norm_new_sel = new_sel.replace("\r\n", "\n")
norm_old_blank = old_blank.replace("\r\n", "\n")
norm_new_blank = new_blank.replace("\r\n", "\n")

if norm_old_sel in norm_content:
    norm_content = norm_content.replace(norm_old_sel, norm_new_sel)
    print("Replaced selectors in setup_page_protection successfully.")
else:
    print("Warning: old_sel not found.")

if norm_old_blank in norm_content:
    norm_content = norm_content.replace(norm_old_blank, norm_new_blank)
    print("Replaced check_for_blank_spaces successfully.")
else:
    print("Warning: old_blank not found.")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(norm_content)

print("Upgrade capture_engine.py completed!")
