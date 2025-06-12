from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()   #khởi động 
driver.get("https://www.saucedemo.com") 


# #tim phần tử bằng ID
username = "user-name"
user_box = driver.find_element(By.ID,username)
user_box.send_keys("standard_user")

password = "password"
pass_box = driver.find_element(By.ID,password)
pass_box.send_keys("secret_sauce")

#nhấn submit đăng nhâp   
id_btn = "login-button"
element_btn = driver.find_element(By.ID, id_btn)
element_btn.click()
time.sleep(5)  #đợi trang load xong


#lấy tên sản phẩm
value_title = "inventory_item_name"
element_title = driver.find_elements(By.CLASS_NAME , value_title)

#lấy giá sản phẩm
value_price = '//div[@class="inventory_item_price"]'
element_price = driver.find_elements(By.XPATH , value_price)

print("tên :", len(element_title))
print("giá :", len(element_price))

#gom dữ liệu
data_output = []
for name , price in zip(element_title, element_price):
    data_output.append({
        "title": name.text,
        "price": price.text
    })

#đóng trình duyệt   
# driver.quit()

#lưu vào file excel
df = pd.DataFrame(data_output)
df.to_excel("products.xlsx", index=False)
print("đã lưu vào file products.xlsx")







time.sleep(1000)




