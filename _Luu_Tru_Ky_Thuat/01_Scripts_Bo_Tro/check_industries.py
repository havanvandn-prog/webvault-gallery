import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.findall(r'"industry":\s*"([^"]+)"', text)
print('Industries in WEBSITES_DATA:', set(m))
