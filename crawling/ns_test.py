import NewsCrawler

heads = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Whale/3.12.129.46 Safari/537.36'}

# 클래스 선언
ns = NewsCrawler.newscrawler(heads)

url = "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101"

news = ns.category_crawler(url)