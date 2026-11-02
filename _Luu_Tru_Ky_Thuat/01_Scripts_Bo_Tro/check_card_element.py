# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'filtered\.forEach\(item => \{.*?\n    \}\);', text, re.DOTALL)
if m:
    print(m.group(0)[:800])
