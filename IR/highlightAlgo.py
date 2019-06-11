from chatAnalyze import ChatAnalyze

import subprocess
import os
import re
import platform
import shutil

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
    highlightlist = list()

    for eachChatlog in chatlogList:
        print("============================================")
        score = chat_analyzer.Preprocessing(eachChatlog)
        videoLen = ChangeToSecond(chat_analyzer.returnLasttime())
        result = chat_analyzer.Scoring(score)
        sectioned_result = chat_analyzer.Sectioned_Scoring(
            result, cummulative_sec)
        sorted_list = sorted(sectioned_result.items(),
                             key=lambda t: t[1], reverse=True)[:numOfHighlights]
        sorted_list = dict(sorted([(t, v) for t, v in sorted_list]))
        print("[{} : Chat analyze result]".format(iteration))
        iteration += 1
        print(sorted_list)

        highlightlist.append(getTimeSection(sorted_list, videoLen, delay))


def ChangeToSecond(timestamp):
    arr = re.split("[:]", timestamp)
    if len(arr) != 3:
        print("check time string :"+timestamp)
    else:
        return int(arr[0])*3600 + int(arr[1])*60 + int(arr[2])
    return -1


def getTimeSection(candidates, videoLen, delay):
    # make raw candidate list (must be sorted by key)
    candidates = list(candidates.keys())

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
    print("[Candidates]")
    print(candidates)

    for i in deleteList:
        candidates[i] = -1

    candidates = [[i-2*delay, mergeList[i]] for i in candidates if i != -1]

    # post-processing
    for i in range(len(candidates)):
        if candidates[i][0] < 0:
            candidates[i][0] = 0
        if candidates[i][1] > videoLen:
            candidates[i][1] = videoLen

    return candidates
