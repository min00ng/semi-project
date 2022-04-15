# 필요한 모듈 불러오기
import numpy as np
import pandas as pd
import itertools
from konlpy.tag import Okt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer


# 데이터 불러오기
from NewsAnalyzer.PreProcesser import preprocesser

file_path = "2022-04-12 news data, test.csv"

pc = preprocesser()
data = pc.road_data(file_path)

# 714번째 결측치 제거
# df = data.drop([714], axis = 0)
# df = df.reset_index()

# 본문 전체를 돌리면 시간이 너무 오래 걸려서 테스트로 10개만 돌려봐았습니다.
content = data["본문"][:10]

### 방법 1. 유사한 단어들 출력 - 문서와 가장 유사한 키워드 출력
model = SentenceTransformer('sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens')

def keyBERT(content):
  keywords = []
  for i in range(len(content)):

    # 기사별 명사 추출
    okt = Okt()
    words = okt.nouns(content[i])

    # 추출한 명사 리스트에서 빼내기
    tokenized_nouns = ' '.join(word for word in words)

    n_gram_range = (1, 1)
    count = CountVectorizer(ngram_range=n_gram_range).fit([tokenized_nouns])
    candidates = count.get_feature_names_out()

    # 모델 적용 
    doc_embedding = model.encode([tokenized_nouns])
    candidate_embeddings = model.encode(candidates)

    # 문서와 가장 유사한 키워드들을 추출
    top_n = 5
    distances = cosine_similarity(doc_embedding, candidate_embeddings)
    keyword = [candidates[index] for index in distances.argsort()[0][-top_n:]]
    keywords.append(keyword)
  return keywords


### 방법 2-1. 다양한 키워드들을 얻기 위한 두 가지 알고리즘 - Max Sum Similarity
model = SentenceTransformer('sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens')

def max_sum_sim(content, top_n, nr_candidates):
    keywords = []
    for i in range(len(content)):

        # 기사별 명사 추출
        okt = Okt()
        words = okt.nouns(content[i])

        # 추출한 명사 리스트에서 빼내기
        tokenized_nouns = ' '.join(word for word in words)

        n_gram_range = (1, 1)
        count = CountVectorizer(ngram_range=n_gram_range).fit([tokenized_nouns])
        candidates = count.get_feature_names_out()

        # 모델 적용 
        doc_embedding = model.encode([tokenized_nouns])
        candidate_embeddings = model.encode(candidates)

        # 문서와 각 키워드들 간의 유사도
        distances = cosine_similarity(doc_embedding, candidate_embeddings)

        # 각 키워드들 간의 유사도
        distances_candidates = cosine_similarity(candidate_embeddings, candidate_embeddings)

        # 코사인 유사도에 기반하여 키워드들 중 상위 top_n개의 단어를 pick.
        words_idx = list(distances.argsort()[0][-nr_candidates:])
        words_vals = [candidates[index] for index in words_idx]
        distances_candidates = distances_candidates[np.ix_(words_idx, words_idx)]

        # 각 키워드들 중에서 가장 덜 유사한 키워드들간의 조합을 계산
        min_sim = np.inf
        candidate = None
        for combination in itertools.combinations(range(len(words_idx)), top_n):
            sim = sum([distances_candidates[i][j] for i in combination for j in combination if i != j])
            if sim < min_sim:
                candidate = combination
                min_sim = sim
        keyword = [words_vals[idx] for idx in candidate]
        keywords.append(keyword)
    return keywords


### 방법 2-2.  다양한 키워드들을 얻기 위한 두 가지 알고리즘 - Maximal Marginal Relevance 
model = SentenceTransformer('sentence-transformers/xlm-r-100langs-bert-base-nli-stsb-mean-tokens')

def mmr(content, top_n, diversity):
    keywords = []
    for i in range(len(content)):

        # 기사별 명사 추출
        okt = Okt()
        words = okt.nouns(content[i])

        # 추출한 명사 리스트에서 빼내기
        tokenized_nouns = ' '.join(word for word in words)

        n_gram_range = (1, 1)
        count = CountVectorizer(ngram_range=n_gram_range).fit([tokenized_nouns])
        candidates = count.get_feature_names_out()

        # 모델 적용 
        doc_embedding = model.encode([tokenized_nouns])
        candidate_embeddings = model.encode(candidates)

        # 문서와 각 키워드들 간의 유사도가 적혀있는 리스트
        word_doc_similarity = cosine_similarity(candidate_embeddings, doc_embedding)

        # 각 키워드들 간의 유사도
        word_similarity = cosine_similarity(candidate_embeddings)

        # 문서와 가장 높은 유사도를 가진 키워드의 인덱스를 추출.
        # 만약, 2번 문서가 가장 유사도가 높았다면
        # keywords_idx = [2]
        keywords_idx = [np.argmax(word_doc_similarity)]

        # 가장 높은 유사도를 가진 키워드의 인덱스를 제외한 문서의 인덱스들
        # 만약, 2번 문서가 가장 유사도가 높았다면
        # ==> candidates_idx = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10 ... 중략 ...]
        candidates_idx = [i for i in range(len(candidates)) if i != keywords_idx[0]]

        # 최고의 키워드는 이미 추출했으므로 top_n-1번만큼 아래를 반복.
        # ex) top_n = 5라면, 아래의 loop는 4번 반복됨.
        for _ in range(top_n - 1):
            candidate_similarities = word_doc_similarity[candidates_idx, :]
            target_similarities = np.max(word_similarity[candidates_idx][:, keywords_idx], axis=1)

            # MMR을 계산
            mmr = (1-diversity) * candidate_similarities - diversity * target_similarities.reshape(-1, 1)
            mmr_idx = candidates_idx[np.argmax(mmr)]

            # keywords & candidates를 업데이트
            keywords_idx.append(mmr_idx)
            candidates_idx.remove(mmr_idx)
            keyword = [candidates[idx] for idx in keywords_idx]
        keywords.append(keyword)

    return keywords