import requests
import json
import time
from openpyxl import Workbook
import pandas as pd

wb = Workbook()
ws = wb.active
path='C:\\Users\\QQ\\Desktop\\Python\\User.xlsx'
for i in range(1,3):
    url="https://youtuiads.cn/tpwo-api/business/rechargeDemandRecord/list"
    params={"pageNum":i,"pageSize":50}
    headers = {"authorization" : "Bearer eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6ImYzMzU3MmFiLTVlODctNGFmNi1hOTQ1LTE4NGNkZjA0YWJkOSJ9.eIfj1i6yjaRRHYdXe9s6e7q6iDnB60KNLp1Mqnpi72amOcQ326rxvVt76Re7AFu2MtdRy90c17-WQUiTt-FF8Q"}
    response = requests.get(url=url,headers=headers,params=params)
    data = response.json()
    df=pd.DataFrame(data['rows'])
    with pd.ExcelWriter(path,engine='openpyxl',mode='a',if_sheet_exists='overlay') as writer:
        df1=pd.DataFrame(pd.read_excel(path))
        df_rows=df1.shape[0]
        df.to_excel(writer,sheet_name='sheet1',startrow=df_rows+1,index=False,header=False)
    # data= pd.DataFrame(data['rows'])
    # data.to_excel(path,index=False,engine="openpyxl")


