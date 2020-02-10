#load a json file and get a value object

import numpy as np
import pandas as pd
import json
import time

with open('test.json') as json_file:
    data = json.load(json_file)
strObj = json.dumps(data)
jsonDict = json.loads(strObj)
listUrls = []
for p in jsonDict['businesses']:
    listUrls.append(p['url'])

# Iterating over 2 files
globalList = []
with open("business0.json") as json_file:
    response_json = json.load(json_file)
json_file.close()

busList = response_json.get('businesses')
for bussDict in busList:
    globalList.append(bussDict)

with open("business1.json") as json_file1:
    response_json1 = json.load(json_file1)
json_file1.close()

busList1 = response_json1.get('businesses')
for bussDict1 in busList1:
    globalList.append(bussDict1)

globalDic = {"businesses": globalList}
data = list(globalDic["businesses"])

print(len(data))
print(list(map(lambda x:x['name'], data)))
