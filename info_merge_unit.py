import os
import shutil
from info_parse import save_user, save_tweet

#用户信息读取
def read_info(src_path):
    if os.path.exists(src_path):
        with open(src_path,'r') as f:
            for i in f:
                try:
                    i = eval(i)
                except:
                    raise ValueError
                yield i
# 合并用户信息
def add_user_info(user, users):
    user_id = user['user_id']
    for i in range(len(user['age'])):
        users[user_id]['age'][i] += user['age'][i]
        users[user_id]['age_tweet'] += user['age_tweet']

    for i in range(len(user['emotion'])):
        users[user_id]['emotion'][i] += user['emotion'][i]
    users[user_id]['emotion_tweet'] += user['emotion_tweet']

    for i in range(len(user['character'])):
        users[user_id]['character'][i] += user['character'][i]
    users[user_id]['character_tweet'] += user['character_tweet']

    if user['location'] not in users[user_id]['location']:
        users[user_id]['location'].append(user['location'])
    if user['name'] not in users[user_id]['name']:
        users[user_id]['name'].append(user['name'])

    users[user_id]['gender'] += user['gender']
    users[user_id]['gender_tweet'] += user['gender_tweet']
    users[user_id]['total_tweet'] += 1

#用户信息合并
def merge_user(src_path_list, dst_path):
    users = {}
    for src_path in src_path_list:
        for user in read_info(src_path):
            if user:
                user_id = user['user_id']
                if user_id not in users:
                    users[user_id] = user
                else:
                    add_user_info(user,users)
            else:
                continue
    save_user(dst_path, users)


#推特信息合并
def merge_tweet(src_path_list, dst_path):
    tweets = []
    for src_path in src_path_list:
        for tweet in read_info(src_path):
            if tweet:
                tweets.append(tweet)
    save_tweet(dst_path, tweets)
