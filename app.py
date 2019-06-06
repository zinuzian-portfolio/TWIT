import sys
import os
from IR.vectorizer import vectorize
from IR.query import get_query, similarity_ranks


def makeStreamersVectors():

    # <Prerequisite>
    # Make streamers vectors and save it as a text file

    # 1. Get std and streamerInfo
    std, streamerInfo = vectorize()
    print(streamerInfo)
    print(std)

    # 2. Get streamer's vectors

    # 3. Save it

    '''
    f = open(os.path.join(os.getcwd(), "StreamerVectors.txt"), 'w')

    for eachVector in streamerVector:
        f.write(eachVector)
    f.close()
    '''

    # No return


def main():
    # example) python main.py <streamer's name>
    #               (argv[0])   (argv[1])
    print('Your input is ', checkArgument(sys.argv))

    # <Prerequisite>
    # Make streamers vectors and save it as a text file
    makeStreamersVectors()

    # 1. Read streamer's vectors from a text file
    # 2. Check if the input streamer is one of them
    #  2.1 If not, return error
    # 3. Get a closest vector to the input streamer
    # 4. Evaluate the closest vector by followers.
    # 5. Print out the result


def checkArgument(argv):
    # If there is no argument
    if len(argv) is 1:
        print('You need one streamer`s name')
        quit()
    elif len(argv) > 2:
        print('There are more than 2 arguments')
        quit()
    else:
        return argv[1]


if __name__ == "__main__":
    main()
