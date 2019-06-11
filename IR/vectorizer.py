from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import text
from sklearn.decomposition import TruncatedSVD
import os
import re
import numpy as np


def vectorize():
    streamerInfo = dict()
    chatters_in_streamer = dict()
    data_path = os.path.join(os.getcwd(), "data")
    # data_path = os.path.join("..", "data")

    corpus = []
    print("Reading Chatlog", end=" ")

    for (yourpath, dir, files) in os.walk(data_path):

        chatloglist = list()
        chatters = set()

        for filename in files:
            target = os.path.join(yourpath, filename)

            # For streamer Info
            # example) { 'streamerA' : [chatlog1.txt, chatlog2.txt, ...], ...}
            chatloglist.append(filename)

            print("#", end="")
            with open(target, 'rb') as f:
                chatlog = f.read()

                # preprocessing - lowercase
                chatlog = chatlog.decode("utf-8").lower()

                # preprocessing - only chat content
                regex_time = re.compile(r'\[\d+:\d{2}:\d{2}\]')  # [0:00:00]
                chatlog = re.sub(regex_time, '', chatlog)   # delete them all


                regex_username = re.compile(r'<([A-Za-z0-9_]+)>')  # <abcd1234>
                chat_users = set(re.findall(regex_username,chatlog))
                chatters.update(chat_users)
                chatlog = re.sub(regex_username, '', chatlog)

                chatlog.replace("\n", " ")
                corpus.append(chatlog)

        # For streamer Info
        # example) { 'streamerA' : [chatlog1.txt, chatlog2.txt, ...], ...}
        temp = yourpath.split('\\')
        streamerInfo[temp[-1]] = chatloglist
        chatters_in_streamer[temp[-1]] = list(chatters)

    print("\nAll chatlog preprocessing complete.")
    print("Total number of chatlog is ", str(len(corpus)))

    # 모든 게임 방송에 자주 등장하는 단어들 [reference : <add your reference>]
    stopword = ['pog', 'poggers', 'pogchamp', 'holy', 'shit', 'wow', 'ez', 'clip', 'nice',
                'omg', 'wut', 'gee', 'god', 'dirty', 'way', 'moly', 'wtf', 'fuck', 'crazy', 'omfg']

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
    svd = TruncatedSVD(n_components=n_topics).fit_transform(
        tf_idf_vectorizer.transform(corpus))
    # print(svd)
    print(svd.shape)

    # delete the first element of streamerInfo since it is 'data':[]
    del streamerInfo['data']
    del chatters_in_streamer['data']
    print(streamerInfo)


    # To average svd result rows per streamer
    streamerVector = {}
    cnt = 0

    for key in streamerInfo.keys():
        num_of_chatlog = len(streamerInfo[key])
        # print(key, num_of_chatlog, svd[cnt:cnt + num_of_chatlog])
        # print(key, cnt, cnt + num_of_chatlog)
        streamerVector[key] = np.divide(np.sum(svd[cnt:cnt + num_of_chatlog], axis=0), num_of_chatlog)
        cnt += num_of_chatlog

    # print(streamerVector)

    return streamerVector, chatters_in_streamer


if __name__ == "__main__":
    vectorize()
