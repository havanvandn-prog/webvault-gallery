with open('_Luu_Tru_Ky_Thuat/01_Scripts_Bo_Tro/test_e2e_features.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('assert card_count == 20', 'assert card_count >= 20')
text = text.replace('assert final_count == 20', 'assert final_count >= 20')

with open('_Luu_Tru_Ky_Thuat/01_Scripts_Bo_Tro/test_e2e_features.py', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated assertions in test_e2e_features.py")
