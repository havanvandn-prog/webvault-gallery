import os
import sys
import json
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

folder = r"D:\AI Agent\Website\Tìm mẫu website\Anh_Chup_Website"

rename_map = {
    "01_Square_Experiential.png": "square-vn.com.png",
    "02_Per_fectiv.png": "per-fectiv.com.png",
    "03_Le_Bros.png": "lebros.vn.png",
    "04_BS_Group.png": "bsgroup.com.vn.png",
    "05_Zeit_Media.png": "zeitmedia.vn.png",
    "06_HoaBinh_Events.png": "hoabinhevents.com.png",
    "07_A_Chau_Event.png": "sukienachau.com.png",
    "08_Vietlink_Event.png": "vietlinkevent.vn.png",
    "09_Apex_Media.png": "apexevent.vn.png",
    "10_Newday_Media.png": "newdaymedia.com.vn.png",
    "11_Cyber_Show.png": "cybershow.vn.png",
    "12_YesEvents.png": "yesevents.vn.png",
    "13_CAT_Event.png": "cat-event.com.vn.png",
    "14_Hoang_Sa_Viet.png": "hoangsaviet.com.png",
    "15_Dat_Viet_Event.png": "datvietevent.com.png",
    "16_Danang_Events.png": "danangevents.com.vn.png",
    "17_Sea_Event.png": "seaevent.vn.png",
    "18_AN_Media.png": "anmedia.vn.png",
    "19_Thang_Long_Event.png": "thanglongevent.com.png",
    "20_AzEvent.png": "azevent.vn.png"
}

print("=== ĐANG ĐỔI TÊN ẢNH THEO TÊN WEBSITE (DOMAIN) ===")
for old_name, new_name in rename_map.items():
    old_path = os.path.join(folder, old_name)
    new_path = os.path.join(folder, new_name)
    if os.path.exists(old_path):
        if os.path.exists(new_path) and old_path != new_path:
            os.remove(new_path)
        os.rename(old_path, new_path)
        print(f"Renamed: {old_name} -> {new_name}")
    else:
        print(f"Old file not found (might already be renamed): {old_name}")

# Cập nhật lại đường dẫn ảnh trong preview_mau_website_su_kien.html
html_path = r"D:\AI Agent\Website\Tìm mẫu website\preview_mau_website_su_kien.html"
if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    for old_name, new_name in rename_map.items():
        content = content.replace(f"Anh_Chup_Website/{old_name}", f"Anh_Chup_Website/{new_name}")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated preview_mau_website_su_kien.html successfully!")
