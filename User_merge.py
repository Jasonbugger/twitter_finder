#用户内容合并
import os
import sys


def read_a_file(path):
    users = {}
    with open(path, 'r', encoding='utf=8') as f:
        for a in f:
            a = a[:-1]
            try:
                a = eval(a)
            except:
                print("not a dict")
                continue
            id = [x for x in a][0]
            users[id] = a[id]
    return users


def merage(total_users, users_in_a_file):
    for m in users_in_a_file:
        if m not in total_users:
            total_users[m] = users_in_a_file[m]
        else:
            orginal_data = total_users[m]
            add_data = users_in_a_file[m]
            orginal_data['age'] = [orginal_data['age'][z] + add_data['age'][z] for z in range(4)]
            orginal_data['emotion'] = [orginal_data['emotion'][z] + add_data['emotion'][z] for z in range(10)]
            orginal_data['character'] = [orginal_data['character'][z] + add_data['character'][z] for z in range(5)]
            orginal_data['gender'] += add_data['gender']
            orginal_data['emotion_tweet'] += add_data['emotion_tweet']
            orginal_data['character_tweet'] += add_data['character_tweet']
            orginal_data['age_tweet'] += add_data['age_tweet']
            orginal_data['gender_tweet'] += add_data['gender_tweet']
            for j in add_data['user_screen_name']:
                if j not in orginal_data['user_screen_name']:
                    orginal_data['user_screen_name'].append(j)
            for j in add_data['location']:
                if j not in orginal_data['location']:
                    orginal_data['location'].append(j)
            total_users[m] = orginal_data
    return total_users


def get_file_list(path):
    file_list = os.listdir(path)
    file_list = [path+"\\"+a for a in file_list]
    return file_list


def save(path, total_users, i):
    try:
        os.mkdir(path)
    except:
        a = 1
    with open(path + 'users' + str(i), 'w') as f:
        for j in total_users.keys():
            f.write('{' + str(j) + ':' + str(total_users[j]) + '}\n')


if __name__ == '__main__':
    total_users = {}
    root = sys.argv[1]
    for i in get_file_list(root):
        try:
            users = read_a_file(i)
            total_users = merage(total_users, users)
        except:
            print("{} crashed".format(i))
            continue

    save("E:\\merage\\", total_users, root.split('_')[-1].replace('\\', ''))
    print(root, "load over")
