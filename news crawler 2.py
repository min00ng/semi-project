from NewsAnalyzer.NewsCrawler import newscrawler

# 14 ~ 8일까지 기사 크롤링 하는 코드

heads = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Whale/3.12.129.46 Safari/537.36'}
ns = newscrawler(heads)
file_path = "C:/sh/study/비정형데이터분석프로젝트/data/"

category_url = ["https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100",
                "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101",
                "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=102",
                "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=103",
                "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=105",
                "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=104"]

all_cg = ["정치","경제","사회","생활/문화","IT/과학","세계"]
cg_num = 0
for url in category_url:
    print(f"{all_cg[cg_num]} 기사 크롤링중...")
    news = ns.category_crawler2(url)
    cg_num += 1
    df = ns.convert2df(news)
    ns.save_news_file_by_category(df=df,file_path=file_path)