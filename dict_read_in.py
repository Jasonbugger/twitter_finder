#相关字典的导入
import xlrd
import csv

# 读入情感字典
def emolex_read_in()->dict:
    work_book = xlrd.open_workbook('Emolex/NRC-Emotion-Lexicon-v0.92/NRC-Emotion-Lexicon-v0.92-In105Languages-Nov2017Translations.xlsx')
    sheet = work_book.sheet_by_index(0)
    emolex_lexcion = {}

    for i in range(1,sheet.nrows):
        #Positive	Negative	Anger	Anticipation	Disgust	Fear	Joy	Sadness	Surprise	Trust
        emolex_lexcion[str(sheet.cell(i,0).value).lower()] = [int(sheet.cell(i,a).value) for a in range(105,115)]
    return emolex_lexcion

# f
def negation_read_in()->dict:

    return

# 读入人格相关字典
def Five_Character_read_in()->dict:
    FCdict = {'A': {},'C': {},'E': {},'N': {},'O': {}}
    x = ['A','C','E','N','O']
    for i in x:
        f = open('Five_Character/%s.top100.1to3grams.gender_age_controlled.rmatrix.csv' %i,'r')
        reader = csv.reader(f)
        flag = True
        for row in reader:
            if row[0] == "":
                continue
            if flag:
                flag = False
                continue
            else:
                FCdict[i][row[0].lower()] = float(row[1])
    return FCdict

# 读入年龄相关字典
def age_read_in()->dict:
    age_dict = {'13_18': {},'19_22': {},'23_29': {},'30_+':{}}
    x = ['13_18','19_22','23_29','30_+']
    for i in x:
        f = open('age/age_bins.%s.gender_adjusted.rmatrix.top100s.csv' %i,'r')
        reader = csv.reader(f)
        flag = True
        for row in reader:
            if row[0] == "":
                continue
            if flag:
                flag = False
                continue
            else:
                age_dict[i][row[0].lower()] = float(row[1])
    return age_dict

# 读入性别判断字典
def gender_read_in()->dict:
    gender_dict = {}
    f = open('gender/gender.top100.1to3grams.csv','r')
    reader = csv.reader(f)
    flag = True
    for row in reader:
        if row[1] == "":
            continue
        if flag:
            flag = False
            continue
        else:
            gender_dict[row[1].lower()] = float(row[2])
    return gender_dict

# 字典生成
Emolex = emolex_read_in()
FCdict = Five_Character_read_in()
gender_dict = gender_read_in()
age_dict = age_read_in()
# for i in FCdict:
#     for j in FCdict[i]:
#         print(j,FCdict[i][j])