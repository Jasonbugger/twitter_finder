# 数据存储结构定义
# 将整理得到的数据写入数据库
from mongoengine import Document, connect, IntField, ListField, StringField, FloatField
import math
import random
import json
connect('tweet', host='localhost', port=27017)
"""
1.用户数据：用户数据是以用户为单位整理的包括用户情绪等属性和用户id，name，地理位置等数据
结构：
    ID：int唯一标识
    screen_name：string用户名，为了简化处理，不同阶段的用户改名不考虑
    location ： list地理位置列表，考虑到后期可能扩充地理位置而准备
    age ： list利用词典得到的年龄属性：分为13-18， 19-信息， xx-xx
    gender ： list利用词典得到的性别推断，负数为男性，正数为女性
    emotion ：list利用词典得到的情绪推断，按顺序为：positive, negative, anger, anticipation
                                            , disgust, fear, joy, sadness, surprise, trust
    character :list利用词典得到的性格判断，按顺序为A,C,E,N,O
    emotion_tweet ： int，包含情绪词的推文数量
    character_tweet ： int，包含性格词的推文数量
    age_tweet ： int 包含年龄词的推文数量
    gender_tweet ： int 包含性别词汇的推文数量
    total_tweet ：int 总的推特数量

方法：
    modify()：将属性数值进行处理的函数，使之具备可比性
    find(userinfo，usertype)：查找并返回在usertype属性上值为userinfo的用户对象，目前支持的usertype有id和属性
    return_characters():返回储存的性格信息和性格相关的推特条数
    itter():迭代器，迭代返数据库中所有的对象
    find_loc_by_hashtag(hashtag,attr):根据所给的hashtag查找符合条件的用户并返回相应的属性
    load_in_db(src_path):将文件中的数据存入数据库 
"""
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

        
    # 写入用户数据
    @staticmethod
    def load_in_db(src_path):
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
                name = eval('u\'' + a['name'] + '\'')
                locations = []
                for x in a['location']:
                    locations.append(eval('u\''+str(x)+'\''))
                age = a['age']
                gender = a['gender']
                emotion = a['emotion']
                character = a['character']
                age_tweet = a['age_tweet']
                gender_tweet = a['gender_tweet']
                emotion_tweet = a['emotion_tweet']
                character_tweet = a['character_tweet']
                total_tweet = a['total_tweet']
                user = TUser(ID=user_id,
                            name=name,
                            location=locations,
                            age=age,
                            gender=gender,
                            emotion=emotion,
                            character=character,
                            age_tweet=age_tweet,
                            gender_tweet=gender_tweet,
                            emotion_tweet=emotion_tweet,
                            character_tweet=character_tweet,
                            total_tweet=total_tweet)

                user.save()


"""
2.推特数据：
结构：
    ID ：int唯一标识
    hashtags ： list：hashtag
    city ：string城市数据，格式为国家加具体位置
    user_id ：int 用户标识
    lat ：float，纬度
    lon ：float，经度
方法：
    find_loc_by_hashtag(hashtag):找到包含指定hashtag的推特并返回推特的地理坐标，初步整理为json易于转换的格式
    load_in_db(src_path):将文件中的数据存入数据库
"""
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
        return str(self.ID) + "\n\t"+str(self.hashtags)+"\n\t"+self.city+"\n\t"+str(self.lon)+","+str(self.lat)

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
                for i in TweetInfo.objects.all():
                    loc.append([i.lon, i.lat, i.city])
            else:
                for i in TweetInfo.objects(hashtags=hashtag):
                    loc.append([i.lon, i.lat, i.city])
        return loc
    # 写入用户数据
    @staticmethod
    def load_in_db(src_path):
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
                id = a['id']
                hashtags = a['hashtags']
                city = eval('u\''+a['city']+'\'')
                user_id = a['user_id']
                lon = a['location'][0]
                lat = a['location'][1]
                tweet = TweetInfo(
                    ID=id,
                    hashtags=hashtags,
                    city=city,
                    user_id=user_id,
                    lat=lat,
                    lon=lon,
                )
                tweet.save()


if __name__ == "__main__":
    TUser.load_in_db("E:\\final_user_data\\0")
    TweetInfo.load_in_db("E:\\final_data\\0")