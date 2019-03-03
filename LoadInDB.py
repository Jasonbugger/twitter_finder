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
    location = ListField(StringField(max_length=200), max_length=50)
    age = ListField(FloatField())
    gender = FloatField()
    emotion = ListField(FloatField())
    character = ListField(FloatField())
    emotion_tweet = IntField()
    character_tweet = IntField()
    age_tweet = IntField()
    gender_tweet = IntField()
    total_tweet = IntField()
    lat = FloatField()
    lon = FloatField()
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
    
    @staticmethod
    def find_loc_by_hashtag(hashtag, attr):
        print(attr)
        index = int(attr[-1])
        attr = attr[:-1]
        tag = 1
        # 测试模块
        loc = []
        if tag == 1:
            for i in range(1000):
                loc.append([random.random()*360-180, random.random()*160-80, random.random()*5])
        else:
            if hashtag == '#all':
                for i in TUser.objects.all():
                    if attr=="gender":
                        loc.append([i.lon,i.lat,i.__getattribute__(attr)])
                    else:
                        loc.append([i.lon,i.lat,i.__getattribute__(attr)[index]])
            else:
                for i in TUser.objects(hashtags=hashtag):
                    if attr=="gender":
                        loc.append([i.lon,i.lat,i.__getattribute__(attr)])
                    else:
                        loc.append([i.lon,i.lat,i.__getattribute__(attr)[index]])
        return loc


class TweetInfo(Document):
    ID = IntField(required=True, unique=True)
    hashtags = ListField(StringField(max_length=50),max_length=20)
    city = StringField(max_length=100)
    user_id = IntField()
    lat = FloatField()
    lon = FloatField()
    meta = {
        'indexes': ['user_id', 'ID']
    }

    def __str__(self):
        return str(self.ID) + "\n\t"+str(self.hashtags)+"\n\t"+self.city+"\n\t"+str(self.X)+","+str(self.Y)

    # 整理成json格式
    @staticmethod
    def find_loc_by_hashtag(hashtag):
        tag = 1
        # 测试模块
        loc = []
        if tag == 1:
            for i in range(1000):
                loc.append([random.random()*360-180, random.random()*160-80, random.random()])
        else:
            if hashtag == '#all':
                for i in TweetInfo.objects():
                    loc.append([i.lon, i.lat, i.city])
            else:
                for i in TweetInfo.objects(hashtags=hashtag):
                    loc.append([i.lon, i.lat, i.city])
        return loc


# 写入用户数据
def load_user_in_DB(src_path):
    with open(src_path, 'r', encoding='utf-8') as f:
        for a in f:
            a = a[:-1]
            try:
                a = eval(a)
                print('u\'' + a['name'] + '\'')
                print([eval('u\''+str(x)+'\'') for x in a['location']])
            except:
                print('not a dict')
                continue
            user_id = a['user_id']
            user = TUser(ID=user_id,
                        name='u\'' + a['name'] + '\'',
                        location=[eval('u\''+str(x)+'\'') for x in a['location']],
                        age=a['age'],
                        gender=a['gender'],
                        emotion=a['emotion'],
                        character=a['character'],
                        age_tweet=a['age_tweet'],
                        gender_tweet=a['gender_tweet'],
                        emotion_tweet=a['emotion_tweet'],
                        character_tweet=a['character_tweet'],
                        total_tweet=a['total_tweet'])

            user.save()


if __name__ == "__main__":
    load_user_in_DB("E:\\final_user_data\\0")