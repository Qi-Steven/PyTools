import requests
import json
import time
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
# header = ["accountBm", "accountId", "ytBm", "remark"]
# ws.append(header)
# for i in range(1,99):
#     time.sleep(1)
# pageNum=str(i)
# url="https://youtuiads.cn/tpwo-api/system/account/list?pageNum="+pageNum+"&pageSize=50"
# url="https://youtuiads.cn/tpwo-api/system/carddemand/list?pageNum=1&pageSize=50&processingStatus=2&account=solana"
url="https://youtuiads.cn/tpwo-api/system/carddemand/list"
params={"pageNum":1,"pageSize":50,"processingStatus":2,"account":"solana"}
# 执行之前需要先更新token
token=open("C:\\Users\\QQ\\Desktop\\Python\\token.txt").readline()
headers = {"authorization" : token}
response = requests.get(url=url,headers=headers,params=params)

data = response.json()
for row in data['rows']:
    Id = row['id']
    jsonData={'id':Id,'account':'solana','processingStatus':1}
    res=requests.post(url="https://youtuiads.cn/tpwo-api/system/carddemand/edit",headers=headers,json=jsonData)
    # accountId = row['accountId']
    # ytBm= row['ytBm']
    # remark= row['remark']
    # ws.append([accountBm, accountId, ytBm,remark])
    # ws.append([Id])
# wb.save('C:\\Users\\EDY\\Desktop\\BankID.xlsx')