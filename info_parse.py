#用户数据统计
from users_stat import Read_tweet
import sys
import time
import json
import os

# 从内容中获取用户位置
def user_location_get(content):
    if 'geo_enabled' in content['user'] and 'location' in content['user'] and content['user']['geo_enabled']:
        location = content['user']['location']
        # name = content['user']['name']
        return location
    return None

# 从内容汇总获取推特位置
def tweet_location_get(content):
    if 'geo' in content:
        location = content['geo']['coordinates'] if content['geo']['type']=='point' else content['geo']['coordinates'][0]
    elif 'coordinates' in content:
        location = content['coordinates']['coordinates'] if content['coordinates']['type'] == \
                                                            'point' else content['coordinates']['coordinates'][0]
    elif 'place' in content:
        temp = content['place']
        location = temp['bounding_box']['coordinates'] if temp['bounding_box']['type'] == \
                                                          'point' else temp['bounding_box']['coordinates'][0]
    else:
        location = []
    return location

# 获取推特城市位置
def tweet_city_get(content):
    if 'place' in content:
        city = content['place']['country']+content['place']['full_name']
    return city

# 判断某条内容是否有hashtag并返回
def has_hashtag(content):
    if content['hashtags']:
        return content['hashtags']
    return []

#推特位置信息和hashtag获取
def parse_hashtag_and_loc(content:dict):
    if content['lang'] != 'en':
        return None
    tweet = {}
    hashtag = has_hashtag(content)
    if hashtag:
        location = tweet_location_get(content)
        city = tweet_city_get(content)
        tweet['id'] = content['id']
        tweet['location'] = location
        tweet['city'] = city
        tweet['hashtags'] = hashtag
        tweet['user_id'] = content['user']['id']
    return tweet

#用户信息获取
def parse_user_info(content:dict):
    if content['lang'] != 'en':
        return None
    age = content['age'] if 'age' in content else [0]*4
    gender = content['gender'] if 'gender' in content else [0]
    user_id = content['user']['id'] if 'user' in content and 'id' in content['user'] else 0
    name = content['user']['name'] if 'user' in content and 'name' \
                                                            in content['user'] else ['']
    emotion = content['emotion'] if 'emotion' in content else [0]*10
    character = content['character'] if 'character' in content else [0]*5
    location = user_location_get(content)
    temp = []
    emotion_tweet = 0
    character_tweet = 0
    age_tweet = 0
    gender_tweet = 0

    for i in character.keys():
        temp.append(character[i])
    character = temp
    temp = []
    for i in age.keys():
        temp.append(age[i])
    age = temp
    if sum(emotion):
        emotion_tweet = 1
    if sum(character):
        character_tweet = 1
    if sum(age):
        age_tweet = 1
    if gender:
        gender_tweet = 1

    user = {'user_id': user_id, 'age': age, 'gender': gender, 'name': name,
                'emotion': emotion, 'location': location, 'character': character, 'emotion_tweet': emotion_tweet,
                'character_tweet': character_tweet, 'age_tweet': age_tweet, 'gender_tweet': gender_tweet}
    return user

# 储存用户信息
def save_user(path: str, users: dict):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    with open(path, 'w', encoding = 'utf-8') as f:
        for i in users:
            temp = users[i]
            json.dump(temp, f, ensure_ascii=False)
            f.write('\n')

# 储存推特内容
def save_tweet(path: str, tweets: list):
    with open(path, 'w', encoding = 'utf-8') as f:
        for i in tweets:
            assert type(i) == type({})
            json.dump(i, f, ensure_ascii=False)
            f.write('\n')



#基本并行单元:获取推文基本信息
def tweet_info_get(src_path:str,dst_path:str):
    if not os.path.exists(src_path):
        print("no such file"+src_path)
        return 
    tweet = []
    if not os.path.exists(os.path.dirname(dst_path)):
        os.makedirs(os.path.dirname)
    for content in Read_tweet(src_path, dst_path):
        try:
            info = parse_hashtag_and_loc(content)
        except:
            raise ValueError
        if info:
            tweet.append(info)
    save_tweet(dst_path, tweet)


#基本并行单元：获取用户信息
def user_info_get(src_path:str, dst_path:str):
    if not os.path.exists(src_path):
        print("no such file"+src_path)
        return 
    users = {}
    if not os.path.exists(os.path.dirname(dst_path)):
        os.makedirs(os.path.dirname)
    for content in Read_tweet(src_path, dst_path):
        try:
            user = parse_user_info(content)
        except:
            continue
        if user:
            user_id = user['user_id']
            if user_id not in users:
                users[user_id] = user
            else:
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
        else:
            continue
    save_user(dst_path,users)