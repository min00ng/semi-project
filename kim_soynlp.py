from soynlp import DoublespaceLineCorpus
from soynlp.word import WordExtractor

# 문서 단위 말뭉치 생성 
corpus = DoublespaceLineCorpus("/content/4.12 news data.csv")
#앞 5개 문서 인쇄
i = 0
for d in corpus:
    print(i, d)
    i += 1
    if i > 4:
        break

word_extractor = WordExtractor()
word_extractor.train(corpus)

#잘되는지 확인해보기
word_score["검수완박"].cohesion_forward
word_score["우크라"].cohesion_forward
word_score["우크라이"].cohesion_forward
word_score["우크라이나"].cohesion_forward
#점점 확률이 올라가는 것을 확인

#1044번 기사 제목 명사 추출1
from soynlp.tokenizer import LTokenizer

scores = {word:score.cohesion_forward for word, score in word_score.items()}
l_tokenizer = LTokenizer(scores=scores)

l_tokenizer.tokenize(title[1044], flatten=False)

#1044번 기사 제목 명사 추출2
from soynlp.tokenizer import MaxScoreTokenizer

maxscore_tokenizer = MaxScoreTokenizer(scores=scores)
maxscore_tokenizer.tokenize(title[1044])