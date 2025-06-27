from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd


def Lookup_Download_Invoice(lookup_code):
    #1 mở trinh duyệt: cấu hình download file selenium
    driver = webdriver.Chrome()     

    try:
        #truy cập vào trang web tra cứu hoá đơn
        driver.get("https://www.meinvoice.vn/tra-cuu")  

        # nhập mã hoá đơn vào ô tương ứng
        # 2 hàm nhập mã tra cứu
        driver.find_element(By.ID, "txtCode").send_keys(lookup_code)

        # 3 hàm thực hiện tìm kiếm 
        driver.find_element(By.ID, "btnSearchInvoice").click()
        time.sleep(5)

        # xử lý kết quả tìm kiếm 
        # 4 hàm thực hiện tải xuống hoá đơn
        driver.find_element(By.CLASS_NAME,"res-btn.download").click()
        time.sleep(5) 

        # tải hoá đơn điện tử (PDF) về hệ thống cục bộ
        # 5 tải hoá đơn , tra cứu thành công
        driver.find_element(By.XPATH, "//div[contains(@class,'txt-download-pdf')]").click()
        time.sleep(5) 
        print(f"Đã tải hóa đơn cho mã: {lookup_code}")
        return "đã tải thành công"
    except Exception as e:
        print("Không tìm thấy hoá đơn")
        return "Không tìm thấy hóa đơn"
    finally:
        driver.quit()  # Đóng trình duyệt ở cuối mỗi lượt  
def main():
     # Đọc file Excel chứa mã tra cứu
    file_path = "C:/Users/binhp/Python_intern/week4/File_input/input_MISA.xlsx"
    df = pd.read_excel(file_path) 

    # Tạo cột Result 
    if 'Result' not in df.columns:
        df['Result'] = ""

    for index, row in df.iterrows():
        lookup_code = str(row['Mã tra cứu']).strip()
        result = Lookup_Download_Invoice(lookup_code)
        df.at[index, 'Result'] = result

    # Ghi kết quả vào file output_MISA
    df.to_excel("C:/Users/binhp/Python_intern/week4/File_output/output_MISA.xlsx", index=False)
    print("✅ Đã ghi kết quả vào output_MISA_result.xlsx")

main()

# duy trì hiện trang
# time.sleep(500) 

