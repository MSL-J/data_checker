import pandas as pd
import numpy as np
import pymongo
import pprint
import os
import re
import datetime
import sys
import json
import matplotlib.pyplot as plt
from matplotlib                  import font_manager, rc, style

dt = datetime.datetime.now()

mapped_mod = json.loads(sys.argv[1])

connection = pymongo.MongoClient('49.247.196.148:27017',
                                 username = 'admin',
                                 password = 'qkffks15!',
                                 authSource = 'admin',
                                 authMechanism = 'SCRAM-SHA-256'
                                )

db = connection["balaan"]
mapped_collection = db["mapped"]

pipelines = list()  
pipelines.append({'$match' : {}})
pipelines.append({'$group' : {'_id' : '$color', 'cnt' : {'$sum' : 1}}})
pipelines.append({'$sort' : {'cnt':-1}})

results = db.mapped.aggregate(pipelines)

df =  pd.DataFrame(list(results))

data_check = df
data_check = data_check.rename(columns={"_id":"color"})
data_check = data_check.fillna('')

color_default = db.mapping_table_color.distinct('main_color')

color_set = {}

for default in color_default:
    
    kor_color_name = []
    en_color_name = []
    
    for color in db.mapping_table_color.find({'main_color' : default, 'color_kor' : {'$exists' : True}}):
        if len(color['color_value']) > 0:
            kor_color_name.append(color['color_kor'].replace(' ', '\s*'))
        if ' ' in color['color_value']:
            kor_color_name.append(color['color_kor'])
            
    for color in db.mapping_table_color.find({'main_color' : default, 'color_value' : {'$exists' : True}}):
        if len(color['color_value']) > 0:
            en_color_name.append(color['color_value'])            
        if ' ' in color['color_value']:
            en_color_name.append(color['color_value'].replace(' ', '\s*'))            

    color_set[default] = kor_color_name + en_color_name

data_check["mapped"] = False
data_check["mapped_none"] = False

for default in color_default:
    
    if 'mapped_' + default not in data_check.index:
        data_check['mapped_' + default] = False
    
    data_check['mapped_' + default] = data_check['color'].str.contains('^\s*'+ default, case = False)
    data_check["mapped"] = data_check["mapped"] | data_check["mapped_" + default]

for default in color_default:

    data_check['mapped_' + default] = data_check['mapped_' + default] | temp_data.str.contains('[\d\s]*[-/]*\s*'+ default, case = False)
    data_check["mapped"] = data_check["mapped"] | data_check["mapped_" + default]

for default in tcolor_default:

    for color in tqdm(color_set[default]):
        data_check['mapped_' + default] = data_check['mapped_' + default]  | temp_data.str.contains('^\s*' + color, case = False)
        data_check["mapped"] = data_check["mapped"] | data_check["mapped_" + default]
        data_check.loc[data_check['mapped_' + default] == True,"mapped_main"] = default
        
data_check.loc[data_check['color'] == '',"mapped"] = ""
data_check.loc[data_check['color'] == '',"mapped_none"] = True

result_color = {}
for column in list(data_check.columns[2:-1]):
    if len(column.split('_')) < 2:
        result_color[column] = int(data_check[data_check[column] == True]['cnt'].sum())
        continue
    temp, main_color = column.split('_')
    result_color[main_color] = int(data_check[data_check[column] == True]['cnt'].sum())

current = result_color['mapped']
no_data = result_color['none']
del(result_color['mapped'], result_color['none'])

insert_data = {}
insert_data['mode']  = mapped_mod
insert_data['date']  = dt.strftime("%Y-%m-%d %H:%M:%S")
insert_data['color'] = { "total": db.mapped.count(),
                         "current": current,
                         "noData": no_data,
                         "each": result_color}

if db.test_history.count_documents({}) != 0:
    last_history = db.test_history.find().sort('_id',-1)[0]
    
    
    if 'color' not in last_history:
        del(last_history['_id'], last_history['color'])
        for data in last_history:
            insert_data[data] = last_history[data]
            
        db.test_history.insert(insert_data)
    
    if 'color' in last_history:
        last_history = db.test_history.find().sort('_id',-1)[0]
        for i in result_color:
            result_color[i] = result_color[i] + last_history['color']['each'][i]
        insert_data['color']['each'] = result_color
        
        del(last_history['_id'], last_history['color'])
        for data in last_history:
            insert_data[data] = last_history[data]

        db.test_history.insert(insert_data)

if db.test_history.count_documents({}) == 0:
    db.test_history.insert(insert_data)
