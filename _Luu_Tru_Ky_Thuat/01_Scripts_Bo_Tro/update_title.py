with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = '<div class="card-thumbnail-box" onclick="openLightbox(\'${item.id}\')">'
replacement = '<div class="card-thumbnail-box" onclick="openLightbox(\'${item.id}\')" title="Nhấp để xem ảnh phóng to Full-Page">'

if target in text:
    text = text.replace(target, replacement, 1)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("SUCCESS")
else:
    print("NOT FOUND")
