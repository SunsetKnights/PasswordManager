class Access():
    """账户类"""
    def __init__(self, tag: str, username: str, password: str, url=""):
        """
        创建账户
        :param tag:标签
        :param username:用户名
        :param password:密码
        :param url:网页链接
        """
        self.tag = tag
        self.username = username
        self.password = password
        self.url = url
