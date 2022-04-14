from kiwipiepy.utils import Stopwords

def stop_words_list(self):
    stopwords = Stopwords()
    stopwords.add(('단독', 'NNG'))
    stopwords.add(('자료', 'NNG'))
    stopwords.add(('사진', 'NNG'))
    stopwords.add(('기자', 'NNG'))
    stopwords.add(('동영상', 'NNG'))
    stopwords.add(('이미지', 'NNG'))
    stopwords.add(('출처', 'NNG'))
    stopwords.add(('뉴스', 'NNG'))
    stopwords.add(('카카오톡', 'NNG'))
    stopwords.add(('news', 'SL'))
    stopwords.add(('co', 'SL'))
    stopwords.add(('kr', 'SL'))
    stopwords.add(('org', 'SL'))
    stopwords.add(('naver', 'SL'))
    stopwords.add(('kmib', 'SL'))
    stopwords.add(('CBS', 'SL'))
    stopwords.add(('yna', 'SL'))
    return stopwords