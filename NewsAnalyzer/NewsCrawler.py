import pandas as pd
from bs4 import BeautifulSoup
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import datetime

class newscrawler:
    def __init__(self,heads):
        self.heads = heads
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def news_crawler(self):
        category_url = ["https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=100",
                        "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=101",
                        "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=102",
                        "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=103",
                        "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=105",
                        "https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=104"]
        all_news = []
        all_cg = ["정치","경제","사회","생활/문화","IT/과학","세계"]
        cg_num = 0
        for url in category_url:
            print(f"{all_cg[cg_num]} 기사 크롤링중...")
            all_news += self.category_crawler(url)
            cg_num += 1
        df = self.convert2df(all_news)
        return df

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

    def go_next_page(self,url,page_num):
        if page_num == 2:
            url2 = url + "#&date=%2000:00:00&page=2"
        elif page_num < 11 and page_num > 2:
            url2 = url[:-1] + str(page_num)
        elif page_num < 101 and page_num > 10:
            url2 = url[:-2] + str(page_num)
        elif page_num <1001 and page_num > 100:
            url2 = url[:-3] + str(page_num)
        return url2

    def get_news(self, url):

        ############ 데이터를 담을 리스트 생성 ############
        # news_category = []
        # press = []
        # main_title = []
        # news_date = []
        # article_content = []

        try:     
            ############### 데이터 프레임 객체 생성 ###############
            # news_data_df = pd.DataFrame()
            
            #################### 파싱하기 ####################

            # 접근을 위한 사용자 정보 입력하기 
            # headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'}
            res = requests.get(url, headers = self.heads)

            # 파싱 시작
            bs = BeautifulSoup(res.text,'html.parser')

            ################ 카테고리 - category ###############
            category = bs.find('div', {'class': 'article_list'})  
            category = category.text.strip()[:2]

            # news_category.append(category)

            ################ 언론사 - press ################
            press = bs.find('div', {'class': 'section'})
            press = press.h4.text.split()[0]

            # press.append(press_data)

            ################ 기사제목 - title ################
            title = bs.find('div', {'class': 'article_info'})
            title = title.h3.text

            # main_title.append(title)

            ################ 날짜 - date ###############
            date = bs.find('span', {'class', 't11'})
            date = date.text.split()[0]

            # news_date.append(n_date)

            ################ 본문 - article_content ####################
            article_content = bs.find('div', {'id': "articleBodyContents"})
            
            # 문단 별로 나누어 리스트에 저장하는 방식   - 1
            # news_article = news_article.text.split('      ')[:]
            
            # 그대로 기사 내용 추출하는 방식    - 2
            article_content = article_content.text

            # article_content.append(news_article)

            
        except Exception as e:
            print(e)
            category = None
            press = None
            title = None
            date = str(datetime.date.today()).replace("-",".") + "."
            article_content = None

        finally:

            ##################### 리스트 만들기 ####################
            # idx = ['카테고리', '언론사', '기사제목', '날짜', '본문']
            news_data = [category, press, title, date, article_content]
            
            #for i, n in zip(idx, news_data):
                #news_data_df[i] = n

            ########## get_news 함수의 값으로 기사 정보를 담은 리스트 반환하기 #########
            return news_data

    def save_news_file(self,file_path,df):#데이터프레임 형식 데이터 입력
        today = str(datetime.date.today())
        outputFileName = today + ' news data.csv'
        df.to_csv(file_path+outputFileName)
        return 

    def category_crawler(self,url):
        all_news = []
        again = True
        page_num = 1
        while again:
            print(f"{page_num} 페이지 크롤링 중...")
            lst = self.get_article_url(url)
            for a_url in lst:
                news = self.get_news(a_url)
                news_date = news[3].replace(".","-")[:-1]
                if news_date != str(datetime.date.today()):
                    again = False
                    break
                else:
                    all_news.append(news)
            page_num += 1
            url = self.go_next_page(url,page_num)
        return all_news[20:]  # 1페이지를 2번 크롤링하는 버그가 발생했는데 도저히 잡을 방법이 없어서 앞에 20개 날림.
                              # 원인을 모르겠음. 디버깅하면 제대로 동작하는데 디버깅없이하면 버그가발생함.

    def convert2df(self,lst):
        df = pd.DataFrame(lst,columns=['카테고리', '언론사', '기사제목', '날짜', '본문'])
        return df

    def category_crawler2(self,url):
        all_news = []
        again = True
        page_num = 1
        while again:
            print(f"{page_num} 페이지 크롤링 중...")
            lst = self.get_article_url(url)
            for a_url in lst:
                news = self.get_news(a_url)
                news_date = news[3].replace(".","-")[:-1]
                if news_date == "2022-04-07":
                    again = False
                    break
                else:
                    all_news.append(news)
            page_num += 1
            url = self.go_next_page(url,page_num)
        return all_news[20:]

    def save_news_file_by_category(self,file_path,df):#데이터프레임 형식 데이터 입력
        today = "2022-04-14 ~ 2022-04-08 "
        cg = df["카테고리"].iloc[0]
        if cg == "정치":
            cg2 = "Politics"
        elif cg == "경제":
            cg2 = "Economy"
        elif cg == "사회":
            cg2 = "Society"
        elif cg == "생활":
            cg2 = "Life"
        elif cg == "IT":
            cg2 = "IT"
        else:
            cg2 = "World"
        outputFileName = today + cg2 +' news data.csv'
        df.to_csv(file_path+outputFileName)
        return 