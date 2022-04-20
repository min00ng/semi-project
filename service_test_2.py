from unicodedata import category
from NewsAnalyzer.Analyzer import analysis
from NewsAnalyzer.PreProcesser import preprocesser

pp = preprocesser()
an = analysis()

def save_file(df,cg):
    df.to_csv("result_data/"+date+" "+cg+" "+"result.csv")

def category_get_result(df,cg,corpus):
    if cg != "all":
        df_p = pp.select_category(df,cg)
    else:
        df_p = df
    all_n = pp.prep(corpus,df=df_p,title=True,tokenizing=False)
    all_keywords = an.get_result(all_n)
    save_file(all_keywords,cg)

date = "2022-04-18"
file_path = "data/"+date+" news data.csv"

df = pp.load_data(file_path)
corpus = pp.make_corpus(file_path)

# 전체 데이터
category_get_result(df,"all",corpus)

# 카테고리 : 정치, 경제, 사회, 생활, IT, 세계
category_get_result(df,"정치",corpus)
category_get_result(df,"경제",corpus)
category_get_result(df,"사회",corpus)
category_get_result(df,"생활",corpus)
category_get_result(df,"IT",corpus)
category_get_result(df,"세계",corpus)