# -*- coding: utf-8 -*-
"""
Cập nhật tính năng xem ảnh Full (Lightbox) cho trạm kiểm duyệt nháp (web_nhap_staging.html)
"""
import sys

def main():
    with open('web_nhap_staging.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. CSS CHO LIGHTBOX & HINT TRÊN THUMBNAIL
    lightbox_css = '''
    /* ZOOM OVERLAY HINT ON THUMBNAIL */
    .thumbnail-zoom-hint {
      position: absolute;
      bottom: 10px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(15, 15, 20, 0.9);
      backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 255, 255, 0.18);
      color: #fff;
      font-size: 11.5px;
      font-weight: 600;
      padding: 5px 12px;
      border-radius: 20px;
      display: flex;
      align-items: center;
      gap: 6px;
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

    /* LIGHTBOX MODAL */
    .lightbox-modal {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.95);
      backdrop-filter: blur(12px);
      z-index: 999;
      display: none;
      flex-direction: column;
    }
    .lightbox-modal.active {
      display: flex;
    }

    .lightbox-header {
      padding: 12px 24px;
      background: #111116;
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

    .lightbox-body {
      flex: 1;
      overflow-y: auto;
      overflow-x: clip;
      padding: 24px;
      display: flex;
      justify-content: center;
      align-items: flex-start;
      scrollbar-width: thin;
      scrollbar-color: rgba(255, 59, 48, 0.5) rgba(255, 255, 255, 0.04);
    }
    .lightbox-body::-webkit-scrollbar {
      width: 7px;
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

    .lightbox-img-wrapper {
      max-width: 1280px;
      width: 100%;
      height: auto;
      background: #000;
      border-radius: 8px;
      border: 1px solid var(--border);
      overflow: hidden;
      box-shadow: 0 24px 60px rgba(0,0,0,0.9);
      flex-shrink: 0;
    }
    .lightbox-img-wrapper img {
      width: 100%;
      height: auto;
      display: block;
    }

    @media (max-width: 768px) {
      .lightbox-header {
        padding: 10px 14px;
        gap: 8px;
      }
      .lightbox-actions {
        width: 100%;
        justify-content: space-between;
        gap: 6px;
      }
      .lightbox-title-box h3 {
        font-size: 13px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 180px;
      }
      .lightbox-body {
        padding: 10px;
      }
    }
'''

    # Chèn CSS trước </style>
    if '</style>' in html:
        html = html.replace('  </style>', lightbox_css + '  </style>')
    else:
        print('Error: </style> not found')
        return

    # 2. HTML CHO LIGHTBOX MODAL
    lightbox_html = '''
  <!-- LIGHTBOX MODAL (XEM ẢNH FULL-PAGE NHANH) -->
  <div class="lightbox-modal" id="lightboxModal">
    <div class="lightbox-header">
      <div class="lightbox-title-box">
        <span class="lightbox-badge-id" id="lbIndex">dc01 (1/20)</span>
        <h3 id="lbTitle">Tên Website</h3>
      </div>
      <div class="lightbox-actions">
        <!-- Nút chuyển trước/sau -->
        <button class="lightbox-nav-btn" onclick="prevLightbox()" title="Xem mẫu trước (Phím mũi tên Trái ←)">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"></polyline></svg>
          Trước
        </button>
        <button class="lightbox-nav-btn" onclick="nextLightbox()" title="Xem mẫu tiếp theo (Phím mũi tên Phải →)">
          Sau
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg>
        </button>

        <!-- Nút duyệt/bỏ qua trực tiếp trong modal -->
        <button id="lbToggleBtn" class="lightbox-toggle-btn is-approved" onclick="toggleLightboxApproval()" title="Bấm để Đổi trạng thái Duyệt / Bỏ qua mẫu này (hoặc phím Space)">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
          <span id="lbToggleText">Giữ Lại Mẫu Này (Đã Duyệt)</span>
        </button>

        <!-- Mở website thật -->
        <a id="lbExternalLink" href="#" target="_blank" rel="noopener noreferrer" class="btn btn-view-hub" style="padding: 6px 12px; font-size: 12px;" title="Mở website thật trên tab mới">
          Mở Web Thật ↗
        </a>

        <!-- Đóng -->
        <button class="btn btn-view-hub" onclick="closeLightbox()" style="padding: 6px 12px; font-size: 12px;" title="Đóng modal (Phím ESC)">
          Đóng (ESC)
        </button>
      </div>
    </div>

    <div class="lightbox-body" onclick="closeLightboxOnBackdrop(event)">
      <div class="lightbox-img-wrapper">
        <img id="lbImage" src="" alt="Full website preview">
      </div>
    </div>
  </div>
'''

    # Chèn trước toastBox
    toast_marker = '  <div class="toast" id="toastBox">'
    if toast_marker in html:
        html = html.replace(toast_marker, lightbox_html + '\n' + toast_marker)
    else:
        print('Error: toastBox not found')
        return

    # 3. CẬP NHẬT CARD THUMBNAIL BOX TRONG renderStaging
    old_thumb_box = '''        <div class="card-thumbnail-box">
          <img src="${item.thumb}" class="card-thumb-img" alt="${item.name}">
        </div>'''

    new_thumb_box = '''        <div class="card-thumbnail-box" onclick="openLightbox('${item.id}')" title="Nhấp vào để xem ảnh full-page toàn bộ trang">
          <img src="${item.thumb}" class="card-thumb-img" alt="${item.name}" loading="lazy">
          <div class="thumbnail-zoom-hint">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            Nhấp xem ảnh Full
          </div>
        </div>'''

    if old_thumb_box in html:
        html = html.replace(old_thumb_box, new_thumb_box)
    else:
        # Thử với \r\n
        old_thumb_crlf = old_thumb_box.replace('\n', '\r\n')
        new_thumb_crlf = new_thumb_box.replace('\n', '\r\n')
        if old_thumb_crlf in html:
            html = html.replace(old_thumb_crlf, new_thumb_crlf)
        else:
            print('Error: old_thumb_box not found')
            return

    # 4. THÊM CÁC HÀM XỬ LÝ LIGHTBOX VÀ PHÍM TẮT TRONG SCRIPT
    lightbox_js = '''
  // LIGHTBOX MODAL CHO TRẠM KIỂM DUYỆT
  let currentLbIndex = 0;

  function openLightbox(id) {
    const idx = CANDIDATES.findIndex(c => c.id === id);
    if (idx === -1) return;
    currentLbIndex = idx;
    updateLightboxContent();

    const modal = document.getElementById('lightboxModal');
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
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

    const lbBody = document.querySelector('.lightbox-body');
    if (lbBody) lbBody.scrollTop = 0;
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
  }

  function prevLightbox() {
    if (currentLbIndex > 0) {
      currentLbIndex--;
    } else {
      currentLbIndex = CANDIDATES.length - 1; // Vòng về cuối
    }
    updateLightboxContent();
  }

  function closeLightbox() {
    const modal = document.getElementById('lightboxModal');
    modal.classList.remove('active');
    document.body.style.overflow = '';
  }

  function closeLightboxOnBackdrop(e) {
    if (e.target.classList.contains('lightbox-body')) {
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
    }
  });
'''

    # Chèn trước document.addEventListener('DOMContentLoaded', renderStaging);
    dom_marker = "document.addEventListener('DOMContentLoaded', renderStaging);"
    if dom_marker in html:
        html = html.replace(dom_marker, lightbox_js + '\n  ' + dom_marker)
    else:
        print('Error: dom_marker not found')
        return

    with open('web_nhap_staging.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print('SUCCESS: Updated web_nhap_staging.html with Full Image Lightbox!')

if __name__ == '__main__':
    main()
