import os
from PIL import Image
import numpy as np

folder = "Anh_Chup_Website"
images = [f for f in sorted(os.listdir(folder)) if f.endswith(".png") and not "stitched" in f and not "fixed" in f and not "test" in f]

suspects = []

for fname in images:
    path = os.path.join(folder, fname)
    img = Image.open(path).convert('RGB')
    arr = np.array(img)
    h, w, _ = arr.shape
    
    # Check 1000px chunks
    has_huge_blank = False
    blank_ranges = []
    chunk_size = 1000
    for y in range(0, h - chunk_size, 500):
        chunk = arr[y:y+chunk_size, :, :]
        white_mask = (chunk[:,:,0] > 245) & (chunk[:,:,1] > 245) & (chunk[:,:,2] > 245)
        pct = white_mask.mean() * 100
        if pct > 98.0:
            has_huge_blank = True
            blank_ranges.append(f"{y}-{y+chunk_size} ({pct:.1f}%)")
            
    if has_huge_blank:
        suspects.append((fname, h, blank_ranges))
        print(f"[SUSPECT] {fname} (H={h}): {', '.join(blank_ranges)}")
    else:
        print(f"[OK] {fname} (H={h})")

print(f"\nTotal suspects with blank gaps: {len(suspects)}/{len(images)}")
