
def cleaned_token(nouns):
    cleaned_tokens =[]
    stop_words_file = open("korean_stop_words.txt","r",encoding='utf-8')
    stop_words_list=[]
    for line in stop_words_file.readlines():
        stop_words_list.append(line.rstrip())
    stop_words_file.close()
    for word in nouns: 
        if word not in stop_words_list: 
            cleaned_tokens.append(word)
    return cleaned_tokens