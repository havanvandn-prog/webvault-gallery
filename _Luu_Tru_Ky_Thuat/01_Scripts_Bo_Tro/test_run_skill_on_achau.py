import os
import sys
import time

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

# Import trực tiếp từ bộ mã nguồn của Skill tim-mau-website
skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)
from capture_engine import capture_smart_clean, check_for_blank_spaces

from playwright.sync_api import sync_playwright
from PIL import Image
import numpy as np

target_url = "https://sukienachau.com/"
output_file = r"D:\AI Agent\Website\Tìm mẫu website\Anh_Chup_Website\sukienachau.com.png"

print(f"=== BẮT ĐẦU CHẠY THỬ NGHIỆM SKILL TIM-MAU-WEBSITE TRÊN: {target_url} ===")
start_t = time.time()

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
    )
    context = browser.new_context(
        viewport={"width": 1440, "height": 900},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    )
    page = context.new_page()
    
    print("1. Đang truy cập website...")
    page.goto(target_url, wait_until="domcontentloaded", timeout=40000)
    time.sleep(2.5)
    
    print("2. Đang kích hoạt capture_smart_clean từ capture_engine của Skill...")
    w, h = capture_smart_clean(page, output_file)
    elapsed = time.time() - start_t
    
    context.close()
    browser.close()

print(f"3. Đã chụp xong: {w}x{h} px sau {elapsed:.1f}s")

# --- KIỂM TRA CHẤT LƯỢNG ẢNH TỰ ĐỘNG ---
print("\n--- BẮT ĐẦU KIỂM ĐỊNH KỸ THUẬT ---")
img = Image.open(output_file).convert('RGB')
arr = np.array(img)
h_img, w_img, _ = arr.shape

# A. Kiểm tra màu hồng của thanh footer-additional: rgb(245, 0, 87)
# Quét dải màu hồng xung quanh tọa độ cũ (Y=700..1100)
chunk_test = arr[700:1100, :, :]
pink_mask = (chunk_test[:,:,0] > 220) & (chunk_test[:,:,1] < 40) & (chunk_test[:,:,2] > 50) & (chunk_test[:,:,2] < 130)
pink_pixels_at_old_spot = pink_mask.sum()
print(f"Số lượng pixel màu hồng tại vị trí cũ (Y=700..1100): {pink_pixels_at_old_spot} pixels")

# B. Kiểm tra toàn bộ ảnh xem có dải màu ngang nào kéo dài 100% không
has_horizontal_bar = False
for y in range(500, h_img - 200):
    row = arr[y, :, :]
    # nếu 90% pixel trong 1 hàng có màu hồng
    pink_row = (row[:,0] > 220) & (row[:,1] < 40) & (row[:,2] > 50) & (row[:,2] < 130)
    if pink_row.mean() > 0.6:
        has_horizontal_bar = True
        print(f"CẢNH BÁO: Phát hiện vạch ngang màu hồng tại Y={y}")
        break

if not has_horizontal_bar and pink_pixels_at_old_spot == 0:
    print("KẾT QUẢ KIỂM ĐỊNH: [PASS] - THANH NGANG MÀU HỒNG ĐÃ ĐƯỢC LOẠI BỎ 100%!")
else:
    print("KẾT QUẢ KIỂM ĐỊNH: [FAIL] - Vẫn còn phát hiện thanh màu hồng!")

# C. Quét khoảng trắng
is_blank, blank_msg = check_for_blank_spaces(output_file)
print(f"Kiểm tra khoảng trắng: {blank_msg}")
