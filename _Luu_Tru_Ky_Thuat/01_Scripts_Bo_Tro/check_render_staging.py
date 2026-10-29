import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('web_nhap_staging.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'function renderStaging' in line:
        print(''.join(lines[i:i+60]))
        break
