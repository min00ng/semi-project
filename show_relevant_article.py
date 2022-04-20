# show_relevant_article 함수

############### 필요 모듈 ################

from krwordrank.word import summarize_with_keywords
import re
from kiwipiepy import Kiwi, Match
from kiwipiepy.utils import Stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import normalize
from sklearn.cluster import KMeans
import numpy as np



############## 필요 함수 정의 ################

def clean_text(title):
    text_rmv = re.sub('[-=+,#/\?:^.@*\"※%~∼ㆍ!【】』㈜©囹圄秋 ■◆◇▷▶◁◀ △▲▽▼<>‘|\(\)\[\]`\'…》→←↑↓↔〓♤♠♡♥♧♣⊙◈▣◐◑☆★\”\“\’·※~ ! @ # $ % ^ & * \ " ]', ' ', title)
    text_rmv = ' '.join(text_rmv.split())
    return text_rmv # 문자열

def noun_extractor(sentence):
    nouns =[]
    kiwi = Kiwi()
    stopwords = Stopwords()
    result_iter = kiwi.tokenize(sentence, normalize_coda=True,stopwords=stopwords)
    i = 0
    for i in range(len(result_iter)):
        if result_iter[i][1] == 'NNP':
            nouns.append(result_iter[i][0])
    return nouns # 리스트로 반환

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
    keywords = summarize_with_keywords(texts, min_count=2, max_length=10,beta=0.85, max_iter=10, stopwords=stopwords, verbose=True)
    passwords = {word:score for word, score in sorted(
        keywords.items(), key=lambda x:-x[1])[:300] if not (word in stopwords)}
    return passwords


############# show_relevant_article 함수 정의 ##############

def show_relevant_article(category, df):     # 사용자에게 카테고리와 데이터를 인자로 입력받음
    df = df[df['카테고리']==category].reset_index()

    # 기사 본문 클러스터링
    text = list(df.기사제목) # 본문보다 효과가 좋은 것 같음. 본문으로 돌리려면 df.본문이라고 수정하면 됨

    lst = []
    for i in range(len(text)):
        text[i] = clean_text(text[i])
        lst.append(text[i])
    
    df['cleaned_제목'] = lst

    content = df['cleaned_제목'].tolist()
    n_clusters = 30 # 군집화할 갯수
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(content)
    X = normalize(X)
    kmeans = KMeans(n_clusters=n_clusters).fit(X)
    labels = kmeans.labels_
    centers = kmeans.cluster_centers_
    df['labels'] = labels
    data = df.labels # 숫자 라벨 생성
    labels_count = data.value_counts()
    
    # kwrodrank로 라벨 키워드 뽑기 
    top_word_30 = []
    for i in range(len(labels_count)):
        df_i = df[df.labels==i]

        df_i_content = list(df_i.cleaned_본문)
        df_content_del = listToString(df_i_content)

        k = kwordrank(df_content_del)
        k_1 = next(iter(k))
        top_word_30.append(k_1)

    # 숫자 라벨과 kwordrank로 추출한 키워드를 replace
    for i in range(len(labels_count)):
        for j in range(len(data)):
            if i == data[j]:
                data[j] = top_word_30[i]

    df = df.drop('cleaned_제목', axis = 1)
    df = df.drop('index', axis = 1)
    df = df.drop('Unnamed: 0', axis = 1)

    return df
