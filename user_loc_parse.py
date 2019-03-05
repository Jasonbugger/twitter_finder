#从推特中按用户提取地理位置，找出出现次数最多的地理位置，作为用户的位置
#利用geppy库解析出中心坐标作为用户坐标，将用户坐标反写回用户数据库
from geopy.geocoders import Nominatim
from LoadInDB import TweetInfo, TUser, Hashtag
from collections import Counter

user_locs = {}
final_loc = {}
user_hashtag = {}
hashtag_user = {}
for a in TweetInfo.objects.all():
    if a.user_id in user_locs:
        if a.city in user_locs[a.user_id]:
            continue
        else:
            user_locs[a.user_id].append(a.city)
    else:
        user_locs[a.user_id] = [a.city]
    if a.user_id not in user_hashtag:
        user_hashtag[a.user_id] = []
    for i in a.hashtags:
        if i not in user_hashtag[a.user_id]:
            user_hashtag[a.user_id].append(i)
    for i in a.hashtags:
        if i not in hashtag_user:
            hashtag_user[i] = {'user_id': [], 'twitter_id': []}
        if a.user_id not in hashtag_user[i]['user_id']:
            hashtag_user[i]['user_id'].append(a.user_id)
        if a.ID not in hashtag_user[i]['twitter_id']:
            hashtag_user[i]['twitter_id'].append(a.ID)

# for i in hashtag_user:
#     try:
#         hashtag = Hashtag(
#             hashtag=i,
#             user_id=hashtag_user[i]['user_id'],
#             twitter_id=hashtag_user[i]['twitter_id']
#         )
#         hashtag.save()
#     except:
#         continue
geolocator = Nominatim()
for i in user_locs:
    word_counts = Counter(user_locs[i])
    final_loc[i] = word_counts.most_common(1)[0]
    user = TUser.objects(ID=i).first()
    try:
        address = geolocator.geocode(final_loc[i][0])
        print(i)
        print(address.longitude)
        print(address.latitude)
        user.lon = address.longitude
        user.lat = address.latitude
        user.save()
    except:
        continue

