with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update CSS
old_css = """    /* FACEBOOK LEAD BUTTONS */
    .btn-fb-text {
      background: #1877f2;
      color: #fff;
      grid-column: span 1;
    }
    .btn-fb-text:hover {
      background: #1464cc;
    }

    .btn-fb-image {
      background: rgba(24, 119, 242, 0.15);
      border: 1px solid rgba(24, 119, 242, 0.4);
      color: #70b4ff;
      grid-column: span 1;
    }
    .btn-fb-image:hover {
      background: rgba(24, 119, 242, 0.25);
      border-color: #1877f2;
      color: #fff;
    }

    .btn-view-full {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid var(--border);
      color: #fff;
    }
    .btn-view-full:hover {
      background: rgba(255, 255, 255, 0.14);
      border-color: var(--border-hover);
    }

    .btn-open-web {
      background: #1a1a24;
      border: 1px solid var(--border);
      color: var(--text-muted);
    }
    .btn-open-web:hover {
      background: #232330;
      color: #fff;
    }"""

new_css = """    /* HÀNG 1: NÚT COPY ẢNH FB - Màu đỏ gradient nổi bật như logo WebVault (#ff3b30 -> #ff6b5b) */
    .btn-fb-image {
      background: linear-gradient(135deg, #ff3b30, #ff6b5b);
      color: #fff;
      box-shadow: 0 4px 12px rgba(255, 59, 48, 0.35);
      border: none;
      font-weight: 700;
    }
    .btn-fb-image:hover {
      background: linear-gradient(135deg, #ff4f45, #ff7a6b);
      transform: translateY(-1px);
      box-shadow: 0 6px 16px rgba(255, 59, 48, 0.5);
      color: #fff;
    }

    /* HÀNG 1: NÚT XEM ẢNH FULL - Kính mờ sang trọng */
    .btn-view-full {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid var(--border);
      color: #fff;
    }
    .btn-view-full:hover {
      background: rgba(255, 255, 255, 0.16);
      border-color: var(--border-hover);
      color: #fff;
    }

    /* HÀNG 2: NÚT TRUY CẬP WEBSITE - Màu xanh nổi bật như nút Copy Comment cũ (#1877f2), chiếm trọn 2 cột */
    .btn-open-web {
      grid-column: span 2;
      background: #1877f2;
      color: #fff;
      box-shadow: 0 4px 12px rgba(24, 119, 242, 0.3);
      border: none;
      font-weight: 700;
    }
    .btn-open-web:hover {
      background: #1464cc;
      box-shadow: 0 6px 16px rgba(24, 119, 242, 0.45);
      transform: translateY(-1px);
      color: #fff;
    }"""

# 2. Update HTML Markup in renderCards
old_html = """          <!-- VŨ KHÍ SĂN LEAD FACEBOOK -->
          <div class="card-actions-grid">
            <button class="btn-action btn-fb-text" onclick="copyFbComment('${item.id}', this)" title="Copy đoạn text có link preview để dán Ctrl+V vào comment Facebook">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
              <span class="desktop-label">Copy Comment FB</span>
              <span class="mobile-label">Copy Comment</span>
            </button>

            <button class="btn-action btn-fb-image" onclick="copyDirectImageToClipboard('${item.id}', this)" title="Copy ảnh tỷ lệ chuẩn 1080x1920 (9:16) để dán Facebook/Zalo to rõ, không bị dài và thu nhỏ">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>
              <span class="desktop-label">Copy Ảnh FB (1080x1920)</span>
              <span class="mobile-label">Copy Ảnh 9:16</span>
            </button>

            <button class="btn-action btn-view-full" onclick="openLightbox('${item.id}')">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="10" r="3"></circle></svg>
              <span class="desktop-label">Xem Full-Page</span>
              <span class="mobile-label">Full-Page</span>
            </button>

            <a href="${item.url}" target="_blank" rel="noopener noreferrer" class="btn-action btn-open-web">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
              <span class="desktop-label">Truy cập Web ↗</span>
              <span class="mobile-label">Xem Web ↗</span>
            </a>
          </div>"""

new_html = """          <!-- CARD ACTIONS: HÀNG 1 (COPY ẢNH + XEM FULL), HÀNG 2 (TRUY CẬP WEBSITE) -->
          <div class="card-actions-grid">
            <button class="btn-action btn-fb-image" onclick="copyDirectImageToClipboard('${item.id}', this)" title="Copy ảnh tỷ lệ chuẩn 1080x1920 (9:16) để dán Facebook/Zalo to rõ, không bị dài và thu nhỏ">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>
              <span class="desktop-label">Copy Ảnh FB</span>
              <span class="mobile-label">Copy FB</span>
            </button>

            <button class="btn-action btn-view-full" onclick="openLightbox('${item.id}')" title="Xem ảnh toàn bộ website từ đầu đến chân trang">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="10" r="3"></circle></svg>
              <span class="desktop-label">Xem Ảnh Full</span>
              <span class="mobile-label">Ảnh Full</span>
            </button>

            <a href="${item.url}" target="_blank" rel="noopener noreferrer" class="btn-action btn-open-web" title="Mở website thật trên tab mới">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
              <span class="desktop-label">Truy cập Website ↗</span>
              <span class="mobile-label">Truy cập Web ↗</span>
            </a>
          </div>"""

norm_text = text.replace('\r\n', '\n')
norm_old_css = old_css.replace('\r\n', '\n')
norm_new_css = new_css.replace('\r\n', '\n')
norm_old_html = old_html.replace('\r\n', '\n')
norm_new_html = new_html.replace('\r\n', '\n')

if norm_old_css in norm_text:
    norm_text = norm_text.replace(norm_old_css, norm_new_css, 1)
    print("CSS replaced")
else:
    print("CSS NOT FOUND")

if norm_old_html in norm_text:
    norm_text = norm_text.replace(norm_old_html, norm_new_html, 1)
    print("HTML replaced")
else:
    print("HTML NOT FOUND")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(norm_text)

print("index.html successfully updated")
