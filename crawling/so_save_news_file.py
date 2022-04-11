import datetime
def_save_news_file():   
    outputFileName = '%s-%s-%s  %s시 %s분 %s초 merging.xlsx' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
    df.to_csv(RESULT_PATH+outputFileName) #파일명 저장 (파일명 설정)