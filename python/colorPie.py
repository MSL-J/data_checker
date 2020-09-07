# -*- coding: utf-8 -*- 

import sys
import pandas as pd
import numpy as np
import pymongo
import datetime
import os
import pprint
import requests
import json

connection = pymongo.MongoClient("mongodb+srv://root:root@cluster0-tpxur.mongodb.net/test")
db = connection["balaan"]
mapped_collection = db["confirmed"]

pipelines = list()
pipelines.append({'$limit' : 5})
pipelines.append({'$match' : {}})
pipelines.append({'$group' : {'_id' : '$color', 'cnt' : {'$sum' : 1}}})
pipelines.append({'$sort' : {'cnt':-1}})

results = db.confirmed.aggregate(pipelines)

df =  pd.DataFrame(list(results))

data_copy = df

data_copy = data_copy.rename(columns={"_id":"color"})
data_copy = data_copy.fillna('')

color_map = pd.DataFrame(columns=['color', 'count'])

color_set = {'red'  : ['red', 'ross', '레드', 'bordeaux', 'burgundy', 'rouge'],
             'blue' : ['blue', 'blu', '블루', '[blue yellow]', '[블루 옐로우]', 'denim', 'indigo', 'bleu', 'azzurro', 'marine'],
             'pink' : ['pink', 'rosa', '핑크', '[핑크 브라운]', '[pink brown]', 'rose', 'fuxia'],
             'gold' : ['gold', 'oro', '골드'],
             'black' : ['black', 'nero', '블랙', 'noir', 'blk', 'preto'],
             'silver' : ['silver', 'argento', '실버'],
             'white' : ['white', 'bianco', '화이트', 'wht'],
             'navy blue' : ['[navy blue]', '[네이비 블루]'],
             'ivory' : ['ivory', '아이보리', 'cream', '크림'],
             'green' : ['green', 'verde', '그린', 'khaki', '카키', 'olive', '올리브'],
             'orange' : ['orange', 'arancio', '오렌지'],
             'brown' : ['brown', 'marrone', '브라운'],
             'gray' : ['gray', 'grigio', '그레이', 'grey'],
             'beige' : ['beige', '베이지', 'biege', 'nude', 'camel', 'ecru', 'tan', 'taupe'],
             'yellow' : ['yellow', 'giallo', '옐로우'],
             'purple' : ['purple', 'viola', '퍼플']
            }

color_defalut = ['red', 'blue', 'pink', 'gold', 'black', 'silver', 'white', 'navy blue', 'ivory', 'green', 'orange', 'brown', 'gray', 'beige', 'yellow', 'purple']

data_copy["mapped"] = False
data_copy["mapped_none"] = False

color_man = {}
color_temps = []

for defalut in color_defalut:
    
    main_colors = color_set[defalut]
    
    for color in main_colors:
        data_copy["mapped_" + color] = data_copy['color'].str.contains('^[a-zA-Z0-9]{0,2}\d*[a-zA-Z0-9]{0,1}\s*[!@#/_\-%^&*]*\s*[(){}\[\]]*'+ color +'*[(){}\[\]]*$', case = False)
        data_copy["mapped"] = data_copy["mapped"] | data_copy["mapped_" + color]
        color_map = color_map.append({"color" :color,"count":data_copy["mapped_" + color].value_counts()[True]},ignore_index=True)

data_copy.loc[data_copy['color'] == '',"mapped"] = "noColor"
data_copy.loc[data_copy['color'] == '',"mapped_none"] = True
data_copy.loc[data_copy['color'] == '',"mapped_none"] = data_copy.loc[data_copy['cnt'] == '',"mapped_none"]
color_map = color_map.append({"color" :"etc","count":data_copy["mapped"].value_counts()[False]},ignore_index=True)    

mapped_data = data_copy.groupby("mapped").sum()['cnt']
final_data = mapped_data.to_dict()
print(final_data)
sys.stdout.flush()


# for x in range(0,1):
#     try:
#         print(final_data)
#         sys.stdout.flush()
#     except requests.exceptions.ConnectionError:
#         status_code = "Connection refused"
#         print(status_code)
