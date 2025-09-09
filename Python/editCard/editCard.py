import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import ssl
import pandas as pd
import time
import secrets

# 自定义 Session 支持旧 TLS 版本
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
    allowed_methods=["POST"]
)
session.mount("https://", TLSAdapter(max_retries=retries))

# 路径配置
excel_path = r"C:\Users\QQ\Desktop\Python\editCard\cardlist.xlsx"

# 读取数据
df = pd.read_excel(excel_path)

# 设置 headers 模拟浏览器访问
headers_base = {
    "Request-Id": "Request-Id",
    "authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ7XCJhY2Nlc3NUb2tlbkV4cGlyZWRcIjoxNzQ5MDk2MTQ5OTEwLFwiYXBwSWRcIjpcIjE5MjE4NTIxOTU5MzUwODUwNTZcIixcImNsaWVudElkXCI6XCJDVDE5MTMwNTk1MjU5ODg3MDY2ODlcIixcImdyYW50VHlwZVwiOlwiY2xpZW50X2NyZWRlbnRpYWxzXCIsXCJvcmdDbGllbnRJZFwiOlwiQ1QxOTEzMDU5NTI1OTg4NzA2Njg5XCIsXCJvcmdVbml0SWRcIjpcIlVUMTkxMzA1OTUyNTk4ODcwNjY5MFwiLFwicXVlcnlBbGxTdWJVbml0XCI6ZmFsc2UsXCJzY29wZVwiOlwiYWxsXCIsXCJ1bml0SWRcIjpcIlVUMTkxMzA1OTUyNTk4ODcwNjY5MFwiLFwidXNlcklkXCI6XCJVUjE5MTMwNTk1MjU5ODg3MDY2ODhcIn0iLCJqdGkiOiI2Nzg3YWFkNy0wMDBjLTQ0NDItYTNhYi0zYzNhYjlhYzM3MGEiLCJpYXQiOjE3NDkwODg5NDksImV4cCI6MTc3OTMyODk0OX0.X4JieoN76aRwATXRhF235BxT0PZC1zeEBjSbAvf3B4E"  # 替换为你自己的 token
}

for index, row in df.iterrows():
    card_id = row['card_id']
    amount = row['amount']

    url = "https://api.cosmicpay.co/card/api/v1/op/recharge"
    params = {
        'account_currency': "USD",
        'amount': amount,
        'card_id': card_id,
        "partner_order_id": secrets.token_hex(16)  # 生成唯一订单号
    }

    headers = headers_base.copy()
    headers["User-Agent"] = secrets.choice([
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15"
    ])

    try:
        response = session.post(url, json=params, headers=headers, timeout=10)
        res_json = response.json()
        print(f"Response for {card_id}: {res_json}")

        if not res_json.get('success') or res_json.get('code') != 'SUCCESS':
            print(f"API failed for {card_id}: {res_json.get('message')}")

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {card_id} -> {str(e)}")

    # 随机延迟，防止被封 IP 或触发限流
    time.sleep(secrets.randbelow(3))  # 0~3 秒之间

print("所有请求完成。")