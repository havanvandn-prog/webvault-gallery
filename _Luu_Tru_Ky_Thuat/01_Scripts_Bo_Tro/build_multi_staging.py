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

    .btn-download {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 12px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      background: linear-gradient(135deg, #10b981, #059669);
      border: 1px solid rgba(16, 185, 129, 0.45);
      color: #fff;
      box-shadow: 0 4px 14px rgba(16, 185, 129, 0.28);
      transition: all 0.2s ease;
      white-space: nowrap;
    }
    .btn-download:hover {
      background: linear-gradient(135deg, #34d399, #10b981);
      transform: translateY(-1px);
    }
    .btn-download:disabled {
      opacity: 0.7;
      cursor: wait;
      transform: none;
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
        <span>⚡</span> Tất Cả Nháp <span class="tab-badge" id="badgeAll">725</span>
      </button>
      <button class="staging-tab-btn active" data-industry="phan-mem-saas" onclick="filterStagingTopic('phan-mem-saas')">
        <span>🚀</span> Phần Mềm & SaaS <span class="tab-badge" id="badgeSaas">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="doanh-nghiep-b2b" onclick="filterStagingTopic('doanh-nghiep-b2b')">
        <span>🏢</span> Doanh Nghiệp B2B <span class="tab-badge" id="badgeB2b">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="khoa-hoc-online-lms" onclick="filterStagingTopic('khoa-hoc-online-lms')">
        <span>🎓</span> Khóa Học Online & LMS <span class="tab-badge" id="badgeKhoaHoc">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="nha-hang-am-thuc" onclick="filterStagingTopic('nha-hang-am-thuc')">
        <span>🍽️</span> Nhà Hàng & Đặt Tiệc <span class="tab-badge" id="badgeNhaHang">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="ve-sinh-chuyen-nha" onclick="filterStagingTopic('ve-sinh-chuyen-nha')">
        <span>🚚</span> Vệ Sinh & Chuyển Nhà <span class="tab-badge" id="badgeVeSinhChuyenNha">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="sua-chua-dien-lanh" onclick="filterStagingTopic('sua-chua-dien-lanh')">
        <span>🔧</span> Điện Lạnh & Sửa Nhà <span class="tab-badge" id="badgeDienLanh">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="qua-tang-hoa-tuoi" onclick="filterStagingTopic('qua-tang-hoa-tuoi')">
        <span>🎁</span> Quà Tặng & Hoa Tươi <span class="tab-badge" id="badgeQuaTang">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="me-va-be" onclick="filterStagingTopic('me-va-be')">
        <span>🍼</span> Mẹ & Bé <span class="tab-badge" id="badgeMeVaBe">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="gia-dung-thiet-bi-bep" onclick="filterStagingTopic('gia-dung-thiet-bi-bep')">
        <span>🍳</span> Gia Dụng & Thiết Bị Bếp <span class="tab-badge" id="badgeGiaDung">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="dien-may-cong-nghe" onclick="filterStagingTopic('dien-may-cong-nghe')">
        <span>💻</span> Điện Máy & Công Nghệ <span class="tab-badge" id="badgeDienMay">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="thoi-trang-giay-dep" onclick="filterStagingTopic('thoi-trang-giay-dep')">
        <span>👗</span> Thời Trang & Giày Dép <span class="tab-badge" id="badgeThoiTrang">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="my-pham-tpcn" onclick="filterStagingTopic('my-pham-tpcn')">
        <span>💄</span> Mỹ Phẩm & TPCN <span class="tab-badge" id="badgeMyPham">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="phong-kham-y-te" onclick="filterStagingTopic('phong-kham-y-te')">
        <span>🏥</span> Phòng Khám & Y Tế <span class="tab-badge" id="badgePhongKham">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="spa-tham-my-vien" onclick="filterStagingTopic('spa-tham-my-vien')">
        <span>💆‍♀️</span> Spa & Thẩm Mỹ Viện <span class="tab-badge" id="badgeSpa">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="nha-khoa" onclick="filterStagingTopic('nha-khoa')">
        <span>🦷</span> Nha Khoa & Trồng Răng <span class="tab-badge" id="badgeNhaKhoa">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="vat-lieu-xay-dung" onclick="filterStagingTopic('vat-lieu-xay-dung')">
        <span>🧱</span> Vật Liệu Xây Dựng <span class="tab-badge" id="badgeVlxd">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="moi-gioi-nha-dat-cho-thue" onclick="filterStagingTopic('moi-gioi-nha-dat-cho-thue')">
        <span>🏘️</span> Môi Giới Nhà Đất & Cho Thuê <span class="tab-badge" id="badgeMoiGioiBds">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="xay-dung" onclick="filterStagingTopic('xay-dung')">
        <span>🏗️</span> Mảng Xây Dựng <span class="tab-badge" id="badgeXayDung">40</span>
      </button>
      <button class="staging-tab-btn" data-industry="trung-tam-tieng-anh-dep" onclick="filterStagingTopic('trung-tam-tieng-anh-dep')">
        <span>🏫</span> Tiếng Anh (Bố Cục Đẹp) <span class="tab-badge" id="badgeAnhNguDep">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="banh-mi-quoc-te" onclick="filterStagingTopic('banh-mi-quoc-te')">
        <span>🥖</span> Bánh Mì Quốc Tế <span class="tab-badge" id="badgeBanhMiQuocTe">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="khach-san" onclick="filterStagingTopic('khach-san')">
        <span>🏨</span> Khách Sạn & Resort <span class="tab-badge" id="badgeKhachSan">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="landing-page-oto-mercedes" onclick="filterStagingTopic('landing-page-oto-mercedes')">
        <span>🚗</span> LP Mercedes & Ô Tô <span class="tab-badge" id="badgeAutoMercedesLP">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="noi-that-sang-trong" onclick="filterStagingTopic('noi-that-sang-trong')">
        <span>✨</span> Nội Thất Sang Trọng <span class="tab-badge" id="badgeNoiThatLux">10</span>
      </button>
      <button class="staging-tab-btn" data-industry="noi-that" onclick="filterStagingTopic('noi-that')">
        <span>🛋️</span> Nội Thất <span class="tab-badge" id="badgeNoiThat">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="phong-thuy" onclick="filterStagingTopic('phong-thuy')">
        <span>☯️</span> Phong Thủy <span class="tab-badge" id="badgePhongThuy">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="phong-kham-thu-y" onclick="filterStagingTopic('phong-kham-thu-y')">
        <span>🐾</span> Phòng Khám Thú Y <span class="tab-badge" id="badgeThuY">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="website-coupon-ma-giam-gia" onclick="filterStagingTopic('website-coupon-ma-giam-gia')">
        <span>🎟️</span> Coupon & Săn Deal <span class="tab-badge" id="badgeCoupon">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="landing-page-lap-mang" onclick="filterStagingTopic('landing-page-lap-mang')">
        <span>🎯</span> Landing Page Lắp Mạng <span class="tab-badge" id="badgeLpLapMang">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="lap-mang-fpt" onclick="filterStagingTopic('lap-mang-fpt')">
        <span>🌐</span> Lắp Mạng FPT <span class="tab-badge" id="badgeFpt">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="cafe-va-banh-mi" onclick="filterStagingTopic('cafe-va-banh-mi')">
        <span>☕</span> Cafe & Bánh Mì <span class="tab-badge" id="badgeCafeBanhMi">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="trung-tam-anh-ngu" onclick="filterStagingTopic('trung-tam-anh-ngu')">
        <span>🎓</span> Trung Tâm Anh Ngữ <span class="tab-badge" id="badgeAnhNgu">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="ban-may-anh" onclick="filterStagingTopic('ban-may-anh')">
        <span>📷</span> Máy Chụp Ảnh <span class="tab-badge" id="badgeMayAnh">1</span>
      </button>
      <button class="staging-tab-btn" data-industry="mua-ban-oto-cu" onclick="filterStagingTopic('mua-ban-oto-cu')">
        <span>🚗</span> Mua Bán Xe Ô Tô Cũ <span class="tab-badge" id="badgeOtoCu">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="du-hoc-dinh-cu-my" onclick="filterStagingTopic('du-hoc-dinh-cu-my')">
        <span>🎓</span> Du Học & Định Cư Mỹ <span class="tab-badge" id="badgeDuHocDinhCu">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="phong-tap-fitness" onclick="filterStagingTopic('phong-tap-fitness')">
        <span>🏋️‍♂️</span> Fitness & Gym <span class="tab-badge" id="badgeFitness">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="ban-dong-ho" onclick="filterStagingTopic('ban-dong-ho')">
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
      Chủ đề đang xem: <b id="statTopicName" style="color:#fff;">Landing Page Lắp Đặt Mạng Internet & FPT (1-Page Chuẩn Chuyển Đổi Google Ads)</b> • Đang chọn <b id="statApproved">0</b> / <span id="statTotalTopic">20</span> mẫu
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

        <button type="button" id="lbDownloadBtn" class="btn-download" onclick="downloadLightboxImage()" title="Tải nhanh ảnh giao diện full-page xuống máy (Phím D)">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
          <span id="lbDownloadText">Tải ảnh</span>
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

  // Chủ đề đang xem (mặc định my-pham-tpcn hoặc đọc từ URL ?industry=...)
  let currentTopic = 'phan-mem-saas';

  function initTopicFromUrl() {
    const params = new URLSearchParams(window.location.search);
    const indParam = params.get('industry') || params.get('topic') || 'phan-mem-saas';
    const validTopics = Array.from(document.querySelectorAll('.staging-tab-btn')).map(btn => btn.dataset.industry);
    if (indParam && validTopics.includes(indParam)) {
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
          <a href="${item.url}" target="_blank" class="browser-url-pill" title="${item.url}">${(item.url || '').replace(/^https?:\/\//, '') || item.domain}</a>
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
            <span class="badge-industry">${item.industry_name || 'Mẫu Web'}</span>
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
      'phan-mem-saas': 'Bán Sản Phẩm Số, Tài Khoản, Phần Mềm & SaaS (SaaS Việt Nam, Shop Tài Khoản Số & Siêu Phẩm UI/UX Quốc Tế)',
      'doanh-nghiep-b2b': 'Doanh Nghiệp B2B (Logistics, Luật, Kế Toán, In Ấn & Dịch Vụ Doanh Nghiệp VN + Quốc Tế)',
      'khoa-hoc-online-lms': 'Bán Khóa Học Online (LMS) & Coaching Cá Nhân (Nền Tảng Học VN, Đào Tạo Kỹ Năng & EdTech Quốc Tế)',
      'nha-hang-am-thuc': 'Nhà Hàng, Lẩu Nướng & Đặt Tiệc (Chuỗi Ẩm Thực VN, Nhà Hàng Cao Cấp & Fine Dining Quốc Tế)',
      've-sinh-chuyen-nha': 'Vệ Sinh Công Nghiệp & Chuyển Nhà Trọn Gói (Chuyển Nhà VN, Vệ Sinh Văn Phòng & Chuẩn CRO Quốc Tế)',
      'sua-chua-dien-lanh': 'Sửa Chữa Điện Lạnh, Điện Nước & Chống Thấm (Dịch Vụ Địa Phương VN & Home Services Chuẩn CRO Quốc Tế)',
      'qua-tang-hoa-tuoi': 'Quà Tặng Doanh Nghiệp, Giỏ Quà Tết & Hoa Tươi (Shop Hoa VN, Quà B2B & Chuẩn UI/UX Quốc Tế)',
      'me-va-be': 'Mẹ & Bé (Chuỗi Siêu Thị Mẹ Bé VN, Đồ Sơ Sinh & Thương Hiệu Baby D2C Quốc Tế Chuẩn UI/UX)',
      'gia-dung-thiet-bi-bep': 'Đồ Gia Dụng Thông Minh & Thiết Bị Bếp (Hãng Gia Dụng VN, Thiết Bị Bếp & D2C Quốc Tế Chuẩn UI/UX)',
      'dien-may-cong-nghe': 'Điện Máy, Laptop & Điện Thoại (Chuỗi Bán Lẻ VN, Showroom Apple/Gaming & Chuẩn UI/UX Quốc Tế)',
      'thoi-trang-giay-dep': 'Thời Trang, Giày Dép & Phụ Kiện (Local Brand VN, Chuỗi Bán Lẻ & D2C Quốc Tế Chuẩn UI/UX)',
      'my-pham-tpcn': 'Mỹ Phẩm & Thực Phẩm Chức Năng (Local Brand VN, Bán Lẻ TPCN & D2C Skincare/Vitamin Quốc Tế)',
      'phong-kham-y-te': 'Phòng Khám Chuyên Khoa & Y Tế (Bệnh Viện Đa Khoa VN, Xét Nghiệm, Đặt Khám & Phòng Khám Quốc Tế)',
      'spa-tham-my-vien': 'Spa, Thẩm Mỹ Viện & Clinic (Clinic Da Liễu VN, Day Spa 5 Sao & MedSpa Quốc Tế Chuẩn UI/UX)',
      'nha-khoa': 'Nha Khoa Thẩm Mỹ & Trồng Răng (Chuỗi Lớn VN, Phòng Khám Thẩm Mỹ & Quốc Tế Chuẩn UI/UX)',
      'vat-lieu-xay-dung': 'Vật Liệu Xây Dựng (Gạch Ốp Lát, Đá Nhân Tạo, Gỗ, Cửa Nhôm Kính, Thiết Bị Vệ Sinh & Quốc Tế)',
      'moi-gioi-nha-dat-cho-thue': 'Môi Giới Nhà Đất Thổ Cư & Cho Thuê Căn Hộ (Sàn VN, Căn Hộ Dịch Vụ & Quốc Tế Chuẩn UI/UX)',
      'xay-dung': 'Mảng Xây Dựng (Tổng Thầu VN, Xây Nhà Trọn Gói, Kết Cấu Thép & Tổng Thầu Quốc Tế)',
      'trung-tam-tieng-anh-dep': 'Trung Tâm Tiếng Anh Bố Cục Đẹp (Quốc Tế Editorial, EdTech & Trung Tâm Hiện Đại)',
      'banh-mi-quoc-te': 'Tiệm Bánh Mì Cho Người Nước Ngoài (Boutique VN, Châu Âu, Úc & Mỹ)',
      'khach-san': 'Khách Sạn & Khu Nghỉ Dưỡng (Boutique Luxury, Di Sản 5 Sao & Chuỗi Quốc Tế)',
      'landing-page-oto-mercedes': 'Landing Page Bán Xe Mercedes-Benz Mới & Ô Tô Việt Nam (Cấu Trúc Chuyển Đổi Google Ads)',
      'noi-that-sang-trong': 'Nội Thất Phong Cách Sang Trọng (Luxury Editorial, Quiet Luxury & Biệt Thự Thượng Lưu)',
      'noi-that': 'Nội Thất & Kiến Trúc Không Gian (Studio Luxury, Thi Công Trọn Gói & Showroom E-Commerce)',
      'phong-thuy': 'Phong Thủy, Kiến Trúc Tâm Linh & Vật Phẩm Đá Quý (Quốc Tế & Top SEO Việt Nam)',
      'phong-kham-thu-y': 'Phòng Khám & Bệnh Viện Thú Y (Chuỗi Quốc Tế & Top Bệnh Viện Việt Nam)',
      'website-coupon-ma-giam-gia': 'Website Dạng Coupon, Mã Giảm Giá & Săn Deal (WordPress & Affiliate)',
      'landing-page-lap-mang': 'Landing Page Lắp Đặt Mạng Internet & FPT (1-Page Chuẩn Chuyển Đổi Google Ads)',
      'lap-mang-fpt': 'Lắp Đặt Mạng Cáp Quang FPT Telecom (Mẫu Tối Ưu Google Ads & Chuyển Đổi Cao)',
      'mua-ban-oto-cu': 'Mua Bán Xe Ô Tô Cũ',
      'cafe-va-banh-mi': 'Cafe & Bánh Mì (Menu & Quán F&B Chuẩn Hà Nội)',
      'trung-tam-anh-ngu': 'Trung Tâm Anh Ngữ (Top Chuỗi & Luyện Thi)',
      'all': 'Tất Cả Nháp Chờ Duyệt',
      'ban-may-anh': 'Máy Chụp Ảnh & Thiết Bị Nhiếp Ảnh (Google Ads & CRO)',
      'du-hoc-dinh-cu-my': 'Du Học & Định Cư Mỹ (Google Ads & CRO)',
      'phong-tap-fitness': 'Phòng Tập Fitness & Gym',
      'ban-dong-ho': 'Bán Đồng Hồ Chính Hãng & Xa Xỉ',
      'decor-su-kien': 'Decor Tiệc & Trang Trí Sự Kiện',
      'tiec-cuoi': 'Tiệc Cưới & Wedding Planner'
    };
    document.getElementById('statTopicName').textContent = topicMapName[currentTopic] || currentTopic;
    document.getElementById('statApproved').textContent = approvedInTopic;
    document.getElementById('statTotalTopic').textContent = currentList.length;
    document.getElementById('btnApprovedCount').textContent = totalApprovedAll;

    // Cập nhật số đếm badge các tab
    if (document.getElementById('badgeAll')) document.getElementById('badgeAll').textContent = CANDIDATES.length;
    if (document.getElementById('badgeSaas')) document.getElementById('badgeSaas').textContent = CANDIDATES.filter(c => c.industry === 'phan-mem-saas').length;
    if (document.getElementById('badgeB2b')) document.getElementById('badgeB2b').textContent = CANDIDATES.filter(c => c.industry === 'doanh-nghiep-b2b').length;
    if (document.getElementById('badgeKhoaHoc')) document.getElementById('badgeKhoaHoc').textContent = CANDIDATES.filter(c => c.industry === 'khoa-hoc-online-lms').length;
    if (document.getElementById('badgeNhaHang')) document.getElementById('badgeNhaHang').textContent = CANDIDATES.filter(c => c.industry === 'nha-hang-am-thuc').length;
    if (document.getElementById('badgeVeSinhChuyenNha')) document.getElementById('badgeVeSinhChuyenNha').textContent = CANDIDATES.filter(c => c.industry === 've-sinh-chuyen-nha').length;
    if (document.getElementById('badgeDienLanh')) document.getElementById('badgeDienLanh').textContent = CANDIDATES.filter(c => c.industry === 'sua-chua-dien-lanh').length;
    if (document.getElementById('badgeQuaTang')) document.getElementById('badgeQuaTang').textContent = CANDIDATES.filter(c => c.industry === 'qua-tang-hoa-tuoi').length;
    if (document.getElementById('badgeMeVaBe')) document.getElementById('badgeMeVaBe').textContent = CANDIDATES.filter(c => c.industry === 'me-va-be').length;
    if (document.getElementById('badgeGiaDung')) document.getElementById('badgeGiaDung').textContent = CANDIDATES.filter(c => c.industry === 'gia-dung-thiet-bi-bep').length;
    if (document.getElementById('badgeDienMay')) document.getElementById('badgeDienMay').textContent = CANDIDATES.filter(c => c.industry === 'dien-may-cong-nghe').length;
    if (document.getElementById('badgeThoiTrang')) document.getElementById('badgeThoiTrang').textContent = CANDIDATES.filter(c => c.industry === 'thoi-trang-giay-dep').length;
    if (document.getElementById('badgeMyPham')) document.getElementById('badgeMyPham').textContent = CANDIDATES.filter(c => c.industry === 'my-pham-tpcn').length;
    if (document.getElementById('badgePhongKham')) document.getElementById('badgePhongKham').textContent = CANDIDATES.filter(c => c.industry === 'phong-kham-y-te').length;
    if (document.getElementById('badgeSpa')) document.getElementById('badgeSpa').textContent = CANDIDATES.filter(c => c.industry === 'spa-tham-my-vien').length;
    if (document.getElementById('badgeNhaKhoa')) document.getElementById('badgeNhaKhoa').textContent = CANDIDATES.filter(c => c.industry === 'nha-khoa').length;
    if (document.getElementById('badgeVlxd')) document.getElementById('badgeVlxd').textContent = CANDIDATES.filter(c => c.industry === 'vat-lieu-xay-dung').length;
    if (document.getElementById('badgeMoiGioiBds')) document.getElementById('badgeMoiGioiBds').textContent = CANDIDATES.filter(c => c.industry === 'moi-gioi-nha-dat-cho-thue').length;
    if (document.getElementById('badgeXayDung')) document.getElementById('badgeXayDung').textContent = CANDIDATES.filter(c => c.industry === 'xay-dung').length;
    if (document.getElementById('badgeBanhMiQuocTe')) document.getElementById('badgeBanhMiQuocTe').textContent = CANDIDATES.filter(c => c.industry === 'banh-mi-quoc-te').length;
    if (document.getElementById('badgeAnhNguDep')) document.getElementById('badgeAnhNguDep').textContent = CANDIDATES.filter(c => c.industry === 'trung-tam-tieng-anh-dep').length;
    if (document.getElementById('badgeKhachSan')) document.getElementById('badgeKhachSan').textContent = CANDIDATES.filter(c => c.industry === 'khach-san').length;
    if (document.getElementById('badgeAutoMercedesLP')) document.getElementById('badgeAutoMercedesLP').textContent = CANDIDATES.filter(c => c.industry === 'landing-page-oto-mercedes').length;
    if (document.getElementById('badgeNoiThatLux')) document.getElementById('badgeNoiThatLux').textContent = CANDIDATES.filter(c => c.industry === 'noi-that-sang-trong').length;
    if (document.getElementById('badgeNoiThat')) document.getElementById('badgeNoiThat').textContent = CANDIDATES.filter(c => c.industry === 'noi-that').length;
    if (document.getElementById('badgePhongThuy')) document.getElementById('badgePhongThuy').textContent = CANDIDATES.filter(c => c.industry === 'phong-thuy').length;
    if (document.getElementById('badgeThuY')) document.getElementById('badgeThuY').textContent = CANDIDATES.filter(c => c.industry === 'phong-kham-thu-y').length;
    if (document.getElementById('badgeCoupon')) document.getElementById('badgeCoupon').textContent = CANDIDATES.filter(c => c.industry === 'website-coupon-ma-giam-gia').length;
    if (document.getElementById('badgeLpLapMang')) document.getElementById('badgeLpLapMang').textContent = CANDIDATES.filter(c => c.industry === 'landing-page-lap-mang').length;
    if (document.getElementById('badgeFpt')) document.getElementById('badgeFpt').textContent = CANDIDATES.filter(c => c.industry === 'lap-mang-fpt').length;
    if (document.getElementById('badgeCafeBanhMi')) document.getElementById('badgeCafeBanhMi').textContent = CANDIDATES.filter(c => c.industry === 'cafe-va-banh-mi').length;
    if (document.getElementById('badgeAnhNgu')) document.getElementById('badgeAnhNgu').textContent = CANDIDATES.filter(c => c.industry === 'trung-tam-anh-ngu').length;
    if (document.getElementById('badgeMayAnh')) document.getElementById('badgeMayAnh').textContent = CANDIDATES.filter(c => c.industry === 'ban-may-anh').length;
    if (document.getElementById('badgeOtoCu')) document.getElementById('badgeOtoCu').textContent = CANDIDATES.filter(c => c.industry === 'mua-ban-oto-cu').length;
    if (document.getElementById('badgeDuHocDinhCu')) document.getElementById('badgeDuHocDinhCu').textContent = CANDIDATES.filter(c => c.industry === 'du-hoc-dinh-cu-my').length;
    if (document.getElementById('badgeFitness')) document.getElementById('badgeFitness').textContent = CANDIDATES.filter(c => c.industry === 'phong-tap-fitness').length;
    if (document.getElementById('badgeDongHo')) document.getElementById('badgeDongHo').textContent = CANDIDATES.filter(c => c.industry === 'ban-dong-ho').length;
    if (document.getElementById('badgeDecor')) document.getElementById('badgeDecor').textContent = CANDIDATES.filter(c => c.industry === 'decor-su-kien').length;
    if (document.getElementById('badgeWedding')) document.getElementById('badgeWedding').textContent = CANDIDATES.filter(c => c.industry === 'tiec-cuoi').length;

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

    const dlLabel = document.getElementById('lbDownloadText');
    const dlBtn = document.getElementById('lbDownloadBtn');
    if (dlLabel) dlLabel.textContent = 'Tải ảnh';
    if (dlBtn) dlBtn.disabled = false;

    const lbBody = document.getElementById('lbBody');
    if (lbBody) {
      lbBody.scrollTop = 0;
      lbBody.scrollLeft = 0;
    }
  }

  function buildDownloadSlug(item) {
    const raw = (item && (item.short_name || item.domain || item.id)) || 'website';
    return raw
      .normalize('NFD')
      .replace(/[\\u0300-\\u036f]/g, '')
      .replace(/đ/g, 'd')
      .replace(/Đ/g, 'D')
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '') || 'website';
  }

  function triggerDownloadHref(href, fileName, revokeAfter) {
    const a = document.createElement('a');
    a.href = href;
    a.download = fileName;
    a.style.display = 'none';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    if (revokeAfter) {
      setTimeout(() => URL.revokeObjectURL(href), 5000);
    }
  }

  async function downloadLightboxImage() {
    const currentList = getFilteredCandidates();
    const item = currentList[currentLbIndex];
    if (!item) return;

    const img = document.getElementById('lbImage');
    const btn = document.getElementById('lbDownloadBtn');
    const label = document.getElementById('lbDownloadText');
    const baseName = `${buildDownloadSlug(item)}-fullpage`;

    if (btn) btn.disabled = true;
    if (label) label.textContent = 'Đang xuất...';

    const finish = (ext, viaFallback) => {
      if (btn) btn.disabled = false;
      if (label) label.textContent = '✓ Đã tải';
      showToast(`⬇️ Đã tải ${baseName}.${ext}${viaFallback ? ' (bản gốc siêu nhẹ)' : ''}`);
      setTimeout(() => {
        if (label) label.textContent = 'Tải ảnh';
      }, 2000);
    };

    try {
      if (window.location.protocol !== 'file:' && img && img.complete && img.naturalWidth > 0) {
        const canvas = document.createElement('canvas');
        canvas.width = img.naturalWidth;
        canvas.height = img.naturalHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(img, 0, 0);

        const pngBlob = await new Promise((resolve) => {
          try {
            canvas.toBlob((blob) => resolve(blob), 'image/png');
          } catch (err) {
            resolve(null);
          }
        });

        if (pngBlob) {
          const blobUrl = URL.createObjectURL(pngBlob);
          triggerDownloadHref(blobUrl, `${baseName}.png`, true);
          finish('png', false);
          return;
        }
      }

      const src = item.full || (img && img.getAttribute('src'));
      if (!src) throw new Error('Không tìm thấy đường dẫn ảnh');

      if (window.location.protocol !== 'file:') {
        const resp = await fetch(src);
        if (resp.ok) {
          const webpBlob = await resp.blob();
          const blobUrl = URL.createObjectURL(webpBlob);
          triggerDownloadHref(blobUrl, `${baseName}.webp`, true);
          finish('webp', true);
          return;
        }
      }

      triggerDownloadHref(src, `${baseName}.webp`, false);
      finish('webp', true);
    } catch (err) {
      console.error('Lỗi tải ảnh:', err);
      if (btn) btn.disabled = false;
      if (label) label.textContent = 'Tải ảnh';
      showToast('⚠️ Chưa tải được ảnh, vui lòng thử lại sau khi ảnh hiển thị xong.');
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
    } else if ((e.key === 'd' || e.key === 'D') && !e.ctrlKey && !e.metaKey && !e.altKey) {
      e.preventDefault();
      downloadLightboxImage();
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
