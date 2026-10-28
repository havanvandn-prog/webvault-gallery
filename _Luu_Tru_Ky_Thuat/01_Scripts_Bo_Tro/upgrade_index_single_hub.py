# -*- coding: utf-8 -*-
import os
import sys
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
index_path = os.path.join(BASE_DIR, "index.html")

with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Clean Header Actions (remove preview links)
old_header_pattern = r'<div class="header-actions">[\s\S]*?<a href="web_nhap_staging\.html"'
new_header_snippet = '<div class="header-actions">\n        <a href="web_nhap_staging.html"'

content = re.sub(old_header_pattern, new_header_snippet, content)
print("[+] Da go bo cac nut link preview rieng le khoi Top Header!")

# 2. Upgrade DOMContentLoaded to use initUrlParams()
content = content.replace("checkPitchUrlParam();", "initUrlParams();")

# 3. Replace checkPitchUrlParam, togglePitchMode, setIndustry with upgraded functions
old_funcs_pattern = r'function checkPitchUrlParam\(\) \{[\s\S]*?function toggleSelectPitch\(id, event\) \{'

new_funcs = """  function initUrlParams() {
    const params = new URLSearchParams(window.location.search);

    // 1. Kiểm tra Pitch Mode (?pitch=01,02,...)
    const pitchParam = params.get('pitch');
    if (pitchParam && pitchParam.trim()) {
      const rawIds = pitchParam.split(',').map(s => s.trim().padStart(2, '0'));
      const validIds = rawIds.filter(id => WEBSITES_DATA.some(w => w.id === id));
      if (validIds.length > 0) {
        selectedPitchIds = new Set(validIds);
        isPitchMode = true;
        document.getElementById('pitchBanner').classList.add('active');
        document.getElementById('viewHeading').textContent = `Mẫu Tuyển Chọn Riêng Cho Dự Án Của Bạn (${validIds.length} Mẫu)`;
        document.getElementById('viewSubheading').textContent = `Được sàng lọc kỹ lưỡng theo định hướng phong cách và mục tiêu chuyển đổi của bạn`;
        document.getElementById('pitchBtnText').textContent = 'Xem Toàn Bộ Mẫu';
        return;
      }
    }

    // 2. Kiểm tra lọc chuyên mục ngành nghề trực tiếp (?industry=... hoặc ?cat=...)
    const indParam = params.get('industry') || params.get('cat');
    if (indParam && indParam.trim()) {
      const targetNav = document.querySelector(`.nav-item[onclick*="'${indParam}'"]`);
      if (targetNav) {
        currentIndustry = indParam;
        updateNavActive(targetNav);
        updateViewHeading();
      }
    }
  }

  function updateViewHeading() {
    if (isPitchMode) return;
    const headingEl = document.getElementById('viewHeading');
    const subHeadingEl = document.getElementById('viewSubheading');

    const industryMap = {
      'all': 'Tất Cả Mẫu Tuyển Chọn',
      'su-kien': 'Sự Kiện & Activation',
      'decor-su-kien': 'Trang Trí & Decor Tiệc',
      'du-lich': 'Du Lịch & Tour Tuyến'
    };

    const indName = industryMap[currentIndustry] || 'Mẫu Website Tuyển Chọn';
    const totalCount = currentIndustry === 'all'
      ? WEBSITES_DATA.length
      : WEBSITES_DATA.filter(w => w.industry === currentIndustry).length;

    headingEl.textContent = `${indName} (${totalCount} Website)`;
    subHeadingEl.textContent = 'Ảnh WebP 2 tầng siêu nhẹ • Tự động cuộn khi rê chuột • Sẵn sàng gửi khách hàng';
  }

  function togglePitchMode() {
    if (isPitchMode) {
      window.history.pushState({}, '', window.location.pathname);
      isPitchMode = false;
      document.getElementById('pitchBanner').classList.remove('active');
      document.getElementById('pitchBtnText').textContent = 'Tạo Gói Gửi Khách';
      updateViewHeading();
      renderCards();
    } else {
      if (selectedPitchIds.size === 0) {
        showToast("💡 Hãy tick chọn ô vuông ở góc trên các card để tạo gói gửi khách!");
        return;
      }
      copyPitchLink();
    }
  }

  function handleSearch() {
    currentSearch = document.getElementById('searchInput').value.trim().toLowerCase();
    renderCards();
  }

  function setIndustry(ind, el) {
    currentIndustry = ind;
    updateNavActive(el);

    // Cập nhật tham số URL mà không load lại trang
    const url = new URL(window.location);
    if (ind === 'all') {
      url.searchParams.delete('industry');
      url.searchParams.delete('cat');
    } else {
      url.searchParams.set('industry', ind);
    }
    window.history.replaceState({}, '', url);

    updateViewHeading();
    renderCards();
  }

  function setVibe(vibe, el) {
    currentVibe = vibe;
    updateNavActive(el);
    renderCards();
  }

  function setLocation(loc, el) {
    currentLocation = loc;
    updateNavActive(el);
    renderCards();
  }

  function updateNavActive(el) {
    if (!el) return;
    const parentList = el.closest('.nav-list');
    if (!parentList) return;
    parentList.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
    el.classList.add('active');
  }

  function toggleSelectPitch(id, event) {"""

content = re.sub(old_funcs_pattern, new_funcs, content)
print("[+] Da nang cap he thong URL Parameter (?industry=...) va cap nhat heading tu dong!")

with open(index_path, "w", encoding="utf-8") as f:
    f.write(content)

print("[SUCCESS] Hoan tat cap nhat index.html!")
