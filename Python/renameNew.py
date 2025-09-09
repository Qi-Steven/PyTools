import requests
import pandas as pd
import time
from datetime import datetime

# 日志打印函数
def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

# 配置路径
excel_path = r"C:\Users\QQ\Desktop\Python\rename.xlsx"
token_path = r"C:\Users\QQ\Desktop\Python\token.txt"
query_url = "https://youtuiads.cn/tpwo-api/business/userDemandRecord/list"
update_url = "https://youtuiads.cn/tpwo-api/business/userDemandRecord/update"

# 读取 token
try:
    with open(token_path, 'r', encoding='utf-8') as f:
        token = f.readline().strip()
except Exception as e:
    log(f"读取 token 出错: {e}")
    exit(1)

# 读取 Excel 数据
try:
    df = pd.read_excel(excel_path,dtype=str)
except Exception as e:
    log(f"读取 Excel 出错: {e}")
    exit(1)

# 获取当前时间
nowTime = datetime.now().strftime('%Y-%m-%d')

# 使用 session 复用连接
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(pool_connections=20, pool_maxsize=20)
session.mount('http://', adapter)
session.mount('https://', adapter)

headers = {
    "authorization": token,
    "Content-Type": "application/json"
}

# 开始处理每一行数据
for index, row in df.iterrows():
    accountId = row.get('accountId')
    if not accountId:
        log(f"第 {index} 行 accountId 为空，跳过")
        continue

    try:
        # 查询用户需求记录
        queryParams = {'pageNum': 1, 'pageSize': 50, 'accountId': accountId}
        response = session.get(query_url, params=queryParams, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        if not data.get("rows"):
            log(f"第 {index} 行未查询到记录，accountId={accountId}")
            continue

        # 更新字段
        post_params = data["rows"][0]

        # 设置需要更新的字段
        # post_params['accountName'] = row.get('accountName')
        post_params['newUserId'] = row.get('newUserId')
        post_params['oldUserId'] = row.get('newUserId')
        # post_params['ytBm'] = row.get('ytBm')
        # post_params['accountBm'] = row.get('accountBm')
        # post_params['demandTime'] = nowTime
        # post_params['processingTime'] = nowTime
        # post_params['reviewTime'] = nowTime
        # post_params['bankCardSerialNumber'] = row.get('bankCardSerialNumber')
        # post_params['bankCardName'] = row.get('bankCardName')
        # post_params['bankCardCode'] = row.get('bankCardCode')
        # post_params['bankCardExpirationDate'] = row.get('bankCardExpirationDate')
        # post_params['bankCardEndingNumber'] = row.get('bankCardEndingNumber')

        # 发送更新请求
        update_response = session.post(update_url, json=post_params, headers=headers, timeout=10)
        update_response.raise_for_status()

        log(f"第 {index} 行更新成功，状态码：{update_response.status_code}")

        # 控制频率，防止被限流
        time.sleep(0.1)

    except requests.exceptions.RequestException as e:
        log(f"第 {index} 行请求出错，accountId={accountId}: {e}")
    except ValueError as e:
        log(f"第 {index} 行 JSON 解析失败: {e}")