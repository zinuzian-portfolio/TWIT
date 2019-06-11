import sys
import os
from IR.vectorizer import vectorize
from IR.query import get_query, similarity_ranks
from IR.evalfunc import distance_func, cosine_func
import pickle


def getStreamerVectors():

    # <Prerequisite>
    # Make streamers vectors and save it as a binary file
    streamerVector = {}
    SVfilepath = os.path.join(os.getcwd(), "StreamerVector.dat")
    print('Loding...', end=' ')
    if os.path.isfile(SVfilepath):
        file = open(SVfilepath, "rb")
        streamerVector = pickle.load(file)

    # If it is the first time making streamer vector
    else:
        _, streamerVector = vectorize()
        file = open(SVfilepath, "wb")
        pickle.dump(streamerVector, file)
        file.close()

    if not streamerVector:
        raise FileNotFoundError

    print('Complete.')
    # print(streamerVector)
    return streamerVector

def chatResult():


def main():
    # example) python main.py <streamer's name>
    #               (argv[0])   (argv[1])
    try:

        # <Prerequisite>
        # Make streamers vectors and save it as a binary file

        SV = getStreamerVectors()

        # 1. Read streamer's vectors from a binary file
        # 2. Check if the input streamer is one of them
        #  2.1 If not, return error
        # 3. Get a closest vector to the input streamer
        # 4. Evaluate the closest vector by followers.
        # 5. Print out the result

        keyword = checkArgument(sys.argv)
        if keyword is None:
            print(
                '\n===============  We provide various streamers below  ===============\n')
            for key in SV.keys():
                print(key)
            print(
                '\n====================================================================')
            keyword = input(
                'Please input one streamer and we will give you the most similar streamer : ')

        print('Your input is ', keyword)

        if keyword not in SV.keys():
            print('Please check your input')
            quit()

        print("\n\n- rank of cosine similarity")
        for rank in cosine_func(SV, keyword):
            print(rank)

        print("\n\n- rank of euclidian distance")
        for rank in distance_func(SV, keyword):
            print(rank)

        # Chatlog Analyze
        print('numOfHighlights : the number of expected highlights for each chatlog')
        print('Your numOfHighlights is ')

        makeHighlightBystreamer(keyword, )

    except(FileNotFoundError):
        print('Error occurred making streamer as a vector.')


def checkArgument(argv):
    # If there is no argument
    if len(argv) != 2:
        return None
    # elif len(argv) > 2:
    #     print('There are more than 2 arguments')
    #     quit()
    else:
        return argv[1]


if __name__ == "__main__":
    main()
