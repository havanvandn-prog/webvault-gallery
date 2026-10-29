# -*- coding: utf-8 -*-
"""
Cập nhật cơ chế xem ảnh Lightbox:
1. Mặc định mở ảnh: Fit 100% toàn bộ giao diện từ đầu đến chân trang trong khung nhìn.
2. Click vào ảnh: Chuyển đổi giữa Fit toàn bộ và Full Size 100% chiều rộng để cuộn đọc chi tiết.
3. Ctrl + Scroll chuột: Phóng to / thu nhỏ giao diện mượt mà theo tỷ lệ.
4. Thanh công cụ Zoom nổi (Fit / 100% / + / -).
"""
import sys

def main():
    with open('web_nhap_staging.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. CẬP NHẬT CSS CHO LIGHTBOX BODY & ZOOM BAR
    old_css_marker = '    /* LIGHTBOX MODAL */'
    
    new_css = '''    /* LIGHTBOX MODAL & MODES */
    .lightbox-modal {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.96);
      backdrop-filter: blur(12px);
      z-index: 999;
      display: none;
      flex-direction: column;
    }
    .lightbox-modal.active {
      display: flex;
    }

    .lightbox-header {
      padding: 10px 24px;
      background: #111116;
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      color: #fff;
      flex-wrap: wrap;
      z-index: 10;
    }

    .lightbox-title-box {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .lightbox-badge-id {
      background: rgba(255, 59, 48, 0.18);
      color: #ff6e66;
      border: 1px solid rgba(255, 59, 48, 0.3);
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.5px;
    }
    .lightbox-title-box h3 {
      font-size: 15px;
      font-weight: 700;
      color: #fff;
    }

    .lightbox-actions {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }

    .lightbox-nav-btn {
      background: #1e1e28;
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
      padding: 6px 14px;
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
    .lightbox-toggle-btn.is-approved:hover {
      background: rgba(1, 169, 21, 0.3);
    }
    .lightbox-toggle-btn.is-rejected {
      background: rgba(239, 68, 68, 0.2);
      border-color: rgba(239, 68, 68, 0.4);
      color: #f87171;
    }
    .lightbox-toggle-btn.is-rejected:hover {
      background: rgba(239, 68, 68, 0.3);
    }

    /* LIGHTBOX BODY CÁC CHẾ ĐỘ HIỂN THỊ */
    .lightbox-body {
      flex: 1;
      position: relative;
      padding: 16px;
      display: flex;
      justify-content: center;
      user-select: none;
      scrollbar-width: thin;
      scrollbar-color: rgba(255, 59, 48, 0.5) rgba(255, 255, 255, 0.04);
    }
    .lightbox-body::-webkit-scrollbar {
      width: 7px;
      height: 7px;
    }
    .lightbox-body::-webkit-scrollbar-track {
      background: rgba(255, 255, 255, 0.04);
      border-radius: 8px;
    }
    .lightbox-body::-webkit-scrollbar-thumb {
      background: rgba(255, 59, 48, 0.5);
      border-radius: 8px;
    }
    .lightbox-body::-webkit-scrollbar-thumb:hover {
      background: #ff3b30;
    }

    /* CHẾ ĐỘ 1: VỪA VẶN MÀN HÌNH (FIT 100% GIAO DIỆN) */
    .lightbox-body.mode-fit {
      align-items: center;
      overflow: hidden;
    }
    .lightbox-body.mode-fit .lightbox-img-wrapper {
      max-width: 100%;
      width: auto !important;
      height: calc(100vh - 110px);
      max-height: calc(100vh - 110px);
      display: flex;
      justify-content: center;
      align-items: center;
      background: transparent;
      box-shadow: 0 16px 48px rgba(0,0,0,0.85);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 6px;
      overflow: hidden;
      cursor: zoom-in;
    }
    .lightbox-body.mode-fit .lightbox-img-wrapper img {
      width: auto !important;
      height: 100% !important;
      max-height: calc(100vh - 110px);
      object-fit: contain;
      display: block;
      cursor: zoom-in;
    }

    /* CHẾ ĐỘ 2: FULL SIZE 100% (CUỘN ĐỌC TỪNG CHI TIẾT) */
    .lightbox-body.mode-full {
      align-items: flex-start;
      overflow-y: auto;
      overflow-x: auto;
    }
    .lightbox-body.mode-full .lightbox-img-wrapper {
      max-width: 1360px;
      width: 100% !important;
      height: auto !important;
      background: #000;
      box-shadow: 0 24px 60px rgba(0,0,0,0.9);
      border: 1px solid var(--border);
      border-radius: 8px;
      overflow: hidden;
      margin: 0 auto;
      cursor: zoom-out;
    }
    .lightbox-body.mode-full .lightbox-img-wrapper img {
      width: 100% !important;
      height: auto !important;
      max-height: none !important;
      display: block;
      cursor: zoom-out;
    }

    /* CHẾ ĐỘ 3: TỰ DO ZOOM BẰNG CTRL + SCROLL */
    .lightbox-body.mode-custom {
      align-items: flex-start;
      overflow: auto;
    }
    .lightbox-body.mode-custom .lightbox-img-wrapper {
      max-width: none !important;
      height: auto !important;
      background: #000;
      box-shadow: 0 24px 60px rgba(0,0,0,0.9);
      border: 1px solid var(--border);
      border-radius: 8px;
      overflow: hidden;
      margin: 0 auto;
      cursor: grab;
      transition: width 0.08s ease-out;
    }
    .lightbox-body.mode-custom.is-dragging .lightbox-img-wrapper {
      cursor: grabbing;
    }
    .lightbox-body.mode-custom .lightbox-img-wrapper img {
      width: 100% !important;
      height: auto !important;
      max-height: none !important;
      display: block;
      pointer-events: none;
    }

    /* THANH ĐIỀU KHIỂN ZOOM NỔI (FLOATING ZOOM BAR) */
    .lightbox-zoom-bar {
      position: absolute;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(18, 18, 24, 0.92);
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
      font-size: 14px;
      transition: all 0.15s ease;
    }
    .zoom-btn:hover {
      background: rgba(255, 255, 255, 0.2);
      transform: scale(1.08);
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
      display: flex;
      align-items: center;
      gap: 4px;
    }
    .zoom-pill-mode-btn:hover, .zoom-pill-mode-btn.active {
      background: var(--accent);
      color: #fff;
      border-color: var(--accent);
    }
    .zoom-level-text {
      font-weight: 700;
      color: #4ade80;
      min-width: 50px;
      text-align: center;
      font-variant-numeric: tabular-nums;
      font-size: 12px;
    }
    .zoom-hint-text {
      font-size: 11px;
      color: var(--text-dim);
      margin-left: 4px;
      padding-left: 8px;
      border-left: 1px solid rgba(255, 255, 255, 0.12);
    }
    @media (max-width: 768px) {
      .zoom-hint-text {
        display: none;
      }
    }
'''

    # Tìm phần CSS cũ từ /* LIGHTBOX MODAL */ đến @media (max-width: 768px)
    start_css = html.find('    /* LIGHTBOX MODAL */')
    end_css = html.find('    @media (max-width: 768px) {')
    if start_css != -1 and end_css != -1:
        html = html[:start_css] + new_css + '\n' + html[end_css:]
        print('Updated Lightbox CSS')
    else:
        print('Error: CSS markers not found', start_css, end_css)
        return

    # 2. CẬP NHẬT HTML CHO LIGHTBOX MODAL
    old_lb_html = '''    <div class="lightbox-body" onclick="closeLightboxOnBackdrop(event)">
      <div class="lightbox-img-wrapper">
        <img id="lbImage" src="" alt="Full website preview">
      </div>
    </div>'''

    new_lb_html = '''    <div class="lightbox-body mode-fit" id="lbBody" onclick="handleLightboxBodyClick(event)">
      <div class="lightbox-img-wrapper" id="lbImgWrapper" onclick="handleImageClick(event)" title="Nhấp để chuyển đổi giữa Fit toàn bộ giao diện và Phóng to 100%">
        <img id="lbImage" src="" alt="Full website preview">
      </div>

      <!-- THANH ĐIỀU KHIỂN ZOOM NỔI -->
      <div class="lightbox-zoom-bar" onclick="event.stopPropagation()">
        <button class="zoom-btn" onclick="zoomStep(-1)" title="Thu nhỏ (Ctrl + Cuộn chuột xuống)">−</button>
        <span class="zoom-level-text" id="lbZoomLevel">Fit 100%</span>
        <button class="zoom-btn" onclick="zoomStep(1)" title="Phóng to (Ctrl + Cuộn chuột lên)">+</button>
        <div style="width: 1px; height: 16px; background: rgba(255,255,255,0.15); margin: 0 2px;"></div>
        <button class="zoom-pill-mode-btn active" id="btnModeFit" onclick="setLightboxMode('fit')">
          ⛶ Toàn bộ (Fit)
        </button>
        <button class="zoom-pill-mode-btn" id="btnModeFull" onclick="setLightboxMode('full')">
          100% Chi tiết
        </button>
        <span class="zoom-hint-text">💡 Ctrl + Cuộn chuột để zoom</span>
      </div>
    </div>'''

    if old_lb_html in html:
        html = html.replace(old_lb_html, new_lb_html)
        print('Updated Lightbox HTML')
    else:
        old_lb_html_crlf = old_lb_html.replace('\n', '\r\n')
        new_lb_html_crlf = new_lb_html.replace('\n', '\r\n')
        if old_lb_html_crlf in html:
            html = html.replace(old_lb_html_crlf, new_lb_html_crlf)
            print('Updated Lightbox HTML (CRLF)')
        else:
            print('Error: Lightbox HTML marker not found')
            return

    # 3. CẬP NHẬT JAVASCRIPT LOGIC CHO LIGHTBOX & ZOOM
    old_js_start = html.find('  // LIGHTBOX MODAL CHO TRẠM KIỂM DUYỆT')
    old_js_end = html.find("  document.addEventListener('DOMContentLoaded', renderStaging);")
    if old_js_start == -1 or old_js_end == -1:
        print('Error: JS markers not found', old_js_start, old_js_end)
        return

    new_js = '''  // LIGHTBOX MODAL & CHẾ ĐỘ ZOOM THÔNG MINH
  let currentLbIndex = 0;
  let currentLbMode = 'fit'; // 'fit' (vừa màn hình) | 'full' (100% chi tiết) | 'custom' (tỷ lệ tùy chỉnh)
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
    // Click vào ảnh: chuyển đổi giữa Fit toàn bộ và Full Size 100%
    if (currentLbMode === 'fit') {
      setLightboxMode('full');
      showToast('🔍 Đã mở Full Size (100%) — Cuộn chuột để xem chi tiết');
    } else {
      setLightboxMode('fit');
      showToast('⛶ Đã thu về Vừa Khung Hình (100% Giao diện)');
    }
  }

  function zoomStep(delta) {
    // delta = +1 (zoom in) hoặc -1 (zoom out)
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
    const idx = CANDIDATES.findIndex(c => c.id === id);
    if (idx === -1) return;
    currentLbIndex = idx;
    updateLightboxContent();

    const modal = document.getElementById('lightboxModal');
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';

    // Luôn mở ở chế độ Fit toàn bộ giao diện đầu tiên để người dùng nhìn trọn vẹn 100%
    setLightboxMode('fit');
  }

  function updateLightboxContent() {
    const item = CANDIDATES[currentLbIndex];
    if (!item) return;

    const isApproved = approvalMap[item.id];

    document.getElementById('lbIndex').textContent = `${item.id.toUpperCase()} (${currentLbIndex + 1}/${CANDIDATES.length})`;
    document.getElementById('lbTitle').textContent = item.name;
    document.getElementById('lbExternalLink').href = item.url;
    document.getElementById('lbImage').src = item.full;

    // Cập nhật trạng thái nút toggle trong modal
    const toggleBtn = document.getElementById('lbToggleBtn');
    if (isApproved) {
      toggleBtn.className = 'lightbox-toggle-btn is-approved';
      toggleBtn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg> <span>Giữ Lại (Đã Duyệt)</span>`;
    } else {
      toggleBtn.className = 'lightbox-toggle-btn is-rejected';
      toggleBtn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg> <span>Bỏ Qua (Đã Loại)</span>`;
    }

    const lbBody = document.getElementById('lbBody');
    if (lbBody) {
      lbBody.scrollTop = 0;
      lbBody.scrollLeft = 0;
    }
  }

  function toggleLightboxApproval() {
    const item = CANDIDATES[currentLbIndex];
    if (!item) return;
    approvalMap[item.id] = !approvalMap[item.id];
    updateLightboxContent();
    renderStaging();
  }

  function nextLightbox() {
    if (currentLbIndex < CANDIDATES.length - 1) {
      currentLbIndex++;
    } else {
      currentLbIndex = 0; // Vòng lại đầu
    }
    updateLightboxContent();
    setLightboxMode('fit');
  }

  function prevLightbox() {
    if (currentLbIndex > 0) {
      currentLbIndex--;
    } else {
      currentLbIndex = CANDIDATES.length - 1; // Vòng về cuối
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
    // Chỉ đóng khi click trực tiếp vào vùng đệm màu đen bên ngoài wrapper
    if (e.target.id === 'lbBody') {
      closeLightbox();
    }
  }

  // PHÍM TẮT TIỆN LỢI: ESC ĐÓNG, MŨI TÊN TRÁI/PHẢI CHUYỂN MẪU, PHÍM SPACE ĐỔI TRẠNG THÁI DUYỆT
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

  // HỖ TRỢ CTRL + CUỘN CHUỘT ĐỂ ZOOM TỶ LỆ GIAO DIỆN
  window.addEventListener('wheel', (e) => {
    const modal = document.getElementById('lightboxModal');
    if (!modal || !modal.classList.contains('active')) return;

    if (e.ctrlKey) {
      e.preventDefault();
      const delta = e.deltaY < 0 ? 1 : -1;
      zoomStep(delta);
    }
  }, { passive: false });
'''

    html = html[:old_js_start] + new_js + '\n  ' + html[old_js_end:]
    print('Updated Lightbox JS')

    with open('web_nhap_staging.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print('SUCCESS: Applied Fit 100% & Smart Zoom to web_nhap_staging.html!')

if __name__ == '__main__':
    main()
