from datetime import datetime
import pandas as pd
now = datetime.now()
file_path =''  #결과 저장할 경로

def save_news_file(file_path,df):
    outputFileName = '%s-%s-%s  %s시 %s분 %s초 merging.xlsx' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    csv = df.to_csv(file_path+outputFileName)
    return csv 