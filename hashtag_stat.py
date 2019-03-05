from LoadInDB import Hashtag

hashtags = []
counter = 0
for i in Hashtag.objects.all():
    counter += 1
    if len(i.twitter_id) > 1000 or len(i.user_id) > 500:
        hashtags.append([i.hashtag]*2)
print(len(hashtags))
print(counter)
# with open("E:\\hashtag.txt",'w',encoding='utf-8') as f:
#     f.write(str(hashtags))
#