from NewsAnalyzer.NewsCrawler import newscrawler

# 오늘의 모든 기사 크롤링하는 코드.

heads = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Whale/3.12.129.46 Safari/537.36'}
ns = newscrawler(heads)
df = ns.news_crawler()
file_path = "C:/sh/study/비정형데이터분석프로젝트/data/"
ns.save_news_file(file_path,df)