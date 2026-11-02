# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open('web_nhap_staging.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'function filterStagingTopic.*?(?=function|\Z)', text, re.DOTALL)
if m:
    print(m.group(0)[:1500])
