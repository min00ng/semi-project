def ca(lst = [],i = 0):
    if i > 5:
        return lst
    lst.append(i)
    i += 1
    ca(lst,i)

print(ca())

def test(url):
    all_news = []

    def compare_articles():
        if last_article:
            return all_news

    compare_articles()