from NewsAnalyzer.Analyzer import analysis
from NewsAnalyzer.PreProcesser import preprocesser

pp = preprocesser()
an = analysis()

file_path = "data/2022-04-18 news data.csv"

df = pp.load_data(file_path)

title_n = pp.prep(file_path=file_path,title=True,tokenizing=False)

all_keywords = an.get_result(title_n)

