# 如果包装不了 就按照下面2个步骤
# pip uninstall crypto pycryptodome
# pip install pycryptodome
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import base64

class PrpCrypt(object):

    def __init__(self):
        self.unpad = lambda date: date[0:-ord(date[-1])]

    def aes_cipher(self, key, aes_str):
        # 使用key,选择加密方式
        aes = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        pad_pkcs7 = pad(aes_str.encode('utf-8'), AES.block_size, style='pkcs7')  # 选择pkcs7补全
        encrypt_aes = aes.encrypt(pad_pkcs7)
        # 加密结果
        encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')  # 解码
        encrypted_text_str = encrypted_text.replace("\n", "")
        # 此处我的输出结果老有换行符，所以用了临时方法将它剔除

        return encrypted_text_str

    # 解密后，去掉补足的空格用strip() 去掉
    def decrypt(self, key, decrData):  # 解密函数
        res = base64.decodebytes(decrData.encode("utf8"))
        aes = AES.new(key.encode('utf-8'), AES.MODE_ECB)
        msg = aes.decrypt(res).decode("utf8")
        return self.unpad(msg)


if __name__ == '__main__':
    # key的长度需要补长(16倍数),补全方式根据情况而定,此处我就手动以‘0’的方式补全的32位key
    # key字符长度决定加密结果,长度16：加密结果AES(128),长度32：结果就是AES(256)
    key = "c72e5b90d42e406e907ceaecc7b00234"
    # # 加密字符串长同样需要16倍数：需注意,不过代码中pad()方法里，帮助实现了补全（补全方式就是pkcs7）
    aes_str = 'hello world'
    encryption_result = PrpCrypt().aes_cipher(key, aes_str)
    print('加密',encryption_result)
    c=PrpCrypt().decrypt(key,encryption_result)
    print('解密',c)
