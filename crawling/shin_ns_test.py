from unicodedata import category
import newscrawler
import pandas as pd
import datetime

heads = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Whale/3.12.129.46 Safari/537.36'}

# 클래스 선언
ns = newscrawler.newscrawler(heads)

category_url = ["https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100",
                "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101",
                "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=102",
                "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=103",
                "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=105",
                "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=104"]

all_news = []
for url in category_url:
    while True:
        lst = ns.get_article_url(url) # 모든 url lst에 담기
        for a_url in lst:
            all_news.append(ns.get_news(a_url))
        url = ns.go_next_page(url) # 다음 페이지 넘어가기
        # 결과적으로 리스트에 모든 뉴스 정보 담기(카테고리 구분 없이)
        # 리스트에 일렬로 담기게 됨

        for i in range(3, len(all_news), 5): # 날짜 인덱스를 계속 반복해야함
            if all_news[i] != datetime.date.today():
                break

df = pd.DataFrame(all_news)
print(df)