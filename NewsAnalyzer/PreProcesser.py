import pandas as pd
from konlpy.tag import Okt
import re
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
import numpy as np
from konlpy.tag import Hannanum

class preprocesser:
    def __init__(self) -> None:
        self.okt = Okt()
        self.han = Hannanum
        
################ 기존 ################    
    def road_data(self,file_path): # 데이터 불러오기, 불필요한 열 삭제, null값 삭제.
        df = pd.read_csv(file_path)
        df2 = df.drop(["Unnamed: 0"],axis=1)
        df3 = df2.dropna(axis=0)
        return df3

    def stemmer(self, text):  # 어간추출
        text = re.sub("[^가-힣ㄱ-ㅎㅏ-ㅣ\\s]","",text)
        text = self.okt.morphs(text, stem= True)
        return text # 각각의 단어가 리스트 형태로 리턴.

    def create_dic(self, texts, num): # 인자로 단어사전에 수록할 단어목록(texts), 단어 개수(num)를 입력 받음
        tk = tf.keras.preprocessing.text.Tokenizer(num_words = num, oov_token = '알 수 없음')
        
        # key값으로 단어, value값으로 빈도순위가 할당된 단어사전 생성
        tk.fit_on_texts(texts)
        word_dic = tk.index_word
        
        return word_dic

    def preprocess(self,sets): # 이중 리스트를 받아서 패딩된 인코딩 리스트로 반환
        texts = []
        for text in sets:
            tt = self.stemmer(text)
            texts.append(tt)

        tokenizer = Tokenizer()
        tokenizer.fit_on_texts(texts)
        encoded = tokenizer.texts_to_sequences(texts)

        max_len = max(len(item) for item in encoded)

        for sentence in encoded:
            while len(sentence) < max_len:
                sentence.append(0)

        padded_np = np.array(encoded)
        return padded_np


########## 새롭게 만들기 ##############
    def clean_text(self, text) : # 문장의 특수문자를 공백으로 대체
        pass

    def get_nouns(self, text): # 문장에서 명사 뽑아오기
        pass