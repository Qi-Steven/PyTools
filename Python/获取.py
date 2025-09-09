import requests
import json
import time
from openpyxl import Workbook
import pandas as pd
path="c:\\Users\\QQ\\Desktop\\Python\\User.xlsx"
url="https://youtuiads.cn/tpwo-api/business/userDemandRecord/list"
params={"pageNum":1,"pageSize":50}
token=open("C:\\Users\\QQ\\Desktop\\Python\\token.txt").readline()
headers = {"authorization" : token}



# 定义一个函数来获取并处理单个请求的数据
def fetch_and_process_data(i):
    params["pageNum"]=i
    response = requests.get(url=url,headers=headers,params=params)
    if response.status_code == 200:
        data = response.json()
        # 假设JSON数据是一个列表，可以直接转换为DataFrame
        if isinstance(data['rows'], list):
            return pd.DataFrame(data['rows'])
        else:
            # 如果不是列表，则根据实际情况调整
            return pd.DataFrame.from_dict(data['rows'], orient='index').transpose()
    else:
        print(f"Failed to retrieve data from {url}: {response.status_code}")
        return None



# 创建一个空列表用于存储所有的DataFrame
dataframes = []

# 遍历URL列表，并对每个URL发起请求
for i in range(1,10):
    df = fetch_and_process_data(i)
    if df is not None:  # 只有在成功获取数据时才添加到列表中
        dataframes.append(df)

# 检查是否至少有一个成功的请求
if dataframes:
    # 方法一：将所有数据合并到一个DataFrame（如果结构相同）
    combined_df = pd.concat(dataframes, ignore_index=True)
    combined_df.to_excel(path, index=False, sheet_name='Sheet1')

    print("Data has been written to combined_output.xlsx")
else:
    print("No data was successfully retrieved.")










# response = requests.get(url=url,headers=headers,params=params)
# data = response.json()
# df= pd.DataFrame(data['rows'])
# df.to_excel(path,index=False,engine="openpyxl")
# for i in range(1,5):
#     params["pageNum"]=i
#     response = requests.get(url=url,headers=headers,params=params)
#     data = response.json()
#     df= pd.DataFrame(data['rows'])
#     df1=pd.DataFrame(pd.read_excel(path,engine="openpyxl"))
#     writer=pd.ExcelWriter(path=path,engine="openpyxl")
#     df_rows =df1.shape[0]
#     df=pd.concat([df1,df],axis=0)
#     df.to_excel(writer,startrow=df_rows+1,engine="openpyxl")
    # with pd.ExcelWriter(path=path) as writer:
    #     df1= pd.read_excel(path)
    #     save_data=pd.concat([df,df1],axis=0,ignore_index=True)
    #     save_data.to_excel(writer,index=False,engine="openpyxl")
# data.to_excel(path,index=False,engine="openpyxl")
