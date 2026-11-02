# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('_Luu_Tru_Ky_Thuat/01_Scripts_Bo_Tro/build_multi_staging.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '<nav class="staging-tabs-bar">' in l:
        print(f"Markup at {i+1}:")
        for j in range(i, i+30):
            print(f"{j+1}: {lines[j]}", end='')
        break
