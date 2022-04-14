from kiwipiepy import Kiwi, Match

def noun_extractor(sentence):
    kiwi = Kiwi()
    result_iter = kiwi.tokenize(sentence, normalize_coda=True)
    i = 0
    for i in range(len(result_iter)):
        if result_iter[i][1] == 'NNG':
            print (result_iter[i][0])
        elif result_iter[i][1] == 'NNP':
            print (result_iter[i][0])
        elif result_iter[i][1] == 'NR':
            print (result_iter[i][0])
        elif result_iter[i][1] == 'NP':
            print (result_iter[i][0])
        elif result_iter[i][1] == 'SL':
            print (result_iter[i][0])