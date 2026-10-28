# -*- coding: utf-8 -*-
import os
import sys
from PIL import Image
import numpy as np

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8')

event_websites = [
    ("01", "square-vn.com", "square-vn.com.png"),
    ("02", "per-fectiv.com", "per-fectiv.com.png"),
    ("03", "zeitmedia.vn", "zeitmedia.vn.png"),
    ("04", "lebros.vn", "lebros.vn.png"),
    ("05", "hoabinhevents.com", "hoabinhevents.com.png"),
    ("06", "vietlinkevent.vn", "vietlinkevent.vn.png"),
    ("07", "newdaymedia.com.vn", "newdaymedia.com.vn.png"),
    ("08", "apexevent.vn", "apexevent.vn.png"),
    ("09", "anmedia.vn", "anmedia.vn.png"),
    ("10", "cybershow.vn", "cybershow.vn.png"),
    ("11", "datvietevent.com", "datvietevent.com.png"),
    ("12", "cat-event.com.vn", "cat-event.com.vn.png"),
    ("13", "yesevents.vn", "yesevents.vn.png"),
    ("14", "sukienachau.com", "sukienachau.com.png"),
    ("15", "hoangsaviet.com", "hoangsaviet.com.png"),
    ("16", "danangevents.com.vn", "danangevents.com.vn.png"),
    ("17", "seaevent.vn", "seaevent.vn.png"),
    ("18", "bsgroup.com.vn", "bsgroup.com.vn.png"),
    ("19", "thanglongevent.com", "thanglongevent.com.png"),
    ("20", "azevent.vn", "azevent.vn.png"),
]

anh_dir = "Anh_Chup_Website"

print(f"{'ID':<4} | {'Domain':<22} | {'Kích thước':<14} | {'Dung lượng':<10} | {'Tình trạng':<20}")
print("-" * 80)

for idx, domain, fname in event_websites:
    p = os.path.join(anh_dir, fname)
    if not os.path.exists(p):
        print(f"{idx:<4} | {domain:<22} | {'FILE MISSING':<14} | {'N/A':<10} | Lỗi: Không tìm thấy file")
        continue
    
    im = Image.open(p)
    w, h = im.size
    kb = round(os.path.getsize(p) / 1024, 1)
    
    status = "OK"
    if domain in ["hoangsaviet.com", "azevent.vn"]:
        status = "CẦN CHỤP LẠI (Dính header/hotline)"
    
    print(f"{idx:<4} | {domain:<22} | {f'{w}x{h}':<14} | {f'{kb} KB':<10} | {status}")
