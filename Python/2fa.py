import pyotp
import qrcode

def main():
    # 生成密钥（实际应用中需安全存储）
    secret_key = input("Enter your 2FA code: ")
    print("Secret Key:", secret_key)

    # 创建 TOTP 对象
    totp = pyotp.TOTP(secret_key)

    # # 生成二维码（可选）
    # uri = totp.provisioning_uri(name="user@example.com", issuer_name="MyApp")
    # img = qrcode.make(uri)
    # img.save("totp_qr.png")

    # 模拟用户获取当前 OTP（实际应由用户从APP获取）
    current_otp = totp.now()
    print("Current OTP (模拟):", current_otp)

    # # 用户输入验证
    # user_input = input("Enter your 2FA code: ")
    # if totp.verify(user_input):
    #     print("✅ 验证成功！")
    # else:
    #     print("❌ 验证失败！")

if __name__ == "__main__":
    main()