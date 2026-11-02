# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('web_nhap_staging.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = None
end_idx = None
for i, line in enumerate(lines):
    if 'const CANDIDATES = [' in line:
        start_idx = i
    if start_idx is not None and line.strip().startswith('];'):
        end_idx = i
        break

print(f"CANDIDATES starts at line {start_idx+1}, ends at line {end_idx+1}")
print("Line at end_idx:", lines[end_idx])
print("Next 5 lines:", "".join(lines[end_idx+1:end_idx+6]))
