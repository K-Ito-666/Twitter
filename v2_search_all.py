#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 23:29:52 2021

@author: kazuhiro-it
"""

import requests
import os
import json
import pprint 
import time
import pandas as pd
import numpy as np
import datetime


bearer_token = "自分のbearer_tokenをここに入れる"
search_url = "https://api.twitter.com/2/tweets/search/all"

maxid=1 #id初期化
get_size=10 #1回のリクエストで取得するtweet数（10〜500）
request_cnt=10 #リクエスト回数
usrword='愚痴' #ユーザーbioにこの文字列があったらget
word = 'の' #tweet内にこの文字列があったらget

# Optional params: start_time,end_time,since_id,until_id,max_results,next_token,
# expansions,tweet.fields,media.fields,poll.fields,place.fields,user.fields
query_params = {'expansions':'author_id',
                'query': word,
                'max_results':get_size ,
                'tweet.fields':'id',
                "user.fields":"description",
                'since_id':maxid
                }

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

def connect_to_endpoint(url, params):
    response = requests.get(url, auth=bearer_oauth, params=params)
    #print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def main(t_cnt,idx,usrname,text,userid):
    json_response = connect_to_endpoint(search_url, query_params)
    tweet = {}
    tweet = json_response
    for i in range(len(tweet['includes']['users'])):
        if usrword in tweet['includes']['users'][i]['description']:
            idx.append(tweet['data'][i]['id'])
            usrname.append(tweet['includes']['users'][i]['description'])
            text.append(tweet['data'][i]['text'])
            userid.append(tweet['includes']['users'][i]['id']) 
            t_cnt += 1
    return t_cnt


idx=[]
usrname=[]
text=[]
userid=[]
t_cnt = 0
for cnt in range(request_cnt):
    if __name__ == "__main__":
        t_cnt = main(t_cnt,idx,usrname,text,userid)
    if len(idx) > 0:
        maxid = int(idx[-1])+1
    time.sleep(1)
    print(t_cnt)
    
    query_params = {'expansions':'author_id',
                    'query': word,
                    'max_results':get_size ,
                    'tweet.fields':'id',
                    "user.fields":"description",
                    'since_id':maxid
                    }


print("抽出数:" + str(t_cnt))
df = pd.DataFrame()
df["id"]=np.array(idx)
df["text"]=np.array(text)
df["description"]=np.array(usrname)
df['userid']=np.array(userid)

dt_now = datetime.datetime.now()

df.to_excel("tweet" + str(dt_now.strftime('%m%d_%H%M%S')) + ".xlsx")
