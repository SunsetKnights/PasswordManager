import json
from Access import Access
from Encrypt import AES_Encrypt


class File_Converter():
    """序列化写入文件或者反序列化读取文件"""
    def __init__(self, file_path: str, password: str):
        """
        负责读取文件并转换为list[Access]
        或者把list[Access]转换成json文件并写入文件
        :param file_path:文件路径
        """
        self.file_path = file_path
        self.password = password

    def read_file(self):
        """
        通过路径读取文件并且转换为list[Access]
        如果路径不是文件，抛出异常
        """
        try:
            context = self.__file_check__("rb").read()
            decrypted = AES_Encrypt().decrypt_by_aes(context, self.password)
            access_list = []
            for access in json.loads(decrypted):
                access_list.append(
                    Access(access["tag"], access["username"],
                           access["password"], access["url"]))
        except (IOError, ValueError, KeyError):
            raise
        return access_list

    def write_file(self, access_list: list):
        """
        把list[Access]序列化并写入文件
        """
        try:
            json_string = json.dumps(access_list,
                                     default=lambda access: access.__dict__)
            encrypted = AES_Encrypt().encrypt_by_aes(json_string,
                                                     self.password)
            self.__file_check__("wb").write(encrypted)
        except IOError as e:
            raise e

    def __file_check__(self, file_mode: str):
        try:
            file_obj = open(self.file_path, file_mode)
        except IOError as e:
            raise e
        return file_obj


if __name__ == "__main__":
    converter = File_Converter(r"PasswordManger\test", "FuckYou")

    # 生成数据并写入文件
    access_list = [
        Access("tag{0}".format(i), "username{0}".format(i),
               "password{0}".format(i), "url{0}".format(i))
        for i in range(1, 11)
    ]
    converter.write_file(access_list)
    # 读取数据并打印
    access_list = converter.read_file()
    for access in access_list:
        print("tag:{tag},username:{username},password:{password},url:{url}".
              format(tag=access.tag,
                     username=access.username,
                     password=access.password,
                     url=access.url))
