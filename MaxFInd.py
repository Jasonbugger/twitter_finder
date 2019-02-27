# 归一化，用户间同一属性可比，用户同类属性可比
# 用户同类属性的处理用总条数除，再除以最大值，是整体属性归一化
# 找到各最大值即可
import math
with open("E:\\merage6\\users9", 'r', encoding='utf-8') as f:
    M = {'gender': 0,
           'emotion': [0]*10,
           'character': [0]*5,
           'age': [0]*4}
    L = {'gender': 0,
           'emotion': [0]*10,
           'character': [0]*5,
           'age': [0]*4}
    counter = 0
    mg = [0]*10
    for a in f:
        a = a[:-1]
        try:
            a = eval(a)
        except:
            print('not a dict')
            continue
        id = [x for x in a][0]
        a = a[[x for x in a][0]]
        counter += 1
        M['gender'] = max([math.fabs(a['gender']), M['gender']])
        L['gender'] += math.log2(math.fabs(a['gender'])+1)* (-1 if a['gender']<0 else 1)
        for i in range(4):
            M['age'][i] = max([math.fabs(a['age'][i]), M['age'][i]])
            L['age'][i] += math.log2(math.fabs(a['age'][i])+1)* (-1 if a['age'][i]<0 else 1)
        for i in range(10):
            M['emotion'][i] = max([math.fabs(a['emotion'][i]), M['emotion'][i]])
            if M['emotion'][i] == a['emotion'][i]:
                mg[i] = id
            L['emotion'][i] += math.log2(math.fabs(a['emotion'][i])+1)
        for i in range(5):
            if a['character'][i]>0:
                print(id)
            M['character'][i] = max([math.fabs(a['character'][i]), M['character'][i]])
            L['character'][i] += math.log2(math.fabs(a['character'][i])+1) * (-1 if a['character'][i]<0 else 1)
    L['gender'] = L['gender']/math.log2(M['gender'])/counter
    for i in range(4):
        L['age'][i] = L['age'][i]/math.log2(max(M['age']))/counter
    for i in range(10):
        L['emotion'][i] = L['emotion'][i]/math.log2(max(M['emotion'][2:]))/counter
    for i in range(5):
        L['character'][i] = L['character'][i] / math.log2(max(M['emotion']))/counter
    print("M:", M)
    print("L:", L)
    print(mg)
