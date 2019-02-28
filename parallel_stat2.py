import subprocess
import os
import re
import time
import queue

pattern = re.compile(r'^[0-9]$')
processes = []
scripts = []

if __name__ == '__main__':
    l = os.listdir("E:\\merage4\\")
    l = ["E:\\merage4\\"+a for a in l]
    counter = 0
    temp = []
    inner_temp = []
    lista = []
    inner_counter = 0
    for i in l:
        inner_temp.append(i)
        inner_counter += 1
        if inner_counter == 4:
            temp.append(inner_temp)
            inner_temp = []
            inner_counter = 0
            counter += 1
        if counter == 4:
            lista.append(temp)
            temp = []
            counter = 0
    lista.append([inner_temp]) if inner_temp else None
    lista.append(temp) if temp else None
    a = 0
    print(lista)
    for i in lista:
        print("round %d" % a, time.asctime(time.localtime(time.time())))
        pythons = []
        for j in i:
            p = subprocess.Popen(['python', ['User_merge2.py ']+[x+"|"for x in j]])
            pythons.append(p)
        for j in pythons:
            j.wait()
        a += 1
