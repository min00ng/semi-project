import tensorflow as tf
import gensim
import sklearn
import nltk
import konlpy
import pandas as pd
from konlpy.tag import Okt
from konlpy.tag import Kkma
import kss
from konlpy.tag import *

def text_cleaning(corpus):
    cleaned_text=""
    # 한국어를 제외한 글자를 제거하는 함수.
    for i in corpus:
        cleaned_text += re.sub("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "", i)
        
    return cleaned_text

def text_tokenizing(corpus, tokenizer):
  token_word=[]

hannanum = Hannanum()
kkma = Kkma()
komoran = Komoran()
#mecab = Mecab()
okt = Okt()

def tokenizer(row):
  return hannanum.morphs(row)

token_result['token']=token_result['본문'].apply(tokenizer)
token_result.head()

token_result['token']=token_result['기사제목'].apply(tokenizer)
token_result.head()

print('최대 토큰 개수:',(max(len(i) for i in token_result['token'])))
print('평균 토큰 개수:',sum(map(len,token_result)))/len(token_result['token'])

"""def tf_sentences(self):
  sentences = []
  for i in range(1, 15):
    target = self.df(i)
    temp = []
    for i in target:
      temp.extend(i.split('\n'))
      hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
      temp = [hangul.sub('', i).strip() for i in temp]
      temp_sen = ''
      
      for i in temp:
        if len(i) > 5:
          temp_sen += i
          sentences.append(okt.nouns(temp_sen))
          
          tf_sentences = []
          for token_set in sentences:
            temp = ' '.join(token_set)
            tf_sentences.append(temp)
            
            return tf_sentences"""