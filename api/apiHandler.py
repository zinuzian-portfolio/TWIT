import urllib3
import certifi
import json
import urllib.parse as urlparse
from urllib.parse import urlencode
import time

http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where())

f = open("./api_key", 'r')
API_KEY = f.readline()
f.close()

def build_get_follow_url(user_id, from_to):
    url = "https://api.twitch.tv/helix/users/follows?first=100&"
    from_to_param_name = ""
    if from_to == "from":
        from_to_param_name = "from_id"
    else:
        from_to_param_name = "to_id"
    url = url + from_to_param_name + "=" + user_id
    return url

def change_url_pagination(url, pagination):
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query['after'] = pagination['cursor']
    url_parts[4] = urlencode(query)
    return urlparse.urlunparse(url_parts)

# get top 500 follows (리퀘스트 너무 많이 보내면 거절당해서 500개만 가져옴)
# if from_to == "from", get ids 'user following'
# if from_to == "to", get ids 'following user'
def getFollows(user_id, from_to):
    follows = list()
    url = build_get_follow_url(user_id, from_to)
    header = {'Client-ID': API_KEY}
    response = http.request(
        'GET',
        url,
        headers = header
    )
    response_dict = json.loads(response.data.decode('utf-8'))
    total = response_dict["total"]
    data = response_dict["data"]
    for follow_info in data:
        follows.append(follow_info["from_id"])
    pagination = response_dict["pagination"]

    loop_count = (int(total)-1)//20
    if loop_count > 4:
        loop_count = 4
    for loop_iterator in range(loop_count):
        url = change_url_pagination(url, pagination)
        # if there is no timeout, response will be 429 (too many request)
        print("#" + str(loop_iterator+1))
        response = http.request(
            'GET',
            url,
            headers = header
        )
        response_dict = json.loads(response.data.decode('utf-8'))
        print(response_dict)
        total = response_dict["total"]
        data = response_dict["data"]
        for follow_info in data:
            follows.append(follow_info["from_id"])
        pagination = response_dict["pagination"]
    return follows

def getApikey():
    return API_KEY

# test code
# get top 500 follows list of thijs (heartstone streamer) 
#print(getFollows('57025612','to'))