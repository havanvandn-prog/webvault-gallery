# -*- coding: utf-8 -*-
file_path = r"C:\Users\ADMIN\.gemini\config\skills\tim-mau-website\scripts\capture_engine.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old_list = "['is-locked', 'locked', 'overflow-hidden', 'no-scroll', 'modal-open', 'has-intro', 'intro-ready', 'noscroll']"
new_list = "['is-locked', 'locked', 'overflow-hidden', 'no-scroll', 'modal-open', 'has-intro', 'intro-ready', 'noscroll', 'hv3-gated']"

if old_list in content:
    content = content.replace(old_list, new_list)
    print("Added hv3-gated to scroll-lock list in capture_engine.py successfully.")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
else:
    print("Warning: old_list not found.")
