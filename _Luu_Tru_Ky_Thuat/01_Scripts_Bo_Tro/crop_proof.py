from PIL import Image

img = Image.open("Anh_Chup_Website/sukienachau.com.png")
# Crop Y=750 to Y=1000
cropped = img.crop((0, 750, 1440, 1050))
cropped.save("_Luu_Tru_Ky_Thuat/03_Du_Lieu_Tam_Va_Test/crop_check_pink_bar.png")
print("Saved crop_check_pink_bar.png successfully! Size:", cropped.size)
