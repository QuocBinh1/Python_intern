from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def main():
    #1 mở trinh duyệt: cấu hình download file selenium
    driver = webdriver.Chrome()     

    driver.get("https://www.meinvoice.vn/tra-cuu")  

    # nhập mã hoá đơn vào ô tương ứng
    # 2 hàm nhập mã tra cứu
    invoice_input = driver.find_element(By.ID,"txtCode").send_keys("B1HEIRR8N0WP")
    try:
        # hàm thực hiện hành động tìm kiếm
        # 3 hàm thực hiện tìm kiếm 
        input_search = driver.find_element(By.ID,"btnSearchInvoice").click()
        time.sleep(2) 

        # xử lý kết quả tìm kiếm 
        # 4 hàm thực hiện tải xuống hoá đơn
        download_button = driver.find_element(By.CLASS_NAME,"res-btn.download").click()
        time.sleep(2) 

        # tải hoá đơn điện tử (PDF) về hệ thống cục bộ
        # 5 tải hoá đơn , tra cứu thành công
        pdf_option = driver.find_element(By.XPATH, "//div[contains(@class,'txt-download-pdf')]").click()

    except Exception as e:
        print("Không tìm thấy hoá đơn")
        

    # duy trì hiện trang
    time.sleep(500) 

    # đóng trình duyệt
    driver.quit() 