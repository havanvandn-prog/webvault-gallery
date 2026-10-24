import json

with open("_Luu_Tru_Ky_Thuat/03_Du_Lieu_Tam_Va_Test/database.json", "r", encoding="utf-8") as f:
    db = json.load(f)

# Build JS array for WEBSITES_DATA
clean_data = []
for item in db:
    clean_data.append({
        "id": item["id"],
        "name": item["name"],
        "short_name": item["short_name"],
        "url": item["url"],
        "domain": item["domain"],
        "industry": item["industry"],
        "tag": item["tag"],
        "vibe": item["vibe"],
        "vibe_name": item["vibe_name"],
        "location": item["location"].split("&")[0].strip(),
        "desc": item["desc"],
        "thumb": item["thumb_image"],
        "full": item["full_image"],
        "fb": item.get("fb_image", f"Kho_Anh_Webp/{item['domain'].replace('.', '_')}_fb.png"),
        "thumb_kb": item["thumb_size_kb"],
        "full_kb": item["full_size_kb"],
        "fb_kb": item.get("fb_size_kb", 0)
    })

js_array_str = "  const WEBSITES_DATA = " + json.dumps(clean_data, ensure_ascii=False, indent=4) + ";"

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace WEBSITES_DATA
import re
pattern_data = re.compile(r"  const WEBSITES_DATA = \[[\s\S]*?\];", re.MULTILINE)
html = pattern_data.sub(js_array_str, html, count=1)

# Update copyDirectImageToClipboard to be 100% pre-cropped instant copy
old_func_pattern = re.compile(r"  // 2\. COPY DIRECT IMAGE TO CLIPBOARD[\s\S]*?  // LIGHTBOX MODAL", re.MULTILINE)

new_func = """  // 2. COPY DIRECT IMAGE TO CLIPBOARD (ẢNH 1080x1920 ĐÃ ĐƯỢC CẮT SẴN TRONG PIPELINE - COPY TỨC THÌ 0ms)
  async function copyDirectImageToClipboard(targetId, btn) {
    const origHtml = btn.innerHTML;
    const item = WEBSITES_DATA.find(w => w.id === targetId) || { short_name: "Website" };
    const fbRelative = item.fb || `Kho_Anh_Webp/${item.domain.replace(/\\./g, '_')}_fb.png`;

    try {
      btn.innerHTML = `<span style="font-size: 11px;">⏳ Đang copy...</span>`;

      // Xác định URL: Nếu chạy cục bộ file:/// -> nạp từ GitHub CDN để hỗ trợ CORS Clipboard Blob
      let fbUrl = fbRelative;
      if (window.location.protocol === 'file:') {
        fbUrl = 'https://havanvandn-prog.github.io/webvault-gallery/' + fbRelative;
      }

      const resp = await fetch(fbUrl);
      if (!resp.ok) throw new Error("Không thể tải file ảnh cắt sẵn");
      const pngBlob = await resp.blob();

      await navigator.clipboard.write([
        new ClipboardItem({ "image/png": pngBlob })
      ]);

      showToast(`✨ Đã nạp ảnh 1080x1920 của ${item.short_name} vào Clipboard! Bấm Ctrl + V trên Facebook/Zalo để dán ngay.`);
      btn.innerHTML = `✓ Đã Copy Ảnh!`;
      setTimeout(() => { btn.innerHTML = origHtml; }, 2500);

    } catch (e) {
      console.error("Lỗi copy ảnh:", e);
      showToast(`⚠️ Chưa thể nạp trực tiếp ảnh. Vui lòng bấm "Xem Full-Page" để xem chi tiết.`);
      btn.innerHTML = origHtml;
    }
  }

  // LIGHTBOX MODAL"""

html = old_func_pattern.sub(new_func, html, count=1)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("INDEX.HTML UPDATED SUCCESSFULLY")
