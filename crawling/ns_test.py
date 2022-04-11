import newscrawler
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

# 드라이버 설정
driver = webdriver.Chrome(ChromeDriverManager().install())
heads = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Whale/3.12.129.46 Safari/537.36'}

# url
url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100"

# 클래스 선언
ns = newscrawler.newscrawler(driver,heads)

lst = ns.get_article_url(url)
df = ns.get_news(lst)

print(lst)
print(df)

