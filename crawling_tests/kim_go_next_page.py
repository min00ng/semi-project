import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

url='https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100'
browser=webdriver.Chrome(ChromeDriverManager().install())
browser.get(url)
page_bar=browser.find_element_by_xpath('//*[@id="paging"]/a[1]')

pages=page_bar.find_element_by_xpath

for page in pages:
    page_num=page.text.strip()

def go_next_pages():
    if page_num in ['맨앞','이전','맨뒤']:
        pass
    elif page_num =='다음':
        page.send_keys('\n')

        return False
    elif int(page_num)>int(page_now):
        page.send_keys('\n')
        return False
