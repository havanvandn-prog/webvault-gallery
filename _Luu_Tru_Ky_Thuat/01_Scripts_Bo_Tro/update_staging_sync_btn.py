# -*- coding: utf-8 -*-
"""
Cập nhật saveApprovalSelection trong web_nhap_staging.html để hỗ trợ 1-Click Direct Sync
"""

def main():
    with open('web_nhap_staging.html', 'r', encoding='utf-8') as f:
        html = f.read()

    old_func_start = html.find('  function saveApprovalSelection() {')
    old_func_end = html.find('  let toastTimer = null;')
    if old_func_start == -1 or old_func_end == -1:
        print('Error: func markers not found')
        return

    new_func = '''  async function saveApprovalSelection() {
    const approvedList = CANDIDATES.filter(c => approvalMap[c.id]);
    if (approvedList.length === 0) {
      showToast('⚠️ Bạn chưa chọn mẫu nào! Nhấn "+ Thêm Mẫu Này" để chọn.');
      return;
    }

    const btn = document.querySelector('.btn-sync-hub');
    const origHtml = btn ? btn.innerHTML : '';
    if (btn) {
      btn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="spin"><circle cx="12" cy="12" r="10"></circle><path d="M12 6v6l4 2"></path></svg> Đang tự động nạp & đẩy lên GitHub...`;
      btn.style.pointerEvents = 'none';
      btn.style.opacity = '0.85';
    }

    showToast(`⏳ Đang nạp tự động ${approvedList.length} mẫu vào WebVault...`);

    const portsToTry = [
      window.location.port ? parseInt(window.location.port) : null,
      8000, 8081, 9000
    ].filter(p => p !== null);

    let syncSuccess = false;
    let syncResult = null;

    const firstItem = approvedList[0];
    const indSlug = firstItem.industry || (firstItem.id.startsWith('dc') ? 'decor-su-kien' : 'ban-dong-ho');
    const indName = firstItem.industry_name || (firstItem.id.startsWith('dc') ? 'Trang Trí & Decor Tiệc' : 'Đồng Hồ Chính Hãng');

    for (const port of portsToTry) {
      try {
        const endpoint = (window.location.protocol.startsWith('http') && window.location.port == port)
          ? '/api/sync-approved'
          : `http://localhost:${port}/api/sync-approved`;

        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 12000);

        const resp = await fetch(endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            approved_items: approvedList,
            industry_slug: indSlug,
            industry_name: indName
          }),
          signal: controller.signal
        });
        clearTimeout(timeoutId);

        if (resp.ok) {
          syncResult = await resp.json();
          if (syncResult && syncResult.success) {
            syncSuccess = true;
            break;
          }
        }
      } catch (err) {
        // Thử port tiếp theo
      }
    }

    if (btn) {
      btn.innerHTML = origHtml;
      btn.style.pointerEvents = '';
      btn.style.opacity = '';
    }

    if (syncSuccess) {
      showToast(`🎉 THÀNH CÔNG! Đã nạp ${approvedList.length} mẫu vào WebVault và đẩy lên GitHub Pages!`);
      setTimeout(() => {
        window.location.href = syncResult.redirect_url || `index.html?industry=${indSlug}`;
      }, 1200);
      return;
    }

    // Nếu mở bản tĩnh (chưa bật run_webvault.bat)
    const urlText = approvedList.map(c => c.url).join('\\n');
    try {
      await navigator.clipboard.writeText(urlText);
    } catch(e) {}

    showToast(`💡 Đã lưu ${approvedList.length} mẫu! Bật run_webvault.bat trên máy để đồng bộ 1-Click tự động.`);
    alert(
      `ĐÃ LƯU THÀNH CÔNG ${approvedList.length} MẪU BẠN CHỌN!\\n\\n` +
      `Để hệ thống tự động đồng bộ 1-Click lên website online mà không cần nhắn tin:\\n` +
      `👉 Bạn chỉ cần nhấp đúp mở file [run_webvault.bat] trong thư mục dự án trên máy tính!\\n\\n` +
      `Hoặc: Danh sách link đã được tự động copy vào Clipboard, bạn có thể dán vào khung chat để AI đồng bộ ngay.`
    );
  }
'''

    html = html[:old_func_start] + new_func + '\n  ' + html[old_func_end:]

    with open('web_nhap_staging.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("SUCCESS: Updated saveApprovalSelection with Direct Sync API call!")

if __name__ == '__main__':
    main()
