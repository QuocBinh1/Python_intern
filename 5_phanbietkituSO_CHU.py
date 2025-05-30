def tach_so_tu_chuoi(chuoi):
    number = [i for i in chuoi if i.isdigit()]
    
    if number:
        print("Chuỗi có chứa ký tự số.")
        print("Các số được tách ra:", number)
    else:
        print("Chuỗi không chứa ký tự số.")

# Ví dụ sử dụng
chuoi_nhap = input("Nhập chuỗi: ")
tach_so_tu_chuoi(chuoi_nhap)
