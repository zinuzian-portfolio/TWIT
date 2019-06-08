# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 10:49:01 2019

@author: user
"""

import numpy as np


def cosine_func(svdict, selected_key):
    temp_list = []
    key_list = []
    for key in svdict.keys():
        a = svdict.get(key)
        b = svdict.get(selected_key)
        temp_list.append(np.dot(a.reshape(1,-1), b.reshape(-1,1))/ ((np.sum(a**2))**(1/2) + np.sum(b**2)**(1/2)))
        key_list.append(key)
    key_list = np.array(key_list)
    key_list = key_list.take(sorted(range(len(temp_list)), reverse = True, key = lambda k: temp_list[k]))
    return key_list[1:]


def distance_func(svdict, selected_key):
    temp_list = []
    key_list = []
    for key in svdict.keys():
        a = svdict.get(key)
        b = svdict.get(selected_key)
        temp_list.append(np.linalg.norm(a-b))
        key_list.append(key)
    key_list = np.array(key_list)
    key_list = key_list.take(sorted(range(len(temp_list)), reverse = False, key = lambda k: temp_list[k]))
    return key_list[1:]

