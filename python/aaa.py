# -*- coding: utf-8 -*- 

import sys
import pandas as pd
import numpy as np
import pymongo
import pprint
import re
import random



connection = pymongo.MongoClient("mongodb://admin:qkffks15!@49.247.196.148", 27017)
db = connection["balaan"]
mapped_collection = db["mapped"]

skip_size = random.randint(0, mapped_collection.estimated_document_count())
all_db = db.mapped.find({}).skip(skip_size).limit(1000)

# print(skip_size)

exsist_color = []
not_exsist = []



for info in all_db:
    if 'color' in info:
        if info['color'] != '': 
            exsist_color.append(info)
            continue          
    not_exsist.append(info)

#     {
#         "main color" : "red",
#         "color" :"maroon"
#         "color_kor":"마룬"
#         "color_value":"#33423"
#     },

 
# print(f'color 컬럼 내용 보유 : {len(exsist_color)}')
# print(f'color 컬럼 내용 미보유 : {len(not_exsist)}')

color_set = {'red'  : ['red', 'ross', '레드', 'bordeaux', 'burgundy', 'rouge', '버건디'],
             'blue' : ['blue', 'blu', '블루', 'blue yellow', '블루 옐로우', 'denim', 'indigo', 'bleu', 'azzurro', 'marine'],
             'pink' : ['pink', 'rosa', '핑크', '핑크 브라운', 'pink brown', 'rose', 'fuxia'],
             'gold' : ['gold', 'oro', '골드'],
             'black' : ['black', 'nero', '블랙', 'noir', 'blk', 'preto'],
             'silver' : ['silver', 'argento', '실버'],
             'white' : ['white', 'bianco', '화이트', 'wht'],
             'navy blue' : ['navy blue', '네이비 블루', 'navy', '네이비'],
             'ivory' : ['ivory', '아이보리', 'cream', '크림'],
             'green' : ['green', 'verde', '그린', 'khaki', '카키', 'olive', '올리브'],
             'orange' : ['orange', 'arancio', '오렌지'],
             'brown' : ['brown', 'marrone', '브라운'],
             'gray' : ['gray', 'grigio', '그레이', 'grey'],
             'beige' : ['beige', '베이지', 'biege', 'nude', 'camel', 'ecru', 'tan', 'taupe'],
             'yellow' : ['yellow', 'giallo', '옐로우'],
             'purple' : ['purple', 'viola', '퍼플', '바이올렛'],
            }

color_defalut = ['red', 'blue', 'pink', 'gold', 'black', 'silver', 'white', 'navy blue', 'ivory', 'green', 'orange', 'brown', 'gray', 'beige', 'yellow', 'purple']

matched = []
not_matched = []

for check in exsist_color:
    for colors in color_defalut:
        for color in color_set[colors]:
            if ' ' in color:
                A = color.replace(' ', '*%*')
                if re.search('^\s*'+ A +'\s*$', check['color'], re.I):
                    matched.append(check)
                    continue
            if re.search('^'+color+'\s*$', check['color'], re.I):
                matched.append(check)
                continue
    if check not in matched:
        not_matched.append(check)

not_matched2 = []

# print(f'1차 분류 후 미매칭: {len(not_matched)}')


for check in not_matched:
    for colors in color_defalut:
        for color in color_set[colors]:
            if ' ' in color:
                A = color.replace(' ', '%*')
                if re.match('^'+ A +'/\w*', check['color'], re.I):
                    matched.append(check)
                    continue         
            if re.match('^'+ color +'/\w*', check['color'], re.I):
                matched.append(check)
                continue
                
    if check not in matched:
        not_matched2.append(check)
        
# print(f'2차 분류 후 미매칭: {len(not_matched2)}')

not_matched3 = []

for check in not_matched2:
    for colors in color_defalut:
        for color in color_set[colors]:
            if ' ' in color:
                A = color.replace(' ', '%*')
                if re.search('^'+ A +'%s*\w*', check['color'], re.I):
                    matched.append(check)
                    continue         
            if re.search('^'+ color +'%s*\w*', check['color'], re.I):
                matched.append(check)
                continue
                
    if check not in matched:
        not_matched3.append(check)

not_matched4 = []

# print(f'3차 분류 후 미매칭: {len(not_matched3)}')

for check in not_matched3:
    for colors in color_defalut:
        for color in color_set[colors]:
            if ' ' in color:
                A = color.replace(' ', '%*')
                if re.search('^'+ A +',', check['color'], re.I):
                    matched.append(check)
                    continue         
            if re.search('^'+ color +',', check['color'], re.I):
                matched.append(check)
                continue
                
    if check not in matched:
        not_matched4.append(check)


print(f'{len(exsist_color)+len(not_exsist)}')
print(f'{len(matched)}')
print(f'{len(not_matched4)}')
print(f'{len(not_exsist)}')