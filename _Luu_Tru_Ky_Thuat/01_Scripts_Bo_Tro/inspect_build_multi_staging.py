# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('_Luu_Tru_Ky_Thuat/01_Scripts_Bo_Tro/build_multi_staging.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'staging-tabs-container' in l:
        print(f"Tabs at {i+1}:")
        for j in range(i, i+25):
            print(f"{j+1}: {lines[j]}", end='')
        break

for i, l in enumerate(lines):
    if 'function initTopicFromUrl' in l:
        print(f"\ninitTopicFromUrl at {i+1}:")
        for j in range(i, i+10):
            print(f"{j+1}: {lines[j]}", end='')
        break

for i, l in enumerate(lines):
    if 'const topicMapName' in l:
        print(f"\ntopicMapName at {i+1}:")
        for j in range(i, i+20):
            print(f"{j+1}: {lines[j]}", end='')
        break
