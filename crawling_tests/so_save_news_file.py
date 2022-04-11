from datetime import datetime
import pandas as pd


file_path='' #파일 저장 경로

def save_news_file(file_path,df):#데이터프레임 형식 데이터 입력
    now = datetime.now()
    outputFileName = '%s-%s-%s  %s시 %s분 %s초 merging.xlsx' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    df.to_excel(file_path+outputFileName)
    return 