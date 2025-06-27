import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
def handle_input():
    return pd.read_excel('week4/File_input/input_FPT.xlsx', dtype=str)

def open_browser(url):
    """Mở chrome"""
   
    chrome_options = webdriver.ChromeOptions()
    download_path = r"C:/Users/binhp/Python_intern/week4/File_output"
    prefs = {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        # "disable_popup_blocking": True,
        "safebrowsing.enabled": True,
        "safebrowsing.disable_download_protection": True 
    }
    chrome_options.add_experimental_option("prefs", prefs)
    return webdriver.Chrome(options=chrome_options)

def process_fpt_invoice(driver, url, ma_so_thue, ma_tra_cuu):
    """xử lý loại hoá đơn FPT"""
    driver.get(url)
    time.sleep(2)
    xpath_ma_so_thue = "//input[@placeholder='MST bên bán']"
    driver.find_element(By.XPATH, xpath_ma_so_thue).send_keys(ma_so_thue)
    time.sleep(2) 

    xpath_ma_tra_cuu = "//input[@placeholder='Mã tra cứu hóa đơn']"
    driver.find_element(By.XPATH, xpath_ma_tra_cuu).send_keys(ma_tra_cuu)

    #nhấn nút tra cứu
    xpath_btn_search = "/html/body/div[3]/div/div/div[3]/div/div[1]/div/div[4]/div[2]/div/button"
    driver.find_element(By.XPATH, xpath_btn_search).click()

    wait = WebDriverWait(driver, 10)
    btn_tai_xml = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Tải XML')]"))
    )
    btn_tai_xml.click()

    print()
    if check_load_success(driver):
        return True
    if check_load_fail(driver):
        return False
def process_misa_invoice(driver, url, ma_so_thue, ma_tra_cuu):
    """"xử lý loại hoá đơn MISA"""
    #1 mở trang web
    driver.get(url)

    #2 nhập mã tra cứu
    xpath_ma_tra_cuu = 'txtCode'
    driver.find_element(By.ID,xpath_ma_tra_cuu ).send_keys(ma_tra_cuu)

    #3 Click nút "Tra cứu"
    Id_btn_search = 'btnSearchInvoice'
    driver.find_element(By.ID, Id_btn_search ).click()
    time.sleep(5)

    #download
    driver.find_element(By.CLASS_NAME,"res-btn.download").click()
    time.sleep(5) 
    
    # tải hoá đơn điện tử (PDF) về hệ thống cục bộ
    # 5 tải hoá đơn , tra cứu thành công
    driver.find_element(By.XPATH, "//div[contains(@class,'txt-download-xml')]").click()
    time.sleep(1) 
    print(f"Đã tải hóa đơn cho mã: {ma_tra_cuu}")

def process_van_invoice(driver, url, ma_so_thue, ma_tra_cuu):
    """"xử lý loại hoá đơn VAN"""
    #1 mở trang web
    driver.get(url)

    #2 nhập mã tra cứu
    xpath_ma_tra_cuu = "//input[@placeholder='Nhập Mã tra cứu Hóa đơn']" 
    driver.find_element(By.XPATH, xpath_ma_tra_cuu).send_keys(ma_tra_cuu)

    #3 Click nút "Tra cứu"
    xpath_btn_search = '//*[@id="Button1"]'
    driver.find_element(By.XPATH, xpath_btn_search ).click()
    time.sleep(5)

    #download
    #4. Chuyển vào iframe chứa hóa đơn
    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "frameViewInvoice"))
    )

    #5. click nút "Tải về" 
    download_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "btnDownload"))
    )
    download_btn.click()
    time.sleep(3)

    #6. Click vào nút "Tải XML"
    link_xml = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "LinkDownXML"))
    )
    link_xml.click()

    time.sleep(1)


def check_load_success(driver):
    pass
def  check_load_fail(driver):
    pass

def process_invoice(df):
    """"xử lý từng loại hoá đơn"""
    # Duyệt từng dòng và thêm vào dict
    # path_folder = 'download'
    for index, row in df.iterrows():
        ma_so_thue = str(row['Mã số thuế']).strip()
        ma_tra_cuu = str(row['Mã tra cứu'])
        url = str(row['URL']).strip()

        driver = open_browser(url) 
        try:
            if "fpt" in url:
                process_fpt_invoice(driver, url, ma_so_thue, ma_tra_cuu)
            elif "meinvoice" in url:
                process_misa_invoice(driver, url, ma_so_thue, ma_tra_cuu)
            elif "van.ehoadon" in url:
                process_van_invoice(driver, url, ma_so_thue, ma_tra_cuu)
        except Exception as e:
            print(f"Lỗi ở dòng {index + 2} (MST: {ma_so_thue}): {e}")
        finally:
            time.sleep(5)
            driver.quit()

        

def main():
    #1. đọc file input excel
    df = handle_input()
    process_invoice(df)

main()

#---------------------------------------------------------------------------------

# dict_input = {
#     'Mã số thuế': [], 
#     'Mã tra cứu': [],
#     'URL': []
# }
# # Lấy 3 cột cần thiết
# df_selected = df[['Mã số thuế', 'Mã tra cứu', 'URL']]


# # In kết quả

# #hàm open browser
# #mở chrome và đi tới URL

# driver = webdriver.Chrome()     
# driver.get("https://www.meinvoice.vn/tra-cuu")  


# #hàm tra cứu
# #chia thành từng trường hợp theo loại : misa , fpt , van

# #hàm check kết quả
# # suscess 
# # fail

# #hàm tải hoá đơn
# #chia thành từng truờng hợp theo loại : misa , fpt , van
# id_iframe = ''
# element_iframe = driver.find_element(By.XPATH, '')
# driver.switch_to.frame(element_iframe)

# #find element : id-divDownloads
# #click download

# #hàm đọc dữ liệu
# #đọc file tải về xml

# f = open('file_xml.xml')
# data_file = f.read()
# print(data_file)

# #hàm trích xuất dữu liệu
# #chia thành tưng trường hợp theo loại : misa , fpt , van