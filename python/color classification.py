import pandas    as pd
import numpy     as np
import pymongo
import pprint
import os
import re
import datetime
import matplotlib.pyplot  as plt
from matplotlib           import font_manager, rc, style
from tqdm                 import tqdm


connection = pymongo.MongoClient('49.247.196.148:27017',
                                username = 'admin',
                                password = 'qkffks15!',
                                authSource = 'admin',
                                authMechanism = 'SCRAM-SHA-256'
                                )
db = connection["balaan"]
mapped_collection = db["mapped"]

all_db = db.mapped.find({}, {'_id' : 1, 'color' : 1}).limit(60000)

data_check = pd.DataFrame(all_db).fillna('')

color_defalut = db.mapping_table_color.distinct('main_color')

color_set = {}

for defalut in color_defalut:
    kor_color_name = [ color['color_kor'] for color in db.mapping_table_color.find({'main_color' : defalut, 'color_kor' : {'$exists' : True}})]
    en_color_name = [ color['color_value'] for color in db.mapping_table_color.find({'main_color' : defalut, 'color_value' : {'$exists' : True}})]
    color_set[defalut] = kor_color_name + en_color_name

data_check["mapped"] = False
data_check["mapped_none"] = False

for defalut in tqdm(color_defalut):
    
    if 'mapped_' + defalut not in data_check.index:
        data_check['mapped_' + defalut] = False
    
    for color in color_set[defalut]:
        if ' ' in color:
            rename = color.replace(' ', '\s*')
            data_check['mapped_' + defalut] = data_check['mapped_' + defalut] | data_check['color'].str.contains('^\s*'+ rename, case = False)
            data_check["mapped"] = data_check["mapped"] | data_check["mapped_" + defalut]
            continue

        data_check['mapped_' + defalut] = data_check['mapped_' + defalut]  | data_check['color'].str.contains('^\s*'+ color, case = False)
        data_check["mapped"] = data_check["mapped"] | data_check["mapped_" + defalut]

data_check.loc[data_check['color'] == '',"mapped"] = ""
data_check.loc[data_check['color'] == '',"mapped_none"] = True

data_check

print('DB에서 가져온 데이터 수 : ', data_check['_id'].count())
print(data_check.eq(1).sum())