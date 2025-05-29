import pandas as pd
from gensim.models import Word2Vec

df_review = pd.read_csv('./cleaned_data/cleaned_reviews.csv')
df_review.info()

reviews = list(df_review['reviews'])
print(df_review.iloc[0, 0], reviews[0]) # 자연어 처리가 끝난(전처리가 다 된) 형태의 문장이 출력됨

# 형태소 단위로 잘라서 list로 볼것
tokens = []
for sentence in reviews:
    token = sentence.split() # token은 형태소들의 리스트
    tokens.append(token) # 리스트의 리스트
print(tokens[0:2])

embedding_model = Word2Vec(tokens, vector_size= 100, window=4,
                           min_count=15, workers=4, epochs=100, sg=1)
embedding_model.save('./models/word2vec_movie_review.model')
print(list(embedding_model.wv.index_to_key))
print(len(embedding_model.wv.index_to_key))