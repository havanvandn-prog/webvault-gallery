with open('preview_mau_website_su_kien.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_css = """.lightbox-body {
      flex: 1;
      overflow-y: auto;
      overflow-x: hidden;
      padding: 24px;
      display: flex;
      justify-content: center;
    }

    .lightbox-img-wrapper {
      max-width: 1200px;
      width: 100%;
      background: #000000;
      border-radius: 8px;
      box-shadow: 0 20px 40px rgba(0,0,0,0.5);
      overflow: hidden;
    }"""

new_css = """.lightbox-body {
      flex: 1;
      overflow-y: auto;
      overflow-x: hidden;
      padding: 24px;
      display: flex;
      justify-content: center;
      align-items: flex-start;
    }

    .lightbox-img-wrapper {
      max-width: 1200px;
      width: 100%;
      height: auto;
      background: #000000;
      border-radius: 8px;
      box-shadow: 0 20px 40px rgba(0,0,0,0.5);
      overflow: hidden;
      flex-shrink: 0;
    }"""

norm_text = text.replace('\r\n', '\n')
norm_old = old_css.replace('\r\n', '\n')
norm_new = new_css.replace('\r\n', '\n')

if norm_old in norm_text:
    norm_text = norm_text.replace(norm_old, norm_new, 1)
    with open('preview_mau_website_su_kien.html', 'w', encoding='utf-8') as f:
        f.write(norm_text)
    print("preview_mau_website_su_kien.html updated")
else:
    print("preview CSS not found")
