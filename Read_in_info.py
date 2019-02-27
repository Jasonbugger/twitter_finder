import nltk
from dict_read_in import Emolex, FCdict, gender_dict, age_dict
import re
import pickle
import linecache
import time
import sys

true = True
false = False
null = " "

dict_pattern = re.compile(r'^{.*}$')

def is_dict(text):
    return dict_pattern.match(text)

# 读取单条信息并提取有用信息
def get_piece(pathload,pathsave,number):
    total_tweet = 0
    emotion_tweet = 0
    character_tweet = 0
    with open(pathload+str(number),'rb') as f:
        output = open(pathsave+str(number),'w',encoding='utf-8')
        en_counter = 0
        counter = 0
        while True:
            content = str(f.readline()[:-1].decode('utf-8'))

            if not content:
                break
               # print(bytes(content, 'utf-8'))
               # f.seek(f.tell(), 8)
            content = content.lower()
            if is_dict(content) is None:
                print('Not dict\t'+content)
                continue
            else:
                content = eval(content)
                # 只取英文内容
                total_tweet += 1
            if content['lang'] == 'en':
                en_counter += 1
                counter += 1
                content = addinfo(content)
# 增加对用户状况的统计
# 增加对信息情况的统计
                emotion = content['emotion']
                character = content['character']
                for i in emotion:
                    if i !=0:
                        emotion_tweet += 1
                        break

                for j in character.keys():
                    if character[j] != 0:
                        character_tweet += 1
                        break
                if counter == 100000:
                    print(time.asctime(time.localtime(time.time())))
                    print("a tweet read over",en_counter,number)
                    counter = 0
                output.write(str(content)+'\n')
        output.close()
    print("total tweet:"+str(total_tweet))
    print("en_tweet:"+str(en_counter))
    print("emotion tweet rate:"+str(emotion_tweet))
    print("character tweet rate"+str(character_tweet))


# 添加情感性格计算信息
# 先不存入数据库
def addinfo(tweet: dict):
    emotion, character, age, gender = sentiment_cal(tweet)
    tweet['emotion'] = emotion
    tweet['character'] = character
    tweet['age'] = age
    tweet['gender'] = gender
    return tweet


# 计算性格和情绪
def sentiment_cal(tweet:dict):
    sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    text = tweet['text']
    sents = sent_tokenizer.tokenize(text)
    words = []
    emotion = [0]*10
    character = {'A': 0.0, 'C': 0.0, 'E': 0.0, 'N': 0.0, 'O': 0.0}
    # 注意规定的index
    age = {'13_18': 0,'19_22': 0,'23_29': 0,'30_+': 0}
    gender = 0
    for i in FCdict.keys():
        for j in FCdict[i].keys():
            if j in text:
                character[i] += FCdict[i][j]
    for i in age_dict.keys():
        for j in age_dict[i].keys():
            if j in text:
                age[i] += age_dict[i][j]
    for i in gender_dict.keys():
        if i in text:
            gender += gender_dict[i]

    for i in sents:
        words += nltk.word_tokenize(i)

    for i in words:
        if i in Emolex.keys():
            for j in range(len(emotion)):
                emotion[j] += Emolex[i][j]


    return emotion, character, age, gender



if __name__=='__main__':
    print(sys.argv)
    pathload = str(sys.argv[1])
    pathsave = str(sys.argv[2])
    number = int(sys.argv[3])
    print(time.asctime(time.localtime(time.time())))
    get_piece(pathload,pathsave,number)
    print(time.asctime(time.localtime(time.time())))
