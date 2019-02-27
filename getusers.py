# 从tweet中按用户整理数据
import nltk
from dict_read_in import *
import re
import pickle
import linecache
import time

dict_pattern = re.compile(r'^{.*}$')


# 判断是否为制定模式的字串 
def is_dict(text):
    return dict_pattern.match(text)

# 读取单条信息并提取有用信息
def get_piece():
    users = {}
    total_tweet = 0
    emotion_tweet = [0]*10
    character_tweet = {'a': 0.0, 'c': 0.0, 'e': 0.0, 'n': 0.0, 'o': 0.0}
    with open('F:/twitter_users_pfofiles_calucated/40/'+str(0),'r',encoding='utf-8') as f:
        counter = 0
        while True:
            content = f.readline()
            if not content:
                break
            content = content.lower()
            if is_dict(content) is None:
                continue
            else:
                content = eval(content)
                # 只取英文内容
            if content['lang'] == 'en':
                counter += 1
                total_tweet += 1

                user_id = content['user']['id']
# 增加对用户状况的统计
# 增加对信息情况的统计
                EmotionTag = 0
                CharacterTag = 0
                emotion = content['emotion']
                character = content['character']
                for i in range(len(emotion)):
                    if emotion[i] !=0:
                        EmotionTag = 1
                        emotion_tweet[i] += 1

                for j in character.keys():
                    if character[j] != 0:
                        character_tweet[j] += 1
                        CharacterTag = 1

                if user_id not in users.keys():
                    users[user_id] = [0]*15

                if EmotionTag:
                    for i in range(len(emotion)):
                        users[user_id][i] += emotion[i]
                if CharacterTag:
                    keys = [a for a in character.keys()]
                    for j in range(len(keys)):
                        users[user_id][9+j] += character[keys[j]]
                if counter // 100000 * 100000 == counter:
                    print(time.asctime(time.localtime(time.time())))
                    print("a tweet read over",total_tweet)
                if counter == 10000000:
                    break
    print("total tweet:"+str(total_tweet))
    print("emotion tweet rate:"+str(emotion_tweet))
    print("character tweet rate"+str(character_tweet))
    print('User number',len(users))
    number = 0
    for i in users.keys():
        if sum(users[i])!=0:
            number += 1
    print("valuable rate",number/len(users))
    with open("totalusers",'w') as user:
        for i in users.keys():
            user.write(str(i)+':'+str(users[i])+'\n')

true = True
false = False
null = None
get_piece()