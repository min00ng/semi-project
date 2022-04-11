# get_news 함수 구현하기

########### 가져올 정보 ###########

# - 뉴스 카테고리
# - 언론사
# - 제목
# - 날짜
# - 본문

###################################


import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_news(url_lst):

    ############ 데이터를 담을 리스트 생성 ############
    news_category = []
    press = []
    main_title = []
    news_date = []
    article_content = []

    try:
        for url in url_lst:          
            #################### 파싱하기 ####################

            # 접근을 위한 사용자 정보 입력하기 
            headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
            res = requests.get(url, headers = headers)

            # 파싱 시작
            bs = BeautifulSoup(res.text,'html.parser')

            ################ 뉴스 카테고리 - news_category ###############
            category = bs.find('div', {'class': 'article_list'})
            category = category.text.strip()[:2]

            news_category.append(category)

            ################ 언론사 - press ################
            press_data = bs.find('div', {'class': 'section'})
            press_data = press_data.h4.text.split()[0]

            press.append(press_data)

            ################ 기사 제목 - main_title ################
            title = bs.find('div', {'class': 'article_info'})
            title = title.h3.text

            main_title.append(title)

            ################ 날짜 - news_date ###############
            n_date = bs.find('span', {'class', 't11'})
            n_date = n_date.text.split()[0]

            news_date.append(n_date)

            ################ 본문 - news_article ####################
            news_article = bs.find('div', {'id': "articleBodyContents"})
           
            # 문단 별로 나누어 리스트에 저장하는 방식   - 1
            # news_article = news_article.text.split('      ')[:]
           
            # 그대로 기사 내용 추출하는 방식    - 2
            news_article = news_article.text

            article_content.append(news_article)

           
    except Exception as e:
        print(e)

    finally:
        ##################### 데이터 프레임 만들기 ####################
        idx = ['뉴스 카테고리', '언론사', '기사제목', '날짜', '본문']  
        news_data = [news_category, press, main_title, news_date, article_content]
        
        for i, n in zip(idx, news_data):
            news_data_df[i] = n

    ########### get_news 함수의 값으로 기사 정보를 담은 데이터 프레임 반환하기 ##########
    return news_data_df

        