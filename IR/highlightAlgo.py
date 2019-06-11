
import subprocess
import os
import re
import platform
import shutil

from IR.chatAnalyze import ChatAnalyze, normalizing


# Parameter description
# 1. streamer : a streamer's name listed in our data
# 2. numOfHighlights : the number of expected highlights for each chatlog
# 3. cummulative_sec : how many next seconds you want to consider for chat analyzing
# 4. delay : how long each highlight section is suppposed to be


def makeHighlightBystreamer(streamer, numOfHighlights, cummulative_sec, delay):

    # Global labeled words
    labeldwords = ['pog', 'poggers', 'pogchamp', 'holy', 'shit', 'wow', 'ez', 'clip', 'nice',
                   'omg', 'wut', 'gee', 'god', 'dirty', 'way', 'moly', 'wtf', 'fuck', 'crazy',
                   'omfg', 'kappa', 'trihard', '4head', 'cmonbruh', 'lul', 'haha', 'sourpls',
                   'feelsbadman', 'feelsgoodman', 'gachigasm',  'monkas', 'pepehands',
                   'destructroid', 'jebaited']

    # 1. Initiate class instance for getting highlights
    chat_analyzer = ChatAnalyze(streamer, labeldwords)

    # 2. Get chatlog list by the given streamer
    chatlogList = chat_analyzer.getChatlogs()
    # 3. Get each chatlog's highlight
    iteration = 1

    for eachChatlog in chatlogList:
        print("============================================")

        f = open(eachChatlog, 'r', encoding=('UTF8'))

        score = chat_analyzer.Preprocessing(f)

        f.close()

        videoLen = ChangeToSecond(chat_analyzer.returnLasttime())

        result = chat_analyzer.Scoring(score)

        sectioned_result = chat_analyzer.Sectioned_Scoring(
            result, cummulative_sec)

        sorted_list = sorted(sectioned_result.items(),
                             key=lambda t: t[1], reverse=True)[:numOfHighlights]

        sorted_list = dict(sorted([(t, v) for t, v in sorted_list]))

        print("")
        print("[({}) : Chat analyze result]".format(iteration))

        iteration += 1
        print(sorted_list)

        highlightlist = getTimeSection(sorted_list, videoLen, delay)
        print("")
        print(" << Highlight result for the chatlog {} belonged to '{}' >>".
              format(eachChatlog, streamer))
        print(highlightlist)


def ChangeToSecond(timestamp):
    arr = re.split(":", timestamp)

    if len(arr) != 3:
        print("check time string :"+timestamp)
    else:
        return int(arr[0].replace("[", ""))*3600 + int(arr[1])*60 + int(arr[2].replace("]", ""))
    return -1


def ChangeToTime(timestamp):

    hour = int(timestamp/3600)
    minute = int((timestamp % 3600)/60)
    second = int(timestamp % 60)

    return str(hour).zfill(2)+":"+str(minute).zfill(2)+":"+str(second).zfill(2)


def getTimeSection(candidatesList, videoLen, delay):
    # make raw candidate list (must be sorted by key)
    candidates = list()

    for k in candidatesList.keys():
        candidates.append(ChangeToSecond(k))

    # if picked points are too close
    mergeList = {}
    deleteList = []
    for i in range(len(candidates)):
        if i in deleteList:
            continue
        else:
            mergeList[candidates[i]] = candidates[i]
            j = 1
            while i+j < len(candidates) and candidates[i+j] - candidates[i] < delay:
                deleteList.append(i + j)
                # ex) 300: 310 -> 300: 320 -> 300: 330
                mergeList[candidates[i]] = candidates[i+j]
                j += 1

    print("Merge List : ", end=' ')
    print(mergeList)
    print("Will be deleted : ", end=' ')
    print(deleteList)

    for i in deleteList:
        candidates[i] = -1

    candidates = [[i-2*delay, mergeList[i]] for i in candidates if i != -1]

    # post-processing
    for i in range(len(candidates)):
        if candidates[i][0] < 0:
            candidates[i][0] = 0
        if candidates[i][1] > videoLen:
            candidates[i][1] = videoLen

    # post-processing (change to time)
    output = list()
    for cand in candidates:
        start = ChangeToTime(cand[0])
        end = ChangeToTime(cand[1])

        output.append([start, end])

    return output
