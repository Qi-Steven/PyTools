import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import ssl
import pandas as pd
import time
import secrets
import os

# 自定义适配器支持旧 TLS 版本
class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.set_ciphers("DEFAULT:@SECLEVEL=1")
        context.options |= ssl.OP_NO_TLSv1_3
        kwargs["ssl_context"] = context
        return super().init_poolmanager(*args, **kwargs)

# 创建 session 并配置重试机制
session = requests.Session()
retries = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504],
    allowed_methods=["GET"]
)
session.mount("https://", TLSAdapter(max_retries=retries))

# 路径配置
excel_path = r"C:\Users\QQ\Desktop\Python\editCard\cardlist.xlsx"
output_file = r"C:\Users\QQ\Desktop\Python\editCard\exportCard.xlsx"

# 读取数据
df = pd.read_excel(excel_path)
results = []

for index, row in df.iterrows():
    card_id = row['card_id']
    url = "https://api.cosmicpay.co/card/api/v1/op/queryCardDetail"
    params = {'card_id': card_id}
    
    headers = {
        "Request-Id": "Request-Id",
        "authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ7XCJhY2Nlc3NUb2tlbkV4cGlyZWRcIjoxNzQ5MDk2MTQ5OTEwLFwiYXBwSWRcIjpcIjE5MjE4NTIxOTU5MzUwODUwNTZcIixcImNsaWVudElkXCI6XCJDVDE5MTMwNTk1MjU5ODg3MDY2ODlcIixcImdyYW50VHlwZVwiOlwiY2xpZW50X2NyZWRlbnRpYWxzXCIsXCJvcmdDbGllbnRJZFwiOlwiQ1QxOTEzMDU5NTI1OTg4NzA2Njg5XCIsXCJvcmdVbml0SWRcIjpcIlVUMTkxMzA1OTUyNTk4ODcwNjY5MFwiLFwicXVlcnlBbGxTdWJVbml0XCI6ZmFsc2UsXCJzY29wZVwiOlwiYWxsXCIsXCJ1bml0SWRcIjpcIlVUMTkxMzA1OTUyNTk4ODcwNjY5MFwiLFwidXNlcklkXCI6XCJVUjE5MTMwNTk1MjU5ODg3MDY2ODhcIn0iLCJqdGkiOiI2Nzg3YWFkNy0wMDBjLTQ0NDItYTNhYi0zYzNhYjlhYzM3MGEiLCJpYXQiOjE3NDkwODg5NDksImV4cCI6MTc3OTMyODk0OX0.X4JieoN76aRwATXRhF235BxT0PZC1zeEBjSbAvf3B4E",
        "User-Agent": secrets.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15"
        ])
    }

    try:
        response = session.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            res_json = response.json()
            if res_json.get('success') and res_json.get('code') == 'SUCCESS':
                card_data = res_json.get('data', {})
                results.append({
                    'card_id': card_data.get('card_id'),
                    'available_balance': card_data.get('available_balance')
                })
            else:
                print(f"API failed for {card_id}: {res_json.get('message')}")
        else:
            print(f"Request failed for {card_id} with status code {response.status_code}")
    except Exception as e:
        print(f"Error occurred for {card_id}: {e}")

    time.sleep(secrets.randbelow(3))  # 控制频率，避免触发反爬

# 保存结果
result_df = pd.DataFrame(results)
result_df.to_excel(output_file, index=False)
print(f"数据已成功导出到 {output_file}")