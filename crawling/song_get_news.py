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
            
            # selenium 활용
            driver.get(url) 

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
            # 없는 기사들이 대부분임!
            # subtitle 

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

            # 실시간으로 변하는 요소들은 bs4로 파싱 불가
            # 우선 selenium으로 해결함 ----> 속도가 느리다는 한계

            # 모든 반응 리스트 - response_lst
            response_lst = driver.find_element_by_xpath('//*[@id="spiLayer"]/div[1]').text

            # 좋아요 - good
            good = response_lst.split()[1]

            # 훈훈해요 - warm
            warm = response_lst.split()[3]

            # 슬퍼요 - sad
            sad = response_lst.split()[5]

            # 화나요 - angry
            angry = response_lst.split()[7]

            # 후속기사 원해요 - want
            want = response_lst.split()[10]

            ##################### 댓글수 - comment_num ####################
            # bs로는 파싱 제대로 수행 X
            # selenium으로 해결
            comment_num = driver.find_element_by_xpath('//*[@id="cbox_module"]/div[2]/div[2]/ul/li[1]/span').text

            ##################### 본문 요약 - news_summary ####################
            # 파싱 제대로 수행 X
            # 해결방법 찾기!! ---> 요약봇의 요약문은 스크랩이 안 되는 듯함. 차라리 요약문을 우리가 생성해보아도 좋을 듯함!
            news_summary = bs.find('div', {'class': '_contents_body'}).text

            ################ 추천수 recommend ####################
            # bs로 파싱 제대로 수행 X
            # selenium으로 해결
            recommend = driver.find_element_by_xpath('//*[@id="toMainContainer"]/a/em[2]').text

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
        
        # 데이터 프레임으로 저장하기 (T = transpose(), 행과 열 위치 바꿔주기, idx가 열이 되게끔)
        news_data = pd.DataFrame(news_data_ser).T 

        