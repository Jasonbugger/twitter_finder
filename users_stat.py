import numpy as np
import os
import sys
import re

true = True
false = False
null = " "

dict_pattern = re.compile(r'^{.*}$')

def is_dict(text):
    return dict_pattern.match(text)


def Read_tweet(src_path, dst_path):
    if os.path.exists(dst_path):
        print("skip", str(src_path))
        yield None
    f = open(src_path, 'r', encoding='utf-8')
    while True:
        content = str(f.readline()[:-1])
        if not content:
            break
        content = content.lower()
        if is_dict(content) is None:
            print('Not dict\t' + content)
            yield None
        else:
            content = eval(content)
        yield content
    f.close()