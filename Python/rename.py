import requests
import pandas as pd
import json
import time
import os
excel_path="C:\\Users\\QQ\\Desktop\\Python\\rename.xlsx"
df= pd.read_excel(excel_path)
token=open("C:\\Users\\QQ\\Desktop\\Python\\token.txt").readline()
# time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
nowTime=time.strftime('%Y-%m-%d', time.localtime())
for index,row in df.iterrows():
    queryParams={'pageNum':1,'pageSize':50,'accountId':row['accountId']}
    headers={"authorization":token}
    url="https://youtuiads.cn/tpwo-api/business/userDemandRecord/list"
    update_url="https://youtuiads.cn/tpwo-api/business/userDemandRecord/update"
    response=requests.get(url=url,params=queryParams,headers=headers)
    data=response.json()
    # print(data["rows"])
    data['rows'][0]['accountName']=row['accountName']
    data['rows'][0]['newUserId']=row['newUserId']
    data['rows'][0]['oldUserId']=row['newUserId']
    # data['rows'][0]['ytBm']=row['ytBm']
    # data['rows'][0]['accountBm']=row['accountBm']
    data['rows'][0]['demandTime']=nowTime
    data['rows'][0]['processingTime']=nowTime
    data['rows'][0]['reviewTime']=nowTime
    # data['rows'][0]['bankCardSerialNumber']=row['bankCardSerialNumber']
    # data['rows'][0]['bankCardName']=row['bankCardName']
    # data['rows'][0]['bankCardCode']=row['bankCardCode']
    # data['rows'][0]['bankCardExpirationDate']=row['bankCardExpirationDate']
    # data['rows'][0]['bankCardEndingNumber']=row['bankCardEndingNumber']
    post_params=data["rows"][0]
    post_response=requests.post(url=update_url,json=post_params,headers=headers)
    time.sleep(0.1)
    # print(data["rows"][0])
    print(post_response.status_code)
        

