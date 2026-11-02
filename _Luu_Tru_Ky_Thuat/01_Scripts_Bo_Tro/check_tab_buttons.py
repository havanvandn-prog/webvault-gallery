# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open('web_nhap_staging.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.findall(r'<button[^>]*class="[^"]*staging-tab-btn[^"]*"[^>]*>.*?</button>', text, re.DOTALL)
for b in m:
    print(' '.join(b.split()))
