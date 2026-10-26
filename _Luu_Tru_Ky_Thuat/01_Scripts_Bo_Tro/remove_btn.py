# -*- coding: utf-8 -*-
import os
import re

index_path = "index.html"
with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

pattern = r'\s*<a href="preview_mau_website_du_lich\.html"[\s\S]*?</a>\s*'
content_new = re.sub(pattern, '\n        ', content, count=1)

if content_new != content:
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content_new)
    print("SUCCESS: Removed travel button from top header!")
else:
    print("FAILED: Button pattern not found!")
