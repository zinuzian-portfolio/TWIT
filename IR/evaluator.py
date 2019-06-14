import os


def load_follower_ids(streamer_list, name=None):
    '''
    Load follower list
    :param streamer_list: list of streamer names in our system
    :param name: specific name you want to know
    :return: dictionary with streamer name as key, follower list as value.
    '''
    ret_followers_dic = {}
    if name is not None:
        # 특정 스트리머의 팔로워 id들을 로드
        followers_path = os.path.join(os.getcwd(), "api", "follows", "follows_" + name + ".txt")
        with open(followers_path, "r") as ff:
            followers = ff.read()
            followers = followers.split(",")
            ret_followers_dic[name] = sorted(followers)
    else:
        # 모든 스트리머들의 팔로워 id들을  로드
        for streamer in streamer_list:
            followers_path = os.path.join(os.getcwd(), "api", "follows", "follows_" + streamer + ".txt")
            with open(followers_path, "r") as ff:
                followers = ff.read()
                followers = followers.split(",")
                ret_followers_dic[streamer] = sorted(followers)
    # print(ret_followers_dic)

    return ret_followers_dic


def evaluate_between(query, result):
    '''
    Calculate evaluation plan in O(min(m,n))
    :param query: list of query streamer's followers
    :param result: list of result streamer's followers
    :return: evaluation value
    '''
    intersection = set()

    i = j = 0
    followers_of_query = len(query)
    followers_of_result = len(result)


    while i < followers_of_query and j < followers_of_result:
        if query[i] == result[j]:
            intersection.add(query[i])
            i += 1
            j += 1
        elif query[i] < result[j]:
            i += 1
        else:
            j += 1

    count = len(list(intersection))
    ratio = count / followers_of_query
    return ratio