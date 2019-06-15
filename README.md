## :high_brightness: TWIT : A STREAMER RECOMMENDATION SYSTEM WITH CHAT HIGHLIGHTS


> &#9989; &#10102; We analyze Twitch chat logs &#127916;

> &#9989; &#10103; We give you back a streamer's name you may like &#128140;

> &#9989; &#10104; We deal with chat logs to get highlights &#128142;

[![Build Status](http://img.shields.io/travis/badges/badgerbadgerbadger.svg?style=flat-square)](https://travis-ci.org/badges/badgerbadgerbadger) [![Coverage Status](http://img.shields.io/coveralls/badges/badgerbadgerbadger.svg?style=flat-square)](https://coveralls.io/r/badges/badgerbadgerbadger) [![License](http://img.shields.io/:license-gpl-blue.svg?style=flat-square)](http://badges.gpl-license.org)


## Installation

**Requirements**

Programming Language: Python 3.7

Open Source SW: NLTK, TCD

Open API : Twitch API v5

Twitch-Chat-Downloader : 3.1.0 [referenc link](https://pypi.org/project/tcd/)

### Clone

- Clone this repo to your local machine using `https://github.com/twit-cau/twit-cau-development.git`

### Setup

1. Move to the repository you cloned
```bash
$ cd ../twit-cau-development
```

2. Add your Twitch key at ../api/api_key 
```bash
You need to create 'api_key' file yourself
1. First, create 'api_key.txt' and add your key
2. Second, delete the format '.txt'
```

3. Run the Python command below
```bash
$ python app.py [a streamer's name that is listed in our database]
```

## Features

> :thumbsup: TF-IDF Matrics
>> `Load and analyze the chatlogs and find traits of the streamer via TF-IDF, SVD using tf-idf-vectorizer and truncatedSVD in scikit-learn`

> :astonished: Streamer recommendation
>> `Choose one streamer we provide`
>> `See the result and check the highlights of streamer on top of the list`

- Check out [Presentation files](https://github.com/twit-cau/twit-cau-documentation)
