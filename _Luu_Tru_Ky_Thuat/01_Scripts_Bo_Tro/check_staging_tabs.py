# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open('web_nhap_staging.html', 'r', encoding='utf-8') as f:
    text = f.read()

tabs = re.findall(r'<button class="tab-btn"[^>]*>.*?</button>', text, re.DOTALL)
for t in tabs:
    print(' '.join(t.split()))

print("\n--- Javascript for tabs/industries ---")
m = re.findall(r'function (?:filter|render|setIndustry|switchTab)[^{]*\{', text)
print(m)
