from datetime import datetime
import pandas as pd
now = datetime.now()

file_path='' #파일 저장 경로
data = {
    'year': [2016, 2017, 2018],
    'GDP rate': [2.8, 3.1, 3.0],
    'GDP': ['1.637M', '1.73M', '1.83M']
}
 
df = pd.DataFrame(data)

def save_news_file(file_path,df):#데이터프레임 형식 데이터 입력
    outputFileName = '%s-%s-%s  %s시 %s분 %s초 merging.xlsx' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    df.to_excel(file_path+outputFileName)
    return 

save_news_file("C:\\Users\\서지혜\\OneDrive\\바탕 화면\\2022-1수업\\지속가능한 기업가정신\\",df)