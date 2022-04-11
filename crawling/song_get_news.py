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
    try:
        for url in url_lst:
            ############### 시리즈 객체 생성 ###############
            news_data_ser = pd.Series()
            
            #################### 파싱하기 ####################

            # 접근을 위한 사용자 정보 입력하기 
            headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
            res = requests.get(url, headers = headers)

            # 파싱 시작
            bs = BeautifulSoup(res.text,'html.parser')

            ################ 뉴스 카테고리 - news_category ###############
            news_category = bs.find('div', {'class': 'article_list'})
            news_category = news_category.text.strip()[:2]

            ################ 언론사 - press ################
            press = bs.find('div', {'class': 'section'})
            press = press.h4.text.split()[0]

            ################ 기사 제목 - main_title ################
            main_title = bs.find('div', {'class': 'article_info'})
            main_title = main_title.h3.text
            
            ################ 날짜 - news_date ###############
            news_date = bs.find('span', {'class', 't11'})
            news_date = news_date.text.split()[0]

            ################ 본문 - news_article ####################
            news_article = bs.find('div', {'id': "articleBodyContents"})
           
            # 문단 별로 나누어 리스트에 저장하는 방식   - 1
            news_article = news_article.text.split('      ')[:]
           
            # 그대로 기사 내용 추출하는 방식    - 2
            news_article = news_article.text

           
    except Exception as e:
        print(e)

    finally:
        idx = ['뉴스 카테고리', '언론사', '기사제목', '날짜', '본문']      
        news_data = [news_category, press, main_title, news_date, news_article]

        # 시리즈에 추가 
        for i, n in zip(idx, news_data):
            news_data_ser[i] = n
        
        # 데이터 프레임으로 저장하기 (T = transpose(), 행과 열 위치 바꿔주기, idx가 열이 되게끔)
        news_data = pd.DataFrame(news_data_ser).T 

    ########### get_news 함수의 값으로 기사 정보를 담은 데이터 프레임 반환하기 ##########
    return news_data

        