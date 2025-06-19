from selenium import webdriver
from selenium.webdriver.common.by import By
import time

 # Khởi động trình duyệt Chrome
driver = webdriver.Chrome() 

# Mở trang web
driver.get("https://www.meinvoice.vn/tra-cuu")  

# Tìm ô và nhập mã hoá đơn
invoice_input = driver.find_element(By.ID,"txtCode").send_keys("B1HEIRR8N0WP")
try:
    # bấm nút tìm kiếm
    input_search = driver.find_element(By.ID,"btnSearchInvoice").click()
    time.sleep(2) 

    # bấm nút tải xuống và hiện ra 2 lựa chọn
    download_button = driver.find_element(By.CLASS_NAME,"res-btn.download").click()
    time.sleep(2) 

    # tìm lựa chọn tải bằng pdf
    pdf_option = driver.find_element(By.XPATH, "//div[contains(@class,'txt-download-pdf')]").click()

except Exception as e:
    print("Không tìm thấy hoá đơn")
    

# duy trì hiện trang
time.sleep(500) 

# đóng trình duyệt
driver.quit() 