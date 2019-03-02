# 用户数据统计
from users_stat import read_tweet
import json
import os
import datetime

# 从内容中获取用户位置
def user_location_get(content):
    if 'geo_enabled' in content['user'] and 'location' in content['user'] and content['user']['geo_enabled']:
        location = content['user']['location']
        return [location]
    return []


# 从内容汇总获取推特位置
def tweet_location_get(content):
    if 'geo' in content:
        geo = content['geo']['coordinates']
        location = [geo[1], geo[0]] if content['geo']['type'] == 'point' else geo[0][0]
    elif 'coordinates' in content:
        geo = content['coordinates']['coordinates']
        location = [geo[1], geo[0]] if content['coordinates']['type'] == 'point' else geo[0][0]
    elif 'place' in content:
        temp = content['place']
        try:
            geo = temp['bounding_box']['coordinates']
        except:
            return []
        location = [geo[1], geo[0]] if temp['bounding_box']['type'] == 'point' else geo[0][0]
    else:
        location = []
    return location


# 获取推特城市位置
def tweet_city_get(content):
    city = ""
    if 'place' in content:
        city = content['place']['country']+","+content['place']['full_name']
    return city


# 判断某条内容是否有hashtag
def has_hashtag(content):
    if content['hashtags']:
        return [x['text'] for x in content['hashtags']]
    return []


# 推特位置信息和hashtag获取
def parse_hashtag_and_loc(content: dict):
    tweet = {}
    hashtag = has_hashtag(content)
    location = tweet_location_get(content)
    if hashtag and location:
        city = tweet_city_get(content)
        tweet['id'] = content['id']
        tweet['location'] = location
        tweet['city'] = city
        tweet['hashtags'] = hashtag
        tweet['user_id'] = content['user']['id']
    return tweet


# 用户信息收集
def parse_user_info(content: dict):
    if content['lang'] != 'en':
        return None
    age = content['age'] if 'age' in content else [0]*4
    gender = content['gender'] if 'gender' in content else [0]
    user_id = content['user']['id'] if 'user' in content and 'id' in content['user'] else 0
    name = content['user']['name'] if 'user' in content and 'name' \
                                                            in content['user'] else ""
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
    #                    a = abs(sum(emotion))
    #                    for i in range(len(emotion)):
    #                        emotion[i] /= a
    if sum(character):
        character_tweet = 1
    #                    a = abs(sum(character))
    #                    for i in range(len(character)):
    #                            character[i] /= a
    if sum(age):
        age_tweet = 1
    #                    a = abs(sum(age))
    #                    for i in range(len(age)):
    #                        age[i] /= a
    if gender:
        gender_tweet = 1

    user = {'user_id': user_id, 'age': age, 'gender': gender, 'name': name,
                'emotion': emotion, 'location': location, 'character': character, 'emotion_tweet': emotion_tweet,
                'character_tweet': character_tweet, 'age_tweet': age_tweet, 'gender_tweet': gender_tweet, 'total_tweet': 1}
    return user


# 储存用户信息
def save_user(path: str, users: dict):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
        print('dir has made')
    with open(path, 'w', encoding='utf-8') as f:
        for i in users:
            temp = users[i]
            try:
                f.write(str(temp))
                f.write('\n')
            except:
                print(temp)


# 储存推特内容
def save_tweet(path: str, tweets: list):
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
        print('dir has made')
    with open(path, 'w', encoding='utf-8') as f:
        for i in tweets:
            try:
                f.write(str(i))
                f.write('\n')
            except:
                print(i)


# 基本并行单元:获取推文基本信息
def tweet_info_get(src_path: str, dst_path: str):
    print("start"+src_path)
    start_time = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    if not os.path.exists(src_path):
        print("no such file"+src_path)
        return
    tweet = []
    if not os.path.exists(os.path.dirname(dst_path)):
        print("the document " + os.path.dirname(dst_path) + "creating ...")
        os.makedirs(os.path.dirname(dst_path))

    for content in read_tweet(src_path, dst_path):
        try:
            info = parse_hashtag_and_loc(content)
        except:
            print(" an error has occured during load file " + src_path)
            print(info)
            raise ValueError
        if info:
            tweet.append(info)
    print('saving')
    save_tweet(dst_path, tweet)
    end_time = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print(src_path+"read over")
    print("start at " + str(start_time))
    print("end at " + str(end_time))


# 基本并行单元：获取用户信息
def user_info_get(src_path: str, dst_path: str):
    start_time = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    if not os.path.exists(src_path):
        print("no such file"+src_path)
        return
    users = {}
    if not os.path.exists(os.path.dirname(dst_path)):
        os.makedirs(os.path.dirname(dst_path))
    for content in read_tweet(src_path, dst_path):
        try:
            user = parse_user_info(content)
        except:
            raise ValueError
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
                    for loc in user['location']:
                        if loc not in users[user_id]['location']:
                            users[user_id]['location'].append(user['location'])

                    users[user_id]['gender'] += user['gender']
                    users[user_id]['gender_tweet'] += user['gender_tweet']
                    users[user_id]['total_tweet'] += 1
        else:
            continue
    save_user(dst_path, users)
    end_time = datetime.datetime.now().strftime("%Y.%m.%d-%H:%M:%S")
    print(src_path+"read over")
    print("start at " + str(start_time))
    print("end at " + str(end_time))


if __name__ == '__main__':
    src = "F:\\user_profiles\\data4_35\\0"
    dst = "E:\\0"
    tweet_info_get(src, dst)
