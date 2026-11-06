# -*- coding: utf-8 -*-
import os
import sys

path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts\capture_engine.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update setup_page_protection
old_eval = """            const originalEval = window.eval;
            try {
                Object.defineProperty(window, 'eval', {
                    get: () => originalEval,
                    set: () => {},
                    configurable: false
                });
            } catch (e) {}"""

new_eval = """            const originalEval = window.eval;
            try {
                Object.defineProperty(window, 'eval', {
                    get: () => originalEval,
                    set: () => {},
                    configurable: false
                });
            } catch (e) {}

            // Bảo vệ window.scrollTo khỏi bị script theme tùy biến ghi đè dạng function scrollTo(id, minusTop)
            try {
                window.scrollTo = function(x, y) {
                    const targetY = (typeof x === 'object' && x !== null && x.top !== undefined) ? x.top : ((typeof x === 'number') ? x : 0);
                    document.documentElement.scrollTop = targetY;
                    document.body.scrollTop = targetY;
                };
            } catch (e) {}"""

if old_eval in content:
    content = content.replace(old_eval, new_eval)
    print("[+] Patched setup_page_protection with safe window.scrollTo")
else:
    print("[*] setup_page_protection already patched or pattern not found")

# 2. Update safe scrolling in capture_smart_clean
old_scroll_1 = 'page.evaluate(f"window.scrollTo(0, {y})")'
new_scroll_1 = '''page.evaluate(f"""() => {{
            const ty = {y};
            try {{ window.scrollTo(0, ty); }} catch(e) {{}}
            document.documentElement.scrollTop = ty;
            document.body.scrollTop = ty;
        }}""")'''

if old_scroll_1 in content:
    content = content.replace(old_scroll_1, new_scroll_1)
    print("[+] Patched page.evaluate(scrollTo) step 1")

old_scroll_2 = 'page.evaluate("window.scrollTo(0, 0)")'
new_scroll_2 = '''page.evaluate("""() => {
        try { window.scrollTo(0, 0); } catch(e) {}
        document.documentElement.scrollTop = 0;
        document.body.scrollTop = 0;
    }""")'''

if old_scroll_2 in content:
    content = content.replace(old_scroll_2, new_scroll_2)
    print("[+] Patched page.evaluate(scrollTo) step 2")

# 3. Update check_for_repeated_header with foreground verification
old_header_func = '''def check_for_repeated_header(image_path, chunk_height=900, header_height=80, diff_threshold=8.0):
    """
    Kiểm tra xem Header đỉnh trang có bị lặp lại ở giữa các mối nối khung hình hay không.
    """
    img = Image.open(image_path).convert('RGB')
    arr = np.array(img)
    h, w, _ = arr.shape
    if h < chunk_height * 2:
        return False, "OK"

    top_header = arr[0:header_height, :, :]
    for step_y in range(chunk_height, h - header_height, chunk_height):
        sub_slice = arr[step_y:step_y + header_height, :, :]
        if sub_slice.shape == top_header.shape:
            diff = np.mean(np.abs(top_header.astype(int) - sub_slice.astype(int)))
            if diff < diff_threshold:
                return True, f"Phát hiện Header bị lặp lại tại mối nối Y={step_y} (diff={diff:.2f})"

    return False, "OK"'''

new_header_func = '''def check_for_repeated_header(image_path, chunk_height=900, header_height=80, diff_threshold=8.0):
    """
    Kiểm tra xem Header đỉnh trang có bị lặp lại ở giữa các mối nối khung hình hay không.
    Tự động phân tích màu nền và chi tiết tiền cảnh (Foreground: logo, text) để loại bỏ 100%
    cảnh báo giả khi mối nối chỉ là một dải nền đơn sắc (trắng, kem, be, đen).
    """
    img = Image.open(image_path).convert('RGB')
    arr = np.array(img)
    h, w, _ = arr.shape
    if h < chunk_height * 2:
        return False, "OK"

    top_header = arr[0:header_height, :, :]
    
    # Ước lượng màu nền chủ đạo của top header
    bg_color = np.median(top_header.reshape(-1, 3), axis=0)
    # Xác định các pixel tiền cảnh (chữ, logo, icon, menu items)
    top_dist = np.linalg.norm(top_header.astype(float) - bg_color, axis=2)
    foreground_mask = top_dist > 25.0
    has_foreground = np.sum(foreground_mask) > 500

    for step_y in range(chunk_height, h - header_height, chunk_height):
        sub_slice = arr[step_y:step_y + header_height, :, :]
        if sub_slice.shape == top_header.shape:
            diff = np.mean(np.abs(top_header.astype(int) - sub_slice.astype(int)))
            if has_foreground:
                # Nếu header có chữ/logo: chỉ báo lỗi khi chữ/logo lặp lại ở mối nối
                fg_diff = np.mean(np.abs(top_header[foreground_mask].astype(int) - sub_slice[foreground_mask].astype(int)))
                if fg_diff < 15.0 and diff < diff_threshold:
                    return True, f"Phát hiện Header bị lặp lại tại mối nối Y={step_y} (fg_diff={fg_diff:.2f}, diff={diff:.2f})"
            else:
                # Nếu header là khối đơn sắc hoàn toàn: siết ngưỡng diff cực thấp < 2.0 để tránh nhầm lẫn nền cùng màu
                if diff < 2.0:
                    return True, f"Phát hiện Header bị lặp lại tại mối nối Y={step_y} (diff={diff:.2f})"

    return False, "OK"'''

if old_header_func in content:
    content = content.replace(old_header_func, new_header_func)
    print("[+] Patched check_for_repeated_header with intelligent foreground detection")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("[+] Successfully completed capture_engine.py upgrade!")
