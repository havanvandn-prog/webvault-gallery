# -*- coding: utf-8 -*-
import os, sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
script_path = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "01_Scripts_Bo_Tro", "build_multi_staging.py")

with open(script_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update Tabs
old_tabs = """      <button class="staging-tab-btn" data-industry="all" onclick="filterStagingTopic('all')">
        <span>⚡</span> Tất Cả Nháp <span class="tab-badge" id="badgeAll">221</span>
      </button>
      <button class="staging-tab-btn active" data-industry="website-coupon-ma-giam-gia" onclick="filterStagingTopic('website-coupon-ma-giam-gia')">"""

new_tabs = """      <button class="staging-tab-btn" data-industry="all" onclick="filterStagingTopic('all')">
        <span>⚡</span> Tất Cả Nháp <span class="tab-badge" id="badgeAll">241</span>
      </button>
      <button class="staging-tab-btn active" data-industry="phong-kham-thu-y" onclick="filterStagingTopic('phong-kham-thu-y')">
        <span>🐾</span> Phòng Khám Thú Y <span class="tab-badge" id="badgeThuY">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="website-coupon-ma-giam-gia" onclick="filterStagingTopic('website-coupon-ma-giam-gia')">"""

if old_tabs in text:
    text = text.replace(old_tabs, new_tabs, 1)
    print("Tabs updated successfully!")
else:
    print("WARNING: old_tabs not found!")

# 2. Update default topic
old_topic = "let currentTopic = 'website-coupon-ma-giam-gia';"
new_topic = "let currentTopic = 'phong-kham-thu-y';"
if old_topic in text:
    text = text.replace(old_topic, new_topic, 1)
    print("Default topic updated!")
else:
    print("WARNING: old_topic not found!")

old_param = "const indParam = params.get('industry') || params.get('topic') || 'website-coupon-ma-giam-gia';"
new_param = "const indParam = params.get('industry') || params.get('topic') || 'phong-kham-thu-y';"
if old_param in text:
    text = text.replace(old_param, new_param, 1)
    print("indParam updated!")
else:
    print("WARNING: old_param not found!")

# 3. Update topicMapName
old_map = "const topicMapName = {"
new_map = """const topicMapName = {
      'phong-kham-thu-y': 'Phòng Khám & Bệnh Viện Thú Y (Chuỗi Quốc Tế & Top Bệnh Viện Việt Nam)',"""
if old_map in text:
    text = text.replace(old_map, new_map, 1)
    print("topicMapName updated!")
else:
    print("WARNING: old_map not found!")

# 4. Update badge update logic
old_badge = "if (document.getElementById('badgeCoupon'))"
new_badge = """if (document.getElementById('badgeThuY')) document.getElementById('badgeThuY').textContent = CANDIDATES.filter(c => c.industry === 'phong-kham-thu-y').length;
    if (document.getElementById('badgeCoupon'))"""
if old_badge in text:
    text = text.replace(old_badge, new_badge, 1)
    print("badge update logic updated!")
else:
    print("WARNING: old_badge not found!")

with open(script_path, "w", encoding="utf-8") as f:
    f.write(text)

print("build_multi_staging.py updated and saved successfully!")
