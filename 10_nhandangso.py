def doc_so_bang_chu(so):
    chu_so = ["", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]

    tram = so // 100        # Lay so hang tram
    chuc = (so % 100) // 10 # Lay so hang chuc
    don_vi = so % 10        # Lay so hang don vi

    ket_qua = chu_so[tram] + " trăm"

    if chuc == 0 and don_vi != 0:
        ket_qua += " lẻ"
    elif chuc != 0:
        if chuc == 1:
            ket_qua += " mười"
        else:
            ket_qua += " " + chu_so[chuc] + " mươi"

    if don_vi != 0:
        if don_vi == 1 and chuc >= 2:
            ket_qua += " mốt"
        elif don_vi == 5 and chuc != 0:
            ket_qua += " lăm"
        else:
            ket_qua += " " + chu_so[don_vi]

    return ket_qua.strip()


# Nhập và kiểm tra
so_nhap = input("Nhập số có 3 chữ số (100–999): ")

if so_nhap.isdigit() and 100 <= int(so_nhap) <= 999:
    doc_chu = doc_so_bang_chu(int(so_nhap))
    print("Bằng chữ:", doc_chu)
else:
    print("Vui lòng nhập số nguyên có 3 chữ số từ 100 đến 999.")
