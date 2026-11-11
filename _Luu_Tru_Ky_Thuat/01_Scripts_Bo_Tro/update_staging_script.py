# -*- coding: utf-8 -*-
import os, sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
staging_script = os.path.join(BASE_DIR, "_Luu_Tru_Ky_Thuat", "01_Scripts_Bo_Tro", "build_multi_staging.py")

with open(staging_script, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Add tab button
old_tabs = """      <button class="staging-tab-btn" data-industry="all" onclick="filterStagingTopic('all')">
        <span>⚡</span> Tất Cả Nháp <span class="tab-badge" id="badgeAll">201</span>
      </button>
      <button class="staging-tab-btn active" data-industry="landing-page-lap-mang" onclick="filterStagingTopic('landing-page-lap-mang')">"""

new_tabs = """      <button class="staging-tab-btn" data-industry="all" onclick="filterStagingTopic('all')">
        <span>⚡</span> Tất Cả Nháp <span class="tab-badge" id="badgeAll">221</span>
      </button>
      <button class="staging-tab-btn active" data-industry="website-coupon-ma-giam-gia" onclick="filterStagingTopic('website-coupon-ma-giam-gia')">
        <span>🎟️</span> Coupon & Săn Deal <span class="tab-badge" id="badgeCoupon">20</span>
      </button>
      <button class="staging-tab-btn" data-industry="landing-page-lap-mang" onclick="filterStagingTopic('landing-page-lap-mang')">"""

if old_tabs in text:
    text = text.replace(old_tabs, new_tabs)
    print("Tab button added!")
else:
    print("Warning: old_tabs not found")

# 2. Update default topic
old_def = "let currentTopic = 'landing-page-lap-mang';"
new_def = "let currentTopic = 'website-coupon-ma-giam-gia';"
if old_def in text:
    text = text.replace(old_def, new_def)
    print("Default topic updated!")

old_param = "const indParam = params.get('industry') || params.get('topic') || 'landing-page-lap-mang';"
new_param = "const indParam = params.get('industry') || params.get('topic') || 'website-coupon-ma-giam-gia';"
if old_param in text:
    text = text.replace(old_param, new_param)
    print("indParam updated!")

# 3. Add to topicMapName
old_topic_map = "const topicMapName = {"
new_topic_map = """const topicMapName = {
      'website-coupon-ma-giam-gia': 'Website Dạng Coupon, Mã Giảm Giá & Săn Deal (WordPress & Affiliate)',"""
if old_topic_map in text:
    text = text.replace(old_topic_map, new_topic_map, 1)
    print("topicMapName updated!")

# 4. Add badge update
old_badge = "if (document.getElementById('badgeLpLapMang'))"
new_badge = """if (document.getElementById('badgeCoupon')) document.getElementById('badgeCoupon').textContent = CANDIDATES.filter(c => c.industry === 'website-coupon-ma-giam-gia').length;
    if (document.getElementById('badgeLpLapMang'))"""
if old_badge in text:
    text = text.replace(old_badge, new_badge, 1)
    print("badge update added!")

with open(staging_script, "w", encoding="utf-8") as f:
    f.write(text)

print("Saved build_multi_staging.py successfully!")
