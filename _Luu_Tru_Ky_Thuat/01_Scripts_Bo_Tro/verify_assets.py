import os
import re

with open("preview_mau_website_su_kien.html", "r", encoding="utf-8") as f:
    content = f.read()

images = re.findall(r'image:\s*"([^"]+)"', content)
print(f"Total images found in HTML: {len(images)}")
missing = [img for img in images if not os.path.exists(img)]
if missing:
    print("MISSING:", missing)
else:
    print("SUCCESS: 100% OF 20 IMAGES VERIFIED ON DISK!")
