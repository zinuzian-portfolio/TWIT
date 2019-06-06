import subprocess
import os
import sys
import platform
import requests
from api.apiHandler import getApikey

'''
    # tcd 를 사용하기 위해 셋팅이 필요
    #
    # python 3.7 이상으로 tcd를 설치(이전 버전에서는 동작하지 않음)
    # git clone https://github.com/PetterKraabol/Twitch-Chat-Downloader
    # cd Twtich-Chat-Downloader
    # python3 setup.py build
    # sudo python3 setup.py install
'''


def getTwitchChat(videoID, savePath):

    # Define chatlog path
    chatLogPath = os.path.join(savePath, str(videoID) + ".txt")

    if os.path.isfile(chatLogPath):
        print("Chatlog already exists ! ")
        return chatLogPath

    system = platform.system()
    if system == "Linux":
        if savePath[-1] != '/':
            savePath = savePath + '/'

        proc = ["sudo", "tcd",
                "-v", videoID,
                "--output", savePath,
                ]
    elif system == "Windows":
        if savePath[-1] != '\\':
            savePath = savePath + '\\'

        proc = ["tcd",
                "-v", videoID,
                "--output", savePath,
                ]
    else:
        print("Cannot detect operating system...")
        return None

    try:
        subprocess.check_call(proc)
        print("twitch chat download finish!")
        print("this file downloaded in ", savePath)

        return chatLogPath

    except subprocess.CalledProcessError as e:
        print("Twitch chat download failed: ", e)
        return None


def checkArgument(argv):
    # If there is no argument
    if len(argv) is 1:
        print('You need "urllists.txt"')
        quit()
    elif len(argv) > 2:
        print('There are more than 2 arguments')
        quit()
    elif argv[1] != 'urllists.txt':
        print('You need "urllists.txt"')
        quit()
    else:
        return argv[1]


def readText(filename):

    with open(os.getcwd() + "/urllists.txt", 'r', encoding='utf-8') as ins:
        array = []
        for line in ins:
            li = line.strip()
            line = line.strip()

            if len(line) < 1:
                continue

            array.append(line)

    urllists = dict()
    videoid_List = list()
    streamer_List = list()

    # Get all video lists
    for eachurl in array:
        videoid = eachurl.split('/')
        videoid_List.append(videoid[-1])

    # Get all distinct streamer names
    for eachVideo in videoid_List:
        streamerName = getStreamerName(eachVideo)
        streamer_List.append(streamerName)
    streamer_List = list(set(streamer_List))

    # Define dictionary = { streamer's Name : [video1, video2] , ...}
    data = dict((eachStreamer, []) for eachStreamer in streamer_List)

    for eachVideo in videoid_List:
        streamerName = getStreamerName(eachVideo)
        data[streamerName].append(eachVideo)

    return data


def getStreamerName(videoId):
    # API요청을 보내기 위한 헤더
    TWITCH_CLIENT_ID = getApikey()
    TWITCH_CLIENT_ID_HEADER = "Client-ID"
    TWITCH_V5_ACCEPT = "application/vnd.twitchtv.v5+json"
    TWITCH_V5_ACCEPT_HEADER = "Accept"
    TWITCH_AUTHORIZATION_HEADER = "Authorization"

    VIDEO_URL = "https://api.twitch.tv/kraken/videos/" + videoId

    headers = {TWITCH_CLIENT_ID_HEADER: TWITCH_CLIENT_ID,
               TWITCH_V5_ACCEPT_HEADER: TWITCH_V5_ACCEPT}

    # API request
    video_request = requests.get(VIDEO_URL, headers=headers)
    video_request_json = video_request.json()

    # Get streamerName
    streamerName = str(video_request_json['channel']['name'])

    return streamerName


def download(urllists):
    # FOR TEST
    print(urllists)
    for name, videoId in urllists.items():

        for eachVideoId in videoId:
            savepath = os.path.join(os.getcwd(), os.path.join('data', name))
            getTwitchChat(eachVideoId, savepath)


def initiate():

    filename = checkArgument(sys.argv)
    urllists = readText(filename)
    download(urllists)


if __name__ == "__main__":
    initiate()
