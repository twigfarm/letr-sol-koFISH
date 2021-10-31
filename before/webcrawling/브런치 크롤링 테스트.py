from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# chrome driver
driver = webdriver.Chrome(r"C:\Users\mode\Desktop\just\chromedriver_win32\chromedriver.exe")
# 암묵적으로 웹 자원 로드를 위해 3초까지 기다려준다.
#driver.implicitly_wait(3)

user = input()

# url 접근
url = "https://brunch.co.kr/"
driver.get(url)


time.sleep(2)

hidden_submenu = driver.find_element_by_css_selector('#btnServiceMenuSearch')

actions = webdriver.ActionChains(driver)
actions.click(hidden_submenu)

actions.perform()

time.sleep(2)

user_search = driver.find_element_by_id("txt_search")

user_search.clear()
user_search.send_keys(user)

user_search.send_keys(Keys.RETURN)

time.sleep(2)

hidden_submenu1 = driver.find_element_by_css_selector('#resultArticle li:nth-child(1)') # 반복문 돌려야 할곳

actions = webdriver.ActionChains(driver)
actions.click(hidden_submenu1)

actions.perform()

#driver.get()
brunchs = driver.find_elements_by_tag_name("h4")

for brunch in brunchs:
    print(brunch.text)
