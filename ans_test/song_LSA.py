# LSA 함수

######################### 사용 모듈 #######################

import pandas as pd
from konlpy.tag import Okt
import re
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


# 데이터 불러오기 (0412 뉴스데이터)
data = pd.read_csv('data/2022-04-14 ~ 2022-04-08 Politics news data.csv')

# 결측치 제거
data = data.dropna()

############################################################



################## 연관 키워드 추출 함수 만들기 ##################

# LSA를 활용하여 사용자가 키워드를 입력했을 때, 관련 있는 상위 10개의 단어를 제시해주는 함수
# 상위 10개 단어와 관련된 헤드라인의 뉴스를 제공해주면 좋을 것 같음



############## 함수 1번 : 기사 제목에서 추출하기 ###############

def show_relevant_keyword_from_title(keyword, df): # 키워드와 사용할 뉴스 데이터를 인자로 입력받음
    
    # stop_words를 전에 했던 것처럼 txt 파일 형태로 제공하면 에러 발생! 
    # 제목이 대상일 때 max_features는 5000에서 가장 이상적인 결과를 보임
    tv = TfidfVectorizer(stop_words = 'english', max_features = 5000)
    x = tv.fit_transform(df.기사제목)

    # words에는 feature가 된 단어들이 5000개 담겨 있음. 
    words = tv.get_feature_names() 

    # 불용어 리스트 불러오기
    stopwords = pd.read_csv('./korean_stop_words.txt', encoding = 'utf8')['아']

    ############## SVD 특이값 분해 ################
    from sklearn.decomposition import TruncatedSVD

    # n_components 는 max_features보다 적어야 함. 
    # 임의로 300개로 설정하였음
    svd = TruncatedSVD(n_components = 300, random_state = 1234)
    word_idx = words.index(keyword) # 사용자에게 입력받은 키워드의 인덱스 위치 확인
    svd.fit(x)

    kw_idx = svd.components_[:, word_idx].argmax()

    relevant_words_df = pd.DataFrame({'단어': words, 'loading': svd.components_[kw_idx]})
    
    ########### 상위 10가지 키워드 보여주기 ##########
    
    # 불용어 처리
    rel_words_df = relevant_words_df[relevant_words_df['단어'] != keyword]
    drop_index = []
    for i in rel_words_df['단어']:
        if i in list(stopwords):
            idx = rel_words_df[rel_words_df['단어'] == i].index[0]
            drop_index.append(idx)
    rel_words_df.drop(drop_index, inplace = True)
    
    # 상위 10개의 단어 추출
    rel_words_df = rel_words_df.sort_values('loading').tail(10)
    rel_words_df = rel_words_df.sort_values('loading', ascending = False)


    # 사용자가 입력한 키워드와 관련있는 상위 10개 단어를 데이터 프레임으로 반환
    return rel_words_df
    





############## 함수 2번 : 기사 본문에서 추출하기 ###############

def show_relevant_keyword_from_article(keyword, df): # 키워드와 사용할 뉴스 데이터를 인자로 입력받음
    
    # stop_words를 전에 했던 것처럼 txt 파일 형태로 제공하면 에러 발생!
    # 일단 에러를 막기 위해 'english'로 설정하였음. 
    # max_features는 3000개에서 이상적인 결과를 보임
    tv = TfidfVectorizer(stop_words = 'english', max_features = 3000)
    x = tv.fit_transform(df.본문)

    # words에는 feature가 된 단어들이 3000개 담겨 있음. 
    words = tv.get_feature_names() 

    # 불용어 리스트 불러오기
    stopwords = pd.read_csv('./korean_stop_words.txt', encoding = 'utf8')['아']

    ############## SVD 특이값 분해 ################
    from sklearn.decomposition import TruncatedSVD

    # n_components 는 max_features보다 적어야 함. 
    # 임의로 300개로 설정하였음
    svd = TruncatedSVD(n_components = 300, random_state = 1234)
    word_idx = words.index(keyword) # 사용자에게 입력받은 키워드의 인덱스 위치 확인
    svd.fit(x)

    kw_idx = svd.components_[:, word_idx].argmax()

    relevant_words_df = pd.DataFrame({'단어': words, 'loading': svd.components_[kw_idx]})
    
    ########### 상위 10가지 키워드 보여주기 ##########
    
    # 불용어 처리
    rel_words_df = relevant_words_df[relevant_words_df['단어'] != keyword]
    drop_index = []
    for i in rel_words_df['단어']:
        if i in list(stopwords):
            idx = rel_words_df[rel_words_df['단어'] == i].index[0]
            drop_index.append(idx)
    rel_words_df.drop(drop_index, inplace = True)
    
    # 상위 10개의 단어 추출
    rel_words_df = rel_words_df.sort_values('loading').tail(10)
    rel_words_df = rel_words_df.sort_values('loading', ascending = False)


    # 사용자가 입력한 키워드와 관련있는 상위 10개 단어를 데이터 프레임으로 반환
    return rel_words_df
    




################## 함수 3번 : 기사 제목 + 본문 #################

def show_relevant_keyword(keyword, df): # 키워드와 사용할 뉴스 데이터를 인자로 입력받음
    
    # max_features는 5000개로 설정함
    tv = TfidfVectorizer(max_features = 5000)
    data = df.기사제목 + df.본문
    x = tv.fit_transform(data)

    # words에는 feature가 된 단어들이 5000개 담겨 있음. 
    words = tv.get_feature_names() 

    # 불용어 리스트 불러오기
    stopwords = pd.read_csv('./korean_stop_words.txt', encoding = 'utf8')['아']

    ############## SVD 특이값 분해 ################
    from sklearn.decomposition import TruncatedSVD

    # n_components 는 max_features보다 적어야 함. 
    # 임의로 300개로 설정하였음
    svd = TruncatedSVD(n_components = 300, random_state = 1234)
    word_idx = words.index(keyword) # 사용자에게 입력받은 키워드의 인덱스 위치 확인
    svd.fit(x)

    kw_idx = svd.components_[:, word_idx].argmax()

    relevant_words_df = pd.DataFrame({'단어': words, 'loading': svd.components_[kw_idx]})
    
    ########### 상위 10가지 키워드 보여주기 ##########
    
    # 불용어 처리
    rel_words_df = relevant_words_df[relevant_words_df['단어'] != keyword]
    drop_index = []
    for i in rel_words_df['단어']:
        if i in list(stopwords):
            idx = rel_words_df[rel_words_df['단어'] == i].index[0]
            drop_index.append(idx)
    rel_words_df.drop(drop_index, inplace = True)
    
    # 상위 10개의 단어 추출
    rel_words_df = rel_words_df.sort_values('loading').tail(10)
    rel_words_df = rel_words_df.sort_values('loading', ascending = False)


    # 사용자가 입력한 키워드와 관련있는 상위 10개 단어를 데이터 프레임으로 반환
    return rel_words_df

