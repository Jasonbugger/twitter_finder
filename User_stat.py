import numpy as np
from matplotlib import pyplot

def get_all_users():
    Users = []
    #规定Users格式
    with open('','r',encoding='utf-8') as f:
        for i in f:
            Users.append(eval(i))
