from NewsAnalyzer.show_relevant_article import show_relevant_article
from NewsAnalyzer.PreProcesser import preprocesser

pp = preprocesser()

date = "2022-04-18"
file_path = "data/"+date+" news data.csv"

df = pp.load_data(file_path)

df_p = show_relevant_article("정치",df)

