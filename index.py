import math
from File_Converter import File_Converter
import getpass
import re
from Access import Access
"""
list:显示列表
add:增加账户
delete:删除账户，以tag为标识
update:修改账户，以tag为标识
open:打开文件
quit:退出
"""


class user_interface():
    def __init__(self):
        self.is_open = False
        self.f_c = None
        self.access_list = None

    def list(self, tag: str):
        if not self.is_open:
            print("请先用open命令")
            return
        show_access_list = []
        # 如果不加参数，全部显示
        if tag:
            for access in self.access_list:
                if tag in access.tag:
                    show_access_list.append(access)
        else:
            show_access_list = self.access_list
        self.__show__(show_access_list)

    def open(self):
        path = input("请输入要解析的文件路径：\n")
        password = getpass.getpass("请输入密码(密码不会显示)：\n")
        try:
            self.f_c = File_Converter(path, password)
            self.access_list = self.f_c.read_file()
            self.is_open = True
            print("解析成功")
        except (IOError, ValueError, KeyError):
            print("错误")

    def update(self, tag: str):
        for access in self.access_list:
            if access.tag == tag:
                return

    def __show__(self, source):
        result = ""
        if source:
            access_list = [Access("标签", "用户名", "密码", "网址")]
            if type(source) is list:
                access_list += source
            elif type(source) is Access:
                access_list.append(source)
            # 找到每个列最长的属性，用来确定列宽
            columns = [0, 0, 0, 0]
            for access in access_list:
                loop = 0
                # 每个半角空格作为一个长度单位，汉字的长度单位是两个，所以长度为字符串长度+汉字的个数
                for v in access.__dict__.values():
                    length = len(v) + len(re.findall(u"[\u4e00-\u9fa5]", v))
                    if length > columns[loop]:
                        columns[loop] = length
                    loop += 1
            columns = [i + 4 for i in columns]
            # 生成打印字符串
            result = ""
            for access in access_list:
                for i in columns:
                    result += "+" + "—" * i
                result += "+\n"
                loop = 0
                for v in access.__dict__.values():
                    length = len(v) + len(re.findall(u"[\u4e00-\u9fa5]", v))
                    temp = (columns[loop] - length) / 2
                    left = int(temp)
                    right = math.ceil(temp)
                    result += "|" + " " * left + str(v) + " " * right
                    loop += 1
                result += "|\n"
            for i in columns:
                result += "+" + "—" * i
            result += "+\n"
        print(result)


if __name__ == "__main__":
    ui = user_interface()
    while True:
        full_command = input(">>> ")
        temp = full_command.lower().strip().split(" ")
        command = temp.pop(0)
        param = temp.pop(0) if temp else ""
        if command == "open":
            ui.open()
        elif command == "list":
            ui.list(param)
        elif command == "quit" or command == "exit":
            break
