from selenium import webdriver
from selenium.webdriver.common.by import By  

browser = webdriver.Edge()
browser.get('https://www.taobao.com')
input_first = browser.find_element(By.ID,'q')
input_second = browser.find_element(By.CSS_SELECTOR,'#q')
input_third = browser.find_element(By.XPATH,'//*[@id="q"]')
print(input_first, input_second, input_third)
browser.close()

## 多节点选取
browser = webdriver.Edge()
browser.get('https://www.taobao.com')
lis = browser.find_elements(By.CSS_SELECTOR,'.first-cate-container--cgcXGejE')
print(lis)
browser.close()
