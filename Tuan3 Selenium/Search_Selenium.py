from selenium import webdriver
from selenium.webdriver.common.by import By
import time
driver = webdriver.Chrome()   #khởi động 
driver.get("https://www.google.com/") #mở trang web google


#tim phần tử bằng class name
search_box = driver.find_element(By.CLASS_NAME,"gLFyf")
search_box.send_keys("việt nam mãi đỉnh")


#nhấn search
search_button = driver.find_elements(By.CLASS_NAME, "gNO89b")[1]
search_button.click()

time.sleep(20) 
driver.quit()
