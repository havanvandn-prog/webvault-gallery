with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = "https://havanvandn-prog.github.io/webvault-gallery/"
replacement = "https://raw.githubusercontent.com/havanvandn-prog/webvault-gallery/main/"

if target in text:
    text = text.replace(target, replacement)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("SUCCESS")
else:
    print("NOT FOUND")
