# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'function renderWebsites\(.*?\n  \}', text, re.DOTALL)
if m:
    print(m.group(0)[:1000])
else:
    m2 = re.findall(r'function [a-zA-Z0-9_]+\(', text)
    print(m2)
