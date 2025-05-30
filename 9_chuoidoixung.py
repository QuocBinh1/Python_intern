def chuoidoixung(s):
    return s == s[::-1]

chuoi = input("Nhập chuỗi: ")
chuoi = chuoi.strip()
chuoi = chuoi.replace(" ", "")
if chuoidoixung(chuoi):
    print("Chuỗi đối xứng")
else:
    print("Chuỗi không đối xứng")