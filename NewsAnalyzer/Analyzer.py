from transformers import PreTrainedTokenizerFast
from transformers import BartForConditionalGeneration
import torch
from krwordrank.word import summarize_with_keywords
import pandas as pd
from konlpy.tag import Okt
import re
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

class analysis:
    def __init__(self) -> None:
        self.tokenizer = PreTrainedTokenizerFast.from_pretrained('digit82/kobart-summarization')
        self.model = BartForConditionalGeneration.from_pretrained('digit82/kobart-summarization')

    def summarizer(self, text):
        text = text.replace('\n', ' ')
        raw_input_ids = self.tokenizer.encode(text)
        input_ids = [self.tokenizer.bos_token_id] + raw_input_ids + [self.tokenizer.eos_token_id]

        summary_ids = self.model.generate(torch.tensor([input_ids]),  num_beams=4,  max_length=1024,  eos_token_id=1)
        k = self.tokenizer.decode(summary_ids.squeeze().tolist(), skip_special_tokens=True)
        return k

    def listToString(self,str_list): #리스트를 문자열로 반환 (특수문자 제거 후 추출된 명사 입력)
        result = ""
        for s in str_list:
            result += s + " "
        string = result.strip()
        return string

    def kwordrank(self, string): #해당 함수에서 불용어 제거 
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

    def extract_keyword(self, str_list):
        s = self.listToString(str_list)
        words = self.kwordrank(s)
        return words

    def show_relevant_keyword(self, keyword, data): # 키워드와 사용할 뉴스 데이터를 인자로 입력받음
    
        # 에러를 막기 위해 'english'로 설정하였음. 
        # max_features는 5000개로 설정함
        tv = TfidfVectorizer(stop_words = 'english', max_features = 5000)
        x = tv.fit_transform(data)

        # words에는 feature가 된 단어들이 5000개 담겨 있음. 
        words = tv.get_feature_names() 

        # 불용어 리스트 불러오기
        stopwords = pd.read_csv('./korean_stop_words.txt', encoding = 'utf8')['아']

        ############## SVD 특이값 분해 ###############

        # n_components 는 max_features보다 적어야 함. 
        # 임의로 300개로 설정하였음
        svd = TruncatedSVD(n_components = 300, random_state = 1234)
        try:
            word_idx = words.index(keyword) # 사용자에게 입력받은 키워드의 인덱스 위치 확인
            svd.fit(x)
            kw_idx = svd.components_[:, word_idx].argmax()
            relevant_words_df = pd.DataFrame({'단어': words, 'loading': svd.components_[kw_idx]})
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
        except ValueError:
            rel_words_df = pd.DataFrame([{"단어":"failed","loading" : 0}])

        # 사용자가 입력한 키워드와 관련있는 상위 10개 단어를 데이터 프레임으로 반환
        return rel_words_df

    def get_result(self,pp_text): # 상위 20개의 키워드 + 중요도 + 연관단어 뽑는 함수.
        keywords = self.extract_keyword(pp_text)
        lst = []
        for word, num in keywords.items():
            k = [word, num]
            lst.append(k)
        all_key_words = lst[:20]
        for word in all_key_words:
            rkw = self.show_relevant_keyword(word[0],pp_text)
            if rkw.단어.iloc[0] != "failed":
                word.append(rkw.단어.values.tolist())
            else:
                word.append([])
        # 기사 제목, 링크, 본문요약 추가
        # result = pd.DataFrame(all_key_words,columns=["키워드","중요도","연관단어"])
        return all_key_words