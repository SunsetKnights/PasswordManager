from Crypto.Cipher import AES
from hashlib import md5
# from base64 import b64encode, b64decode
from Crypto.Util.Padding import pad, unpad


class AES_Encrypt():
    def encrypt_by_aes(self, json_string: str, key: str):
        """
        通过aes加密json字符串

        :param json_string:要加密的json字符串
        :param key:密钥
        """
        cipher = AES.new(self.__complete_key__(key),
                         AES.MODE_CBC,
                         iv=self.__get_iv__(key))
        # pad用于填充长度不够的数据（右对齐）
        ct_bytes = cipher.encrypt(pad(bytes(json_string, "utf8"), 16))
        # 对ct（密文）和iv（初始化向量）进行base64编码，以便转换为可以打印的字符
        # 否则会有无法编码的字节
        # ct = b64encode(ct_bytes).decode("utf8")
        return ct_bytes

    def decrypt_by_aes(self, aes_string: bytes, key: str):
        """
        把密文解密

        :param aes_string:加密过的数据
        :param key:密钥
        :param iv:初始化向量，加密和解密用到的相同，CBC加密模式必须要有这个值才能解密
        """
        try:
            # 对iv和ct进行base64解码，使之成为byte数组
            # ct = b64decode(aes_string)
            # 指定key，ct和iv进行解密
            cipher = AES.new(self.__complete_key__(key),
                             AES.MODE_CBC,
                             iv=self.__get_iv__(key))
            # 对结果进行unpad（去除填充的数据）（去除右对齐）
            result = unpad(cipher.decrypt(aes_string), 16)
        except (ValueError, KeyError):
            raise
        return str(result, encoding="utf8")

    def __complete_key__(self, source_key: str):
        """
        处理密钥，把密钥补全为256位的数据
        把原始密钥分成2份，分别做md5运算（md5运算生成128bit数据）

        :param source_key:用户输入的密码
        """
        half = int(len(source_key) / 2)
        md5_obj = md5()
        md5_obj.update(source_key[:half].encode(encoding="utf8"))
        result_1 = md5_obj.digest()
        md5_obj.update(source_key[half:].encode(encoding="utf8"))
        result_2 = md5_obj.digest()
        result = result_1 + result_2
        return result

    def __get_iv__(self, source_key: str):
        """
        通过密码用md5生成128bit的初始化向量

        :param source_key:用户数输入的原始密码
        """
        md5_obj = md5()
        md5_obj.update(source_key.encode(encoding="utf8"))
        return md5_obj.digest()


if __name__ == "__main__":
    # 加密
    encrypt = AES_Encrypt()
    encrypted = encrypt.encrypt_by_aes("test", "123")
    print(encrypted)
    # 解密
    decrypted = encrypt.decrypt_by_aes(encrypted, "123")
    print(decrypted)
