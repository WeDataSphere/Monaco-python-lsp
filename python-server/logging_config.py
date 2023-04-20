import datetime
import logging
import os
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

from properties_read import Properties


class GetLog(object):
    def __init__(self, logger_name):
        self.name = logger_name
        self.level = logging.DEBUG
        properties = Properties("params.properties").getProperties()
        self.filename = properties["log_path"]
        self.log_dir = os.path.join(os.path.dirname(self.filename), 'logs')

    def get_log(self):
        # 检查日志文件夹是否存在，不存在则创建
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # 设置logger
        logger = logging.getLogger(name=self.name)
        logger.setLevel(level=self.level)
        if not logger.handlers:
            # 初始化handler
            stream_handler = logging.StreamHandler()
            # 按照日期切割日志文件
            timed_handler = TimedRotatingFileHandler(
                filename=os.path.join(self.log_dir, datetime.datetime.now().strftime('%Y-%m'),
                                      'python-server-out-' + datetime.datetime.now().strftime('%m%d') + '.log'),
                when='midnight',
                backupCount=30,
                encoding='utf-8'
            )
            # 按照日志大小切割日志文件
            size_handler = RotatingFileHandler(
                filename=self.filename,
                maxBytes=1024 * 1024 * 200,  # 每个日志文件的最大大小为200MB
                backupCount=0,
                encoding='utf-8'
            )
            # 设置handler等级
            stream_handler.setLevel(level=self.level)
            timed_handler.setLevel(level=self.level)
            size_handler.setLevel(level=self.level)
            # 设置日志格式
            sf_format = logging.Formatter("%(asctime)s-%(name)s-[line:%(lineno)d]-%(levelname)s-%(message)s")
            stream_handler.setFormatter(sf_format)
            timed_handler.setFormatter(sf_format)
            size_handler.setFormatter(sf_format)
            # 将handler添加到logger
            logger.addHandler(stream_handler)
            logger.addHandler(timed_handler)
            logger.addHandler(size_handler)
        # 返回logger
        return logger
