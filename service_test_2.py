from NewsAnalyzer.Analyzer import analysis
from NewsAnalyzer.PreProcesser import preprocesser

pp = preprocesser()
an = analysis()

file_path = "data/2022-04-18 news data.csv"

df = pp.load_data(file_path)
corpus = pp.make_corpus(file_path)

all_n = pp.prep(corpus,df=df,title=True,tokenizing=False)

all_keywords = an.get_result(all_n)

# 카테고리 : 정치, 경제, 사회, 생활, IT, 세계

df_p = pp.select_category(df,"정치")
df_e = pp.select_category(df,"정치")
df_s = pp.select_category(df,"정치")
df_l = pp.select_category(df,"정치")
df_i = pp.select_category(df,"정치")
df_w = pp.select_category(df,"세계")