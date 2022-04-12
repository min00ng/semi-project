# 단어사전 만들기

import tensorflow as tf

def create_dic(self, texts, num): # 인자로 단어사전에 수록할 단어목록(texts), 단어 개수(num)를 입력 받음
    tk = tf.keras.preprocessing.text.Tokenizer(num_words = num, oov_token = '알 수 없음')
    
    # key값으로 단어, value값으로 빈도순위가 할당된 단어사전 생성
    tk.fit_on_texts(texts)
    word_dic = tk.word_index
    
    return word_dic