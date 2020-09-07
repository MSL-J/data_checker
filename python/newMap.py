import pymongo
import os
import re
import datetime
import sys
import json
import pandas as pd
import numpy  as np

dt = datetime.datetime.now()

save_choice = sys.argv[1:][0]
mapped_mod  = sys.argv[1:][1]

connection = pymongo.MongoClient('49.247.196.148:27017',
                                  username = 'admin',
                                  password = 'qkffks15!',
                                  authSource = 'admin',
                                  authMechanism = 'SCRAM-SHA-256'
                                )

db = connection["balaan"]

color_default = db.mapping_table_color.distinct('main_color')

color_set = {}

def color_list_maker(lang):
    
    for default in color_default:
        
        color_name = []
    
        for color in db.mapping_table_color.find({'main_color' : default, lang : {'$ne' : ''}}):
            if ' 'in color[lang]:
                color_name.append(color[lang].replace(' ', '\s*'))
                continue
            color_name.append(color[lang])
        
        if default in color_set:
            color_set[default] = color_set[default] + color_name
        else:
            color_set[default] = color_name
    

color_list_maker('color_kor')
color_list_maker('color_value')

pipelines = list()  
pipelines.append({'$match' : {"matched['color']" : {'$exists' : False}, 'src_not_found' : {'$exists' : False}}})
pipelines.append({'$group' : {'_id' : '$color', 'cnt' : {'$sum' : 1}, 'id_list' : {'$push' : '$_id'}}})
pipelines.append({'$sort' : {'cnt':-1}})

results = db.mapped.aggregate(pipelines, allowDiskUse = True)

df =  pd.DataFrame(list(results))

data_check = df
data_check = data_check.rename(columns={"_id":"color"})
data_check = data_check.fillna('')

data_check["mapped"] = False
data_check["mapped_none"] = False

for default in color_default:
    data_check['mapped_' + default] = False

regexr_role = [
    lambda color : '^\s*' + color + '\s*',
    lambda color : color + '$',
    lambda color : '^([a-zA-Z]){0,2}[\d\s]*[-/]*\s*'+ color
    
]

def mapping_color_fun(match_mod):
    for regexr in regexr_role:
        
        for default in color_default:
            if match_mod == 'default':
                data_check['mapped_' + default] = data_check['mapped_' + default] | data_check[data_check['mapped'] == False]['color'].str.contains(regexr(default), case = False)
                data_check["mapped"] = data_check["mapped"] | data_check["mapped_" + default]
                data_check.loc[data_check['mapped_' + default] == True,"mapped_main"] = default
                
            if match_mod == 'all':
                for color in color_set[default]:
                    data_check['mapped_' + default] = data_check['mapped_' + default]  | data_check[data_check['mapped'] == False]['color'].str.contains(regexr(color), case = False)
                    data_check["mapped"] = data_check["mapped"] | data_check["mapped_" + default]
                    data_check.loc[data_check['mapped_' + default] == True,"mapped_main"] = default

mapping_color_fun('default')
mapping_color_fun('all')

data_check.loc[data_check['color'] == '',"mapped"] = ""
data_check.loc[data_check['color'] == '',"mapped_none"] = True
data_check = data_check.fillna('')

result_color = {}
for column in list(data_check.columns[2:-1]):
    
    if len(column.split('_')) < 2:
        result_color[column] = int(data_check[data_check[column] == True]['cnt'].sum())
        continue
        
    temp, main_color = column.split('_')
    result_color[main_color] = int(data_check[data_check[column] == True]['cnt'].sum())

total   = db.mapped.find({'src_not_found' : {'$exists' : False}}).count()
mapped  = db.mapped.find({"matched['color']" : {'$exists' : True}}).count()
current = result_color['mapped']
no_data = result_color['none']
unmapped_count  = total-current-no_data
unmapped_result = data_check[data_check['mapped'] != True]['color'].tolist()
del(result_color['mapped'], result_color['none'], result_color['list'])

insert_data = {}
insert_data['mode']  = mapped_mod
insert_data['date'] = dt.strftime("%Y-%m-%d %H:%M:%S")
insert_data['color'] = { "TOTAL": total,
                         "MAPPED": mapped,
                         "CURRENT" : current,
                         "NODATA": no_data,
                         "MAPPED_RESULT": result_color,
                         "UNMAPPED_UNIQUE_COUNT": unmapped_count,
                         "UNMAPPED_RESULT" : unmapped_result
                       }

db.history.insert_one(insert_data)

if save_choice == 'true':
    update_list = data_check[data_check['mapped'] == True].loc[:, ['color','id_list', 'mapped_main']]
    for num in update_list.index:
        mapping_main = update_list.loc[num, 'mapped_main']
        for object_id in update_list.loc[num, 'id_list']:
            db.mapped.update({'_id' : object_id }, { '$set' : { 'matched.color' : mapping_main}})
            
sys.stdout.flush()