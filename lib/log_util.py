#-*- coding: UTF-8 -*-

# logging是线程安全的
import logging

def set_default_log_configure():
    logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] [%(filename)s] [line:%(lineno)d] [%(levelname)s] [%(message)s]", datefmt="%d %b %Y %H:%M:%S", filename="mylog.log", filemode="w")

def get_log_handle():
    # 使用一个名字为fib的logger
    logger = logging.getLogger('test')
    # 设置logger的level为DEBUG
    logger.setLevel(logging.DEBUG)
    # 创建一个输出日志到控制台的StreamHandler
    hdr = logging.FileHandler("test", "w")
    formatter = logging.Formatter('[%(asctime)s] [%(filename)s] [line:%(lineno)d] [%(levelname)s] [%(message)s]')
    hdr.setFormatter(formatter)
    # 给logger添加上handler
    logger.addHandler(hdr)
    return logger


if __name__ == '__main__':

    set_default_log_configure()
    logging.debug("this is a test")
    logging.info("this is a test")
    logging.warning("this is a test")

    # logger = get_log_handle()
    # logger.warning("test")
