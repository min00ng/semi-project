import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup

driver = webdriver.Chrome(ChromeDriverManager().install())
url='https://news.naver.com/'
def select_category():
    try :
        driver.get(url)
        driver.find_element_by_xpath('/html/body/section/header/div[2]/div/div/div[1]/div/div/ul/li[2]/a').click()
        time.sleep(0.5)
        url1='https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101'
        driver.get(url1)
        time.sleep(0.5)
        url2='https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=102'
        driver.get(url2)
        time.sleep(0.5)
        url3='https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=103'
        driver.get(url3)
        time.sleep(0.5)
        url4='https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=105'
        driver.get(url4)
        time.sleep(0.5)
        url5='https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=104'
        driver.get(url5)
        time.sleep(0.5)
        
    except Exception as e :
        print(e)
    
    finally :
        print('\n')
        print('complete')