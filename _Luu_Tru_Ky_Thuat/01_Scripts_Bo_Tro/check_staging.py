import json, re

with open('web_nhap_staging.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'const CANDIDATES\s*=\s*(\[\s*\{.*?\}\s*\]);', text, re.DOTALL)
if m:
    try:
        data = json.loads(m.group(1))
        print("Count of candidates in staging:", len(data))
        if data:
            print("First candidate:", data[0]['name'])
    except Exception as e:
        print("Error parsing json:", e)
else:
    print("Not found CANDIDATES array")
