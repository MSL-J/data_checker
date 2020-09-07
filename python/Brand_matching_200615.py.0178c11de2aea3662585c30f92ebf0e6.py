import os
import pymongo
import pprint
import re
import json
import sys
import datetime
import pandas                 as pd
import numpy                  as np
import matplotlib.pyplot      as plt
from matplotlib               import font_manager, rc, style
from tqdm                     import tqdm



connection = pymongo.MongoClient( '49.247.196.148:27017',
                                   username = 'admin',
                                   password = 'qkffks15!',
                                   authSource = 'admin',
                                   authMechanism = 'SCRAM-SHA-256'
                                )

db = connection["balaan"]
mapped_collection = db["mapped"]




not_mapped = mapped_collection.find({'brand_name' : {'$exists': True}, 'matched_brandno' : {'$exists': False}}).count()
not_mapped



mapped = mapped_collection.find({'brand_name' : {'$exists': True}, 'matched_brandno' : {'$exists': True}}).count()
mapped



no_data = mapped_collection.find({'brand_name' : {'$exists': False}, 'matched_brandno' : {'$exists': False}}).count()
no_data



wrong = mapped_collection.find({'brand_name' : {'$exists': False}, 'matched_brandno' : {'$exists': True}}).count()
wrong




total = mapped_collection.count()
total



brand_pie_1 = [mapped, not_mapped, no_data, wrong]
print(total, brand_pie_1)




pie_chart = plt.pie(brand_pie_1, autopct='%1.1f%%',shadow=True)
plot1, = plt.plot(brand_pie_1)
plot2, = plt.plot(brand_pie_1)
plot3, = plt.plot(brand_pie_1)
plot4, = plt.plot(brand_pie_1)
plots = [plot1, plot2, plot3, plot4]
labels = ["mapped", "not mapped", "no data", "wrong"]
plt.legend(plots, labels, loc=2, bbox_to_anchor=(1,0.5))
plt.show()



brand_pie_2 = [mapped, not_mapped]
print(total, brand_pie_2)
pie_chart = plt.pie(brand_pie_2, autopct='%1.1f%%',shadow=True)
plot1, = plt.plot(brand_pie_2)
plot2, = plt.plot(brand_pie_2)
plots = [plot1, plot2]
labels = ["mapped", "not mapped"]
plt.legend(plots, labels, loc=2, bbox_to_anchor=(1,0.5))
plt.show()




not_mapped_each = mapped_collection.find({'brand_name' : {'$exists': True}, 'matched_brandno' : {'$exists': False}})
not_mapped_each



array = list(not_mapped_each)

print (array)






