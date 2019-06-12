# 2nd week process
# 현재 : 유저목록과 팔로워 목록 교집합 구하기->퍼센트 출력, 교집합 목록 정민이게 전달

from api.apiHandler import getFollows
from api.apiHandler import get_id_by_name
import os


'''
Input : Dictionary { 스트리머 : [5개 채팅의 서로 다른 유저목록] }
Output : mode (0) = 유저목록 중 몇퍼센트가 팔로워인가 ? 
         mode (1) = [5개 채팅의 서로 다른 유저목록 중 팔로워목록 리스트]
'''


def intersect(dictionary, mode=1):

    output = dict()
    ratio = dict()

    for streamer, userlist in dictionary.items():

        # TODO 호출필요
        # if from_to == "from", get ids 'user following'
        # if from_to == "to", get ids 'following user'
        streamerID = get_id_by_name(streamer)
        followers = getFollows(streamerID, from_to="from")
        # ['abc', 'a1', ...]

        intersect = list()
        countFollowers = 0
        totalUser = len(userlist)

        # Check each follower if is in userlist
        for eachFollower in followers:
            if eachFollower in userlist:
                intersect.append(eachFollower)
                countFollowers += 1

        output[streamer] = intersect
        ratio[streamer] = round(countFollowers/totalUser) * 100

    # mode (0) = 유저목록 중 몇퍼센트가 팔로워인가 ?
    if mode == 0:

        return ratio

    # mode (1) = [5개 채팅의 서로 다른 유저목록 중 팔로워목록 리스트]
    elif mode == 1:

        return output

