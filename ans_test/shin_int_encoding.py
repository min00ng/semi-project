import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer

# df 예시
df = pd.DataFrame(['복숭아', '바나나', '복숭아' '딸기', '복숭아', '복숭아','복숭아','사과','사과','사과','사과','배','배','배','오리','오리','감자','감자','토마토'], columns = ['과일'])

# 정수 인코딩 함수 
def int_encoding(df):
  tokenizer = Tokenizer()
  tokenizer.fit_on_texts(df['과일'])
  word_dict = tokenizer.word_index

  return word_dict
