def xenke(s):
    result  = ""
    for i in range(len(s)):
        if i % 2 == 0:
            result += s[i].upper()
        else:
            result += s[i].lower()
    return result
chuoi = input("Nhập chuỗi: ")
chuoi = chuoi.strip()
chuoi = chuoi.replace(" ", "")
chuoi = xenke(chuoi)
print(chuoi)