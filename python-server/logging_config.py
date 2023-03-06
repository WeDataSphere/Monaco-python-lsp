import logging
import os
from properties_read import Properties


class GetLog(object):
    def __init__(self, logger_name):
        self.name = logger_name
        self.level = logging.DEBUG
        properties = Properties("params.properties").getProperties()
        self.filename = properties["log_path"]
        self.create_log_file()

    def get_log(self):
        # 设置logger
        logger = logging.getLogger(name=self.name)
        logger.setLevel(level=self.level)

        if not logger.handlers:
            # 初始化handler
            stream_handler = logging.StreamHandler()
            file_handler = logging.FileHandler(filename=self.filename)

            # 设置handler等级
            stream_handler.setLevel(level=self.level)
            file_handler.setLevel(level=self.level)

            # 设置日志格式
            sf_format = logging.Formatter("%(asctime)s-%(name)s-[line:%(lineno)d]-%(levelname)s-%(message)s")
            stream_handler.setFormatter(sf_format)
            file_handler.setFormatter(sf_format)

            # 将handler添加到self.__logger
            logger.addHandler(stream_handler)
            logger.addHandler(file_handler)

        # 返回logger
        return logger

    def create_log_file(self):
        if not os.path.exists(self.filename):
            os.makedirs(os.path.dirname(self.filename), exist_ok=True)
            with open(self.filename, "w") as f:
                f.write("This is a new file.")
