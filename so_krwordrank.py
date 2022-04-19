from krwordrank.word import summarize_with_keywords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import datetime



def listToString(str_list): #리스트를 문자열로 반환 (특수문자 제거 후 추출된 명사 입력)
    result = ""
    for s in str_list:
        result += s + " "
    string = result.strip()
    return string

def kwordrank(string): #해당 함수에서 불용어 제거 
    stop_words_list=[]
    stop_words_file = open("korean_stop_words.txt","r",encoding='utf-8')
    for line in stop_words_file.readlines():
        stop_words_list.append(line.rstrip())
        stop_words_file.close()
    stopwords=stop_words_list
    texts = [string]
    keywords = summarize_with_keywords(texts, min_count=10, max_length=10,beta=0.85, max_iter=10, stopwords=stopwords, verbose=True)
    passwords = {word:score for word, score in sorted(
        keywords.items(), key=lambda x:-x[1])[:300] if not (word in stopwords)}
    return passwords


def make_wordcloud(passwords):
    krwordrank_cloud = WordCloud(
        font_path = font_path,
        width = 800,
        height = 800,
        background_color="black"
    )
    krwordrank_cloud = krwordrank_cloud.generate_from_frequencies(passwords)
    %matplotlib inline
    fig = plt.figure(figsize=(10, 10))
    plt.axis('off')
    plt.imshow(krwordrank_cloud, interpolation="bilinear")
    plt.show()
    outputFileName = '%s-%s-%s.png' % (now.year, now.month, now.day)
    fig.savefig(outputFileName) #파일명 추후 카테고리 이름 추가 


    
