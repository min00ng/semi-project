import sqlalchemy.types
from sqlalchemy import create_engine
import pymysql
import pandas as pd
from bs4 import BeautifulSoup
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

class newscrawler:
    def __init__(self,heads):
        self.heads = heads
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def get_article_url(self,url):
        try:
            self.driver.get(url)
            html = self.driver.page_source
            bs = BeautifulSoup(html,"html.parser")
            div = bs.find("div",{"class" : "section_body"})
            li = div.findAll("li")
            url_list = [[] for i in range(len(li))]
            for i in range(len(li)):
                dt = li[i].find("dt",{"class" : "photo"})
                a = dt.find("a")
                url_list[i] = "https://news.naver.com/" + a["href"]
        except Exception as e:
            print(e)
        finally :
            return url_list

    def go_next_page(self):
        pass

    def get_news(self,url_lst):
        ############ 데이터를 담을 리스트 생성 ############
        news_category = []
        press = []
        main_title = []
        news_date = []
        article_content = []

        try:
            for url in url_lst:
                ############### 데이터 프레임 객체 생성 ###############
                news_data_df = pd.DataFrame()
                
                #################### 파싱하기 ####################

                # 접근을 위한 사용자 정보 입력하기 
                res = requests.get(url, headers = self.heads)

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

                ################ 본문 - article_content ####################
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

    def save_news_file(self):
        pass