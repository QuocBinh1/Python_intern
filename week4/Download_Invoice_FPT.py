import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time , xmltodict

def handle_input():
    return pd.read_excel('week4/File_input/input_FPT.xlsx', dtype=str)

def open_browser(download_path):
    """Mở chrome"""
    chrome_options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "safebrowsing.disable_download_protection": True 
    }
    chrome_options.add_experimental_option("prefs", prefs)
    return webdriver.Chrome(options=chrome_options)

def process_fpt_invoice(driver, url, ma_so_thue, ma_tra_cuu):
    """xử lý loại hoá đơn FPT"""
    driver.get(url)
    time.sleep(1)

    xpath_ma_so_thue = "//input[@placeholder='MST bên bán']"
    driver.find_element(By.XPATH, xpath_ma_so_thue).send_keys(ma_so_thue)
    time.sleep(1) 

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
              

    print(f"Đã tải hóa đơn FPT cho mã: {ma_tra_cuu}")

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

def process_invoice(df , download_path):
    """"xử lý từng loại hoá đơn"""
    # Duyệt từng dòng và thêm vào dict
    # path_folder = 'download'
    for index, row in df.iterrows():
        ma_so_thue = str(row['Mã số thuế']).strip()
        ma_tra_cuu = str(row['Mã tra cứu'])
        url = str(row['URL']).strip()

        driver = open_browser(download_path) 
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

#hàm đọc file xmt thành to dict
def read_xml_to_dict(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = xmltodict.parse(f.read())
    return data
#hàm đọc file
def Read_All_Xml_In_Folder(folder_path):
    xml_file = [f for f in os.listdir(folder_path) if f.endswith('.xml')]
    for file_name in xml_file:
        file_path = os.path.join(folder_path, file_name)
        data_dict = read_xml_to_dict(file_path)
        

        # print(data_dict)
        info = extract_fpt_invoice_info(data_dict)
        if info:
            print(f"{file_name}")
            for key , value in info.items():
                print(f"{key}: {value}")
            print("-" * 100)
    
def extract_fpt_invoice_info(data_dict):
    try:
        print(f"DEBUG: Root keys: {list(data_dict.keys())}")
        
        # Trường hợp TDiep > DLieu > HDon
        if "TDiep" in data_dict:
            print("DEBUG: Tìm thấy TDiep")
            dlieu = data_dict["TDiep"].get("DLieu", {})
            if not dlieu:
                print("DEBUG: Không tìm thấy DLieu trong TDiep")
                return None
            hdon = dlieu.get("HDon", {})
            if not hdon:
                print("DEBUG: Không tìm thấy HDon trong DLieu")
                return None

        # Trường hợp DLieu > HDon
        elif "DLieu" in data_dict:
            print("DEBUG: Tìm thấy DLieu")
            hdon = data_dict["DLieu"].get("HDon", {})
            if not hdon:
                print("DEBUG: Không tìm thấy HDon trong DLieu")
                return None

        # Trường hợp bắt đầu luôn từ HDon
        elif "HDon" in data_dict:
            print("DEBUG: Tìm thấy HDon")
            hdon = data_dict["HDon"]
        else:
            print("DEBUG: Không tìm thấy thẻ HDon hợp lệ trong XML")
            return None

        print(f"DEBUG: HDon keys: {list(hdon.keys())}")
        
        if "DLHDon" not in hdon:
            print("DEBUG: Không tìm thấy DLHDon trong HDon")
            return None
            
        dlh = hdon["DLHDon"]
        print(f"DEBUG: DLHDon có các key: {list(dlh.keys())}")
        
        ndhdon = dlh.get("NDHDon", {})
        if not ndhdon:
            print("DEBUG: Không tìm thấy NDHDon")
            return None
            
        nban = ndhdon.get("NBan", {})
        nmua = ndhdon.get("NMua", {})

        info = {
            "Số hóa đơn": dlh.get("TTChung", {}).get("SHDon"),
            "Đơn vị bán hàng": nban.get("Ten"),
            "Mã số thuế bán": nban.get("MST"),
            "Địa chỉ bán": nban.get("DChi"),
            "Họ tên người mua hàng": nmua.get("Ten"),
            "Địa chỉ mua": nmua.get("DChi"),
            "Mã số thuế mua": nmua.get("MST"),
           
        }
        return info
    except Exception as e:
        print(f"Lỗi khi trích xuất hóa đơn: {e}")
        return None

def create_output_file(df_input, xml_data_list):
    """Tạo file output_FPT.xlsx từ dữ liệu input và thông tin XML"""
    
    # Tạo DataFrame output từ input
    df_output = df_input.copy()
    
    # Thêm các cột mới
    df_output['Số hóa đơn'] = ''
    df_output['Đơn vị bán hàng'] = ''
    df_output['Mã số thuế bán'] = ''
    df_output['Địa chỉ bán'] = ''
    df_output['Họ tên người mua hàng'] = ''
    df_output['Địa chỉ mua'] = ''
    df_output['Mã số thuế mua'] = ''
    df_output['Trạng thái'] = ''
    
    # Điền dữ liệu từ XML vào các cột
    for i, xml_data in enumerate(xml_data_list):
        if i < len(df_output) and xml_data:
            df_output.loc[i, 'Số hóa đơn'] = xml_data.get('Số hóa đơn', '')
            df_output.loc[i, 'Đơn vị bán hàng'] = xml_data.get('Đơn vị bán hàng', '')
            df_output.loc[i, 'Mã số thuế bán'] = xml_data.get('Mã số thuế bán', '')
            df_output.loc[i, 'Địa chỉ bán'] = xml_data.get('Địa chỉ bán', '')
            df_output.loc[i, 'Họ tên người mua hàng'] = xml_data.get('Họ tên người mua hàng', '')
            df_output.loc[i, 'Địa chỉ mua'] = xml_data.get('Địa chỉ mua', '')
            df_output.loc[i, 'Mã số thuế mua'] = xml_data.get('Mã số thuế mua', '')
            df_output.loc[i, 'Trạng thái'] = 'Thành công' if xml_data else 'Thất bại'
        elif i < len(df_output):
            df_output.loc[i, 'Trạng thái'] = 'Thất bại'
    
    # Lưu file output
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, 'File_output')
    output_path = os.path.join(output_dir, 'output_FPT.xlsx')
    os.makedirs(output_dir, exist_ok=True)
    df_output.to_excel(output_path, index=False)
    print(f"Đã tạo file output: {output_path}")
    
    return df_output

def process_all_xml_files(folder_path):
    """Xử lý tất cả file XML và trả về danh sách thông tin"""
    xml_data_list = []
    
    if not os.path.exists(folder_path):
        print(f"Thư mục {folder_path} không tồn tại")
        return xml_data_list
    
    xml_files = [f for f in os.listdir(folder_path) if f.endswith('.xml')]
    
    for file_name in xml_files:
        file_path = os.path.join(folder_path, file_name)
        try:
            data_dict = read_xml_to_dict(file_path)
            info = extract_fpt_invoice_info(data_dict)
            xml_data_list.append(info)
            
            if info:
                print(f"\nFile: {file_name}")
                for key, value in info.items():
                    print(f"{key}: {value}")
                print("-" * 50)
        except Exception as e:
            print(f"Lỗi khi xử lý file {file_name}: {e}")
            xml_data_list.append(None)
    
    return xml_data_list

def main():
    """Hàm chính để chạy toàn bộ quy trình"""
    
    # Tạo thư mục download nếu chưa có
    script_dir = os.path.dirname(os.path.abspath(__file__))
    download_path = os.path.join(script_dir, "download")
    os.makedirs(download_path, exist_ok=True)

    #1. đọc file input excel
    df = handle_input()
    print(f"Đã đọc {len(df)} dòng dữ liệu từ file input")

    #2. xử lý từng loại hoá đơn
    process_invoice(df, download_path)
    
    #3. đọc tất cả file xml trong thư mục download và trích xuất thông tin
    xml_data_list = process_all_xml_files(download_path)
    
    #4. tạo file output với thông tin đầy đủ
    df_output = create_output_file(df, xml_data_list)
    
    print(f"\nHoàn thành! Đã xử lý {len(xml_data_list)} file XML")

def main_test():
    """Hàm test chỉ tạo file output với dữ liệu mẫu"""
    print("Chạy test tạo file output...")
    test_create_output()

def test_create_output():
    """Test tạo file output mà không cần selenium"""
    print("Test tạo file output...")
    
    # Đọc file input
    df = handle_input()
    print(f"Đã đọc {len(df)} dòng dữ liệu từ file input")
    
    # Tạo dữ liệu XML mẫu (giả lập)
    xml_data_list = []
    for i in range(len(df)):
        xml_data = {
            'Số hóa đơn': f'HD{i+1:03d}',
            'Đơn vị bán hàng': f'Công ty ABC {i+1}',
            'Mã số thuế bán': f'123456789{i+1:02d}',
            'Địa chỉ bán': f'Địa chỉ {i+1}',
            'Họ tên người mua hàng': f'Khách hàng {i+1}',
            'Địa chỉ mua': f'Địa chỉ khách {i+1}',
            'Mã số thuế mua': f'987654321{i+1:02d}',
        }
        xml_data_list.append(xml_data)
    
    # Tạo file output
    df_output = create_output_file(df, xml_data_list)
    print(f"Đã tạo file output với {len(df_output)} dòng dữ liệu")
    
    return df_output

def test_xml_processing():
    """Hàm test chỉ để xử lý XML có sẵn"""
    # Đọc file input
    df = handle_input()
    print(f"Đã đọc {len(df)} dòng dữ liệu từ file input")
    
    # Xử lý XML có sẵn
    download_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "download")
    xml_data_list = process_all_xml_files(download_path)
    
    # Tạo file output
    df_output = create_output_file(df, xml_data_list)
    
    print(f"\nHoàn thành! Đã xử lý {len(xml_data_list)} file XML")
    return df_output

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Chạy test tạo file output với dữ liệu mẫu
        print("Chạy test tạo file output...")
        main_test()
    elif len(sys.argv) > 1 and sys.argv[1] == "xml":
        # Chạy test xử lý XML có sẵn
        print("Chạy test xử lý XML có sẵn...")
        test_xml_processing()
    else:
        # Chạy quy trình đầy đủ
        print("Chạy quy trình download và tạo file output...")
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