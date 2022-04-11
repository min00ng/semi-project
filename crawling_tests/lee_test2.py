from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100"
driver = webdriver.Chrome(ChromeDriverManager().install())

heads = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Whale/3.12.129.46 Safari/537.36'}


try:
    driver.get(url)
    html = driver.page_source
    bs = BeautifulSoup(html,"html.parser")
    div = bs.find("div",{"class" : "section_body"})
    li = div.findAll("li")
    url_list = [[] for i in range(len(li))]
    for i in range(len(li)):
        dt = li[i].find("dt",{"class" : "photo"})
        a = dt.find("a")
        url_list[i] = a["href"]
except Exception as e:
    print(e)

finally :
    print(url_list)