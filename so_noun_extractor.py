from kiwipiepy import Kiwi, Match
from kiwipiepy.utils import Stopwords

def noun_extractor(sentence):
    nouns =[]
    kiwi = Kiwi()
    stopwords = Stopwords()
    kiwi.add_user_word('국방부', 'NNP', 0)
    kiwi.add_user_word('젤렌스키', 'NNP', 0)
    kiwi.add_user_word('윤희숙', 'NNP', 0)
    kiwi.add_user_word('내로남불', 'NNP', 0)
    kiwi.add_user_word('검수완박', 'NNP', 0)
    result_iter = kiwi.tokenize(sentence, normalize_coda=True,stopwords=stopwords)
    i = 0
    for i in range(len(result_iter)):
        if result_iter[i][1] == 'NNG':
            nouns.append(result_iter[i][0])
        elif result_iter[i][1] == 'NNP':
            nouns.append(result_iter[i][0])
        elif result_iter[i][1] == 'NR':
            nouns.append(result_iter[i][0])
        elif result_iter[i][1] == 'NP':
            nouns.append(result_iter[i][0])
        elif result_iter[i][1] == 'SL':
            nouns.append(result_iter[i][0])
    return nouns