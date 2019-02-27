# 计算相关数据分布情况
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import pylab

def get_users():
    Users = []
    with open("H:/users/" + 'users1', 'r',encoding='utf-8') as f:
        for i in f:
            user = eval(i)
            user_id = [a for a in user.keys()][0]
            user = user[user_id]
            # 预处理用户单条信息
            if sum(user['emotion']):
                for i in range(len(user['emotion'])):
                    user['emotion'][i] /= user['emotion_tweet']
            if sum(user['character']):
                for i in range(len(user['character'])):
                    user['character'][i] /= user['character_tweet']
            if sum(user['age']):
                for i in range(len(user['age'])):
                    user['age'][i] /= user['age_tweet']
            if user['gender_tweet']:
                user['gender'] /= user['gender_tweet']
            user['user_id'] = user_id
            Users.append(user)
    return Users


def data_process(user_list):
    col_name = ['13_18','19_22','23_29','30_+','Agreeableness','Conscientiousness','Extrvesion','Neuroticism','Openness'
        ,'Positive','Negative','Anger','Anticipation','Disgust','Fear','Joy','Sadness','Surprise','Trust', 'gender']
    user_content = []
    row_name = []
    for i in user_list:
        row_name.append(i['user_id'])
        content = i['age'] + i['character'] + i['emotion'] + [i['gender']]
        user_content.append(content)
    array = np.array(user_content)
    data = pd.DataFrame(array,columns = col_name, index=row_name)
    data.to_csv('users.csv')
    return data


if __name__ == '__main__':
    users = get_users()
    
    data = data_process(users)
    #data = pd.DataFrame.from_csv('users')
    bins = [0.001 * a - 0.5 for a in range(1000)]
    tags = ['Neuroticism', 'Agreeableness', 'Conscientiousness', 'Extrvesion', 'Openness']
    for i in range(1, 6):
        plt.subplot(2, 3, i)
        plt.title(tags[i-1])
        pylab.rcParams['figure.figsize'] = (15.0, 8.0)
        print(tags[i-1]+":",data[tags[i-1]].mean())
        plt.hist(data[tags[i - 1]], bins=bins)
    plt.show()