# -*- coding: utf-8 -*-
import json, os, sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
candidates_file = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "03_Du_Lieu_Tam_Va_Test", "staging_all_candidates.json")

with open(candidates_file, "r", encoding="utf-8") as f:
    candidates = json.load(f)

js_candidates = json.dumps(candidates, ensure_ascii=False, indent=2)

template = """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Trạm Kiểm Duyệt Mẫu Website Đa Ngành (WebVault Staging) — Dark Zeit Edition</title>
  <link rel="icon" type="image/svg+xml" href="favicon.svg">
  <link rel="icon" type="image/png" href="favicon.png">
  <link rel="apple-touch-icon" href="favicon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-dark: #070709;
      --bg-surface: #101014;
      --bg-card: #121217;
      --border: rgba(255, 255, 255, 0.08);
      --border-hover: rgba(255, 255, 255, 0.22);
      --accent: #ff3b30;
      --accent-glow: rgba(255, 59, 48, 0.25);
      --success: #01a915;
      --success-glow: rgba(1, 169, 21, 0.25);
      --danger: #ef4444;
      --text-main: #f4f4f5;
      --text-muted: #a1a1aa;
      --text-dim: #71717a;
      --radius: 12px;
    }

    /* CUSTOM SLEEK DARK SCROLLBAR */
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      scrollbar-width: thin;
      scrollbar-color: rgba(255, 255, 255, 0.18) transparent;
    }

    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }

    ::-webkit-scrollbar-track {
      background: transparent;
    }

    ::-webkit-scrollbar-thumb {
      background: rgba(255, 255, 255, 0.18);
      border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
      background: rgba(255, 59, 48, 0.7);
    }

    ::-webkit-scrollbar-button {
      display: none !important;
      width: 0;
      height: 0;
    }

    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background-color: var(--bg-dark);
      color: var(--text-main);
      line-height: 1.5;
      -webkit-font-smoothing: antialiased;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    /* STICKY TOP STAGING BAR */
    .staging-header {
      background: rgba(16, 16, 20, 0.94);
      backdrop-filter: blur(14px);
      border-bottom: 1px solid var(--border);
      position: sticky;
      top: 0;
      z-index: 50;
      padding: 14px 24px;
    }

    .staging-header-inner {
      max-width: 1440px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
    }

    .staging-brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .staging-badge {
      background: linear-gradient(135deg, #ff3b30, #ff6b5b);
      color: #fff;
      font-size: 11px;
      font-weight: 800;
      padding: 4px 8px;
      border-radius: 6px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .staging-title h1 {
      font-size: 16px;
      font-weight: 800;
      color: #fff;
    }
    .staging-title p {
      font-size: 12px;
      color: var(--text-muted);
    }

    .staging-actions {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }

    .btn {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      font-size: 12px;
      font-weight: 600;
      padding: 8px 14px;
      border-radius: 8px;
      cursor: pointer;
      border: 1px solid transparent;
      transition: all 0.2s ease;
      text-decoration: none;
      white-space: nowrap;
    }

    .btn-approve-all {
      background: rgba(255, 255, 255, 0.08);
      border-color: rgba(255, 255, 255, 0.15);
      color: #fff;
    }
    .btn-approve-all:hover {
      background: rgba(255, 255, 255, 0.16);
      border-color: rgba(255, 255, 255, 0.3);
    }

    .btn-sync-hub {
      background: linear-gradient(135deg, #01a915, #018f12);
      color: #fff;
      box-shadow: 0 4px 14px var(--success-glow);
    }
    .btn-sync-hub:hover {
      transform: translateY(-1px);
      box-shadow: 0 6px 18px rgba(1, 169, 21, 0.4);
    }

    .btn-view-hub {
      background: rgba(255, 255, 255, 0.05);
      border-color: var(--border);
      color: var(--text-muted);
    }
    .btn-view-hub:hover {
      color: #fff;
      border-color: var(--border-hover);
    }

    /* STAGING TABS BAR (CHUYỂN ĐỔI CHỦ ĐỀ ĐA NGÀNH) */
    .staging-tabs-bar {
      background: rgba(14, 14, 18, 0.95);
      border-bottom: 1px solid var(--border);
      padding: 10px 24px;
      position: sticky;
      top: 61px;
      z-index: 45;
      backdrop-filter: blur(10px);
    }

    .staging-tabs-container {
      max-width: 1440px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      gap: 8px;
      overflow-x: auto;
      padding-bottom: 2px;
      scrollbar-width: none;
    }
    .staging-tabs-container::-webkit-scrollbar {
      display: none;
    }

    .staging-tab-btn {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      padding: 7px 14px;
      border-radius: 20px;
      font-size: 12.5px;
      font-weight: 600;
      color: var(--text-muted);
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.08);
      cursor: pointer;
      transition: all 0.2s ease;
      white-space: nowrap;
      user-select: none;
    }
    .staging-tab-btn:hover {
      color: #fff;
      background: rgba(255, 255, 255, 0.08);
      border-color: rgba(255, 255, 255, 0.18);
    }
    .staging-tab-btn.active {
      background: #ff3b30;
      color: #fff;
      border-color: #ff3b30;
      box-shadow: 0 4px 14px rgba(255, 59, 48, 0.35);
    }
    .tab-badge {
      background: rgba(0, 0, 0, 0.25);
      padding: 1px 7px;
      border-radius: 10px;
      font-size: 11px;
      font-weight: 700;
    }
    .staging-tab-btn.active .tab-badge {
      background: rgba(255, 255, 255, 0.25);
      color: #fff;
    }

    /* COUNTER STRIP */
    .counter-strip {
      max-width: 1440px;
      margin: 16px auto 0;
      padding: 0 24px;
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
    }

    .counter-text {
      font-size: 13px;
      color: var(--text-muted);
    }
    .counter-text b {
      color: #4ade80;
    }

    .topic-guide-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(255, 59, 48, 0.08);
      border: 1px solid rgba(255, 59, 48, 0.2);
      color: #ff9b94;
      font-size: 12px;
      padding: 4px 10px;
      border-radius: 6px;
    }

    /* MAIN CONTAINER & GRID */
    .main-container {
      max-width: 1440px;
      margin: 16px auto 40px;
      padding: 0 24px;
      width: 100%;
      flex: 1;
    }

    .cards-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 20px;
    }

    @media (min-width: 1280px) {
      .cards-grid {
        grid-template-columns: repeat(4, 1fr);
      }
    }

    /* STAGING CARD */
    .staging-card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      position: relative;
    }
    .staging-card:hover {
      border-color: var(--border-hover);
      transform: translateY(-3px);
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
    }

    .staging-card.is-selected {
      border-color: rgba(1, 169, 21, 0.6);
      box-shadow: 0 8px 24px rgba(1, 169, 21, 0.15);
    }

    .card-browser-bar {
      padding: 8px 12px;
      background: #0d0d10;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }

    .browser-url-pill {
      font-size: 11px;
      color: var(--text-muted);
      text-decoration: none;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 210px;
      font-family: monospace;
    }
    .browser-url-pill:hover {
      color: #fff;
      text-decoration: underline;
    }

    .card-thumbnail-box {
      position: relative;
      width: 100%;
      height: 200px;
      background: #09090b;
      overflow: hidden;
      cursor: pointer;
    }

    .card-thumb-img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: top center;
      transition: transform 0.4s ease;
      display: block;
    }

    .card-thumbnail-box:hover .card-thumb-img {
      transform: scale(1.03);
    }

    .thumbnail-zoom-hint {
      position: absolute;
      bottom: 10px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(15, 15, 20, 0.92);
      backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 255, 255, 0.18);
      color: #fff;
      font-size: 11px;
      font-weight: 600;
      padding: 4px 10px;
      border-radius: 20px;
      display: flex;
      align-items: center;
      gap: 5px;
      opacity: 0;
      transition: opacity 0.2s ease, transform 0.2s ease;
      pointer-events: none;
      box-shadow: 0 4px 16px rgba(0,0,0,0.5);
      white-space: nowrap;
    }
    .card-thumbnail-box:hover .thumbnail-zoom-hint {
      opacity: 1;
      transform: translateX(-50%) translateY(-2px);
    }

    .card-body {
      padding: 14px;
      display: flex;
      flex-direction: column;
      flex: 1;
      gap: 8px;
    }

    .card-meta-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      font-size: 11px;
    }

    .badge-industry {
      background: rgba(255, 59, 48, 0.12);
      color: #ff756d;
      border: 1px solid rgba(255, 59, 48, 0.25);
      padding: 2px 7px;
      border-radius: 4px;
      font-weight: 700;
    }

    .badge-vibe {
      background: rgba(255, 255, 255, 0.06);
      color: var(--text-muted);
      border: 1px solid rgba(255, 255, 255, 0.1);
      padding: 2px 7px;
      border-radius: 4px;
      font-weight: 500;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      max-width: 140px;
    }

    .card-title {
      font-size: 14px;
      font-weight: 700;
      color: #fff;
      line-height: 1.35;
    }

    .card-desc {
      font-size: 12px;
      color: var(--text-muted);
      line-height: 1.5;
      display: -webkit-box;
      -webkit-line-clamp: 3;
      -webkit-box-orient: vertical;
      overflow: hidden;
      flex: 1;
    }

    .approval-toggle-btn {
      margin-top: 6px;
      padding: 8px 12px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.2s ease;
      border: 1px solid transparent;
      width: 100%;
    }

    .btn-selected {
      background: rgba(1, 169, 21, 0.16);
      border-color: rgba(1, 169, 21, 0.5);
      color: #4ade80;
    }
    .btn-selected:hover {
      background: rgba(239, 68, 68, 0.18);
      border-color: rgba(239, 68, 68, 0.45);
      color: #f87171;
    }

    .btn-unselected {
      background: rgba(255, 255, 255, 0.05);
      border-color: rgba(255, 255, 255, 0.12);
      color: var(--text-main);
    }
    .btn-unselected:hover {
      background: rgba(1, 169, 21, 0.18);
      border-color: rgba(1, 169, 21, 0.4);
      color: #4ade80;
    }

    /* LIGHTBOX MODAL */
    .lightbox-modal {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.96);
      backdrop-filter: blur(14px);
      z-index: 999;
      display: none;
      flex-direction: column;
    }
    .lightbox-modal.active {
      display: flex;
    }

    .lightbox-header {
      padding: 10px 20px;
      background: #101015;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      color: #fff;
      flex-wrap: wrap;
    }

    .lightbox-title-box {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .lightbox-badge-id {
      background: rgba(255, 59, 48, 0.18);
      color: #ff6e66;
      border: 1px solid rgba(255, 59, 48, 0.3);
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 11.5px;
      font-weight: 700;
    }
    .lightbox-title-box h3 {
      font-size: 14.5px;
      font-weight: 700;
      color: #fff;
    }

    .lightbox-actions {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }

    .lightbox-nav-btn {
      background: #1c1c24;
      border: 1px solid var(--border);
      color: var(--text-main);
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      transition: all 0.2s ease;
    }
    .lightbox-nav-btn:hover {
      background: #2a2a38;
      color: #fff;
    }

    .lightbox-toggle-btn {
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
      border: 1px solid transparent;
    }
    .lightbox-toggle-btn.is-approved {
      background: rgba(1, 169, 21, 0.2);
      border-color: rgba(1, 169, 21, 0.4);
      color: #4ade80;
    }
    .lightbox-toggle-btn.is-unselected {
      background: rgba(255, 255, 255, 0.08);
      border-color: rgba(255, 255, 255, 0.15);
      color: #fff;
    }

    .lightbox-body {
      flex: 1;
      overflow-y: auto;
      overflow-x: auto;
      padding: 20px;
      display: flex;
      justify-content: center;
      align-items: flex-start;
      position: relative;
    }

    .lightbox-body.mode-fit {
      overflow: hidden;
      align-items: center;
    }
    .lightbox-body.mode-fit .lightbox-img-wrapper {
      max-width: 100%;
      height: 100%;
      display: flex;
      justify-content: center;
      align-items: center;
    }
    .lightbox-body.mode-fit .lightbox-img-wrapper img {
      max-width: 100%;
      max-height: 85vh;
      object-fit: contain;
      cursor: zoom-in;
    }

    .lightbox-body.mode-full .lightbox-img-wrapper {
      max-width: 1360px;
      width: 100%;
      margin: 0 auto;
    }
    .lightbox-body.mode-full .lightbox-img-wrapper img {
      width: 100%;
      height: auto;
      display: block;
      cursor: zoom-out;
    }

    .lightbox-body.mode-custom .lightbox-img-wrapper {
      max-width: none;
      margin: 0 auto;
    }
    .lightbox-body.mode-custom .lightbox-img-wrapper img {
      width: 100%;
      height: auto;
      display: block;
    }

    .lightbox-zoom-bar {
      position: absolute;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(18, 18, 24, 0.94);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 30px;
      padding: 6px 14px;
      display: flex;
      align-items: center;
      gap: 8px;
      box-shadow: 0 12px 36px rgba(0, 0, 0, 0.7);
      z-index: 100;
      font-size: 12px;
      color: #fff;
    }

    .zoom-btn {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: #fff;
      width: 26px;
      height: 26px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-weight: 700;
    }
    .zoom-btn:hover {
      background: rgba(255, 255, 255, 0.2);
    }

    .zoom-pill-mode-btn {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: var(--text-main);
      padding: 4px 10px;
      border-radius: 14px;
      font-size: 11.5px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .zoom-pill-mode-btn.active {
      background: var(--accent);
      color: #fff;
      border-color: var(--accent);
    }

    .zoom-level-text {
      font-weight: 700;
      color: #4ade80;
      min-width: 50px;
      text-align: center;
    }

    .zoom-hint-text {
      font-size: 11px;
      color: var(--text-dim);
      border-left: 1px solid rgba(255, 255, 255, 0.12);
      padding-left: 8px;
    }

    /* TOAST */
    .toast {
      position: fixed;
      bottom: 24px;
      right: 24px;
      background: #16161e;
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: #fff;
      padding: 12px 18px;
      border-radius: 10px;
      font-size: 13px;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 10px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.6);
      transform: translateY(100px);
      opacity: 0;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      z-index: 1000;
    }
    .toast.show {
      transform: translateY(0);
      opacity: 1;
    }

    @media (max-width: 768px) {
      .staging-header {
        padding: 12px 16px;
      }
      .staging-tabs-bar {
        top: 104px;
        padding: 8px 16px;
      }
      .counter-strip {
        padding: 0 16px;
      }
      .main-container {
        padding: 0 16px;
      }
      .cards-grid {
        grid-template-columns: 1fr;
      }
      .zoom-hint-text {
        display: none;
      }
    }
  </style>
</head>
<body>

  <!-- STAGING HEADER -->
  <header class="staging-header">
    <div class="staging-header-inner">
      <div class="staging-brand">
        <span class="staging-badge">Kiểm Duyệt Nháp</span>
        <div class="staging-title">
          <h1>Trạm Thẩm Định Mẫu Website Đa Ngành</h1>
          <p>Lưu trữ các chủ đề nghiên cứu chờ duyệt — Bấm chọn để nạp vào WebVault</p>
        </div>
      </div>

      <div class="staging-actions">
        <button class="btn btn-approve-all" id="btnToggleAll" onclick="toggleAll()">
          Chọn Tất Cả
        </button>

        <button class="btn btn-sync-hub" onclick="saveApprovalSelection()">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
          Sao Chép Danh Sách Duyệt (<span id="btnApprovedCount">0</span>)
        </button>

        <a href="index.html" class="btn btn-view-hub">
          Mở Thư Viện Chính WebVault ↗
        </a>
      </div>
    </div>
  </header>

  <!-- STAGING TABS BAR (CHỦ ĐỀ ĐA NGÀNH) -->
  <nav class="staging-tabs-bar">
    <div class="staging-tabs-container">
      <button class="staging-tab-btn" data-industry="all" onclick="filterStagingTopic('all')">
        <span>⚡</span> Tất Cả Nháp <span class="tab-badge" id="badgeAll">60</span>
      </button>
      <button class="staging-tab-btn active" data-industry="ban-dong-ho" onclick="filterStagingTopic('ban-dong-ho')">
        <span>⌚</span> Bán Đồng Hồ <span class="tab-badge" id="badgeDongHo">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="decor-su-kien" onclick="filterStagingTopic('decor-su-kien')">
        <span>🎀</span> Decor Sự Kiện <span class="tab-badge" id="badgeDecor">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="tiec-cuoi" onclick="filterStagingTopic('tiec-cuoi')">
        <span>💍</span> Tiệc Cưới & Wedding <span class="tab-badge" id="badgeWedding">20</span>
      </button>
    </div>
  </nav>

  <!-- COUNTER STRIP -->
  <div class="counter-strip">
    <div class="counter-text">
      Chủ đề đang xem: <b id="statTopicName" style="color:#fff;">Bán Đồng Hồ</b> • Đang chọn <b id="statApproved">0</b> / <span id="statTotalTopic">20</span> mẫu
    </div>
    <div class="topic-guide-pill">
      💡 Nhấn '+ Thêm Mẫu Này' để chọn mẫu bạn ưng ý đưa lên WebVault
    </div>
  </div>

  <!-- MAIN CARDS -->
  <main class="main-container">
    <div class="cards-grid" id="cardsGrid">
      <!-- Generated by JS -->
    </div>
  </main>

  <!-- LIGHTBOX MODAL (XEM ẢNH FULL-PAGE) -->
  <div class="lightbox-modal" id="lightboxModal">
    <div class="lightbox-header">
      <div class="lightbox-title-box">
        <span class="lightbox-badge-id" id="lbIndex">DH01</span>
        <h3 id="lbTitle">Tên Website</h3>
      </div>
      <div class="lightbox-actions">
        <button class="lightbox-nav-btn" onclick="prevLightbox()" title="Xem mẫu trước (Phím mũi tên Trái ←)">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"></polyline></svg>
          Trước
        </button>
        <button class="lightbox-nav-btn" onclick="nextLightbox()" title="Xem mẫu tiếp theo (Phím mũi tên Phải →)">
          Sau
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg>
        </button>

        <button id="lbToggleBtn" class="lightbox-toggle-btn is-unselected" onclick="toggleLightboxApproval()">
          <span id="lbToggleText">+ Thêm Mẫu Này Để Đồng Bộ</span>
        </button>

        <a id="lbExternalLink" href="#" target="_blank" rel="noopener noreferrer" class="btn btn-view-hub" style="padding: 6px 12px; font-size: 12px;">
          Mở Web Thật ↗
        </a>

        <button class="btn btn-view-hub" onclick="closeLightbox()" style="padding: 6px 12px; font-size: 12px;">
          Đóng (ESC)
        </button>
      </div>
    </div>

    <div class="lightbox-body mode-fit" id="lbBody" onclick="handleLightboxBodyClick(event)">
      <div class="lightbox-img-wrapper" id="lbImgWrapper" onclick="handleImageClick(event)">
        <img id="lbImage" src="" alt="Full preview">
      </div>

      <div class="lightbox-zoom-bar" onclick="event.stopPropagation()">
        <button class="zoom-btn" onclick="zoomStep(-1)">−</button>
        <span class="zoom-level-text" id="lbZoomLevel">Fit 100%</span>
        <button class="zoom-btn" onclick="zoomStep(1)">+</button>
        <div style="width: 1px; height: 16px; background: rgba(255,255,255,0.15); margin: 0 2px;"></div>
        <button class="zoom-pill-mode-btn active" id="btnModeFit" onclick="setLightboxMode('fit')">
          ⛶ Vừa màn hình
        </button>
        <button class="zoom-pill-mode-btn" id="btnModeFull" onclick="setLightboxMode('full')">
          100% Chi tiết
        </button>
        <span class="zoom-hint-text">💡 Ctrl + Cuộn chuột để zoom</span>
      </div>
    </div>
  </div>

  <div class="toast" id="toastBox">
    <span id="toastMsg">Thao tác thành công</span>
  </div>

<script>
  // TỔNG HỢP CÁC CHỦ ĐỀ CHỜ DUYỆT (60 MẪU)
  const CANDIDATES = __CANDIDATES_JSON__;

  // Tải trạng thái phê duyệt từ LocalStorage
  let approvalMap = {};
  try {
    const saved = localStorage.getItem('webvault_staging_approval_v2');
    if (saved) approvalMap = JSON.parse(saved);
  } catch(e) {
    approvalMap = {};
  }

  // Chủ đề đang xem (mặc định ban-dong-ho hoặc đọc từ URL ?industry=...)
  let currentTopic = 'ban-dong-ho';

  function initTopicFromUrl() {
    const params = new URLSearchParams(window.location.search);
    const indParam = params.get('industry') || params.get('topic');
    if (indParam && ['all', 'ban-dong-ho', 'decor-su-kien', 'tiec-cuoi'].includes(indParam)) {
      currentTopic = indParam;
    }
  }

  function getFilteredCandidates() {
    if (currentTopic === 'all') return CANDIDATES;
    return CANDIDATES.filter(c => c.industry === currentTopic);
  }

  function filterStagingTopic(topic) {
    currentTopic = topic;
    
    // Cập nhật tab active
    document.querySelectorAll('.staging-tab-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.industry === topic);
    });

    // Cập nhật URL mà không reload trang
    const newUrl = new URL(window.location);
    if (topic === 'all') {
      newUrl.searchParams.delete('industry');
      newUrl.searchParams.delete('topic');
    } else {
      newUrl.searchParams.set('industry', topic);
    }
    window.history.replaceState({}, '', newUrl);

    renderStaging();
  }

  function renderStaging() {
    const grid = document.getElementById('cardsGrid');
    grid.innerHTML = '';

    const currentList = getFilteredCandidates();
    let approvedInTopic = 0;
    let totalApprovedAll = 0;

    CANDIDATES.forEach(c => {
      if (approvalMap[c.id]) totalApprovedAll++;
    });

    currentList.forEach(item => {
      const isSelected = !!approvalMap[item.id];
      if (isSelected) approvedInTopic++;

      const card = document.createElement('div');
      card.className = `staging-card ${isSelected ? 'is-selected' : ''}`;
      card.id = `card-${item.id}`;

      card.innerHTML = `
        <div class="card-browser-bar">
          <a href="${item.url}" target="_blank" class="browser-url-pill">https://${item.domain}/</a>
          <span style="font-size: 11px; color: var(--text-dim);">${item.location}</span>
        </div>

        <div class="card-thumbnail-box" onclick="openLightbox('${item.id}')" title="Nhấp vào để xem ảnh full-page toàn bộ trang">
          <img src="${item.thumb}" class="card-thumb-img" alt="${item.name}" loading="lazy" onerror="this.src='https://placehold.co/600x400/121217/ffffff?text=${encodeURIComponent(item.short_name)}'">
          <div class="thumbnail-zoom-hint">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            Nhấp xem ảnh Full
          </div>
        </div>

        <div class="card-body">
          <div class="card-meta-row">
            <span class="badge-industry">${item.industry_name || 'Đồng Hồ'}</span>
            <span class="badge-vibe" title="${item.vibe}">${item.vibe}</span>
          </div>

          <h3 class="card-title">${item.id.toUpperCase()}. ${item.short_name}</h3>
          <p class="card-desc">${item.desc}</p>

          <button class="approval-toggle-btn ${isSelected ? 'btn-selected' : 'btn-unselected'}" onclick="toggleApproval('${item.id}')">
            ${isSelected 
              ? `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg> ✓ Đã Thêm (Nhấn để hủy)` 
              : `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg> + Thêm Mẫu Này Để Đồng Bộ`}
          </button>
        </div>
      `;

      grid.appendChild(card);
    });

    // Cập nhật thống kê
    const topicMapName = {
      'all': 'Tất Cả Nháp Chờ Duyệt',
      'ban-dong-ho': 'Bán Đồng Hồ Chính Hãng & Xa Xỉ',
      'decor-su-kien': 'Decor Tiệc & Trang Trí Sự Kiện',
      'tiec-cuoi': 'Tiệc Cưới & Wedding Planner'
    };
    document.getElementById('statTopicName').textContent = topicMapName[currentTopic] || currentTopic;
    document.getElementById('statApproved').textContent = approvedInTopic;
    document.getElementById('statTotalTopic').textContent = currentList.length;
    document.getElementById('btnApprovedCount').textContent = totalApprovedAll;

    // Cập nhật nhãn nút Chọn tất cả
    const toggleAllBtn = document.getElementById('btnToggleAll');
    if (toggleAllBtn) {
      const allSelectedInTopic = currentList.length > 0 && currentList.every(c => approvalMap[c.id]);
      toggleAllBtn.textContent = allSelectedInTopic ? `Bỏ Chọn Chủ Đề Này` : `Chọn Hết ${currentList.length} Mẫu Này`;
    }

    // Lưu LocalStorage
    try {
      localStorage.setItem('webvault_staging_approval_v2', JSON.stringify(approvalMap));
    } catch(e) {}
  }

  function toggleApproval(id) {
    approvalMap[id] = !approvalMap[id];
    const isNowSelected = approvalMap[id];
    const item = CANDIDATES.find(c => c.id === id);
    const itemName = item ? item.short_name : 'mẫu';

    if (isNowSelected) {
      showToast(`✨ Đã thêm ${itemName} vào danh sách duyệt!`);
    } else {
      showToast(`Đã bỏ chọn ${itemName}.`);
    }

    renderStaging();
  }

  function toggleAll() {
    const currentList = getFilteredCandidates();
    if (currentList.length === 0) return;

    const allSelectedInTopic = currentList.every(c => approvalMap[c.id]);
    const nextState = !allSelectedInTopic;

    currentList.forEach(c => {
      approvalMap[c.id] = nextState;
    });

    showToast(nextState ? `✓ Đã chọn ${currentList.length} mẫu trong chủ đề!` : `Đã bỏ chọn các mẫu trong chủ đề.`);
    renderStaging();
  }

  function saveApprovalSelection() {
    const approvedList = CANDIDATES.filter(c => approvalMap[c.id]);
    if (approvedList.length === 0) {
      showToast('⚠️ Bạn chưa chọn mẫu nào! Nhấn "+ Thêm Mẫu Này" để chọn.');
      return;
    }

    // Tạo danh sách URL để copy nhanh
    const urlText = approvedList.map(c => c.url).join('\\n');
    navigator.clipboard.writeText(urlText).then(() => {
      showToast(`✓ Đã sao chép ${approvedList.length} link đã duyệt vào Clipboard! Bạn có thể dán vào khung chat.`);
    }).catch(() => {
      showToast(`✓ Đã lưu ${approvedList.length} mẫu đã duyệt.`);
    });
  }

  let toastTimer = null;
  function showToast(msg) {
    const toast = document.getElementById('toastBox');
    const toastMsg = document.getElementById('toastMsg');
    if (!toast || !toastMsg) return;
    toastMsg.textContent = msg;
    toast.classList.add('show');

    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => {
      toast.classList.remove('show');
    }, 2800);
  }

  // LIGHTBOX MODAL
  let currentLbIndex = 0;
  let currentLbMode = 'fit';
  let currentCustomWidth = 1360;
  const BASE_FULL_WIDTH = 1360;

  function setLightboxMode(mode) {
    const lbBody = document.getElementById('lbBody');
    const wrapper = document.getElementById('lbImgWrapper');
    const levelText = document.getElementById('lbZoomLevel');
    const fitBtn = document.getElementById('btnModeFit');
    const fullBtn = document.getElementById('btnModeFull');
    if (!lbBody || !wrapper) return;

    currentLbMode = mode;
    lbBody.className = `lightbox-body mode-${mode}`;

    if (mode === 'fit') {
      wrapper.style.width = '';
      wrapper.style.maxWidth = '';
      if (levelText) levelText.textContent = 'Fit 100%';
      if (fitBtn) fitBtn.classList.add('active');
      if (fullBtn) fullBtn.classList.remove('active');
      lbBody.scrollTop = 0;
      lbBody.scrollLeft = 0;
    } else if (mode === 'full') {
      currentCustomWidth = BASE_FULL_WIDTH;
      wrapper.style.width = '100%';
      wrapper.style.maxWidth = '1360px';
      if (levelText) levelText.textContent = '100%';
      if (fitBtn) fitBtn.classList.remove('active');
      if (fullBtn) fullBtn.classList.add('active');
    } else if (mode === 'custom') {
      wrapper.style.maxWidth = 'none';
      wrapper.style.width = `${currentCustomWidth}px`;
      const pct = Math.round((currentCustomWidth / BASE_FULL_WIDTH) * 100);
      if (levelText) levelText.textContent = `${pct}%`;
      if (fitBtn) fitBtn.classList.remove('active');
      if (fullBtn) fullBtn.classList.remove('active');
    }
  }

  function handleImageClick(e) {
    e.stopPropagation();
    if (currentLbMode === 'fit') {
      setLightboxMode('full');
      showToast('🔍 Đã mở Full Size (100%)');
    } else {
      setLightboxMode('fit');
      showToast('⛶ Đã thu về Vừa Khung Hình');
    }
  }

  function zoomStep(delta) {
    if (currentLbMode === 'fit') {
      currentCustomWidth = BASE_FULL_WIDTH;
    }
    const step = 200;
    let newWidth = currentCustomWidth + (delta * step);
    if (newWidth < 450) {
      setLightboxMode('fit');
      return;
    }
    if (newWidth > 3600) newWidth = 3600;
    currentCustomWidth = newWidth;
    setLightboxMode('custom');
  }

  function openLightbox(id) {
    const currentList = getFilteredCandidates();
    const idx = currentList.findIndex(c => c.id === id);
    if (idx === -1) return;
    currentLbIndex = idx;
    updateLightboxContent();

    const modal = document.getElementById('lightboxModal');
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
    setLightboxMode('fit');
  }

  function updateLightboxContent() {
    const currentList = getFilteredCandidates();
    const item = currentList[currentLbIndex];
    if (!item) return;

    const isApproved = !!approvalMap[item.id];

    document.getElementById('lbIndex').textContent = `${item.id.toUpperCase()} (${currentLbIndex + 1}/${currentList.length})`;
    document.getElementById('lbTitle').textContent = `${item.name} (${item.industry_name || ''})`;
    document.getElementById('lbExternalLink').href = item.url;
    document.getElementById('lbImage').src = item.full;

    const toggleBtn = document.getElementById('lbToggleBtn');
    if (toggleBtn) {
      if (isApproved) {
        toggleBtn.className = 'lightbox-toggle-btn is-approved';
        toggleBtn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg> <span>✓ Đã Thêm (Nhấn để hủy)</span>`;
      } else {
        toggleBtn.className = 'lightbox-toggle-btn is-unselected';
        toggleBtn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg> <span>+ Thêm Mẫu Này Để Đồng Bộ</span>`;
      }
    }

    const lbBody = document.getElementById('lbBody');
    if (lbBody) {
      lbBody.scrollTop = 0;
      lbBody.scrollLeft = 0;
    }
  }

  function toggleLightboxApproval() {
    const currentList = getFilteredCandidates();
    const item = currentList[currentLbIndex];
    if (!item) return;
    approvalMap[item.id] = !approvalMap[item.id];
    updateLightboxContent();
    renderStaging();
  }

  function nextLightbox() {
    const currentList = getFilteredCandidates();
    if (currentLbIndex < currentList.length - 1) {
      currentLbIndex++;
    } else {
      currentLbIndex = 0;
    }
    updateLightboxContent();
    setLightboxMode('fit');
  }

  function prevLightbox() {
    const currentList = getFilteredCandidates();
    if (currentLbIndex > 0) {
      currentLbIndex--;
    } else {
      currentLbIndex = currentList.length - 1;
    }
    updateLightboxContent();
    setLightboxMode('fit');
  }

  function closeLightbox() {
    const modal = document.getElementById('lightboxModal');
    modal.classList.remove('active');
    document.body.style.overflow = '';
  }

  function handleLightboxBodyClick(e) {
    if (e.target.id === 'lbBody') {
      closeLightbox();
    }
  }

  document.addEventListener('keydown', (e) => {
    const modal = document.getElementById('lightboxModal');
    if (!modal || !modal.classList.contains('active')) return;

    if (e.key === 'Escape') {
      closeLightbox();
    } else if (e.key === 'ArrowRight') {
      nextLightbox();
    } else if (e.key === 'ArrowLeft') {
      prevLightbox();
    } else if (e.key === ' ' || e.code === 'Space') {
      e.preventDefault();
      toggleLightboxApproval();
    } else if (e.key === '+' || e.key === '=') {
      zoomStep(1);
    } else if (e.key === '-' || e.key === '_') {
      zoomStep(-1);
    } else if (e.key === '0') {
      setLightboxMode('fit');
    } else if (e.key === '1') {
      setLightboxMode('full');
    }
  });

  window.addEventListener('wheel', (e) => {
    const modal = document.getElementById('lightboxModal');
    if (!modal || !modal.classList.contains('active')) return;

    if (e.ctrlKey) {
      e.preventDefault();
      const delta = e.deltaY < 0 ? 1 : -1;
      zoomStep(delta);
    }
  }, { passive: false });

  document.addEventListener('DOMContentLoaded', () => {
    initTopicFromUrl();
    // Cập nhật tab active
    document.querySelectorAll('.staging-tab-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.industry === currentTopic);
    });
    renderStaging();
  });
</script>

</body>
</html>
"""

final_html = template.replace("__CANDIDATES_JSON__", js_candidates)

staging_html_path = os.path.join(BASE_DIR, "web_nhap_staging.html")
with open(staging_html_path, "w", encoding="utf-8") as f:
    f.write(final_html)

print(f"[+] Đã tạo mới web_nhap_staging.html chuẩn Đa Ngành ({len(candidates)} mẫu nháp)!")
