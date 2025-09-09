import requests
import base64
from io import BytesIO
from PIL import Image
import easyocr

# 请求接口
res = requests.get("https://youtuiads.cn/tpwo-api/captchaImage")
data = res.json()

uuid = data['uuid']
img_base64 = data['img']

# 解码 base64
image_data = base64.b64decode(img_base64)
image = Image.open(BytesIO(image_data))

# OCR 识别（不依赖 Tesseract）
reader = easyocr.Reader(['en'], gpu=False)
results = reader.readtext(image)

# 合并识别结果
expression = ''.join([item[1] for item in results]).replace(" ", "")
print("识别的表达式:", expression)

# 计算
try:
    if all(c in "0123456789+-*/" for c in expression):
        result = eval(expression)
        print("计算结果:", result)
    else:
        print("非法字符，不能计算")
except Exception as e:
    print("表达式有误：", e)

print("验证码 UUID:", uuid)
