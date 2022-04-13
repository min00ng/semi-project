import pandas as pd
from math import log

docs=docs=[
    '먹고 싶은 사과',
    '먹고 싶은 바나나',
    '길고 노란 바나나',
    '저는 과일이 좋아요']

vocab=list(set(i for doc in docs for i in doc.split()))
vocab.sort()

#TF,IDF, TF-IDF 구하는 함수 구현

N=len(docs) #종 문서의 수

#특정 문서 d에서 특정 단어 t의 등장 횟수
def tf(t,d):
    return d.count(t)

#df(t): 특정 단어 t가 등장한 문서의 수
#idf(d,t):df(t)에 반비례하는 수
#log를 씌워주지 않으면, 희귀 단어들에 엄청난 가중치
#log 안의 식에서 분모에 1을 더해주는 이유는 첫번째 이유로는 특정 단어가 전체 문서에서 등장하지 않을 경우에 분모가 0이 되는 상황을 방지하기 위함
def idf(t):
    df=0
    for doc in docs :
        df += t in doc
    return log(N/(df+1))

def tfidf(t,d):
    return tf(t,d),idf(t)

#DTM 을 데이터 프레임에 저장하여 출력 
result=[]
for i in range(N):
    result.append([])
    d=docs[i]
    for j in range(len(vocab)):
        t=vocab[j]
        result[-1].append(tf(t,d))
tf_=pd.DataFrame(result,columns=vocab)

print(tf_)

#각 단어에 대한 IDF 값 구하기
result=[]
for j in range(len(vocab)):
    t=vocab[j]
    result.append(idf(t))

idf_=pd.DataFrame(result,index=vocab,columns=['IDF'])
print(idf_)

#TF-IDF 행렬 출력
result =[]
for i in range(N):
  result.append([])
  d=docs[i]

  for j in range(len(vocab)):
    t=vocab[j]

    result[-1].append(tfidf(t,d))

  tfidf_=pd.DataFrame(result,columns=vocab)
  print(tfidf_)
