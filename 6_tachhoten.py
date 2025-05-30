def tachhoten(name):
    name = name.strip()
    tach = name.split()

    if len(tach) == 0:
        return "" ,""
    elif len(tach) == 1:
        return "",tach[0]
    else:
        ho = ' '.join(tach[:-1])
        ten = tach[-1]
        return ho, ten
    
ho_ten = input("Nhập họ tên: ")
ho_lot, ten = tachhoten(ho_ten)

print("Họ và lót:", ho_lot)
print("Tên:", ten)
