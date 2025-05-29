import sys

import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtCore import QStringListModel #자동완성
from scipy.io import mmread
import pickle
from gensim.models import Word2Vec
from sklearn.metrics.pairwise import linear_kernel



#GUI띄우는 코드

form_window = uic.loadUiType('./movie_recommendation.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.tfidf_matrix = mmread('./models/tfidf_movie_review.mtx').tocsr()
        with open('./models/tfidf.pickle', 'rb') as f:
            self.tfidf = pickle.load(f)
        self.embedding_model = Word2Vec.load('./models/word2vec_movie_review.model')

        #콤보박스에 영화 제목을 추가해주는 코드
        self.df_reviews = pd.read_csv('./cleaned_data/cleaned_reviews.csv')
        self.titles = list(self.df_reviews['titles'])
        self.titles.sort()
        for title in self.titles:
            self.comboBox.addItem(title)

        #키워드를 작성할 때 자동완성
        model = QStringListModel()
        model.setStringList(self.titles) #자동완성 리스트
        completer = QCompleter()
        completer.setModel(model)
        self.le_keyword.setCompleter(completer)


        self.comboBox.currentIndexChanged.connect(self.combobox_slot)
        self.btn_recommendation.clicked.connect(self.btn_slot)


    #키워드를 작성했을 때 추천
    def btn_slot(self):
        user_input = self.le_keyword.text()
        if user_input in self.titles:
            self.movie_title_recomm(user_input)
        else:
            self.keyword_slot(user_input.split()[0]) #여러 키워드를 작성해도 처음것만 반영


    def keyword_slot(self, keyword):
        sim_word = self.embedding_model.wv.most_similar(keyword, topn=10)
        words = [keyword]
        for word, _ in sim_word:
            words.append(word)
        sentence = []
        count = 10

        for word in words:
            sentence = sentence + [word] * count
            count -= 1
        sentence = ' '.join(sentence)
        print(sentence)

        sentence_vec = self.tfidf.transform([sentence])
        cosine_sim = linear_kernel(sentence_vec, self.tfidf_matrix)
        recommendation = self.getRecommendation(cosine_sim)
        print(recommendation)
        print(type (recommendation))
        recommendation = '\n'.join(recommendation[:10]) #키워드로 추천 시 0번~9번까지 총 10개 출력
        self.lbl_recommendation.setText(recommendation)


    def getRecommendation(self, cosine_sim):  # 입력된 코사인 유사도(cosine similarity)행렬을 기반으로 추천 결과를 추출하는 함수의 시작
        simScore = list(enumerate(cosine_sim[-1]))  # 코사인 유사도 벡터에서 가장 유사한 인덱스 추출
        simScore = sorted(simScore, key=lambda x: x[1], reverse=True)  # 유사도 기준으로 정렬
        simScore = simScore[:11]  # 자기 자신(0번째)을 제외하고 상위 N개 선택. 상위 10개 선택
        movie_idx = [i[0] for i in simScore]  # 인덱스만 추출
        rec_movie_list = self.df_reviews.iloc[movie_idx, 0]  # 원본 데이터프레임(추천 영화 리스트)에서 해당 영화명(첫 번째 열 값) 가져오기
        return rec_movie_list[:11]

    def combobox_slot(self):
        title = self.comboBox.currentText()
        self.movie_title_recomm(title)


    def movie_title_recomm(self, title):
        movie_idx = self.df_reviews[self.df_reviews['titles'] == title].index[0]
        cosine_sim = linear_kernel(self.tfidf_matrix[movie_idx],
                                   self.tfidf_matrix)
        recommendation = self.getRecommendation(cosine_sim) #recommendation이 문자열이 아님
        #recommendation을 문자열로 바꿔줌
        recommendation = '\n'.join(recommendation[1:])
        self.lbl_recommendation.setText(recommendation)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec())

