from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd



# khởi động trình duyệt Chrome
driver = webdriver.Chrome()  

# tạo file ecxel 
writer = pd.ExcelWriter("Enterprise.xlsx", engine='openpyxl')

#lặp qua các page
for i in range(1,5):
    url = f'https://thuvienphapluat.vn/ma-so-thue/tra-cuu-ma-so-thue-doanh-nghiep?page={i}&pageSize=50'
    driver.get(url)  # Mở trang web
    time.sleep(2)  

    #lấy tất cả thông tin
    element_rows = '//tbody//tr[contains(@class, "item_mst")]'
    full_rows = driver.find_elements(By.XPATH,element_rows)

    #gom dữ liệu
    data_output = []
    for row in full_rows:
        try:
            index = row.find_element(By.XPATH, './/td[1]').text.strip()
            tax_code = row.find_element(By.XPATH, './/td[2]').text.strip()
            name = row.find_element(By.XPATH, './/td[3]').text.strip()
            date = row.find_element(By.XPATH, './/td[4]').text.strip()
            data_output.append({
                "STT": index,
                "Mã số thuế": tax_code,
                "Tên doanh nghiệp": name,
                "Ngày cấp": date,
            })
        except Exception as e:
            print(f"Lỗi: {e}")
            continue

    # Lưu dữ liệu vào file Excel
    df = pd.DataFrame(data_output)
    sheet_name = f"Page_{i}"
    df.to_excel( writer, sheet_name=sheet_name, index=False)
    print(f"Đã lưu dữ liệu trang {i} vào sheet {sheet_name}")

print("kết thúc chạy")
writer.close()
driver.quit()
# Đóng trình duyệt
time.sleep(1000)
