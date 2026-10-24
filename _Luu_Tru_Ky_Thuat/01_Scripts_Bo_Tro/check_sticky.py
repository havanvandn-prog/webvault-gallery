import os
from PIL import Image
import numpy as np

folder = "Anh_Chup_Website"
images = [f for f in sorted(os.listdir(folder)) if f.endswith(".png")]

print("Checking header repetition across 20 websites...")

for fname in images:
    path = os.path.join(folder, fname)
    img = Image.open(path).convert('RGB')
    arr = np.array(img)
    h, w, _ = arr.shape
    
    # Grab the top header slice (e.g. y=0 to y=80)
    header_slice = arr[10:70, :, :]
    
    matches = []
    # Search down the image in 800-1000px intervals
    for check_y in range(500, h - 100, 100):
        test_slice = arr[check_y:check_y+60, :, :]
        # Compute mean absolute difference
        diff = np.abs(test_slice.astype(float) - header_slice.astype(float)).mean()
        if diff < 12.0: # Very close match
            matches.append(check_y)
            
    if len(matches) > 1:
        print(f"[REPEATED STICKY HEADER DETECTED] {fname}: matches around Y={matches}")
    else:
        print(f"[CLEAN] {fname}")
