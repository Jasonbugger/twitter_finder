import users_stat
import sys
import time
import json
import os

def user_location_get(content):
    if 'geo_enabled' in content['user'] and 'location' in content['user'] and content['user']['geo_enabled']:
        location = content['user']['location']
        # name = content['user']['name']
        return [content['user']['id'], location]
    return None


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


def tweet_city_get(content):
    if 'place' in content:
        city = content['place']['country']+content['place']['full_name']
    return city


def has_hashtag(content, hashtag_list):
    for hashtag in content['hashtags']:
        if hashtag['text'] in hashtag_list:
            print("catch hashtag" + hashtag['text'])
            return True
    return False


def save_user_loc(path: str, user_loc: dict):
    with open(path, 'w', encoding = 'utf-8') as f:
        for i in user_loc:
            temp = {'id': i, 'loc': user_loc[i]}
            json.dump(temp, f, ensure_ascii=False)
            f.write('\n')


def save_tweet(path: str, tweets: dict):
    with open(path, 'w', encoding = 'utf-8') as f:
        for i in tweets:
            temp = {'id': i, 'content': tweets[i]['content']}
            json.dump(temp, f, ensure_ascii=False)
            f.write('\n')


if __name__ == '__main__':
    hashtag_list = ['terroism', 'islamic', 'isis', 'saudi', 'muslims', 'islam', 'counterterrorism', 'islamicterrorism',\
                    'terrorists', 'domesticterrorism']
    path = sys.argv[1]
    path_dst = sys.argv[2]
    print(path, "start\t", time.asctime(time.localtime(time.time())))
    path_dst1 = path_dst + "\\" + 'user' + "\\"
    path_dst2 = path_dst + "\\" + "tweet" + "\\"
    print("will generate ", path_dst)
    if not os.path.exists(path_dst):
        os.mkdir(path_dst)
    if not os.path.exists(path_dst1):
        os.mkdir(path_dst1)
    if not os.path.exists(path_dst2):
        os.mkdir(path_dst2)
    for x in range(5):
        path1 = path_dst1+str(x)+'.json'
        path2 = path_dst2+str(x)+'.json'
        if os.path.exists(path1):
            continue
        user_location = {}
        tweets = {}
        for content in users_stat.Read_tweet(x, path1, path):
            # try:
            item = user_location_get(content)
            if item:
                user_location[item[0]] = item[1]
            # except:
            #     print('error location')
            #     flag = 1
            if has_hashtag(content, hashtag_list):
                if content['id'] not in tweets:
                    tweets[content['id']] = {}
                tweets[content['id']]['content'] = content

        save_user_loc(path1, user_location)
        save_tweet(path2, tweets)
    print(path, "end\t", time.asctime(time.localtime(time.time())))
