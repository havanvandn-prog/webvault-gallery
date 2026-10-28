import json
import sys

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open(r'_Luu_Tru_Ky_Thuat\03_Du_Lieu_Tam_Va_Test\decor_metadata.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total items: {len(data)}")
success_count = sum(1 for d in data if d.get('status') == 'SUCCESS')
print(f"Success count: {success_count}/{len(data)}")
for i, d in enumerate(data, 1):
    print(f"{i:02d}. [{d['status']}] {d['id']} - {d['name']} | Thumb: {d['thumb']} ({d.get('thumb_kb')} KB) | Full: {d['full']} ({d.get('full_kb')} KB)")
