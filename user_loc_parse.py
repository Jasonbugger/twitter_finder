#从推特中按用户提取地理位置，找出出现次数最多的地理位置，作为用户的位置
#利用geppy库解析出中心坐标作为用户坐标，将用户坐标反写回用户数据库
import geopy
from LoadInDB import TweetInfo, TUser
import LoadInDB
from collections import Counter

user_locs = {}
final_loc = {}
for a in TweetInfo.objects.all():
    if a.user_id in user_locs:
        if a.city in user_locs[a.user_id]:
            continue
        else:
            user_locs[a.user_id].append(a.city)
    else:
        user_locs[a.user_id] = [a.city]
for i in user_locs:
    word_counts = Counter(user_locs[i])
    final_loc[i] = word_counts.most_common(1)[0]


