# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

navs = re.findall(r'<li class="nav-item"[^>]*>.*?</li>', text, re.DOTALL)
for n in navs:
    print(' '.join(n.split()))

print("\n--- industryMap ---")
m = re.search(r'const industryMap = \{.*?\};', text, re.DOTALL)
if m:
    print(m.group(0))
