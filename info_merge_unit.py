import os
import shutil
from info_parse import save_user, save_tweet
null = None
true = True
true = True


# 用户信息读取
def read_info(src_path):
    print(src_path)
    if os.path.exists(src_path):
        with open(src_path, 'r', encoding='utf-8') as f:
            for i in f:
                try:
                    i = eval(i[:-1])
                except:
                    print(i)
                    continue
                yield i
        print('read over' + src_path)
    return


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
    for loc in user['location']:
        if loc not in users[user_id]['location']:
            users[user_id]['location'].append(loc)
    if user['name'] != users[user_id]['name']:
        users[user_id]['name']= user['name']

    users[user_id]['gender'] += user['gender']
    users[user_id]['gender_tweet'] += user['gender_tweet']
    users[user_id]['total_tweet'] += 1
    return users


# 用户信息合并
def merge_user(src_path_list, dst_path):
    print(src_path_list)
    users = {}
    for src_path in src_path_list:
        for user in read_info(src_path):
            if user:
                user_id = user['user_id']
                if user_id not in users:
                    users[user_id] = user
                else:
                    users = add_user_info(user, users)
            else:
                continue
    save_user(dst_path, users)


# 推特信息合并
def merge_tweet(src_path_list, dst_path):
    tweets = []
    for src_path in src_path_list:
        for tweet in read_info(src_path):
            if tweet:
                tweets.append(tweet)
    save_tweet(dst_path, tweets)


if __name__ == '__main__':
    src_path_list = ['E:\\data\\data2_0\\0', 'E:\\data\\data2_0\\1', 'E:\\data\\data2_0\\2']
    dst_path = "E:\\0"
    merge_user(src_path_list, dst_path)