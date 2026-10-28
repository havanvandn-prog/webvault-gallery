with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace lightbox CSS
old_css = """.lightbox-body {
      flex: 1;
      overflow-y: auto;
      overflow-x: clip;
      padding: 24px;
      display: flex;
      justify-content: center;
      scrollbar-width: thin;
      scrollbar-color: rgba(255, 59, 48, 0.5) rgba(255, 255, 255, 0.04);
    }
    .lightbox-body::-webkit-scrollbar {
      width: 7px;
    }
    .lightbox-body::-webkit-scrollbar-track {
      background: rgba(255, 255, 255, 0.04);
      border-radius: 8px;
    }
    .lightbox-body::-webkit-scrollbar-thumb {
      background: rgba(255, 59, 48, 0.5);
      border-radius: 8px;
    }
    .lightbox-body::-webkit-scrollbar-thumb:hover {
      background: #ff3b30;
    }

    .lightbox-img-wrapper {
      max-width: 1280px;
      width: 100%;
      background: #000;
      border-radius: 8px;
      border: 1px solid var(--border);
      overflow: hidden;
      box-shadow: 0 24px 60px rgba(0,0,0,0.9);
    }"""

new_css = """.lightbox-body {
      flex: 1;
      overflow-y: auto;
      overflow-x: clip;
      padding: 24px;
      display: flex;
      justify-content: center;
      align-items: flex-start;
      scrollbar-width: thin;
      scrollbar-color: rgba(255, 59, 48, 0.5) rgba(255, 255, 255, 0.04);
    }
    .lightbox-body::-webkit-scrollbar {
      width: 7px;
    }
    .lightbox-body::-webkit-scrollbar-track {
      background: rgba(255, 255, 255, 0.04);
      border-radius: 8px;
    }
    .lightbox-body::-webkit-scrollbar-thumb {
      background: rgba(255, 59, 48, 0.5);
      border-radius: 8px;
    }
    .lightbox-body::-webkit-scrollbar-thumb:hover {
      background: #ff3b30;
    }

    .lightbox-img-wrapper {
      max-width: 1280px;
      width: 100%;
      height: auto;
      background: #000;
      border-radius: 8px;
      border: 1px solid var(--border);
      overflow: hidden;
      box-shadow: 0 24px 60px rgba(0,0,0,0.9);
      flex-shrink: 0;
    }"""

norm_text = text.replace('\r\n', '\n')
norm_old = old_css.replace('\r\n', '\n')
norm_new = new_css.replace('\r\n', '\n')

if norm_old in norm_text:
    norm_text = norm_text.replace(norm_old, norm_new, 1)
    print("CSS replaced")
else:
    print("CSS NOT FOUND")

# Also update openLightbox to reset scrollTop to 0
old_lb_func = """    const modal = document.getElementById('lightboxModal');
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }"""

new_lb_func = """    const modal = document.getElementById('lightboxModal');
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
    const lbBody = document.querySelector('.lightbox-body');
    if (lbBody) lbBody.scrollTop = 0;
  }"""

norm_old_func = old_lb_func.replace('\r\n', '\n')
norm_new_func = new_lb_func.replace('\r\n', '\n')

if norm_old_func in norm_text:
    norm_text = norm_text.replace(norm_old_func, norm_new_func, 1)
    print("JS openLightbox replaced")
else:
    print("JS NOT FOUND")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(norm_text)
print("index.html updated successfully")
