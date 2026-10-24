import re

with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

# Pattern matching copyDirectImageToClipboard to end of showCopyGuideModal
pattern = re.compile(
    r"  // 2\. COPY DIRECT IMAGE TO CLIPBOARD[\s\S]*?  // LIGHTBOX MODAL",
    re.MULTILINE
)

new_func = """  // 2. COPY DIRECT IMAGE TO CLIPBOARD (CẮT CHUẨN TỶ LỆ 1080x1920 9:16 CHO FACEBOOK/MESSENGER/ZALO)
  async function copyDirectImageToClipboard(targetId, btn) {
    const origHtml = btn.innerHTML;
    const item = WEBSITES_DATA.find(w => w.id === targetId) || { full: targetId, short_name: "Website" };
    const relativeUrl = item.full || item.thumb;

    try {
      btn.innerHTML = `<span style="font-size: 11px;">⏳ Đang cắt ảnh...</span>`;

      // Xác định nguồn ảnh an toàn: Nếu mở bằng file:/// -> nạp từ GitHub CDN để tránh lỗi chặn Canvas
      let fetchUrl = relativeUrl;
      if (window.location.protocol === 'file:') {
        fetchUrl = 'https://havanvandn-prog.github.io/webvault-gallery/' + relativeUrl;
      }

      let bitmap;
      try {
        const resp = await fetch(fetchUrl);
        const blob = await resp.blob();
        bitmap = await createImageBitmap(blob);
      } catch (err) {
        // Fallback: nếu fetch thất bại, thử nạp bằng Image object
        const img = new Image();
        img.crossOrigin = "anonymous";
        img.src = fetchUrl;
        await new Promise((resolve, reject) => {
          img.onload = resolve;
          img.onerror = () => reject(new Error("Không thể tải file ảnh"));
        });
        bitmap = img;
      }

      const natW = bitmap.naturalWidth || bitmap.width;
      const natH = bitmap.naturalHeight || bitmap.height;

      // Cắt lát chuẩn 9:16 từ đỉnh trang (Hero + Điểm nhấn nổi bật)
      const sliceH = Math.min(natH, Math.round(natW * (16 / 9)));

      // Canvas kích thước chuẩn quốc tế 1080 x 1920
      const canvas = document.createElement("canvas");
      canvas.width = 1080;
      canvas.height = 1920;
      const ctx = canvas.getContext("2d");

      ctx.imageSmoothingEnabled = true;
      ctx.imageSmoothingQuality = "high";

      // Nền đen Zeit tone
      ctx.fillStyle = "#070709";
      ctx.fillRect(0, 0, 1080, 1920);

      // Cắt phần đầu trang và co giãn chuẩn về 1080x1920
      ctx.drawImage(bitmap, 0, 0, natW, sliceH, 0, 0, 1080, 1920);

      const pngBlob = await new Promise(resolve => canvas.toBlob(resolve, "image/png"));
      if (!pngBlob) throw new Error("Chuyển đổi Blob thất bại");

      await navigator.clipboard.write([
        new ClipboardItem({ "image/png": pngBlob })
      ]);

      showToast(`✨ Đã nạp ảnh 1080x1920 vào Clipboard! Bấm Ctrl + V trên Facebook/Zalo để dán ngay.`);
      btn.innerHTML = `✓ Đã Copy Ảnh!`;
      setTimeout(() => { btn.innerHTML = origHtml; }, 2500);

    } catch (e) {
      console.error("Lỗi copy ảnh:", e);
      showToast(`⚠️ Chưa thể nạp trực tiếp ảnh. Vui lòng bấm "Xem Full-Page" để xem chi tiết.`);
      btn.innerHTML = origHtml;
    }
  }

  // LIGHTBOX MODAL"""

if pattern.search(text):
    text = pattern.sub(new_func, text, count=1)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(text)
    print("SUCCESS")
else:
    print("PATTERN NOT MATCHED")
