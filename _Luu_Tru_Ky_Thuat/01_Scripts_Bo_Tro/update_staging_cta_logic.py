# -*- coding: utf-8 -*-
"""
Cập nhật logic CTA cho web_nhap_staging.html:
1. Mặc định chưa chọn (Pending).
2. Nút CTA ban đầu: '+ Thêm Mẫu Này Để Đồng Bộ' (Nhấn vào là XÁC NHẬN THÊM VÀO VÀ SẼ ĐỒNG BỘ).
3. Sau khi nhấn: Thẻ viền xanh, nút chuyển thành '✓ Đã Thêm (Nhấn để hủy)'.
4. Nút top header: 'Chọn Tất Cả' / 'Bỏ Chọn Hết', đếm số lượng được chọn realtime.
5. Cửa sổ Lightbox đồng bộ: '+ Thêm Mẫu Này Để Đồng Bộ' / '✓ Đã Thêm (Nhấn để hủy)'.
"""

def main():
    with open('web_nhap_staging.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. CẬP NHẬT CSS CHO STAGING CARD VÀ APPROVAL TOGGLE BTN
    old_card_css_start = html.find('    /* STAGING CARD */')
    old_card_css_end = html.find('    /* BROWSER BAR */')
    if old_card_css_start == -1 or old_card_css_end == -1:
        print('Error: card css markers not found')
        return

    new_card_css = '''    /* STAGING CARD */
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
      border-color: rgba(255, 255, 255, 0.22);
      transform: translateY(-2px);
    }

    /* KHI ĐÃ ĐƯỢC CHỌN THÊM ĐỒNG BỘ */
    .staging-card.is-selected {
      border-color: rgba(1, 169, 21, 0.7);
      box-shadow: 0 10px 30px -6px var(--success-glow);
      background: linear-gradient(180deg, rgba(1, 169, 21, 0.05) 0%, var(--bg-card) 100%);
    }
'''
    html = html[:old_card_css_start] + new_card_css + '\n' + html[old_card_css_end:]
    print('Updated Card CSS')

    # 2. CẬP NHẬT CSS CHO TOGGLE BUTTON
    old_btn_start = html.find('    /* TOGGLE APPROVAL BUTTON */')
    old_btn_end = html.find('    /* TOAST */')
    if old_btn_start == -1 or old_btn_end == -1:
        print('Error: btn css markers not found')
        return

    new_btn_css = '''    /* TOGGLE APPROVAL BUTTON */
    .approval-toggle-btn {
      width: 100%;
      padding: 11px 16px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      cursor: pointer;
      border: 1px solid transparent;
      transition: all 0.2s ease;
      margin-top: auto;
    }

    /* CHƯA CHỌN: Nút CTA rõ ràng kêu gọi bấm để THÊM VÀO ĐỒNG BỘ */
    .approval-toggle-btn.btn-unselected {
      background: #181824;
      border: 1px solid rgba(255, 255, 255, 0.16);
      color: #fff;
    }
    .approval-toggle-btn.btn-unselected:hover {
      background: #252536;
      border-color: var(--accent);
      color: #fff;
      transform: translateY(-1px);
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
    }

    /* ĐÃ CHỌN: Nút xác nhận ĐÃ THÊM VÀO ĐỒNG BỘ */
    .approval-toggle-btn.btn-selected {
      background: rgba(1, 169, 21, 0.18);
      border: 1px solid rgba(1, 169, 21, 0.55);
      color: #4ade80;
      font-weight: 700;
    }
    .approval-toggle-btn.btn-selected:hover {
      background: rgba(1, 169, 21, 0.28);
      border-color: rgba(1, 169, 21, 0.8);
    }
'''
    html = html[:old_btn_start] + new_btn_css + '\n' + html[old_btn_end:]
    print('Updated Toggle Button CSS')

    # 3. CẬP NHẬT CSS CHO LIGHTBOX TOGGLE BUTTON
    old_lb_btn_start = html.find('    .lightbox-toggle-btn.is-approved {')
    old_lb_btn_end = html.find('    /* LIGHTBOX BODY CÁC CHẾ ĐỘ HIỂN THỊ */')
    if old_lb_btn_start != -1 and old_lb_btn_end != -1:
        new_lb_btn_css = '''    .lightbox-toggle-btn.is-unselected {
      background: #1e1e28;
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #fff;
    }
    .lightbox-toggle-btn.is-unselected:hover {
      background: #2b2b3a;
      border-color: var(--accent);
    }
    .lightbox-toggle-btn.is-approved {
      background: rgba(1, 169, 21, 0.2);
      border: 1px solid rgba(1, 169, 21, 0.55);
      color: #4ade80;
    }
    .lightbox-toggle-btn.is-approved:hover {
      background: rgba(1, 169, 21, 0.32);
    }
'''
        html = html[:old_lb_btn_start] + new_lb_btn_css + '\n' + html[old_lb_btn_end:]
        print('Updated Lightbox Toggle Button CSS')

    # 4. CẬP NHẬT HEADER & COUNTER STRIP
    old_header_btn = '<button class="btn btn-approve-all" onclick="toggleAll()">'
    if old_header_btn in html:
        new_header_btn = '<button class="btn btn-approve-all" id="btnToggleAll" onclick="toggleAll()">'
        html = html.replace(old_header_btn, new_header_btn)

    old_counter_tip = "💡 Mẹo: Những mẫu bạn bấm 'Bỏ qua' sẽ không được nạp vào kho chính thức"
    new_counter_tip = "💡 Mẹo: Nhấn nút '+ Thêm Mẫu Này Để Đồng Bộ' trên các mẫu bạn ưng ý để nạp vào kho chính thức"
    if old_counter_tip in html:
        html = html.replace(old_counter_tip, new_counter_tip)
        print('Updated Counter Tip')

    # 5. CẬP NHẬT JS LOGIC: MẶC ĐỊNH LÀ FALSE (CHƯA THÊM)
    old_js_start = html.find('  // Trạng thái: Mặc định duyệt tất cả')
    old_js_end = html.find('  // LIGHTBOX MODAL & CHẾ ĐỘ ZOOM THÔNG MINH')
    if old_js_start == -1 or old_js_end == -1:
        print('Error: JS markers not found', old_js_start, old_js_end)
        return

    new_js_logic = '''  // Trạng thái phê duyệt: Mặc định chưa chọn mẫu nào (Người dùng nhấn để Thêm vào đồng bộ)
  let approvalMap = {};
  CANDIDATES.forEach(c => approvalMap[c.id] = false);

  function renderStaging() {
    const grid = document.getElementById('cardsGrid');
    grid.innerHTML = '';

    let approvedCount = 0;

    CANDIDATES.forEach(item => {
      const isSelected = !!approvalMap[item.id];
      if (isSelected) approvedCount++;

      const card = document.createElement('div');
      card.className = `staging-card ${isSelected ? 'is-selected' : ''}`;
      card.id = `card-${item.id}`;

      card.innerHTML = `
        <div class="card-browser-bar">
          <a href="${item.url}" target="_blank" class="browser-url-pill">https://${item.domain}/</a>
          <span style="font-size: 11px; color: var(--text-dim);">${item.location}</span>
        </div>

        <div class="card-thumbnail-box" onclick="openLightbox('${item.id}')" title="Nhấp vào để xem ảnh full-page toàn bộ trang">
          <img src="${item.thumb}" class="card-thumb-img" alt="${item.name}" loading="lazy">
          <div class="thumbnail-zoom-hint">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
            Nhấp xem ảnh Full
          </div>
        </div>

        <div class="card-body">
          <div class="card-meta-row">
            <span class="badge-vibe">${item.vibe}</span>
            <span style="font-size: 11px; color: ${isSelected ? '#4ade80' : 'var(--text-dim)'}; font-weight: 700;">
              ${isSelected ? '✓ ĐÃ CHỌN ĐỒNG BỘ' : 'Chưa thêm vào kho'}
            </span>
          </div>

          <h3 class="card-title">${item.id}. ${item.short_name}</h3>
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

    document.getElementById('statApproved').textContent = approvedCount;
    document.getElementById('btnApprovedCount').textContent = approvedCount;

    // Cập nhật nút Chọn/Bỏ tất cả
    const toggleAllBtn = document.getElementById('btnToggleAll');
    if (toggleAllBtn) {
      if (approvedCount === CANDIDATES.length) {
        toggleAllBtn.textContent = 'Bỏ Chọn Tất Cả';
      } else {
        toggleAllBtn.textContent = `Chọn Tất Cả (${CANDIDATES.length} Mẫu)`;
      }
    }
  }

  function toggleApproval(id) {
    approvalMap[id] = !approvalMap[id];
    const isNowSelected = approvalMap[id];
    const item = CANDIDATES.find(c => c.id === id);
    const itemName = item ? item.short_name : 'mẫu';

    if (isNowSelected) {
      showToast(`✨ Đã thêm ${itemName} vào danh sách đồng bộ!`);
    } else {
      showToast(`Đã bỏ chọn ${itemName}.`);
    }

    renderStaging();
  }

  function toggleAll() {
    const values = Object.values(approvalMap);
    const allSelected = values.length > 0 && values.every(v => v === true);
    // Nếu đã chọn tất cả -> bỏ chọn hết; ngược lại -> chọn tất cả
    const nextState = !allSelected;
    CANDIDATES.forEach(c => approvalMap[c.id] = nextState);
    showToast(nextState ? `✓ Đã chọn toàn bộ ${CANDIDATES.length} mẫu để đồng bộ!` : 'Đã bỏ chọn tất cả các mẫu.');
    renderStaging();
  }

  function saveApprovalSelection() {
    const approvedList = CANDIDATES.filter(c => approvalMap[c.id]);
    if (approvedList.length === 0) {
      showToast('⚠️ Bạn chưa chọn mẫu nào! Hãy nhấn "+ Thêm Mẫu Này Để Đồng Bộ" trên các mẫu bạn ưng ý.');
      return;
    }

    const jsonStr = JSON.stringify(approvedList, null, 2);
    localStorage.setItem('webvault_approved_selection', jsonStr);
    showToast(`✓ Đã xác nhận đồng bộ (${approvedList.length} mẫu) vào WebVault!`);
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
'''

    html = html[:old_js_start] + new_js_logic + '\n\n' + html[old_js_end:]
    print('Updated JS Logic in web_nhap_staging.html')

    # 6. CẬP NHẬT LIGHTBOX UPDATECONTENT CHO TOGGLE BUTTON
    old_lb_update = '''    // Cập nhật trạng thái nút toggle trong modal
    const toggleBtn = document.getElementById('lbToggleBtn');
    if (isApproved) {
      toggleBtn.className = 'lightbox-toggle-btn is-approved';
      toggleBtn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg> <span>Giữ Lại (Đã Duyệt)</span>`;
    } else {
      toggleBtn.className = 'lightbox-toggle-btn is-rejected';
      toggleBtn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg> <span>Bỏ Qua (Đã Loại)</span>`;
    }'''

    new_lb_update = '''    // Cập nhật trạng thái nút toggle trong modal
    const toggleBtn = document.getElementById('lbToggleBtn');
    if (toggleBtn) {
      if (isApproved) {
        toggleBtn.className = 'lightbox-toggle-btn is-approved';
        toggleBtn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg> <span>✓ Đã Thêm (Nhấn để hủy)</span>`;
        toggleBtn.title = 'Nhấn để hủy bỏ thêm mẫu này';
      } else {
        toggleBtn.className = 'lightbox-toggle-btn is-unselected';
        toggleBtn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg> <span>+ Thêm Mẫu Này Để Đồng Bộ</span>`;
        toggleBtn.title = 'Nhấn để xác nhận thêm mẫu này và đồng bộ vào kho';
      }
    }'''

    if old_lb_update in html:
        html = html.replace(old_lb_update, new_lb_update)
        print('Updated Lightbox Update Function')
    else:
        old_lb_crlf = old_lb_update.replace('\n', '\r\n')
        new_lb_crlf = new_lb_update.replace('\n', '\r\n')
        if old_lb_crlf in html:
            html = html.replace(old_lb_crlf, new_lb_crlf)
            print('Updated Lightbox Update Function (CRLF)')
        else:
            print('Warning: old_lb_update not found, skipping')

    with open('web_nhap_staging.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print('SUCCESS: Applied new Add-to-Sync CTA logic to web_nhap_staging.html!')

if __name__ == '__main__':
    main()
