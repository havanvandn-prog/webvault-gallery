with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Add overscroll-behavior: contain to .sidebar
old_css = """    .sidebar {
      width: var(--sidebar-w);
      background: var(--bg-surface);
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      position: fixed;
      top: 0;
      left: 0;
      height: 100vh;
      overflow-y: auto;
      z-index: 30;
      flex-shrink: 0;
    }"""

new_css = """    .sidebar {
      width: var(--sidebar-w);
      background: var(--bg-surface);
      border-right: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      position: fixed;
      top: 0;
      left: 0;
      height: 100vh;
      overflow-y: auto;
      overscroll-behavior: contain;
      z-index: 30;
      flex-shrink: 0;
    }"""

if old_css in text:
    text = text.replace(old_css, new_css, 1)
    print("CSS updated")
else:
    # try normalized
    norm_text = text.replace('\r\n', '\n')
    norm_old = old_css.replace('\r\n', '\n')
    norm_new = new_css.replace('\r\n', '\n')
    if norm_old in norm_text:
        norm_text = norm_text.replace(norm_old, norm_new, 1)
        text = norm_text
        print("CSS updated (norm)")
    else:
        print("CSS NOT FOUND")

# 2. Add id="sidebar" to aside
text = text.replace('<aside class="sidebar">', '<aside class="sidebar" id="sidebar">', 1)

# 3. Add JS wheel isolation listener in DOMContentLoaded
old_init = """  document.addEventListener("DOMContentLoaded", () => {
    checkPitchUrlParam();
    renderCards();
  });"""

new_init = """  document.addEventListener("DOMContentLoaded", () => {
    checkPitchUrlParam();
    renderCards();

    // KHÓA CUỘN ĐỘC LẬP CHO SIDEBAR: Khi cuộn trên sidebar, giao diện chính tuyệt đối không bị cuộn theo
    const sidebarEl = document.querySelector('.sidebar');
    if (sidebarEl) {
      sidebarEl.addEventListener('wheel', (e) => {
        const { scrollTop, scrollHeight, clientHeight } = sidebarEl;
        const isAtTop = scrollTop <= 0 && e.deltaY < 0;
        const isAtBottom = (scrollTop + clientHeight >= scrollHeight - 1) && e.deltaY > 0;
        if (scrollHeight <= clientHeight || isAtTop || isAtBottom) {
          e.preventDefault();
        }
        e.stopPropagation();
      }, { passive: false });
    }
  });"""

if old_init in text:
    text = text.replace(old_init, new_init, 1)
    print("INIT updated")
else:
    norm_text = text.replace('\r\n', '\n')
    norm_old = old_init.replace('\r\n', '\n')
    norm_new = new_init.replace('\r\n', '\n')
    if norm_old in norm_text:
        text = norm_text.replace(norm_old, norm_new, 1)
        print("INIT updated (norm)")
    else:
        print("INIT NOT FOUND")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("FILE SAVED")
