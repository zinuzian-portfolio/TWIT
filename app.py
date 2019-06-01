import sys


def main():
    # example) python main.py <streamer's name>
    #               (argv[0])   (argv[1])
    print('Your input is ', checkArgument(sys.argv))

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
