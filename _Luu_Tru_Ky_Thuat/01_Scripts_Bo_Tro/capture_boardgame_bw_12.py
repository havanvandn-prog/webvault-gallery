# -*- coding: utf-8 -*-
import os, sys, time, json

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
skill_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts"
sys.path.append(skill_path)

from capture_engine import setup_page_protection, capture_smart_clean, compress_tri_layer, verify_captured_image
from playwright.sync_api import sync_playwright

output_dir = os.path.join(BASE_DIR, "Anh_Chup_Website")
kho_webp_dir = os.path.join(BASE_DIR, "Kho_Anh_Webp")
metadata_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "boardgame_bw_candidates.json")

os.makedirs(output_dir, exist_ok=True)
os.makedirs(kho_webp_dir, exist_ok=True)

candidates = [
    {
        "id": "bg01",
        "name": "For The Win — Board Game Cafe & Bar (Toronto)",
        "short_name": "For The Win Cafe & Bar",
        "url": "https://www.forthewincafe.com/",
        "domain": "forthewincafe.com",
        "slug": "bg_bw_forthewincafe",
        "industry": "board-game-den-trang",
        "industry_name": "Board Game Đen Trắng & F&B",
        "category": "Monochrome B&W Board Game Cafe & Bar",
        "category_vn": "Board Game Cafe & Bar Tối Giản Đen Trắng",
        "tag": "bw-fnb",
        "vibe": "Đen Trắng Thuần Túy • EAT DRINK PLAY • Minimalist Typography",
        "location": "Toronto (Canada)",
        "desc": "Quán board game cafe & bar nổi tiếng tại Toronto với giao diện nền trắng – chữ đen tối giản tuyệt đối. Chia 3 trụ cột rõ ràng: EAT (đồ ăn), DRINK (cocktail, cà phê, bia thủ công) và PLAY (thư viện board game đồ sộ)."
    },
    {
        "id": "bg02",
        "name": "Dice & Fork — Games Bar and Eatery (Auckland)",
        "short_name": "Dice & Fork",
        "url": "https://www.diceandfork.co.nz/",
        "domain": "diceandfork.co.nz",
        "slug": "bg_bw_diceandfork",
        "industry": "board-game-den-trang",
        "industry_name": "Board Game Đen Trắng & F&B",
        "category": "B&W Editorial Board Game Bar & Eatery",
        "category_vn": "Quán Bar & Nhà Hàng Board Game Phong Cách Đen Trắng",
        "tag": "bw-fnb",
        "vibe": "Logo Đen Trắng Đậm Chất • Typography B&W • Bar & Eatery",
        "location": "Auckland (New Zealand)",
        "desc": "Quán bar kết hợp nhà hàng board game hàng đầu Auckland. Website mang nhận diện đen – trắng sắc nét, font hiển thị cá tính, điều hướng thẳng vào Menu đồ ăn, Danh sách Game và Đặt bàn."
    },
    {
        "id": "bg03",
        "name": "The Treehouse — Board Game Cafe & Kitchen (Sheffield)",
        "short_name": "The Treehouse Sheffield",
        "url": "https://www.treehousesheffield.com/",
        "domain": "treehousesheffield.com",
        "slug": "bg_bw_treehouse",
        "industry": "board-game-den-trang",
        "industry_name": "Board Game Đen Trắng & F&B",
        "category": "Dark Charcoal & White Board Game Cafe",
        "category_vn": "Board Game Cafe & Kitchen Nền Đen Tối Giản",
        "tag": "dark-fnb",
        "vibe": "Nền Đen Than #1A1A1A • Chữ Trắng Sắc Lẹm • Eat & Drink",
        "location": "Sheffield (Anh)",
        "desc": "Board game cafe & kitchen tại Sheffield với giao diện nền đen than – chữ trắng hiện đại. Menu điều hướng tinh gọn (BOOK, PLAY, EAT & DRINK, SHOP) mang lại trải nghiệm đọc lướt rất thoáng."
    },
    {
        "id": "bg04",
        "name": "Table Top Café — Board Game Cafe & Pub (Edmonton)",
        "short_name": "Table Top Cafe",
        "url": "https://www.tabletopcafe.ca/",
        "domain": "tabletopcafe.ca",
        "slug": "bg_bw_tabletopcafe",
        "industry": "board-game-den-trang",
        "industry_name": "Board Game Đen Trắng & F&B",
        "category": "Black Header & Moody Tabletop Cafe",
        "category_vn": "Board Game Cafe & Bia Thủ Công Tông Đen Trắng",
        "tag": "dark-fnb",
        "vibe": "Header Đen Tuyền • Nút Viền Trắng Tối Giản • Cafe & Beer",
        "location": "Edmonton (Canada)",
        "desc": "Thương hiệu board game cafe tiên phong tại Edmonton từ 2013, phục vụ cà phê, bia thủ công và pizza. Giao diện sử dụng thanh header đen tuyền kết hợp nút CTA viền trắng sắc nét."
    },
    {
        "id": "bg05",
        "name": "Bad Moon Cafe — Tabletop, Coffee & Craft Beer (London)",
        "short_name": "Bad Moon Cafe",
        "url": "https://www.badmooncafe.co.uk/",
        "domain": "badmooncafe.co.uk",
        "slug": "bg_bw_badmooncafe",
        "industry": "board-game-den-trang",
        "industry_name": "Board Game Đen Trắng & F&B",
        "category": "Monochrome Dark Tabletop & Pizza Bar",
        "category_vn": "Board Game Cafe, Pizza & Craft Beer Tông Trầm",
        "tag": "bw-fnb",
        "vibe": "Đen Trắng Tối Giản • Nền Xám Nhạt – Đen • Coffee & Pizza",
        "location": "London (Anh)",
        "desc": "Điểm hẹn board game, wargaming kết hợp cà phê đặc sản, bia thủ công và pizza tại London. Thiết kế web tối giản tông đen – xám – trắng sạch sẽ, tập trung đặt bàn và lịch sự kiện."
    },
    {
        "id": "bg06",
        "name": "Sip & Play — Brooklyn Board Game Cafe (NYC)",
        "short_name": "Sip & Play NYC",
        "url": "https://www.sipnplaynyc.com/",
        "domain": "sipnplaynyc.com",
        "slug": "bg_bw_sipnplay",
        "industry": "board-game-den-trang",
        "industry_name": "Board Game Đen Trắng & F&B",
        "category": "Clean White & Black Editorial Game Cafe",
        "category_vn": "Board Game Cafe & Boba/Sandwich Phong Cách Trắng Đen",
        "tag": "bw-fnb",
        "vibe": "Nền Trắng Tinh Khôi • Typography Đen Đậm • 500+ Games & F&B",
        "location": "Brooklyn, NYC (Mỹ)",
        "desc": "Board game cafe nổi tiếng tại Brooklyn với hơn 500 tựa game, trà sữa, cà phê, bia và sandwich. Giao diện nền trắng chữ đen cực kỳ dễ đọc, trình bày rõ giá bàn và giờ mở cửa ngay đầu trang."
    },
    {
        "id": "bg07",
        "name": "Replay Bristol — Board Game Cafe & Event Space",
        "short_name": "Replay Bristol",
        "url": "https://replaybristol.com/",
        "domain": "replaybristol.com",
        "slug": "bg_bw_replaybristol",
        "industry": "board-game-den-trang",
        "industry_name": "Board Game Đen Trắng & F&B",
        "category": "Grayscale & White Minimalist Game Cafe",
        "category_vn": "Board Game Cafe & Bar Tông Xám Trắng Tối Giản",
        "tag": "bw-fnb",
        "vibe": "Xám Đen & Trắng • Tích Hợp Đặt Bàn Nhanh • Cocktail & Games",
        "location": "Bristol (Anh)",
        "desc": "Không gian board game cafe, cocktail và tổ chức sự kiện tại Bristol. Giao diện sử dụng bảng màu xám chì – trắng tối giản, tích hợp module đặt bàn ResDiary trực quan ngay trang chủ."
    },
    {
        "id": "bg08",
        "name": "The Ludoquist — Board Game Cafe & Kitchen (London)",
        "short_name": "The Ludoquist",
        "url": "https://www.theludoquist.com/",
        "domain": "theludoquist.com",
        "slug": "bg_bw_theludoquist",
        "industry": "board-game-den-trang",
        "industry_name": "Board Game Đen Trắng & F&B",
        "category": "Stark Black & White Board Game Cafe",
        "category_vn": "Board Game Cafe & Đồ Ăn Tông Đen Trắng Thanh Lịch",
        "tag": "bw-fnb",
        "vibe": "Header Đen • Nền Trắng Sạch • Coffee, Food & 1,400+ Games",
        "location": "Croydon, London (Anh)",
        "desc": "Quán board game đạt nhiều giải thưởng tại London, phục vụ cà phê, đồ ăn nóng và hàng nghìn tựa game. Bố cục website đen trắng thoáng đãng, tập trung vào câu chuyện trải nghiệm và đặt bàn."
    },
    {
        "id": "bg09",
        "name": "Across The Board — Game Café & Dining (Winnipeg)",
        "short_name": "Across The Board",
        "url": "https://acrosstheboardcafe.com/",
        "domain": "acrosstheboardcafe.com",
        "slug": "bg_bw_acrosstheboard",
        "industry": "board-game-den-trang",
        "industry_name": "Board Game Đen Trắng & F&B",
        "category": "Bold Monochrome Dining & Board Game Cafe",
        "category_vn": "Nhà Hàng & Cafe Board Game Phong Cách Trắng Đen",
        "tag": "bw-fnb",
        "vibe": "Typography Trắng Đen Lớn • Play. Dine. Shop • Full Kitchen",
        "location": "Winnipeg (Canada)",
        "desc": "Mô hình nhà hàng kết hợp thư viện board game quy mô lớn với thông điệp 'play. dine. shop.'. Giao diện sạch, font chữ đen trắng tương phản cao, kết hợp thực đơn ăn uống và đặt chỗ."
    },
    {
        "id": "bg10",
        "name": "Sugar & Dice — Independent Board Game Cafe (Liverpool)",
        "short_name": "Sugar & Dice",
        "url": "https://www.sugaranddice.co.uk/",
        "domain": "sugaranddice.co.uk",
        "slug": "bg_bw_sugaranddice",
        "industry": "board-game-den-trang",
        "industry_name": "Board Game Đen Trắng & F&B",
        "category": "Black-Canvas Board Game & Bakery Cafe",
        "category_vn": "Board Game Cafe & Bánh Ngọt Nền Đen Tương Phản",
        "tag": "dark-fnb",
        "vibe": "Nền Đen Tuyền • Chữ Trắng Nổi Bật • Bánh Ngọt & Đồ Uống",
        "location": "Liverpool (Anh)",
        "desc": "Quán board game cafe độc lập tại trung tâm Liverpool nổi tiếng với bánh ngọt tự làm, đồ uống và hơn 350 tựa game. Website sử dụng nền đen chủ đạo tạo độ tương phản cao cho nội dung."
    },
    {
        "id": "bg11",
        "name": "Meeples & Coffee — Board Game Bistro (Prague)",
        "short_name": "Meeples & Coffee",
        "url": "https://www.meeples.cafe/",
        "domain": "meeples.cafe",
        "slug": "bg_bw_meeples",
        "industry": "board-game-den-trang",
        "industry_name": "Board Game Đen Trắng & F&B",
        "category": "Minimal White & Black Cafe Bistro",
        "category_vn": "Board Game Bistro & Bữa Sáng Phong Cách Châu Âu",
        "tag": "bw-fnb",
        "vibe": "Nền Trắng Chữ Đen • Phong Cách Bistro • Coffee & Breakfast",
        "location": "Prague (Séc)",
        "desc": "Board game cafe nằm ngay khu phố cổ Prague, phục vụ cà phê đặc sản, bữa sáng quốc tế và tủ game phong phú. Website bố cục sạch sẽ trên nền trắng – chữ đen dễ theo dõi."
    },
    {
        "id": "bg12",
        "name": "Too Bad Games — Monochrome Tabletop Studio",
        "short_name": "Too Bad Games",
        "url": "https://www.toobadgames.com/",
        "domain": "toobadgames.com",
        "slug": "bg_bw_toobadgames",
        "industry": "board-game-den-trang",
        "industry_name": "Board Game Đen Trắng & F&B",
        "category": "Pure Dark Monochrome Board Game UI Benchmark",
        "category_vn": "Studio Board Game Đen Trắng Thuần Túy (Chuẩn UI/UX)",
        "tag": "bw-studio",
        "vibe": "Đen Trắng 100% • Card UI Sắc Nét • Minh Họa Xúc Xắc Dark Mode",
        "location": "Madrid (Tây Ban Nha)",
        "desc": "Studio phát hành board game độc lập với giao diện đen than – trắng tinh khiết gần như 100%. Mẫu tham khảo xuất sắc về cách trình bày thẻ bài/game, nút bấm viền mảnh và đồ họa xúc xắc dark-mode."
    }
]

print(f"=== CHỤP & KIỂM ĐỊNH {len(candidates)} WEBSITE BOARD GAME ĐEN TRẮNG ===")
results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for idx, site in enumerate(candidates, 1):
        print(f"\n[{idx:02d}/{len(candidates)}] {site['name']} ({site['url']})...")
        raw_png = os.path.join(output_dir, f"{site['slug']}.png")
        full_webp = os.path.join(kho_webp_dir, f"{site['slug']}_full.webp")

        site["image"] = f"Anh_Chup_Website/{site['slug']}.png"
        site["thumb"] = f"Kho_Anh_Webp/{site['slug']}_thumb.webp"
        site["full"] = f"Kho_Anh_Webp/{site['slug']}_full.webp"
        site["fb"] = f"Kho_Anh_Webp/{site['slug']}_fb.png"

        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            ignore_https_errors=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        setup_page_protection(page)
        try:
            page.goto(site['url'], timeout=45000, wait_until="domcontentloaded")
            time.sleep(3.5)
            # Dismiss cookie/consent banners cleanly
            page.evaluate("""() => {
                const selectors = [
                    'button[aria-label*="Close" i]', 'button[aria-label*="accept" i]',
                    '.onetrust-close-btn-handler', '#onetrust-accept-btn-handler',
                    '.cookie-accept', '.btn-close-popup', '.popup-close', '.close-modal',
                    '#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll',
                    '.iubenda-cs-accept-btn', '.sqs-cookie-banner-v2-accept',
                    'button:has-text("Accept")'
                ];
                selectors.forEach(sel => {
                    try { document.querySelectorAll(sel).forEach(btn => { try { btn.click(); } catch(e) {} }); } catch(e) {}
                });
                // Also click buttons matching text Accept / Decline All / Ok / Reject
                document.querySelectorAll('button, a').forEach(el => {
                    const t = (el.innerText || '').trim().toLowerCase();
                    if (['accept', 'accept all', 'decline all', 'ok', 'rechazar analítica', 'aceptar analítica', 'got it'].includes(t)) {
                        try { el.click(); } catch(e) {}
                    }
                });
            }""")
            time.sleep(0.8)
            capture_smart_clean(page, raw_png, viewport_height=900, scroll_delay=0.3)
            thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb = compress_tri_layer(raw_png, site['slug'], kho_webp_dir)
            valid, msg = verify_captured_image(full_webp)
            print(f"  [+] QA: {'PASS' if valid else 'FAIL'} - {msg}")
            if not valid:
                print("  [!] Thử chụp lại với networkidle + delay 0.45s...")
                page.goto(site['url'], timeout=45000, wait_until="networkidle")
                time.sleep(3.5)
                capture_smart_clean(page, raw_png, viewport_height=900, scroll_delay=0.45)
                thumb_name, full_name, fb_name, thumb_kb, full_kb, fb_kb = compress_tri_layer(raw_png, site['slug'], kho_webp_dir)
                valid, msg = verify_captured_image(full_webp)
                print(f"  [+] QA Vòng 2: {'PASS' if valid else 'FAIL'} - {msg}")

            site["thumb_kb"] = thumb_kb
            site["full_kb"] = full_kb
            site["fb_kb"] = fb_kb
            site["size_mb"] = f"{round(os.path.getsize(raw_png) / (1024*1024), 2)} MB"
            site["audit_msg"] = msg
            site["status"] = "SUCCESS" if valid else "FAIL"
            results.append((site["id"], site["domain"], "PASS" if valid else "FAIL", msg))
        except Exception as e:
            print(f"  [-] Error {site['domain']}: {e}")
            site["status"] = "FAIL"
            site["audit_msg"] = str(e)[:120]
            results.append((site["id"], site["domain"], "FAIL", str(e)[:80]))
        finally:
            context.close()
    browser.close()

with open(metadata_file, "w", encoding="utf-8") as f:
    json.dump(candidates, f, ensure_ascii=False, indent=2)

print("\n=== TỔNG KẾT QA 12 ỨNG VIÊN BOARD GAME ĐEN TRẮNG ===")
for r in results:
    print(f"  {r[0]} | {r[1]:24s} | {r[2]:4s} | {r[3]}")
