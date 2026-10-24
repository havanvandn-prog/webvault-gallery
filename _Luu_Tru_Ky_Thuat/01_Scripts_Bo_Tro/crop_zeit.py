from PIL import Image

img = Image.open(r"D:\AI Agent\Website\Tìm mẫu website\Anh_Chup_Website\zeitmedia.vn.png")
print("Total size:", img.size)

# The dragon banner is between y=1200 and y=2400
cropped = img.crop((0, 1200, 1440, 2500))
cropped.save(r"_Luu_Tru_Ky_Thuat\03_Du_Lieu_Tam_Va_Test\zeit_dragon_crop.png")
print("Saved zeit_dragon_crop.png successfully!")
