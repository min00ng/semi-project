import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer

# df 예시
df = pd.DataFrame(['복숭아', '바나나', '복숭아' '딸기', '복숭아', '복숭아','복숭아','사과','사과','사과','사과','배','배','배','오리','오리','감자','감자','토마토'], columns = ['과일'])

# 패딩 적용 함수s
def padding(df):
  tokenizer = Tokenizer()
  tokenizer.fit_on_texts(df['과일'])
  encoded = tokenizer.texts_to_sequences(df['과일']) # 뒤에 설정 넣을 수 있음(아래로)

  return encoded
