# -*- coding: utf-8 -*-
import json
import os
import sys

# Ensure UTF-8 output on Windows console
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
metadata_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "decor_metadata.json")
output_html = os.path.join(BASE_DIR, "preview_mau_website_decor_su_kien.html")

if not os.path.exists(metadata_path):
    print(f"[-] Metadata chưa tồn tại: {metadata_path}")
    sys.exit(1)

with open(metadata_path, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

websites = []
for item in raw_data:
    websites.append({
        "id": item["id"],
        "name": item["name"],
        "short_name": item.get("short_name", item["name"]),
        "domain": item["domain"],
        "url": item["url"],
        "tag": item.get("tag", "all"),
        "category": item["category_vn"],
        "vibe": item.get("vibe", "creative-art"),
        "vibe_name": item.get("vibe_name", "Hiện đại & Sáng tạo"),
        "location": item["location"],
        "thumb": item.get("thumb") or f"Anh_Chup_Website/{item['domain']}.png",
        "full": item.get("full") or f"Anh_Chup_Website/{item['domain']}.png",
        "fb": item.get("fb", ""),
        "thumb_kb": item.get("thumb_kb", 0),
        "full_kb": item.get("full_kb", 0),
        "size_mb": item.get("size_mb", "N/A"),
        "desc": item["desc"]
    })

websites_json = json.dumps(websites, ensure_ascii=False, indent=2)

html_content = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>20 Mẫu Website Trang Trí & Decor Tiệc Sự Kiện Đẹp, Chuẩn SEO — WebVault</title>
  <link rel="icon" type="image/svg+xml" href="favicon.svg">
  <link rel="icon" type="image/png" href="favicon.png">
  <link rel="apple-touch-icon" href="favicon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    :root {{
      --primary: #d97706;
      --primary-hover: #b45309;
      --primary-light: #fef3c7;
      --primary-border: #fde68a;
      --accent-rose: #e11d48;
      --accent-rose-light: #ffe4e6;
      --accent-emerald: #059669;
      --accent-emerald-light: #d1fae5;
      --slate-900: #0f172a;
      --slate-800: #1e293b;
      --slate-700: #334155;
      --slate-600: #475569;
      --slate-500: #64748b;
      --slate-400: #94a3b8;
      --slate-200: #e2e8f0;
      --slate-100: #f1f5f9;
      --slate-50: #f8fafc;
      --border: #e2e8f0;
      --card-bg: #ffffff;
      --radius: 12px;
      --shadow: 0 4px 6px -1px rgba(0,0,0,0.06), 0 2px 4px -2px rgba(0,0,0,0.04);
      --shadow-hover: 0 14px 28px -4px rgba(217, 119, 6, 0.16), 0 6px 12px -2px rgba(0,0,0,0.06);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      scrollbar-width: thin;
      scrollbar-color: rgba(217, 119, 6, 0.3) transparent;
    }}

    ::-webkit-scrollbar {{
      width: 6px;
      height: 6px;
    }}
    ::-webkit-scrollbar-track {{
      background: transparent;
    }}
    ::-webkit-scrollbar-thumb {{
      background: rgba(217, 119, 6, 0.3);
      border-radius: 10px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
      background: var(--primary);
    }}

    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: var(--slate-50);
      color: var(--slate-800);
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
      overflow-x: clip;
    }}

    /* HEADER */
    header {{
      background: #ffffff;
      border-bottom: 1px solid var(--border);
      position: sticky;
      top: 0;
      z-index: 40;
    }}

    .header-container {{
      max-width: 1400px;
      margin: 0 auto;
      padding: 14px 24px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }}

    .brand-title {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .brand-badge {{
      background: linear-gradient(135deg, #d97706, #f59e0b);
      color: #fff;
      font-size: 11px;
      font-weight: 800;
      padding: 5px 11px;
      border-radius: 7px;
      text-transform: uppercase;
      letter-spacing: 0.6px;
      box-shadow: 0 3px 10px rgba(217, 119, 6, 0.28);
    }}

    .brand-title h1 {{
      font-size: 17px;
      font-weight: 800;
      color: var(--slate-900);
      letter-spacing: -0.3px;
    }}

    .header-actions {{
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }}

    .btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 13px;
      font-weight: 600;
      padding: 8px 14px;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.2s ease;
      text-decoration: none;
      border: none;
      white-space: nowrap;
    }}

    .btn-primary {{
      background: var(--primary);
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(217, 119, 6, 0.25);
    }}
    .btn-primary:hover {{
      background: var(--primary-hover);
    }}

    .btn-secondary {{
      background: var(--slate-100);
      color: var(--slate-700);
      border: 1px solid var(--border);
    }}
    .btn-secondary:hover {{
      background: var(--slate-200);
      color: var(--slate-900);
    }}

    /* HERO STRIP */
    .hero-strip {{
      background: linear-gradient(180deg, #ffffff 0%, var(--slate-50) 100%);
      border-bottom: 1px solid var(--border);
      padding: 32px 24px 28px;
    }}

    .hero-container {{
      max-width: 1400px;
      margin: 0 auto;
    }}

    .hero-badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      background: var(--primary-light);
      border: 1px solid var(--primary-border);
      color: var(--primary-hover);
      border-radius: 20px;
      font-size: 12px;
      font-weight: 700;
      margin-bottom: 12px;
    }}

    .hero-title {{
      font-size: 28px;
      font-weight: 900;
      color: var(--slate-900);
      letter-spacing: -0.6px;
      margin-bottom: 8px;
    }}

    .hero-desc {{
      font-size: 14.5px;
      color: var(--slate-600);
      max-width: 820px;
      line-height: 1.6;
      margin-bottom: 20px;
    }}

    /* STATS ROW */
    .stats-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-bottom: 20px;
    }}

    .stat-pill {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: #ffffff;
      border: 1px solid var(--border);
      padding: 6px 14px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      color: var(--slate-700);
      box-shadow: var(--shadow);
    }}
    .stat-pill b {{
      color: var(--primary-hover);
      font-weight: 800;
    }}

    /* CONTROLS (FILTER & SEARCH) */
    .controls-wrapper {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      margin-top: 12px;
    }}

    .filter-tabs {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}

    .tab-btn {{
      padding: 7px 14px;
      border-radius: 8px;
      font-size: 12.5px;
      font-weight: 600;
      background: #ffffff;
      border: 1px solid var(--border);
      color: var(--slate-600);
      cursor: pointer;
      transition: all 0.2s ease;
    }}

    .tab-btn:hover {{
      background: var(--slate-100);
      color: var(--slate-900);
      border-color: var(--slate-400);
    }}

    .tab-btn.active {{
      background: var(--primary);
      border-color: var(--primary);
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(217, 119, 6, 0.25);
    }}

    .search-box {{
      position: relative;
      min-width: 280px;
      flex: 1;
      max-width: 380px;
    }}

    .search-input {{
      width: 100%;
      padding: 8px 12px 8px 36px;
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 8px;
      font-size: 13px;
      color: var(--slate-800);
      outline: none;
      transition: all 0.2s;
    }}

    .search-input:focus {{
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(217, 119, 6, 0.15);
    }}

    .search-icon {{
      position: absolute;
      left: 11px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--slate-400);
      pointer-events: none;
    }}

    /* MAIN GRID */
    main {{
      max-width: 1400px;
      margin: 0 auto;
      padding: 32px 24px 80px;
    }}

    .cards-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
      gap: 24px;
    }}

    /* WEBSITE CARD */
    .website-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      overflow: hidden;
      box-shadow: var(--shadow);
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      display: flex;
      flex-direction: column;
    }}

    .website-card:hover {{
      transform: translateY(-5px);
      box-shadow: var(--shadow-hover);
      border-color: var(--primary-border);
    }}

    /* CARD BROWSER BAR */
    .card-browser-bar {{
      background: #f8fafc;
      border-bottom: 1px solid var(--border);
      padding: 8px 14px;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .browser-dots {{
      display: flex;
      gap: 5px;
    }}
    .b-dot {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
    }}
    .b-dot.red {{ background: #ef4444; }}
    .b-dot.yellow {{ background: #f59e0b; }}
    .b-dot.green {{ background: #10b981; }}

    .browser-url-pill {{
      flex: 1;
      margin-left: 8px;
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: 4px;
      font-size: 11.5px;
      color: var(--slate-600);
      padding: 2px 10px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      text-decoration: none;
      font-family: monospace;
    }}
    .browser-url-pill:hover {{
      color: var(--primary-hover);
      border-color: var(--primary-border);
    }}

    /* THUMBNAIL BOX (HOVER SCROLL) */
    .card-thumbnail-box {{
      position: relative;
      height: 250px;
      background: #0f172a;
      overflow: hidden;
      cursor: pointer;
    }}

    .card-thumb-img {{
      width: 100%;
      height: auto;
      display: block;
      transform: translateY(0);
      transition: transform 0.6s cubic-bezier(0.16, 1, 0.3, 1);
      will-change: transform;
    }}

    .card-thumbnail-box:hover .card-thumb-img {{
      transform: translateY(calc(-100% + 250px));
      transition: transform 15s linear;
    }}

    .card-size-tag {{
      position: absolute;
      bottom: 8px;
      right: 8px;
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(4px);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: #38bdf8;
      font-size: 11px;
      font-weight: 700;
      padding: 2px 7px;
      border-radius: 4px;
    }}

    .hover-hint {{
      position: absolute;
      top: 8px;
      left: 8px;
      background: rgba(15, 23, 42, 0.75);
      backdrop-filter: blur(4px);
      color: #f1f5f9;
      font-size: 10.5px;
      font-weight: 600;
      padding: 3px 8px;
      border-radius: 4px;
      pointer-events: none;
      opacity: 0.85;
      transition: opacity 0.2s;
    }}
    .card-thumbnail-box:hover .hover-hint {{
      opacity: 0;
    }}

    /* CARD BODY */
    .card-body {{
      padding: 18px;
      display: flex;
      flex-direction: column;
      flex: 1;
    }}

    .card-meta-row {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 10px;
    }}

    .meta-badge {{
      font-size: 11px;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.4px;
    }}
    .meta-badge.category {{
      background: var(--primary-light);
      color: var(--primary-hover);
      border: 1px solid var(--primary-border);
    }}
    .meta-badge.vibe {{
      background: #f1f5f9;
      color: var(--slate-700);
      border: 1px solid var(--slate-200);
    }}
    .meta-badge.location {{
      background: #f0fdf4;
      color: #15803d;
      border: 1px solid #bbf7d0;
    }}

    .card-title {{
      font-size: 15.5px;
      font-weight: 800;
      color: var(--slate-900);
      margin-bottom: 6px;
      letter-spacing: -0.2px;
      line-height: 1.35;
    }}

    .card-desc {{
      font-size: 12.5px;
      color: var(--slate-600);
      line-height: 1.55;
      margin-bottom: 16px;
      flex: 1;
    }}

    /* CARD ACTIONS */
    .card-actions-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-bottom: 8px;
    }}

    .btn-card {{
      padding: 8px 10px;
      border-radius: 7px;
      font-size: 12px;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      cursor: pointer;
      text-decoration: none;
      transition: all 0.2s;
      border: none;
    }}

    .btn-view-full {{
      background: var(--slate-900);
      color: #ffffff;
    }}
    .btn-view-full:hover {{
      background: var(--primary);
    }}

    .btn-open-web {{
      background: var(--slate-100);
      border: 1px solid var(--slate-200);
      color: var(--slate-700);
    }}
    .btn-open-web:hover {{
      background: var(--slate-200);
      color: var(--slate-900);
    }}

    .btn-copy-url {{
      grid-column: span 2;
      background: var(--primary-light);
      border: 1px solid var(--primary-border);
      color: var(--primary-hover);
    }}
    .btn-copy-url:hover {{
      background: var(--primary);
      color: #ffffff;
      border-color: var(--primary);
    }}

    /* LIGHTBOX MODAL */
    .lightbox-modal {{
      position: fixed;
      inset: 0;
      background: rgba(15, 23, 42, 0.95);
      backdrop-filter: blur(8px);
      z-index: 100;
      display: none;
      flex-direction: column;
    }}
    .lightbox-modal.active {{
      display: flex;
    }}

    .lightbox-header {{
      padding: 12px 24px;
      background: #0f172a;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      color: #ffffff;
    }}

    .lightbox-title-box {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .lightbox-title-box h3 {{
      font-size: 15px;
      font-weight: 700;
    }}

    .lightbox-close {{
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #ffffff;
      width: 32px;
      height: 32px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.2s;
    }}
    .lightbox-close:hover {{
      background: var(--accent-rose);
      border-color: var(--accent-rose);
    }}

    .lightbox-body {{
      flex: 1;
      overflow-y: auto;
      overflow-x: clip;
      padding: 24px;
      display: flex;
      justify-content: center;
    }}

    .lightbox-img-wrapper {{
      max-width: 1280px;
      width: 100%;
      background: #000;
      border-radius: 8px;
      box-shadow: 0 24px 60px rgba(0,0,0,0.8);
      overflow: hidden;
    }}
    .lightbox-img-wrapper img {{
      width: 100%;
      height: auto;
      display: block;
    }}

    /* TOAST */
    .toast {{
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: #0f172a;
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: #ffffff;
      padding: 12px 20px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      box-shadow: 0 12px 32px rgba(0,0,0,0.4);
      display: flex;
      align-items: center;
      gap: 10px;
      opacity: 0;
      transform: translateY(12px);
      transition: all 0.25s ease;
      z-index: 120;
      pointer-events: none;
    }}
    .toast.show {{
      opacity: 1;
      transform: translateY(0);
    }}

    /* RESPONSIVE */
    @media (max-width: 768px) {{
      .hero-title {{
        font-size: 22px;
      }}
      .cards-grid {{
        grid-template-columns: 1fr;
      }}
      .controls-wrapper {{
        flex-direction: column;
        align-items: stretch;
      }}
      .search-box {{
        max-width: 100%;
      }}
    }}
  </style>
</head>
<body>

<!-- HEADER -->
<header>
  <div class="header-container">
    <div class="brand-title">
      <div class="brand-badge">DECOR VAULT</div>
      <h1>Bộ Sưu Tập 20 Mẫu Website Trang Trí & Decor Sự Kiện</h1>
    </div>

    <div class="header-actions">
      <a href="index.html" class="btn btn-secondary">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
        WebVault Tổng
      </a>
      <button class="btn btn-primary" onclick="copyAllUrls()">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
        Sao Chép 20 URL
      </button>
    </div>
  </div>
</header>

<!-- HERO STRIP -->
<section class="hero-strip">
  <div class="hero-container">
    <div class="hero-badge">
      <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
      TUYỂN CHỌN ĐẶC QUYỀN
    </div>
    <h2 class="hero-title">Khảo Sát Giao Diện & Ý Tưởng Trang Trí Tiệc Sự Kiện Hàng Đầu</h2>
    <p class="hero-desc">Tuyển tập 20 website thương hiệu decor sự kiện, tiệc cưới nghệ thuật, thôi nôi sinh nhật và dạ tiệc doanh nghiệp xuất sắc nhất Việt Nam. Ảnh chụp full-page 1440px định dạng WebP siêu nhẹ, tích hợp hiệu ứng cuộn mượt mà khi rê chuột.</p>

    <!-- STATS ROW -->
    <div class="stats-row">
      <div class="stat-pill">
        <span>Quy mô:</span> <b>20 Website</b>
      </div>
      <div class="stat-pill">
        <span>Định dạng:</span> <b>WebP Tri-Layer</b>
      </div>
      <div class="stat-pill">
        <span>Phân nhóm:</span> <b>4 Phân Khúc</b>
      </div>
      <div class="stat-pill">
        <span>Tối ưu:</span> <b>Anti-Blank 100%</b>
      </div>
    </div>

    <!-- CONTROLS -->
    <div class="controls-wrapper">
      <div class="filter-tabs">
        <button class="tab-btn active" onclick="filterCategory('all', this)">Tất Cả (20)</button>
        <button class="tab-btn" onclick="filterCategory('luxury-bespoke', this)">Tiệc Cưới & Nghệ Thuật (4)</button>
        <button class="tab-btn" onclick="filterCategory('birthday-party', this)">Sinh Nhật & Private Party (8)</button>
        <button class="tab-btn" onclick="filterCategory('balloon-backdrop', this)">Cổng Bóng & Backdrop (5)</button>
        <button class="tab-btn" onclick="filterCategory('corporate-gala', this)">Gala & Sự Kiện Công Ty (3)</button>
      </div>

      <div class="search-box">
        <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <input type="text" id="searchInput" class="search-input" placeholder="Tìm theo tên thương hiệu, tên miền..." oninput="handleSearch()">
      </div>
    </div>
  </div>
</section>

<!-- MAIN CONTENT -->
<main>
  <div class="cards-grid" id="cardsGrid">
    <!-- Rendered via JavaScript -->
  </div>
</main>

<!-- LIGHTBOX MODAL -->
<div class="lightbox-modal" id="lightboxModal" onclick="closeLightbox(event)">
  <div class="lightbox-header" onclick="event.stopPropagation()">
    <div class="lightbox-title-box">
      <span class="meta-badge category" id="lbCategory">CATEGORY</span>
      <h3 id="lbTitle">Website Name</h3>
    </div>
    <div style="display: flex; align-items: center; gap: 10px;">
      <a href="#" target="_blank" id="lbOpenBtn" class="btn btn-secondary" style="font-size: 11.5px; padding: 5px 10px;">Mở Website Thật</a>
      <button class="lightbox-close" onclick="closeLightbox(event)">✕</button>
    </div>
  </div>
  <div class="lightbox-body">
    <div class="lightbox-img-wrapper" onclick="event.stopPropagation()">
      <img id="lbImg" src="" alt="Full Preview">
    </div>
  </div>
</div>

<!-- TOAST -->
<div class="toast" id="toastBox">
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg>
  <span id="toastMsg">Đã sao chép liên kết vào bộ nhớ tạm!</span>
</div>

<script>
  const WEBSITES_DATA = {websites_json};

  let currentCategory = 'all';
  let searchQuery = '';

  function renderCards(list) {{
    const grid = document.getElementById('cardsGrid');
    if (!list || list.length === 0) {{
      grid.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 60px; color: var(--slate-500); font-weight: 600;">Không tìm thấy mẫu website phù hợp với từ khóa.</div>';
      return;
    }}

    grid.innerHTML = list.map(item => `
      <div class="website-card" data-tag="${{item.tag}}">
        <!-- BROWSER BAR -->
        <div class="card-browser-bar">
          <div class="browser-dots">
            <span class="b-dot red"></span>
            <span class="b-dot yellow"></span>
            <span class="b-dot green"></span>
          </div>
          <a href="${{item.url}}" target="_blank" rel="noopener" class="browser-url-pill">${{item.domain}}</a>
        </div>

        <!-- THUMBNAIL (HOVER SCROLL) -->
        <div class="card-thumbnail-box" onclick="openLightbox('${{item.id}}')">
          <img class="card-thumb-img" src="${{item.thumb}}" alt="${{item.name}}" loading="lazy">
          <div class="hover-hint">Rê chuột cuộn xem</div>
          <div class="card-size-tag">${{item.thumb_kb}} KB</div>
        </div>

        <!-- BODY -->
        <div class="card-body">
          <div class="card-meta-row">
            <span class="meta-badge category">${{item.category}}</span>
            <span class="meta-badge vibe">${{item.vibe_name}}</span>
            <span class="meta-badge location">${{item.location}}</span>
          </div>

          <h3 class="card-title">${{item.name}}</h3>
          <p class="card-desc">${{item.desc}}</p>

          <div class="card-actions-grid">
            <button class="btn-card btn-view-full" onclick="openLightbox('${{item.id}}')">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 3h6v6M9 21H3v-6M21 3l-7 7M3 21l7-7"/></svg>
              Xem Chi Tiết
            </button>
            <a href="${{item.url}}" target="_blank" rel="noopener" class="btn-card btn-open-web">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
              Mở Website
            </a>
            <button class="btn-card btn-copy-url" onclick="copySingleUrl('${{item.url}}', '${{item.name}}')">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
              Sao Chép URL
            </button>
          </div>
        </div>
      </div>
    `).join('');
  }}

  function filterCategory(tag, btn) {{
    currentCategory = tag;
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');
    applyFilters();
  }}

  function handleSearch() {{
    searchQuery = document.getElementById('searchInput').value.trim().toLowerCase();
    applyFilters();
  }}

  function applyFilters() {{
    const filtered = WEBSITES_DATA.filter(item => {{
      const matchCat = (currentCategory === 'all' || item.tag === currentCategory);
      const matchSearch = (!searchQuery ||
        item.name.toLowerCase().includes(searchQuery) ||
        item.domain.toLowerCase().includes(searchQuery) ||
        item.desc.toLowerCase().includes(searchQuery) ||
        item.location.toLowerCase().includes(searchQuery)
      );
      return matchCat && matchSearch;
    }});
    renderCards(filtered);
  }}

  function openLightbox(id) {{
    const item = WEBSITES_DATA.find(w => w.id === id);
    if (!item) return;

    document.getElementById('lbCategory').textContent = item.category;
    document.getElementById('lbTitle').textContent = item.name + ' (' + item.domain + ')';
    document.getElementById('lbOpenBtn').href = item.url;
    document.getElementById('lbImg').src = item.full || item.thumb;
    document.getElementById('lightboxModal').classList.add('active');
    document.body.style.overflow = 'hidden';
  }}

  function closeLightbox(e) {{
    document.getElementById('lightboxModal').classList.remove('active');
    document.body.style.overflow = '';
  }}

  document.addEventListener('keydown', (e) => {{
    if (e.key === 'Escape') closeLightbox();
  }});

  function showToast(msg) {{
    const toast = document.getElementById('toastBox');
    document.getElementById('toastMsg').textContent = msg;
    toast.classList.add('show');
    setTimeout(() => {{
      toast.classList.remove('show');
    }}, 2500);
  }}

  function copySingleUrl(url, name) {{
    navigator.clipboard.writeText(url).then(() => {{
      showToast('Đã sao chép link ' + name);
    }}).catch(() => {{
      showToast('Sao chép: ' + url);
    }});
  }}

  function copyAllUrls() {{
    const text = WEBSITES_DATA.map((w, i) => `${{i+1}}. ${{w.name}} - ${{w.url}}`).join('\\n');
    navigator.clipboard.writeText(text).then(() => {{
      showToast('Đã sao chép toàn bộ 20 URL website decor!');
    }}).catch(() => {{
      showToast('Không thể tự động sao chép');
    }});
  }}

  // Khởi chạy ban đầu
  renderCards(WEBSITES_DATA);
</script>

</body>
</html>
"""

with open(output_html, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"[+] Đã tạo thành công giao diện tương tác: {output_html}")
