with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace padding: 7px 10px; with padding: 11px 12px;
old_str = """    .btn-action {
      padding: 7px 10px;"""

new_str = """    .btn-action {
      padding: 11px 12px;"""

norm_text = text.replace('\r\n', '\n')
norm_old = old_str.replace('\r\n', '\n')
norm_new = new_str.replace('\r\n', '\n')

if norm_old in norm_text:
    norm_text = norm_text.replace(norm_old, norm_new, 1)
    print("Desktop button padding updated to 11px 12px")
else:
    print("Desktop button padding NOT FOUND")

# Also update mobile if needed
old_mob = """      .btn-action {
        padding: 7px 4px !important;"""
new_mob = """      .btn-action {
        padding: 10px 6px !important;"""

norm_old_mob = old_mob.replace('\r\n', '\n')
norm_new_mob = new_mob.replace('\r\n', '\n')

if norm_old_mob in norm_text:
    norm_text = norm_text.replace(norm_old_mob, norm_new_mob, 1)
    print("Mobile button padding updated")
else:
    print("Mobile button padding NOT FOUND")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(norm_text)
print("SAVED index.html")
