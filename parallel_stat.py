import subprocess
import os
import re
import time
import queue

pattern = re.compile(r'^[0-9]$')
processes = []
scripts = []

if __name__ == '__main__':
    l = os.listdir("E:\\users\\")
    l = ["E:\\users\\"+a+"\\" for a in l]
    counter = 0
    temp = []
    lista = []
    for i in l:
        temp.append(i)
        counter += 1
        if counter == 6:
            lista.append(temp)
            temp = []
            counter = 0
    lista.append(temp) if temp else None
    a = 0
    for i in lista:
        print("round %d" % a, time.asctime(time.localtime(time.time())))
        pythons = []
        for j in i:
            p = subprocess.Popen(['python', ['User_merge.py ', j]])
            pythons.append(p)
        for j in pythons:
            j.wait()
        a += 1
