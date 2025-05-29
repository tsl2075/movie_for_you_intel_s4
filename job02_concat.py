import  pandas as pd
import glob



#직접한 크롤링 데이터 전처리

# data_paths = glob.glob('./data/*') #data들의 경로를 보여줌
# print(data_paths)
#
# df = pd.DataFrame() #빈 dataframe을 만들어 줌
#
#
# #하나의 데이터프레임으로 통합
# for path in data_paths: #여러 csv파일 경로가 들어 있는 리스트
#     df_temp = pd.read_csv(path) #각 csv파일을 pandas dataframe으로 읽어 옴
#     df_temp.dropna(inplace=True) # null값 drop
#     df = pd.concat([df, df_temp], ignore_index=True) #df와 df_temp를 세로 방향(행)으로 연결함. ignore_index=True는 인덱스를 다시 0부터 자동 재부여.
# df.drop_duplicates(inplace=True)#중복제거
# df.info() #통합된 df의 열 구조,null 개수, 데이터 타입 등을 요약
# print(df.head()) #앞부분 5줄을 출력해서 내용 확인
# df.to_csv('./preprocessed_data/kino.csv', index=False)#전처리 데이터 저장





#교수님이 공유해주신 크롤링 전처리

#crawling_data.csv

# data_paths = glob.glob('./crawling_data/*') #data들의 경로를 보여줌
# print(data_paths)
#
# df = pd.DataFrame() #빈 dataframe을 만들어 줌
#
#
# #하나의 데이터프레임으로 통합
# for path in data_paths: #여러 csv파일 경로가 들어 있는 리스트
#     df_temp = pd.read_csv(path) #각 csv파일을 pandas dataframe으로 읽어 옴
#     df_temp.columns = ['titles', 'reviews'] #타이틀과 컬럼을 통일 시켜줌
#     df_temp.dropna(inplace=True) # null값 drop
#     df = pd.concat([df, df_temp], ignore_index=True) #df와 df_temp를 세로 방향(행)으로 연결함. ignore_index=True는 인덱스를 다시 0부터 자동 재부여.
# df.drop_duplicates(inplace=True)#중복제거
# df.info() #통합된 df의 열 구조,null 개수, 데이터 타입 등을 요약
# print(df.head()) #앞부분 5줄을 출력해서 내용 확인
# df.to_csv('./preprocessed_data/reviews.csv', index=False)#전처리 데이터 저장





#movie_revies.csv
#
# data_paths = glob.glob('./movie_reviews/*') #data들의 경로를 보여줌
# df = pd.DataFrame() #빈 dataframe을 만들어 줌
#
#
# #하나의 데이터프레임으로 통합
# for path in data_paths: #여러 csv파일 경로가 들어 있는 리스트
#     df_temp = pd.read_csv(path) #각 csv파일을 pandas dataframe으로 읽어 옴
#     df_temp.columns = ['titles', 'reviews']
#     titles = []
#     reviews = []
#     old_title = ''
#     for i in range(len(df_temp)):  #중복된 제목을 제거 : 리뷰를 하나로 합침
#         title =df_temp.iloc[i, 0]
#         if title != old_title:
#             titles.append(title)
#             old_title = title
#             df_movie = df_temp[(df_temp.titles == title)]
#             review = ' '.join(df_movie.reviews) #리뷰스를 띄어쓰기 기준으로 하나로 합침
#             reviews.append(review)
#     print(len(titles))
#     print(len(reviews))
#     df_batch = pd.DataFrame({'titles':titles, 'reviews':reviews})
#     df = pd.concat([df, df_batch], ignore_index=True)
# df.drop_duplicates(inplace=True)
# df.info()
# df.to_csv('./preprocessed_data/batchs.csv', index=False)






#위에서 만들어진 preprocessed_data에 만든 파일들을 하나로 합침

# data_paths = glob.glob('./preprocessed_data/*') #data들의 경로를 보여줌
# print(data_paths)
#
# df = pd.DataFrame() #빈 dataframe을 만들어 줌
#
#
# #하나의 데이터프레임으로 통합
# for path in data_paths: #여러 csv파일 경로가 들어 있는 리스트
#     df_temp = pd.read_csv(path) #각 csv파일을 pandas dataframe으로 읽어 옴
#     df_temp.columns = ['titles', 'reviews']
#     df_temp.dropna(inplace=True) # null값 drop
#     df = pd.concat([df, df_temp], ignore_index=True) #df와 df_temp를 세로 방향(행)으로 연결함. ignore_index=True는 인덱스를 다시 0부터 자동 재부여.
# df.drop_duplicates(inplace=True)#중복제거(제목과 리뷰가 완전히 같아야지 제거 됨)
# df.info() #통합된 df의 열 구조,null 개수, 데이터 타입 등을 요약
# print(df.head()) #앞부분 5줄을 출력해서 내용 확인
# df.to_csv('./cleaned_data/movie_reviews.csv', index=False)#전처리 데이터 저장





#비슷해도 중복 제거

data_paths = glob.glob('./cleaned_data/*') #data들의 경로를 보여줌
df = pd.DataFrame() #빈 dataframe을 만들어 줌


#하나의 데이터프레임으로 통합
for path in data_paths: #여러 csv파일 경로가 들어 있는 리스트
    df_temp = pd.read_csv(path) #각 csv파일을 pandas dataframe으로 읽어 옴
    df_temp.columns = ['titles', 'reviews']
    titles = []
    reviews = []
    old_title = ''
    for i in range(len(df_temp)):  #중복된 제목을 제거 : 리뷰를 하나로 합침
        title =df_temp.iloc[i, 0]
        if title != old_title:
            titles.append(title)
            old_title = title
            df_movie = df_temp[(df_temp.titles == title)]
            review = ' '.join([str(r) for r in df_movie.reviews if pd.notnull(r)]) #하나로 합친 리뷰들을 공백을 기준으로 구분
            reviews.append(review)#리뷰를 리스트에 추가
    print(len(titles))
    print(len(reviews))
    df_batch = pd.DataFrame({'titles':titles, 'reviews':reviews})
    df = pd.concat([df, df_batch], ignore_index=True)
df.drop_duplicates(inplace=True)
df.info()
df.to_csv('./cleaned_data/movie_reviews.csv', index=False)








