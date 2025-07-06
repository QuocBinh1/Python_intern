import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time , xmltodict , sys

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
    
    # Đợi 2 giây để trang xử lý
    time.sleep(2)

    # Kiểm tra trạng thái tra cứu
    status = check_load(driver)
    
    if status == 'fail':
        print(f"Tra cứu thất bại cho mã: {ma_tra_cuu}")
        return False
    elif status == 'success':
        # Nếu thành công thì tải XML
        try:
            btn_tai_xml = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Tải XML')]"))
            )
            btn_tai_xml.click()
            print(f"Đã tải hóa đơn FPT thành công cho mã: {ma_tra_cuu}")
            return True
        except Exception as e:
            print(f"lỗi khi tải XML cho mã {ma_tra_cuu}: {e}")
            return False
    else:  # status == 'unknown'
        print(f" Không thể xác định trạng thái cho mã: {ma_tra_cuu}")
        return False
    
def process_misa_invoice(driver, url, ma_so_thue, ma_tra_cuu):
    """"xử lý loại hoá đơn MISA"""
    try:
        #1 mở trang web
        driver.get(url)
        time.sleep(2)

        #2 nhập mã tra cứu
        xpath_ma_tra_cuu = 'txtCode'
        driver.find_element(By.ID, xpath_ma_tra_cuu).send_keys(ma_tra_cuu)

        #3 Click nút "Tra cứu"
        Id_btn_search = 'btnSearchInvoice'
        driver.find_element(By.ID, Id_btn_search).click()
        time.sleep(5)

        # Kiểm tra kết quả tra cứu
        try:
            # Kiểm tra có thông báo lỗi không
            error_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'không tìm thấy') or contains(text(), 'không tồn tại') or contains(text(), 'lỗi')]")
            if error_elements:
                print(f"Tra cứu MISA thất bại cho mã: {ma_tra_cuu}")
                return False
                
            #download
            download_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "res-btn.download"))
            )
            download_btn.click()
            time.sleep(3) 
            
            # tải XML
            xml_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'txt-download-xml')]"))
            )
            xml_btn.click()
            time.sleep(2)
            print(f"Đã tải hóa đơn MISA thành công cho mã: {ma_tra_cuu}")
            return True
            
        except Exception as e:
            print(f"Lỗi khi tải XML MISA cho mã {ma_tra_cuu}: {e}")
            return False
            
    except Exception as e:
        print(f"Lỗi tổng quát khi xử lý MISA cho mã {ma_tra_cuu}: {e}")
        return False

def process_van_invoice(driver, url, ma_so_thue, ma_tra_cuu):
    """"xử lý loại hoá đơn VAN"""
    try:
        #1 mở trang web
        driver.get(url)
        time.sleep(2)

        #2 nhập mã tra cứu
        xpath_ma_tra_cuu = "//input[@placeholder='Nhập Mã tra cứu Hóa đơn']" 
        driver.find_element(By.XPATH, xpath_ma_tra_cuu).send_keys(ma_tra_cuu)

        #3 Click nút "Tra cứu"
        xpath_btn_search = '//*[@id="Button1"]'
        driver.find_element(By.XPATH, xpath_btn_search).click()
        time.sleep(5)

        # Kiểm tra có iframe không (dấu hiệu thành công)
        try:
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
            time.sleep(2)
            
            print(f"Đã tải hóa đơn VAN thành công cho mã: {ma_tra_cuu}")
            return True
            
        except Exception as e:
            print(f"Tra cứu VAN thất bại cho mã {ma_tra_cuu}: {e}")
            return False
            
    except Exception as e:
        print(f"Lỗi tổng quát khi xử lý VAN cho mã {ma_tra_cuu}: {e}")
        return False

def check_load(driver):
    """Kiểm tra trạng thái tra cứu hóa đơn - Trả về 'success', 'fail', hoặc 'unknown'"""
    try:
        # Bước 1: Kiểm tra thông báo lỗi trước (nhanh hơn)
        error_messages = [
            "Không tìm thấy hóa đơn",
            "Mã tra cứu không đúng", 
            "Không tồn tại",
            "Hóa đơn không hợp lệ",
            "Lỗi tra cứu",
            "Thông tin không chính xác"
        ]
        
        for msg in error_messages:
            try:
                error_element = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{msg}')]"))
                )
                if error_element.is_displayed():
                    print(f"Tra cứu thất bại: {msg}")
                    return 'fail'
            except:
                continue
        # Bước 2: Kiểm tra nút "Tải XML" (dấu hiệu thành công)
        try:
            btn_tai_xml = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Tải XML')]"))
            )
            if btn_tai_xml:
                print("Tra cứu thành công - Tìm thấy nút 'Tải XML'")
                return 'success'
        except:
            pass
        
        # Bước 3: Nếu không tìm thấy gì
        print("Không thể xác định trạng thái tra cứu")
        return 'unknown'
        
    except Exception as e:
        print(f"Lỗi khi kiểm tra trạng thái: {e}")
        return 'unknown'

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
        
        # Thử trích xuất với các loại hóa đơn khác nhau
        info = extract_fpt_invoice_info(data_dict)
        invoice_type = "FPT"
        
        if not info:
            info = extract_misa_invoice_info(data_dict)
            invoice_type = "MISA"
            
        if not info:
            info = extract_van_invoice_info(data_dict)
            invoice_type = "VAN"
            
        if info:
            print(f"{file_name} (Loại: {invoice_type})")
            for key , value in info.items():
                print(f"{key}: {value}")
            print("-" * 100)
        else:
            print(f"{file_name} - Không thể trích xuất thông tin")
            print("-" * 100)
    
def extract_fpt_invoice_info(data_dict):
    
    # Trường hợp TDiep > DLieu > HDon
    if "TDiep" in data_dict:
        dlieu = data_dict["TDiep"].get("DLieu", {})
        if not dlieu:
            return None
        hdon = dlieu.get("HDon", {})
        if not hdon:
            return None

    # Trường hợp DLieu > HDon
    elif "DLieu" in data_dict:
        hdon = data_dict["DLieu"].get("HDon", {})
        if not hdon:
            return None

    # Trường hợp bắt đầu luôn từ HDon
    elif "HDon" in data_dict:
        hdon = data_dict["HDon"]
    else:
        return None
    
    if "DLHDon" not in hdon:
        return None
        
    dlh = hdon["DLHDon"]
    
    ndhdon = dlh.get("NDHDon", {})
    if not ndhdon:
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

def extract_misa_invoice_info(data_dict):
    """Trích xuất thông tin từ file XML hóa đơn MISA"""
    try:
        # Cấu trúc MISA thường là: Invoice > InvoiceData
        if "Invoice" in data_dict:
            invoice_data = data_dict["Invoice"]
        elif "HDon" in data_dict:
            invoice_data = data_dict["HDon"]
        else:
            return None
            
        # Thông tin chung về hóa đơn
        general_info = invoice_data.get("TTChung", {})
        
        # Thông tin người bán
        seller_info = invoice_data.get("NBan", {})
        
        # Thông tin người mua  
        buyer_info = invoice_data.get("NMua", {})
        
        info = {
            "Số hóa đơn": general_info.get("SHDon") or general_info.get("InvoiceNumber"),
            "Đơn vị bán hàng": seller_info.get("Ten") or seller_info.get("Name"),
            "Mã số thuế bán": seller_info.get("MST") or seller_info.get("TaxCode"),
            "Địa chỉ bán": seller_info.get("DChi") or seller_info.get("Address"),
            "Họ tên người mua hàng": buyer_info.get("Ten") or buyer_info.get("Name"),
            "Địa chỉ mua": buyer_info.get("DChi") or buyer_info.get("Address"),
            "Mã số thuế mua": buyer_info.get("MST") or buyer_info.get("TaxCode"),
        }
        return info
        
    except Exception as e:
        print(f"Lỗi khi trích xuất thông tin MISA: {e}")
        return None

def extract_van_invoice_info(data_dict):
    """Trích xuất thông tin từ file XML hóa đơn VAN"""
    try:
        # Cấu trúc VAN có thể khác, thường bắt đầu từ root khác
        if "Envelope" in data_dict:
            body = data_dict["Envelope"].get("Body", {})
            invoice_data = body.get("Invoice", {}) or body.get("HDon", {})
        elif "Invoice" in data_dict:
            invoice_data = data_dict["Invoice"]
        elif "HDon" in data_dict:
            invoice_data = data_dict["HDon"]
        else:
            return None
            
        # Thông tin chung
        header_info = invoice_data.get("Header", {}) or invoice_data.get("TTChung", {})
        
        # Thông tin người bán
        seller_info = invoice_data.get("Seller", {}) or invoice_data.get("NBan", {})
        
        # Thông tin người mua
        buyer_info = invoice_data.get("Buyer", {}) or invoice_data.get("NMua", {})
        
        info = {
            "Số hóa đơn": header_info.get("InvoiceNo") or header_info.get("SHDon"),
            "Đơn vị bán hàng": seller_info.get("CompanyName") or seller_info.get("Ten"),
            "Mã số thuế bán": seller_info.get("TaxCode") or seller_info.get("MST"),
            "Địa chỉ bán": seller_info.get("Address") or seller_info.get("DChi"),
            "Họ tên người mua hàng": buyer_info.get("CompanyName") or buyer_info.get("Ten"),
            "Địa chỉ mua": buyer_info.get("Address") or buyer_info.get("DChi"),
            "Mã số thuế mua": buyer_info.get("TaxCode") or buyer_info.get("MST"),
        }
        return info
        
    except Exception as e:
        print(f"Lỗi khi trích xuất thông tin VAN: {e}")
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

def process_all_xml_files_by_ma_tra_cuu(folder_path, df_input):
    """Xử lý file XML theo mã tra cứu từ file input để đảm bảo đúng thứ tự"""
    xml_data_list = []
    
    if not os.path.exists(folder_path):
        print(f"Thư mục {folder_path} không tồn tại")
        return [None] * len(df_input)
    
    # Lấy tất cả file XML
    xml_files = [f for f in os.listdir(folder_path) if f.endswith('.xml')]
    
    # Duyệt từng dòng trong file input
    for index, row in df_input.iterrows():
        ma_tra_cuu = str(row['Mã tra cứu']).strip()
        url = str(row['URL']).strip()
        xml_data = None
        
        # Tìm file XML có tên chứa mã tra cứu
        matching_file = None
        for xml_file in xml_files:
            if ma_tra_cuu in xml_file:
                matching_file = xml_file
                break
        
        if matching_file:
            file_path = os.path.join(folder_path, matching_file)
            try:
                data_dict = read_xml_to_dict(file_path)
                
                # Chọn hàm trích xuất dựa vào URL
                if "fpt" in url.lower():
                    xml_data = extract_fpt_invoice_info(data_dict)
                    invoice_type = "FPT"
                elif "meinvoice" in url.lower() or "misa" in url.lower():
                    xml_data = extract_misa_invoice_info(data_dict)
                    invoice_type = "MISA"
                elif "van.ehoadon" in url.lower() or "van" in url.lower():
                    xml_data = extract_van_invoice_info(data_dict)
                    invoice_type = "VAN"
                else:
                    # Thử các hàm theo thứ tự nếu không xác định được từ URL
                    xml_data = extract_fpt_invoice_info(data_dict)
                    if not xml_data:
                        xml_data = extract_misa_invoice_info(data_dict)
                        invoice_type = "MISA"
                    if not xml_data:
                        xml_data = extract_van_invoice_info(data_dict)
                        invoice_type = "VAN"
                    else:
                        invoice_type = "FPT"
                
                if xml_data:
                    print(f"\nDòng {index+1} - File: {matching_file} (Loại: {invoice_type})")
                    print(f"Mã tra cứu: {ma_tra_cuu}")
                    for key, value in xml_data.items():
                        print(f"{key}: {value}")
                    print("-" * 50)
                else:
                    print(f"Dòng {index+1} - Không thể trích xuất dữ liệu từ file: {matching_file}")
            except Exception as e:
                print(f"Lỗi khi xử lý file {matching_file} cho dòng {index+1}: {e}")
        else:
            print(f"Dòng {index+1} - Không tìm thấy file XML cho mã tra cứu: {ma_tra_cuu}")
        
        xml_data_list.append(xml_data)
    
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
    
    #3. đọc tất cả file xml trong thư mục download và trích xuất thông tin theo đúng thứ tự
    xml_data_list = process_all_xml_files_by_ma_tra_cuu(download_path, df)
    
    #4. tạo file output với thông tin đầy đủ
    df_output = create_output_file(df, xml_data_list)
    
    print(f"\nHoàn thành! Đã xử lý {len(xml_data_list)} file XML")

if __name__ == "__main__":
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