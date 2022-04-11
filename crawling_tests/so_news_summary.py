from gensim.summarization import summarize
from newspaper import Article


def news_summary(url):
    news = Article(url, language='ko')
    news.download()
    news.parse()
    summarized_news=summarize(news.text, word_count=50)
    print(summarized_news)
    