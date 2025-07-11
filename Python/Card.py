import requests
import pandas as pd
excel_path="C:\\Users\\QQ\\Desktop\\Python\\card.xlsx"
df= pd.read_excel(excel_path)
token=open("C:\\Users\\QQ\\Desktop\\Python\\token.txt").readline()
# time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
# nowTime=time.strftime('%Y-%m-%d', time.localtime())

for index,row in df.iterrows():
    headers={"authorization":token}
    update_url="https://youtuiads.cn/tpwo-api/system/airwallex/edit"
    post_params={"account":row['account'],"cardId":row['cardId'],"cardStatus":row['cardStatus']}
    post_response=requests.post(url=update_url,json=post_params,headers=headers)
    # print(data["rows"][0])
    print(post_response.status_code)
        

