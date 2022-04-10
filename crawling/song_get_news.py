# get_news 함수 구현하기

########### 가져올 정보 ###########

# - 뉴스 카테고리
# - 언론사
# - 제목
# - 날짜
# - 소제목
# - 본문
# - 기사에 대한 반응
# - 댓글
# - 본문 요약 (요약봇, 없는 기사가 있을수도 있음)
# - 추천수 (이 기사를 추천합니다)

###################################

import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup

driver = webdriver.Chrome(r'C:\Users\scw47\project\chromedriver.exe')

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

            ################ 소제목 - subtitle ################
            # 없는 기사들이 대부분임!!! # 
            # subtitle = bs.fine()

            ################ 날짜 - news_date ###############
            news_date = bs.find('span', {'class', 't11'})
            news_date = news_date.text.split()[0]

            ################ 본문 - news_article ####################
            news_article = bs.find('div', {'id': "articleBodyContents"})
           
            # 문단 별로 나누어 리스트에 저장하는 방식   - 1
            news_article = news_article.text.split('      ')[:]
           
            # 그대로 기사 내용 추출하는 방식    - 2
            news_article = news_article.text

            ################ 기사에 대한 반응 - response_lst ###############

            # 실시간으로 변하는 요소들은 제대로 파싱 불가!!!
            # 댓글수도 마찬가지임. webdriver 사용?

            # 모든 반응 리스트 - response_lst
            response_lst = bs.find('div', {'class': "_reactionModule u_likeit"})
            response_lst = list(i for i in response_lst.text.split('\n')[11:] if i)

            # 좋아요 - good
            good = bs.find('li', {'class', 'u_likeit_list good'})
            good = good.text.strip()

            # 훈훈해요 - warm
            warm = bs.find('li',{'class': 'u_likeit_list warm'})
            warm = warm.text.strip()

            # 슬퍼요 - sad
            sad = bs.find('li', {'class', 'u_likeit_list sad'})
            sad = sad.text.strip()

            # 화나요 - angry
            angry = bs.find('li', {'class', 'u_likeit_list angry'})
            angry = angry.text.strip()

            # 후속기사 원해요 - want
            want = bs.find('li', {'class', 'u_likeit_list want'})
            want = want.text.strip()

            ##################### 댓글수 - comment_num ####################
            # 파싱 제대로 수행 X
            # 해결방법 찾아야 함. 

            comment_num = bs.find('li', {'class': 'u_cbox_count_info'})
            # comment_num = bs.find('li', {'class': 'u_cbox_comment_count u_cbox_comment_count3'}).find('span', {'class': 'u_cbox_info_txt'})
            comment_num = comment_num.text

            ##################### 본문 요약 - news_summary ####################
            # 파싱 제대로 수행 X
            # 해결방법 찾기!!
            news_summary = bs.find('div', {'class': '_contents_body'})
            news_summary = news_summary.text


            ################ 추천수 recommend ####################
            # 파싱 제대로 수행 X
            # 해결방법 찾기!!
            recommend = bs.find('em', {'class': 'u_cnt _count'})
            recommend = recommend.text


    except Exception as e:
        print(e)

    finally:
        idx = ['뉴스 카테고리', '언론사', '기사제목', '날짜', '본문', '기사에 대한 반응',
        '댓글수', '본문 요약', '추천수']      
        news_data = [news_category, press, main_title, news_date, news_article, response_lst, 
        comment_num, news_summary, recommend]

        # 시리즈에 추가 
        for i, n in zip(idx, news_data):
            news_data_ser[i] = n
        
        # 데이터 프레임으로 저장하기 (T = transpose(), 행과 열 위치 바꿔주기)
        news_data = pd.DataFrame(news_data_ser).T 

        