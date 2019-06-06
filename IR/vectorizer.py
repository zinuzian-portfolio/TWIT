from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
from sklearn.decomposition import TruncatedSVD
import os, re

def vectorize():
    data_path = "..\\data"

    corpus = []


    print("Reading Chatlog",end=" ")
    for (path, dir, files) in os.walk(data_path):
        for filename in files:
            target = os.path.join(path,filename)
            # print("file location: " + target)
            print("#", end="")
            with open(target, 'rb') as f:
                chatlog = f.read()

                # preprocessing - lowercase
                chatlog = chatlog.decode("utf-8").lower()

                # preprocessing - only chat content
                regex_time = re.compile(r'\[\d+:\d{2}:\d{2}\]') # [0:00:00]
                regex_username = re.compile(r'<([A-Za-z0-9_]+)>') # <abcd1234>
                chatlog = re.sub(regex_time, '', chatlog)
                chatlog = re.sub(regex_username, '', chatlog)

                chatlog.replace("\n"," ")
                corpus.append(chatlog)


    print("\nAll chatlog preprocessing complete.")
    print("Total number of chatlog is ",str(len(corpus)))
    # 모든 게임에 공통적으로 등장할것으로 생각되는 단어들
    stopword = ['pog', 'poggers', 'pogchamp', 'holy', 'shit', 'wow', 'ez', 'clip', 'nice', 'omg', 'wut', 'gee', 'god', 'dirty', 'way', 'moly', 'wtf', 'fuck', 'crazy', 'omfg']

    # 영어 기본 stop words
    my_stop_words = text.ENGLISH_STOP_WORDS.union(stopword)

    print("tf-idf...")
    tf_idf_vectorizer = TfidfVectorizer(
        min_df=3,
        stop_words=my_stop_words,
    ).fit(corpus)
    print(str(len(tf_idf_vectorizer.vocabulary_)) + "개의 vocabulary")

    # 매트릭스로 확인하려하면 메모리오류 뜸
    # print(tf_idf_vectorizer.transform(corpus).toarray())


    print("svd...")
    n_topics = 10
    svd = TruncatedSVD(n_components=n_topics).fit_transform(tf_idf_vectorizer.transform(corpus))
    # print(svd)
    print(svd.shape)



if __name__ == "__main__":
    vectorize()