from selenium import webdriver
from selenium.webdriver.common.by import By
import time
driver = webdriver.Chrome()   #khởi động 
driver.get("https://www.facebook.com/") 

# #tim phần tử bằng ID và nhập
search_box = driver.find_element(By.ID,"email") 
search_box.send_keys("binhplayll@gmail.com")

search_box = driver.find_element(By.ID,"pass") 
search_box.send_keys("Benhi11@")

#nhấn vào nút đăng nhập
search_button = driver.find_element(By.NAME, "login")
search_button.click()
time.sleep(20) 
driver.quit()
