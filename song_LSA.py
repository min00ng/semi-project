# LSA 관련 구상 (구상단계임)



######################### 사용 데이터 #######################

import pandas as pd
from konlpy.tag import Okt
import re
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np


###### 필요한 함수 두 개 정의 ######

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

####################################

# 데이터 불러오기 (0412 뉴스데이터)
data = pd.read_csv('data/2022-04-12 news data, test.csv')

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


########## 전처리 관련 시도 ##########
okt = Okt()

tokenized_title = okt.pos(title[1045])
tokenized_nouns = ' '.join([word[0] for word in tokenized_title if word[1] == 'Noun'])

print('품사 태깅 10개만 출력 :',tokenized_title[:10])
print('명사 추출 :',tokenized_nouns)

#####################################

############################################################


################## 키워드 추출 함수 만들기 ##################

# LSA를 활용하여 사용자가 키워드를 입력했을 때, 관련 있는 상위 5개의 단어를 제시해주는 함수
# 상위 5개 단어와 관련된 헤드라인의 뉴스를 제공해주면 좋을 것 같음

# 둘 중 하나 사용하면 됨. Tfidf 사용

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer



def show_relevant_keyword(word, df): # 키워드, 사용할 뉴스 데이터를 인자로 입력받음
    cv = TfidfVectorizer(stop_words = 지정해줘야 함, max_features = 1000)
    x = cv.fit_transform(df.기사제목)
    words = cv.get_feature_names()




