def tim_ky_tu_pho_bien_nhat(chuoi):
    # Bỏ qua khoảng trắng nếu không muốn tính
    chuoi = chuoi.replace(" ", "")
    
    # Tạo dictionary để đếm tần suất ký tự
    tan_suat = {}
    for ky_tu in chuoi:
        tan_suat[ky_tu] = tan_suat.get(ky_tu, 0) + 1

    # Tìm ký tự có tần suất lớn nhất
    ky_tu_max = max(tan_suat, key=tan_suat.get)
    so_lan = tan_suat[ky_tu_max]

    return ky_tu_max, so_lan

# Ví dụ sử dụng
chuoi_nhap = input("Nhập chuỗi: ")
ky_tu, so_lan = tim_ky_tu_pho_bien_nhat(chuoi_nhap)
print(f"Ký tự xuất hiện nhiều nhất là '{ky_tu}' với {so_lan} lần.")
