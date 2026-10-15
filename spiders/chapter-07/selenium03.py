# 节点交互
from selenium.webdriver.common.by import By  
from selenium import webdriver
import time

browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
input = browser.find_element(By.ID,'q')
input.send_keys('iPhone')
time.sleep(1)
input.clear()
input.send_keys('iPad')
button = browser.find_element(By.CLASS_NAME,'btn-search')
button.click()