from selenium import webdriver  
from selenium.webdriver.common.by import By  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.support.ui import WebDriverWait  

# 创建 Edge 的 WebDriver 实例  
browser = webdriver.Edge()  
'''
这里如果直接在百度搜索框中搜索‘python’并使用其顶端的url，就无法得到网页
源代码。具体详情见test_selenium.py里面的程序运行的结果。
'''

try:  
    # 打开百度  
    browser.get('https://www.baidu.com')  
    
    # 找到搜索框并输入关键词  
    input_element = browser.find_element(By.ID, 'kw')  # 使用 By.ID  
    input_element.send_keys('Python')  
    input_element.send_keys(Keys.ENTER)  
    
    # 等待搜索结果加载  
    wait = WebDriverWait(browser, 10)  
    wait.until(EC.presence_of_all_elements_located((By.ID, 'content_left')))  
    
    # 打印当前 URL、Cookies 和页面源代码  
    print(browser.current_url)  
    # print(browser.get_cookies())  
    # print(browser.page_source)  

finally:  
    # 关闭浏览器  
    browser.close()