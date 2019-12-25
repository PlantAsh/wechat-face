

class WechatError(Exception):

    def __init__(self, ErrorInfo):
        # 初始化父类
        super().__init__(self)
        self.info = ErrorInfo
        print(ErrorInfo)

    def __str__(self):
        return self.info
