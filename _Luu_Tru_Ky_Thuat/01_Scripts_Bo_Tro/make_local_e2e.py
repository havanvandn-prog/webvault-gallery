with open('_Luu_Tru_Ky_Thuat/01_Scripts_Bo_Tro/test_e2e_features.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Allow testing on local file or online URL
text = text.replace('TARGET_URL = "https://havanvandn-prog.github.io/webvault-gallery/"', 'TARGET_URL = os.path.abspath("index.html").replace(os.sep, "/")\n    if not TARGET_URL.startswith("http"):\n        TARGET_URL = f"file:///{TARGET_URL}"')

with open('_Luu_Tru_Ky_Thuat/01_Scripts_Bo_Tro/test_e2e_local.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("Created test_e2e_local.py")
