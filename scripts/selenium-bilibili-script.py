"""
loading packages
"""
import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException

"""
initiate a driver
"""
driver = webdriver.Firefox()


"""
define Waits
"""
wait = WebDriverWait(driver, 10)


"""
Go to 'https://www.bilibili.com/', search for keywords, submit, switch window, 
  check total pages, and the results of the first page.
"""
def search():
    try:
        print('开始访问 b 站')
        driver.get('https://www.bilibili.com/')
        input = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".nav-search > form > input")
            ))
        submit = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.nav-search > form > div > button")
            ))
        input.send_keys('蔡徐坤 打球')
        submit.click()
        print('跳转到新窗口')
        all_handles = driver.window_handles
        driver.switch_to.window(all_handles[1])
        save_to_df()
        total = wait.until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "li.page-item.last > button"))
        )
        return int(total.text)
    except TimeoutException:
        return search()   


"""
Go to 'https://www.bilibili.com/', search for keywords, submit, switch window, 
  check total pages, and the results of the first page.
"""
def search():
    try:
        print('开始访问 b 站')
        driver.get('https://www.bilibili.com/')
        input = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".nav-search > form > input")
            ))
        submit = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.nav-search > form > div > button")
            ))
        input.send_keys('蔡徐坤 打球')
        submit.click()
        print('跳转到新窗口')
        all_handles = driver.window_handles
        driver.switch_to.window(all_handles[1])
        save_to_df()
        total = wait.until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, "li.page-item.last > button"))
        )
        return int(total.text)
    except TimeoutException:
        return search()   


"""
iterate over all pages and get the result from each page
"""
def next_page(page_num):
    try:
        print('开始前往第 ' + str(page_num) + " 页")
        next_btn = wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, "li.page-item.next > button"
        )))
        time.sleep(5)
        next_btn.click()
        save_to_df()
        print('第 ' + str(page_num) + ' 页已抓取结束')
        
    except TimeoutException:
        driver.refresh()
        print('第 ' + str(page_num) + ' 页有错误')
        return next_page(page_num)



"""
define the main function. Close the browser after the task is done.
"""
def main():
    try:
        total = search()
        for i in range(2, int(total+1)):
            next_page(i)
    finally:
        driver.close()
        driver.quit()


"""
initiate an empty df
"""
columns = ['title', 'link', 'view', 'uploader', 'upload time']
df = pd.DataFrame(columns = columns)


"""
Run
"""
if __name__ == '__main__':
    main()