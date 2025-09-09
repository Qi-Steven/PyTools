import pandas as pd
import requests
import time
# 配置文件路径和API地址
input_excel_path = "C:\\Users\\QQ\\Desktop\\Python\\exportCard\\input_data.xlsx"     # 输入Excel文件路径
output_excel_path = "C:\\Users\\QQ\\Desktop\\Python\\exportCard\\output_data.xlsx"   # 输出Excel文件路径
api_url = 'https://api.cosmicpay.co/card/api/v1/trade/queryCardTransactions' # 替换为你的API地址


# 自定义请求头（根据你的API要求修改）
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ7XCJhY2Nlc3NUb2tlbkV4cGlyZWRcIjoxNzQ5MDQwODg0NzI4LFwiYXBwSWRcIjpcIjE5MjE4NTIxOTU5MzUwODUwNTZcIixcImNsaWVudElkXCI6XCJDVDE5MTMwNTk1MjU5ODg3MDY2ODlcIixcImdyYW50VHlwZVwiOlwiY2xpZW50X2NyZWRlbnRpYWxzXCIsXCJvcmdDbGllbnRJZFwiOlwiQ1QxOTEzMDU5NTI1OTg4NzA2Njg5XCIsXCJvcmdVbml0SWRcIjpcIlVUMTkxMzA1OTUyNTk4ODcwNjY5MFwiLFwicXVlcnlBbGxTdWJVbml0XCI6ZmFsc2UsXCJzY29wZVwiOlwiYWxsXCIsXCJ1bml0SWRcIjpcIlVUMTkxMzA1OTUyNTk4ODcwNjY5MFwiLFwidXNlcklkXCI6XCJVUjE5MTMwNTk1MjU5ODg3MDY2ODhcIn0iLCJqdGkiOiI3ZmNlMWNjZi1mNmMzLTQ4OWMtYWQwNS0xMTlhNzU4YTM4YTgiLCJpYXQiOjE3NDkwMzM2ODQsImV4cCI6MTc3OTI3MzY4NH0.5hwnLh7GJ4bT2ZLqUoHcZzONyw4a4El8_r6ilrvYx-k',  # 示例 token
    'Content-Type': 'application/json',
    "Request-Id": "Request-Id"
}

# 用于保存所有交易记录的列表
all_transactions = []

# 读取输入Excel（假设只有一列 card_id）
df_input = pd.read_excel(input_excel_path)

# 遍历每个 card_id 发起请求
for index, row in df_input.iterrows():
    card_id = row['card_id']

    # 构造请求参数
    params = {
      "card_id": card_id,
      "begin_time": '2025-01-01 00:00:00',
      "end_time": '2099-01-01 00:00:00',
      "page_no":1,
      "page_size":9999
    }

    try:
        response = requests.get(api_url, headers=headers, params=params,timeout=(5,10))
        response.raise_for_status()
        json_response = response.json()

        # 提取 data.list 数据
        transactions = json_response.get('data', {}).get('list', [])

        # 将每条交易记录直接加入总列表（字典结构）
        all_transactions.extend(transactions)

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
    time.sleep(1)
# 将结果转为 DataFrame 并写入 Excel
df_output = pd.DataFrame(all_transactions)
df_output.to_excel(output_excel_path, index=False)

print(f"处理完成，交易明细已保存至 {output_excel_path}")