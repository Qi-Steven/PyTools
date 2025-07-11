import pandas as pd
import requests

# Excel 文件路径
excel_file = "C:\\Users\\QQ\\Desktop\\Python\\NickName.xlsx"

# 接口地址
api_url = 'https://gateway.cosmicpay.co/card/pbc/card/op/updateCardInfo'

# 读取 Excel 表格（默认第一个 sheet）
df = pd.read_excel(excel_file)

# 可选：查看前几行数据
print(df.head())

# 遍历 DataFrame 的每一行并发送请求
for index, row in df.iterrows():
    # 构造要发送的数据（根据你的接口要求调整字段名）
    payload = {
        'cardId': row['cardId'],
        'nickName': row['nickName']
    }

    # 发送 POST 请求
    headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ7XCJjbGllbnRJZFwiOlwiQ1QxOTEzMDU5NTI1OTg4NzA2Njg5XCIsXCJjcmVhdGVUaW1lXCI6XCIyMDI1LTA1LTI4VDEzOjUzOjAzLjQ0ODcyNzk5OFwiLFwiZXhwaXJlVGltZVwiOlwiMjAyNS0wNS0yOFQxNjo1MzowMy40NDg3MTIyOTNcIixcIm5leHRMb2dpblRpbWVcIjpcIjIwMjUtMDUtMjhUMjE6NTM6MDMuNDQ4NzI0OTkzXCIsXCJ0eXBlXCI6XCJwYmNcIixcInVuaXRJZFwiOlwiVVQxOTEzMDU5NTI1OTg4NzA2NjkwXCIsXCJ1c2VySWRcIjpcIlVSMTkxMzA1OTUyNTk4ODcwNjY4OFwifSIsImp0aSI6IjAyNTkwYTI5LTY3OGYtNGY5OS04NzRiLTUxMzY5OWU0ZjgyMCIsImlhdCI6MTc0ODQxMTU4MywiZXhwIjoxNzc4NjUxNTgzfQ.SyQTqm7dvzRVV8lDc-7XlOsTwPqn0vWWctQtlvx3IDA',
    'Content-Type': 'application/json'
    }
    response = requests.post(api_url, json=payload, headers=headers)

    # 检查响应状态码
    if response.status_code == 200:
        print(f"第 {index + 1} 行数据提交成功: {payload}")
    else:
        print(f"第 {index + 1} 行数据提交失败: {response.status_code}, 响应: {response.text}")