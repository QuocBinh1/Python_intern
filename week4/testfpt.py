from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def open_browser():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=chrome_options)

def get_xml_from_fpt(mst, ma_tra_cuu, output_path="output.xml"):
    url = "https://tracuuhoadon.fpt.com/"
    driver = open_browser()
    wait = WebDriverWait(driver, 15)

    try:
        driver.get(url)
        time.sleep(2)

        # Nhập MST
        input_mst = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='MST bên bán']")))
        input_mst.send_keys(mst)

        # Nhập mã tra cứu
        input_code = driver.find_element(By.XPATH, "//input[@placeholder='Mã tra cứu hóa đơn']")
        input_code.send_keys(ma_tra_cuu)

        # Nhấn nút tra cứu
        btn_tra_cuu = driver.find_element(By.XPATH, "//button[contains(., 'Tra cứu')]")
        btn_tra_cuu.click()

        # Đợi hiện nút "Tải XML"
        btn_tai_xml = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Tải XML')]")))
        btn_tai_xml.click()

        # Đợi hiển thị nội dung XML (giả sử hiển thị trong thẻ <pre>)
        pre_xml = wait.until(EC.presence_of_element_located((By.XPATH, "//pre")))

        xml_text = pre_xml.text.strip()

        # Lưu file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(xml_text)

        print(f"✅ Đã lưu XML vào {output_path}")

    except Exception as e:
        print("❌ Lỗi:", e)

    finally:
        driver.quit()

# Gọi hàm để test
get_xml_from_fpt("0304244470", "r08e17y79g", output_path="C:/Users/binhp/Python_intern/week4/File_output/fpt_output.xml")
