import pandas as pd

class preprocesser:
    def __init__(self) -> None:
        pass
    
    # 결측값 처리 -> 특수문자 제거 -> 어간추출 -> 불용어 제거 -> 인덱스벡터라이즈 -> 패딩

    def road_data(self,file_path): # 데이터 불러오기, 불필요한 열 삭제, null값 삭제.
        df = pd.read_csv(file_path)
        df2 = df.drop(["Unnamed: 0"],axis=1)
        df3 = df2.dropna(axis=0)
        return df3


