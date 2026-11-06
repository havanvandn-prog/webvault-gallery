# -*- coding: utf-8 -*-
file_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts\capture_engine.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_popup = """    for i in range(len(center_chunks) - 1):
        y1, c1 = center_chunks[i]
        y2, c2 = center_chunks[i+1]
        if c1.shape == c2.shape:
            diff = np.mean(np.abs(c1.astype(int) - c2.astype(int)))
            if diff < diff_threshold:
                return True, f"Phát hiện Popup/Modal khuyến mãi lặp lại tại vùng trung tâm (Y={y1} và Y={y2}, diff={diff:.2f})\""""

new_popup = """    for i in range(len(center_chunks) - 1):
        y1, c1 = center_chunks[i]
        y2, c2 = center_chunks[i+1]
        if c1.shape == c2.shape:
            diff = np.mean(np.abs(c1.astype(int) - c2.astype(int)))
            is_mostly_white = ((c1 > 245).mean() > 0.90) and ((c2 > 245).mean() > 0.90)
            if not is_mostly_white and diff < diff_threshold:
                return True, f"Phát hiện Popup/Modal khuyến mãi lặp lại tại vùng trung tâm (Y={y1} và Y={y2}, diff={diff:.2f})"
            elif is_mostly_white and diff < 1.0:
                return True, f"Phát hiện Popup/Modal khuyến mãi lặp lại tại vùng trung tâm (Y={y1} và Y={y2}, diff={diff:.2f})\""""

norm_content = content.replace("\r\n", "\n")
norm_old = old_popup.replace("\r\n", "\n")
norm_new = new_popup.replace("\r\n", "\n")

if norm_old in norm_content:
    norm_content = norm_content.replace(norm_old, norm_new)
    print("Updated check_for_repeated_center_popup successfully.")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(norm_content)
else:
    print("Warning: old_popup target not found.")
