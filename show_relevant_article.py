# 연관 기사와 그에 따른 키워드 추출하기 클래스

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.preprocessing import normalize
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from krwordrank.word import summarize_with_keywords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from kiwipiepy import Kiwi, Match
from kiwipiepy.utils import Stopwords
from konlpy.tag import Okt
from keybert import KeyBERT
import pandas as pd
import re

df = pd.read_csv('./2022-04-18 news data.csv')
df = df[df['카테고리']=='정치']

class showRelevantArticle:
    def __init__(self):
        pass

    def clean_text(self, text):
        text_rmv = re.sub('[-=+,#/\?:^.@*\"※%~∼ㆍ!【】』㈜©囹圄秋 ■◆◇▷▶◁◀ △▲▽▼<>‘|\(\)\[\]`\'…》→←↑↓↔〓♤♠♡♥♧♣⊙◈▣◐◑☆★\”\“\’·※~ ! @ # $ % ^ & * \ " ]', ' ', text)
        text_rmv = ' '.join(text_rmv.split())
        return text_rmv

    def clustering (self, df): #df.본문

        # 특수 기호 삭제하여 새로운 열에 추가
        df['cleaned_본문'] = df.apply(self.clean_text)
        content = df['cleaned_본문'].tolist()

        n_clusters = 10 # 군집 개수
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(content)
        X = normalize(X)
        kmeans = KMeans(n_clusters = n_clusters).fit(X)
        labels = kmeans.labels_
        centers = kmeans.cluster_centers_

        # labels 열 생성
        df['labels'] = labels

        return df.labels

    
    def listToString(str_list): #리스트를 문자열로 반환 (특수문자 제거 후 추출된 명사 입력)
        result = ""
        for s in str_list:
            result += s + " "
        string = result.strip()
        return string

    
    def kwordrank(string): #해당 함수에서 불용어 제거 
        stop_words_list=[]
        stop_words_file = open("korean_stop_words.txt",encoding='utf-8')
        for line in stop_words_file.readlines():
            stop_words_list.append(line.rstrip())
            stop_words_file.close()
        stopwords=stop_words_list
        texts = [string]
        keywords = summarize_with_keywords(texts, min_count=10, max_length=10,beta=0.85, max_iter=10, stopwords=stopwords, verbose=True)
        passwords = {word:score for word, score in sorted(
            keywords.items(), key=lambda x:-x[1])[:300] if not (word in stopwords)}
        return passwords




    def execute_class(self, data):
        self.clustering (self, df)
        # labels 별로 df 출력

        for i in range(len(labels_conut)):
            df_i = df[df.labels==i]
            df_i_title = list(df_i.기사제목)

            title_del = self.listToString(df_i_title)
            k = self.kwordrank(title_del)
                



###########################################################################################





## 키버트 돌리기 

content = df_9[df_9['본문'].str.contains('정호영')]
content = content['본문']
len(content)

def noun_extractor(sentence):
    nouns =[]
    kiwi = Kiwi()
    stopwords = Stopwords()
    result_iter = kiwi.tokenize(sentence, normalize_coda=True,stopwords=stopwords)
    i = 0
    for i in range(len(result_iter)):
        if result_iter[i][1] == 'NNP':
            nouns.append(result_iter[i][0])
    return nouns


# tokenizing = True로 쓰기 (기본값)

from konlpy.tag import Okt
from keybert import KeyBERT

def keyBERT(content):
  kw = KeyBERT()
  article = []

  for i in content:

    # 결과적으로 불용어까지 제거된 토큰화 목록이 필요함
    # 기사별 명사 추출 -> 기사별로 명사를 추출해야 기사별로 CountVectorizer사용해서 단어사전 만들고 키워드 단어 뽑을 수 있음
    # 임의로 okt.nouns 사용
    words = noun_extractor(i)

    # 추출한 명사 리스트에서 빼내기
    tokenized_nouns = ' '.join(word for word in words)

    # keyBERT_mms 모델 적용 
    keywords = kw.extract_keywords(tokenized_nouns, keyphrase_ngram_range=(1, 1), stop_words=None)

    # 리스트에 넣기
    article.append(keywords)

  return article


article_keywords = keyBERT(content)
article_keywords


kw_num = [] # 각각의 기사에서 keyBERT로 몇 개의 키워드가 추출되었는지 리스트에 기사순으로 저장
for i in range(len(article_keywords)):
    k = len(article_keywords[i])
    kw_num.append(k)


# 각각의 기사 키워드에서 고유명사를 뽑기 위해 keyBERT로 뽑은 키워드들을 하나의 리스트 안에 담는 코드
key = [] # 모든 키워드들을 담은 리스트임

for i in range(len(article_keywords)):
    word_len = kw_num[i]
    for j in range(word_len):
        key.append(article_keywords[i][j][0])



# 고유명사 키워드를 빈도순으로 나열하여 상위 5개 키워드 추출
count_dic = {}

for i in key:
    count_dic[i] = key.count(i)
    
top_5_kw = sorted(count_dic,key=lambda x:count_dic[x])[::-1][0:5]
top_5_kw

# 겹치는 단어 있으면 빼야할 것 같은데...
if '정호영' in top_5_kw:
  top_5_kw.remove('정호영')
  print(top_5_kw)


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


 



# 실행
show_relevant_keyword('정호영', df)