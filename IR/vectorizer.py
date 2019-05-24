from sklearn.feature_extraction.text import TfidfVectorizer
import os

data_path = "..\\data"


for (path, dir, files) in os.walk(data_path):
    for filename in files:
        target = os.path.join(path,filename)
        print("file location: " + target)
        with open(target, 'rb') as f:
            corpus = f.read()
            corpus = corpus.decode("utf-8")
            # print(corpus)
            corpus = corpus.split("\n")
            tfidv = TfidfVectorizer(stop_words='english').fit(corpus)
            print(tfidv.transform(corpus).toarray())


