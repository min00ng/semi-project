import pandas as pd
from NewsAnalyzer.Analyzer import analysis
from NewsAnalyzer.PreProcesser import preprocesser
from NewsAnalyzer.show_relevant_article import show_relevant_article

pp = preprocesser()
an = analysis()

def save_file_all(df,cg):
    df2 = pd.DataFrame(df)
    df2.to_csv("result_data/"+date+" "+cg+" "+"result.csv")

def save_file(df,cg):
    for i in range(len(df)):
        del df[i][3]
    df2 = pd.DataFrame(df)
    df2.to_csv("result_data/"+date+" "+cg+" "+"result no link.csv")

def category_get_result(df,cg,corpus):
    if cg != "all":
        df_p = pp.select_category(df,cg)
    else:
        df_p = df
    all_n = pp.prep(corpus,df=df_p,title=True,tokenizing=False)
    all_keywords = an.get_result(all_n)
    return all_keywords

def add_link(df1, df2):
    # df1 : 키워드, 연관단어
    # df2 : 기사링크
    for i in range(len(df1)):
        articles = []
        for j in range(len(df2)):
            if df1[i][0] == df2.labels.iloc[j]:
                articles.append([df2.기사제목.iloc[j],df2.기사링크.iloc[j],df2.본문.iloc[j]])
        df1[i].append(articles)
    return df1

def add_summ(df):
    for i in range(len(df)):
        try:
            data = df[i][3][0][2]
            text = an.summarizer(data)
            df[i].append(text)
        except:
            df[i].append("no summarization")
    return df

date = "2022-04-18"
file_path = "data/"+date+" news data.csv"

df = pp.load_data(file_path)

df_p_2 = show_relevant_article("정치",df)
df_e_2 = show_relevant_article("경제",df)
df_s_2 = show_relevant_article("사회",df)
df_l_2 = show_relevant_article("생활",df)
df_i_2 = show_relevant_article("IT",df)
df_w_2 = show_relevant_article("세계",df)

corpus = pp.make_corpus(file_path)

# 전체 데이터
category_get_result(df,"all",corpus)

# 카테고리 : 정치, 경제, 사회, 생활, IT, 세계
df_p_1 = category_get_result(df,"정치",corpus)
df_e_1 = category_get_result(df,"경제",corpus)
df_s_1 = category_get_result(df,"사회",corpus)
df_l_1 = category_get_result(df,"생활",corpus)
df_i_1 = category_get_result(df,"IT",corpus)
df_w_1 = category_get_result(df,"세계",corpus)

# 링크, 본문 추가
df_p_3 = add_link(df1 = df_p_1, df2=df_p_2)
df_e_3 = add_link(df1 = df_e_1, df2=df_e_2)
df_s_3 = add_link(df1 = df_s_1, df2=df_s_2)
df_l_3 = add_link(df1 = df_l_1, df2=df_l_2)
df_i_3 = add_link(df1 = df_i_1, df2=df_i_2)
df_w_3 = add_link(df1 = df_w_1, df2=df_w_2)

# 요약 추가
df_p_4 = add_summ(df_p_3)
df_e_4 = add_summ(df_e_3)
df_s_4 = add_summ(df_s_3)
df_l_4 = add_summ(df_l_3)
df_i_4 = add_summ(df_i_3)
df_w_4 = add_summ(df_w_3)

# 전체파일 세이브
save_file_all(df_p_4,"politic")
save_file_all(df_e_4,"economy")
save_file_all(df_s_4,"social")
save_file_all(df_l_4,"life")
save_file_all(df_i_4,"it")
save_file_all(df_w_4,"world")

# 링크없이 세이브
save_file(df_p_4,"politic")
save_file(df_e_4,"economy")
save_file(df_s_4,"social")
save_file(df_l_4,"life")
save_file(df_i_4,"it")
save_file(df_w_4,"world")