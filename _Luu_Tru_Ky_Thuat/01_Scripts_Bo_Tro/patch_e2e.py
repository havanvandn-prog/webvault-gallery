with open('_Luu_Tru_Ky_Thuat/01_Scripts_Bo_Tro/test_e2e_features.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_test5 = """    # 5. Test Copy Comment FB
    print("[TEST 5] Nút Copy Comment FB")
    page.locator(".btn-fb-text").first.click()
    page.wait_for_timeout(300)
    toast_text = page.locator("#toastMsg").text_content()
    print(f"   -> Thông báo Toast: {toast_text}")
    assert "copy" in toast_text.lower(), f"Lỗi Toast: {toast_text}"

    # 6. Test Copy Ảnh FB (1080x1920)
    print("[TEST 6] Nút Copy Ảnh FB (1080x1920)")
    page.locator(".btn-fb-image").first.click()
    page.wait_for_timeout(500)
    toast_img_text = page.locator("#toastMsg").text_content()
    print(f"   -> Thông báo Toast sau khi bấm copy ảnh: {toast_img_text}")
    assert "1080x1920" in toast_img_text or "nạp ảnh" in toast_img_text.lower() or "ảnh" in toast_img_text.lower(), f"Lỗi copy ảnh: {toast_img_text}" """

new_test5 = """    # 5. Test Nút Truy cập Website ↗
    print("[TEST 5] Nút Truy cập Website (Hàng 2, full width)")
    web_link = page.locator(".btn-open-web").first
    href = web_link.get_attribute("href")
    target = web_link.get_attribute("target")
    print(f"   -> Link URL: {href}, Target: {target}")
    assert href and "http" in href, f"Lỗi link: {href}"
    assert target == "_blank", "Link phải mở tab mới"

    # 6. Test Copy Ảnh FB (1080x1920)
    print("[TEST 6] Nút Copy Ảnh FB (Hàng 1, màu đỏ nổi bật)")
    page.locator(".btn-fb-image").first.click()
    page.wait_for_timeout(500)
    toast_img_text = page.locator("#toastMsg").text_content()
    print(f"   -> Thông báo Toast sau khi bấm copy ảnh: {toast_img_text}")
    assert "1080x1920" in toast_img_text or "nạp ảnh" in toast_img_text.lower() or "ảnh" in toast_img_text.lower(), f"Lỗi copy ảnh: {toast_img_text}" """

norm_text = text.replace('\r\n', '\n')
norm_old = old_test5.replace('\r\n', '\n').strip()
norm_new = new_test5.replace('\r\n', '\n').strip()

if norm_old in norm_text:
    norm_text = norm_text.replace(norm_old, norm_new, 1)
    with open('_Luu_Tru_Ky_Thuat/01_Scripts_Bo_Tro/test_e2e_features.py', 'w', encoding='utf-8') as f:
        f.write(norm_text)
    print("test_e2e_features.py updated")
else:
    print("test_e2e_features.py not matched")
