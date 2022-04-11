from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100"
driver = webdriver.Chrome(ChromeDriverManager().install())

def get_article_url(url):
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
        return url_list

lst = get_article_url(url)

print(lst)
