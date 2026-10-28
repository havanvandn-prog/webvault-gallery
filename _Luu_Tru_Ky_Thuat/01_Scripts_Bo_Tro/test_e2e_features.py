# -*- coding: utf-8 -*-
"""
Bộ kiểm thử E2E tự động tất cả các tính năng của WebVault
"""
import sys
import os
from playwright.sync_api import sync_playwright

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

live_url = "https://havanvandn-prog.github.io/webvault-gallery/"
print(f"[*] Bắt đầu kiểm thử toàn diện trên: {live_url}")

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={'width': 1440, 'height': 900}, permissions=['clipboard-read', 'clipboard-write'])
    page = context.new_page()
    
    # 1. Page Load
    res = page.goto(live_url)
    print(f"[TEST 1] Tải trang: HTTP {res.status}")
    page.wait_for_selector('.website-card')
    cards = page.locator('.website-card')
    card_count = cards.count()
    print(f"   -> Đã hiển thị: {card_count} thẻ card (Kỳ vọng: 20)")
    assert card_count >= 20, f"Lỗi số lượng card: {card_count}"
    
    # 2. Test Vibe Filter: Dark Mode & Sang trong
    print("[TEST 2] Bộ lọc Phong cách: 'Dark Mode & Sang trọng'")
    page.locator("text=Dark Mode & Sang trọng").first.click()
    page.wait_for_timeout(300)
    dark_cards = page.locator('.website-card:visible').count()
    print(f"   -> Số card hiển thị: {dark_cards} (Kỳ vọng: 5)")
    assert dark_cards == 5, f"Lỗi lọc Dark Mode: {dark_cards}"
    
    # Reset vibe filter
    page.locator("text=Tất cả phong cách").click()
    page.wait_for_timeout(300)
    
    # 3. Test Search
    print("[TEST 3] Tìm kiếm thời gian thực: từ khóa 'Square'")
    page.fill("#searchInput", "square")
    page.wait_for_timeout(300)
    search_cards = page.locator('.website-card:visible').count()
    print(f"   -> Kết quả tìm kiếm: {search_cards} (Kỳ vọng: 1)")
    assert search_cards == 1, f"Lỗi tìm kiếm: {search_cards}"
    
    # Clear search
    page.fill("#searchInput", "")
    page.wait_for_timeout(300)
    
    # 4. Test Lightbox Modal
    print("[TEST 4] Xem ảnh Full-Page (Lightbox modal)")
    page.locator(".btn-view-full").first.click()
    page.wait_for_selector(".lightbox-modal.active")
    lb_active = page.locator(".lightbox-modal.active").is_visible()
    lb_img_src = page.locator("#lbImage").get_attribute("src")
    print(f"   -> Modal mở thành công: {lb_active}, Đường dẫn ảnh: {lb_img_src}")
    assert lb_active and lb_img_src, "Lỗi mở modal Lightbox"
    
    # Close lightbox with ESC
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
    lb_closed = not page.locator(".lightbox-modal.active").is_visible()
    print(f"   -> Đóng modal bằng phím ESC: {lb_closed}")
    assert lb_closed, "Lỗi đóng modal Lightbox"
    
    # 5. Test Nút Truy cập Website ↗
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
    assert "1080x1920" in toast_img_text or "nạp ảnh" in toast_img_text.lower() or "ảnh" in toast_img_text.lower(), f"Lỗi copy ảnh: {toast_img_text}"
    
    # 7. Test Pitch Selection & Pitch URL
    print("[TEST 7] Tạo Gói Gửi Khách (Client Pitch Pack)")
    page.locator(".pitch-checkbox").nth(0).check()
    page.locator(".pitch-checkbox").nth(1).check()
    page.wait_for_timeout(300)
    selected_count = page.locator("#selectedCount").text_content()
    bar_visible = page.locator("#floatingPitchBar").is_visible()
    print(f"   -> Số lượng đã chọn: {selected_count}, Thanh nổi hiển thị: {bar_visible}")
    assert selected_count == "2", f"Lỗi đếm số lượng: {selected_count}"
    
    # Test Loading Pitch URL directly
    pitch_url = f"{live_url}?pitch=01,02"
    print(f"[TEST 8] Truy cập đường link Pitch Pack: {pitch_url}")
    page.goto(pitch_url)
    page.wait_for_timeout(500)
    pitch_cards = page.locator(".website-card:visible").count()
    banner_visible = page.locator("#pitchBanner").is_visible()
    print(f"   -> Số mẫu VIP hiển thị: {pitch_cards} (Kỳ vọng: 2), Banner VIP: {banner_visible}")
    assert pitch_cards == 2, f"Lỗi số card pitch: {pitch_cards}"
    assert banner_visible, "Banner VIP không hiển thị"
    
    # 8. Test Exiting Pitch Mode
    page.locator("text=Xem Toàn Bộ Mẫu").click()
    page.wait_for_timeout(300)
    all_restored = page.locator(".website-card:visible").count()
    print(f"   -> Thoát chế độ Pitch khôi phục toàn bộ: {all_restored} cards")
    assert all_restored == 20, f"Lỗi khôi phục toàn bộ mẫu: {all_restored}"

    # 9. Test Mobile Responsive Viewport (390px)
    print("[TEST 9] Kiểm tra Responsive Mobile (390px)")
    page.set_viewport_size({"width": 390, "height": 844})
    page.wait_for_timeout(300)
    scroll_w = page.evaluate("document.documentElement.scrollWidth")
    inner_w = page.evaluate("window.innerWidth")
    overflow = scroll_w > inner_w
    print(f"   -> Viewport: {inner_w}px, ScrollWidth: {scroll_w}px, Tràn viền: {overflow}")
    assert not overflow, f"Lỗi tràn viền trên mobile 390px: {scroll_w} > {inner_w}"

    print("\n[CHÚC MỪNG] TOÀN BỘ 9 BÀI KIỂM THỬ ĐÃ PASS 100% TRÊN MÁY CHỦ THẬT!")
    browser.close()
