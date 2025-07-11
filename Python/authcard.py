import requests
import pandas as pd
from time import sleep

# 配置API请求的基本信息
base_url = 'https://gateway.cosmicpay.co/card/pbc/transaction/pageTransactions'  # 替换为你的API地址
headers = {
    'authorize-token': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ7XCJjbGllbnRJZFwiOlwiQ1QxOTEzMDU5NTI1OTg4NzA2Njg5XCIsXCJjcmVhdGVUaW1lXCI6XCIyMDI1LTA1LTIzVDE0OjA3OjM2LjYwNTg2NDk4MlwiLFwiZXhwaXJlVGltZVwiOlwiMjAyNS0wNS0yM1QxNzowNzozNi42MDU4MjY2OTlcIixcIm5leHRMb2dpblRpbWVcIjpcIjIwMjUtMDUtMjNUMjI6MDc6MzYuNjA1ODU2ODUyXCIsXCJ0eXBlXCI6XCJwYmNcIixcInVuaXRJZFwiOlwiVVQxOTEzMDU5NTI1OTg4NzA2NjkwXCIsXCJ1c2VySWRcIjpcIlVSMTkxMzA1OTUyNTk4ODcwNjY4OFwifSIsImp0aSI6IjA2N2MzMjM1LWVjNDQtNDBhMy05NDc0LTJhNzhiNTBhZTRiZiIsImlhdCI6MTc0Nzk4MDQ1NiwiZXhwIjoxNzc4MjIwNDU2fQ.sXEk_HZkIR6ZI-KScVrsQ0tn0Om88veEPaRAjXLXz-Q',  # 如果需要身份验证，请替换为你的真实Token
    'Content-Type': 'application/json'
}

def fetch_data(page_no):
    """Fetch data from the API for a given page number using POST."""
    payload = {
  "pageNo": 1,
  "pageSize": 1000,
  "bizType": "Auth"
}
    
    response = requests.post(base_url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

def collect_all_pages():
    """Collect all pages of data into a single list."""
    all_records = []
    page_no = 1
    
    while True:
        print(f"Fetching page {page_no}...")
        data = fetch_data(page_no)
        
        if not data or 'data' not in data or 'list' not in data['data']:
            break
        
        all_records.extend(data['data']['list'])
        
        # 如果当前页不是最后一页，则继续获取下一页
        if page_no >= data['data']['pages']:
            break
        else:
            page_no += 1
            
        # 防止请求过快，适当添加延迟
        sleep(0.5)
        
    return all_records

def main():
    all_records = collect_all_pages()
    
    if all_records:
        df = pd.json_normalize(all_records)
        output_file = 'transactions.xlsx'
        df.to_excel(output_file, index=False, engine='openpyxl')
        print(f"✅ 数据已成功导出到 {output_file}")
    else:
        print("未能获取到任何数据")

if __name__ == '__main__':
    main()