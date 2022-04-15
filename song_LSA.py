# LSA 관련 구상 (구상단계임)



######################### 사용 데이터 #######################

import pandas as pd
from konlpy.tag import Okt
import re
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np



###### 필요한 함수 정의 ######

def stemmer(text):
    text = re.sub("[^가-힣ㄱ-ㅎㅏ-ㅣ\\s]","",text)
    okt = Okt()
    text = okt.morphs(text, stem= True)
    return text

def remove_stop_words(text):
    word_token = stemmer(text)
    stop_words = pd.read_csv("./korean_stop_words.txt")
    result = [word for word in word_token if not word in stop_words]
    return result

def create_dic(texts, num):
    tk = tf.keras.preprocessing.text.Tokenizer(num_words = num, oov_token = '알 수 없음')
    
    # 빈도순으로 순위 인덱스 매긴 단어 목록 생성
    tk.fit_on_texts(texts)
    word_dic = tk.word_index
    
    return word_dic



# 데이터 불러오기 (0412 뉴스데이터)
data = pd.read_csv('./2022-04-12 news data, test.csv')

# 714번째 결측치 제거
df = data.drop([714], axis = 0)
df = df.reset_index()

title = df['기사제목']

clean_title = []
for i in range(len(title)):
    clean_title.append(remove_stop_words(title[i]))

# 이중 리스트 1차원으로 변환
clean_title = sum(clean_title, [])

# 단어사전 만들기
title_dic = create_dic(clean_title, 1000)



############################################################



################## 키워드 추출 함수 만들기 ##################

# LSA를 활용하여 사용자가 키워드를 입력했을 때, 관련 있는 상위 5개의 단어를 제시해주는 함수
# 상위 5개 단어와 관련된 헤드라인의 뉴스를 제공해주면 좋을 것 같음



############## 함수 1번 : 기사 제목에서 추출하기 ###############

from sklearn.feature_extraction.text import TfidfVectorizer

def show_relevant_keyword_from_title(keyword, df): # 키워드와 사용할 뉴스 데이터를 인자로 입력받음
    
    # stop_words를 전에 했던 것처럼 txt 파일 형태로 제공하면 에러 발생! 
    # 제목이 대상일 때 max_features는 5000에서 가장 이상적인 결과를 보임
    tv = TfidfVectorizer(stop_words = 'english', max_features = 5000)
    x = tv.fit_transform(df.기사제목)
    # words에는 feature가 된 단어들이 2000개 담겨 있음. 
    words = tv.get_feature_names() 

    ############## SVD 특이값 분해 ################
    from sklearn.decomposition import TruncatedSVD

    # n_components 는 max_features보다 적어야 함. 
    # 임의로 300개로 설정하였음
    svd = TruncatedSVD(n_components = 300, random_state = 1234)
    word_idx = words.index(keyword) # 사용자에게 입력받은 키워드의 인덱스 위치 확인
    svd.components_[: word_idx]

    # 시각화 
    # import matplotlib.pyplot as plt
    # plt.plot(svd.components_[:, word_idx])

    kw_idx = svd.components_[:, word_idx].argmax()

    relevant_words_df = pd.DataFrame({'단어': words, 'loading': svd.components_[kw_idx]})
    rel_words_df = relevant_words_df.sort_values('loading').tail()
    rel_words_df = rel_words_df.sort_values('loading', ascending = False)

    # 사용자가 입력한 키워드와 관련있는 상위 5개 단어를 데이터 프레임으로 반환
    return rel_words_df
    




############## 함수 2번 : 기사 본문에서 추출하기 ###############

def show_relevant_keyword_from_article(keyword, df): # 키워드와 사용할 뉴스 데이터를 인자로 입력받음
    
    # stop_words를 전에 했던 것처럼 txt 파일 형태로 제공하면 에러 발생!
    # 일단 에러를 막기 위해 'english'로 설정하였음. 
    # max_features는 3000개에서 이상적인 결과를 보임
    tv = TfidfVectorizer(stop_words = 'english', max_features = 3000)
    x = tv.fit_transform(df.본문)
    # words에는 feature가 된 단어들이 2000개 담겨 있음. 
    words = tv.get_feature_names() 

    ############## SVD 특이값 분해 ################
    from sklearn.decomposition import TruncatedSVD

    # n_components 는 max_features보다 적어야 함. 
    # 임의로 300개로 설정하였음
    svd = TruncatedSVD(n_components = 300, random_state = 1234)
    word_idx = words.index(keyword) # 사용자에게 입력받은 키워드의 인덱스 위치 확인
    svd.fit(x)

    # 시각화 
    # import matplotlib.pyplot as plt
    # plt.plot(svd.components_[:, word_idx])

    kw_idx = svd.components_[:, word_idx].argmax()

    relevant_words_df = pd.DataFrame({'단어': words, 'loading': svd.components_[kw_idx]})
    rel_words_df = relevant_words_df.sort_values('loading').tail()
    rel_words_df = rel_words_df.sort_values('loading', ascending = False)

    # 사용자가 입력한 키워드와 관련있는 상위 5개 단어를 데이터 프레임으로 반환
    return rel_words_df
    

################## 함수 3번 : 기사 제목 + 본문 #################

def show_relevant_keyword(keyword, df): # 키워드와 사용할 뉴스 데이터를 인자로 입력받음
    
    # stop_words를 전에 했던 것처럼 txt 파일 형태로 제공하면 에러 발생!
    # 일단 에러를 막기 위해 'english'로 설정하였음. 
    # max_features는 8000개로 설정함
    tv = TfidfVectorizer(stop_words = 'english', max_features = 8000)
    data = df.기사제목 + df.본문
    x = tv.fit_transform(data)
    # words에는 feature가 된 단어들이 2000개 담겨 있음. 
    words = tv.get_feature_names() 

    ############## SVD 특이값 분해 ################
    from sklearn.decomposition import TruncatedSVD

    # n_components 는 max_features보다 적어야 함. 
    # 임의로 300개로 설정하였음
    svd = TruncatedSVD(n_components = 300, random_state = 1234)
    word_idx = words.index(keyword) # 사용자에게 입력받은 키워드의 인덱스 위치 확인
    svd.fit(x)

    # 시각화 
    # import matplotlib.pyplot as plt
    # plt.plot(svd.components_[:, word_idx])

    kw_idx = svd.components_[:, word_idx].argmax()

    relevant_words_df = pd.DataFrame({'단어': words, 'loading': svd.components_[kw_idx]})
    rel_words_df = relevant_words_df.sort_values('loading').tail()
    rel_words_df = rel_words_df.sort_values('loading', ascending = False)

    # 사용자가 입력한 키워드와 관련있는 상위 5개 단어를 데이터 프레임으로 반환
    return rel_words_df