# -*- coding: utf-8 -*-
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('Tất Cả Mẫu Tuyển Chọn (20 Website)', 'Tất Cả Mẫu Tuyển Chọn (43 Website)')
text = text.replace('Hiển thị: <b>20/20</b>', 'Hiển thị: <b>43/43</b>')

# Ensure updateViewHeading is called in initUrlParams
if "updateViewHeading();\n  }" not in text:
    target = """    if (indParam && indParam.trim()) {
      const targetNav = document.querySelector(`.nav-item[onclick*="'${indParam}'"]`);
      if (targetNav) {
        currentIndustry = indParam;
        updateNavActive(targetNav);
        updateViewHeading();
      }
    }
  }"""
    replacement = """    if (indParam && indParam.trim()) {
      const targetNav = document.querySelector(`.nav-item[onclick*="'${indParam}'"]`);
      if (targetNav) {
        currentIndustry = indParam;
        updateNavActive(targetNav);
      }
    }
    updateViewHeading();
  }"""
    text = text.replace(target, replacement)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("[+] Da dong bo thanh cong!")
