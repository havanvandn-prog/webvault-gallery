import re
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m_hdr = re.search(r'<div class="header-actions">[\s\S]*?</div>', text)
if m_hdr:
    print('Header actions:')
    print(m_hdr.group(0))

m_data = re.search(r'"id": "23"[\s\S]*?\];', text)
if m_data:
    print('\nEnd of WEBSITES_DATA:')
    print(m_data.group(0))

