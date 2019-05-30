from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
from sklearn.decomposition import TruncatedSVD

import os, re

data_path = "..\\data"


for (path, dir, files) in os.walk(data_path):
    for filename in files:
        target = os.path.join(path,filename)
        print("file location: " + target)
        with open(target, 'rb') as f:
            corpus = f.read()
            corpus = corpus.decode("utf-8").lower().split("\n")
            regex_time = re.compile(r'\[\d+:\d{2}:\d{2}\]') # [0:00:00]
            regex_username = re.compile(r'<([A-Za-z0-9_]+)>') # <abcd1234>

            preprocessed = []
            for line in corpus:
                line = re.sub(regex_time, '', line)
                line = re.sub(regex_username, '', line)
                preprocessed.append(line.strip())


            # 모든 게임에 공통적으로 등장할것으로 생각되는 단어들
            stopword = ['pog', 'poggers', 'pogchamp', 'holy', 'shit', 'wow', 'ez', 'clip', 'nice', 'omg', 'wut', 'gee', 'god', 'dirty', 'way', 'moly', 'wtf', 'fuck', 'crazy', 'omfg']

            # 영어 기본 stop words
            my_stop_words = text.ENGLISH_STOP_WORDS.union(stopword)

            print("tf-idf...")
            tf_idf_vectorizer = TfidfVectorizer(
                min_df=3,
                stop_words=my_stop_words,
            ).fit(preprocessed)
            print(str(len(tf_idf_vectorizer.vocabulary_)) + "개의 vocabulary")

            # 매트릭스로 확인하려하면 메모리오류 뜸
            # print(tf_idf_vectorizer.transform(corpus).toarray())


            print("svd...")
            n_topics = 300
            svd = TruncatedSVD(n_components=n_topics).fit_transform(tf_idf_vectorizer.transform(corpus))
            print(svd)


