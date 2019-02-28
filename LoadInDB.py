# 将整理得到的数据写入数据库
from mongoengine import Document, connect, IntField, ListField, StringField, FloatField
import math
import random
import json
connect('tweet', host='localhost', port=27017)

# 定义表项
class TUser(Document):
    ID = IntField(required=True, unique=True)
    name = StringField(max_length=50)
    location = ListField(StringField(max_length=50), max_length=50)
    age = ListField(FloatField())
    gender = FloatField()
    emotion = ListField(FloatField())
    # emotion_positive = IntField()
    # emotion_negative = IntField()
    # emotion_anger = IntField()
    # emotion_anticipation = IntField()
    # emotion_disgust = IntField()
    # emotion_fear = IntField()
    # emotion_joy = IntField()
    # emotion_sadness = IntField()
    # emotion_surprise = IntField()
    # emotion_trust = IntField()
    character = ListField(FloatField())

    # character_A = FloatField()
    # character_C = FloatField()
    # character_E = FloatField()
    # character_N = FloatField()
    # character_O = FloatField()
    emotion_tweet = IntField()
    character_tweet = IntField()
    age_tweet = IntField()
    gender_tweet = IntField()
    total_tweet = IntField()
    meta = {
        'indexes': ['ID', 'location']
    }

    def __str__(self):
        return str(self.ID)

    def modify(self):
        self.age = [round(math.fabs(self.age[a]), 4)*(-1 if self.age[a] < 0 else 1) for a in range(4)]
        self.emotion = self.emotion[:2] + \
                    [round(self.emotion[a] / (self.total_tweet+1), 2) for a in range(2, 10)]
        x = sum(self.emotion[2:])+1
        self.emotion = self.emotion[:2] + \
                    [round(self.emotion[a] / x, 2) for a in range(2, 10)]
        self.character = [round(self.character[a] / (self.total_tweet+1), 2) for a in range(5)]
        self.gender = round(self.gender / (self.total_tweet + 1), 2)
    
    @staticmethod
    def find(user_type, user_info):
        user_list = []
        user = None
        if user_type == 'name':
            print('name')
            try:
                user = TUser.objects(name=user_info)
            except:
                return None
        elif user_type == 'id':
            try:
                user_info = int(user_info)
                user = TUser.objects(ID=user_info)
            except:
                return None
        if user:
            for i in user:
                user_list.append(i.ID)
            user = user.first()
            user.modify()
        return user

    def return_characters(self):
        return [self.character, self.character_tweet]
    
    @staticmethod
    def itter():
        for i in TUser.objects.all():
            yield i

    def find_loc_by_hashtag(self, hashtag):
        tag = 1
        if tag == 1:
            loc = []
            for i in range(1000000):
                loc.append([random.random() * 360 - 180, random.random() * 160 - 80])
        else:
            loc = []
            for i in self.objects(hashtags=hashtag):
                loc.append(i.lon)
                loc.append(i.lat)
        return loc


class Tweet_Info(Document):
    ID = IntField(required=True, unique=True)
    hashtags = ListField(StringField(max_length=50),max_length=20)
    city = StringField(max_length=100)
    user_id = IntField()
    lat = FloatField()
    lon = FloatField()
    meta = {
        'indexes': ['user_id']
    }

    def __str__(self):
        return str(self.ID) + "\n\t"+str(self.hashtags)+"\n\t"+self.city+"\n\t"+str(self.X)+","+str(self.Y)

    # 整理成json格式
    def find_loc_by_hashtag(self, hashtag):
        tag = 1
        # 测试模块
        if tag == 1:
            loc = []
            for i in range(100):
                loc.append([random.random()*360-180, random.random()*160-80,random.randint(1, 10)])
            
        else:
            loc = []
            for i in self.objects(hashtags = hashtag):
                loc.append(i.lon)
                loc.append(i.lat)
        return loc


# 写入用户数据
def load_user_in_DB(src_path):
    with open(src_path, 'r', encoding='utf-8') as f:
        for a in f:
            a = a[:-1]
            try:
                a = eval(a)
            except:
                print('not a dict')
                continue
            user_id = [x for x in a][0]
            user = TUser(ID=user_id,
                        name=a[user_id]['name'] if a[user_id]['name'] != [['']] else ["NoName"],
                        location=a[user_id]['location'] if a[user_id]['location'] else ["NoLocation"],
                        age=a[user_id]['age'],
                        gender=a[user_id]['gender'],
                        emotion=a[user_id]['emotion'],
                        character=a[user_id]['character'],
                        age_tweet=a[user_id]['age_tweet'],
                        gender_tweet=a[user_id]['gender_tweet'],
                        emotion_tweet=a[user_id]['emotion_tweet'],
                        character_tweet=a[user_id]['character_tweet'],
                        total_tweet=a[user_id]['total_tweet'])

            print(user_id)
            user.save()