def dem_tan_suat_ky_tu(chuoi):
    tan_suat = {}
    for ky_tu in chuoi:
        if ky_tu != ' ': 
            tan_suat[ky_tu] = tan_suat.get(ky_tu, 0) + 1

    for ky_tu, so_lan in tan_suat.items():
        print(f"Ký tự '{ky_tu}' xuất hiện {so_lan} lần.")

# Ví dụ sử dụng
chuoi_nhap = input("Nhập chuỗi: ")
dem_tan_suat_ky_tu(chuoi_nhap)
