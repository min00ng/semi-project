def stemmer(text):
    text = re.sub("[^가-힣ㄱ-ㅎㅏ-ㅣ\\s]","",text)
    okt = Okt()
    maxscore_tokenizer = MaxScoreTokenizer(scores=scores)
    text = maxscore_tokenizer.tokenize(text)#okt.morphs(text, stem= True)
    return text
    
def remove_stop_words(text):
    word_token = stemmer(text)
    stop_words = pd.read_csv("./korean_stop_words.txt")
    result = [word for word in word_token if not word in stop_words]
    return result

#결과확인
remove_stop_words(title[2])