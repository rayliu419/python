import logging
import sys
from colorama import *


def get_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logging.basicConfig(level=logging.INFO)
    if not logger.handlers:
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(" %(message)s")
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    return logger


class ColorLog:
    logger = get_logger()

    @staticmethod
    def debug(msg):
        ColorLog.logger.debug(Fore.WHITE + "[DEBUG]: " + str(msg) + Style.RESET_ALL)

    @staticmethod
    def info(msg):
        ColorLog.logger.info(Fore.WHITE + "[INFO]: " + str(msg) + Style.RESET_ALL)

    @staticmethod
    def warning(msg):
        ColorLog.logger.warning("\033[38;5;214m" + "[WARNING]: " + str(msg) + "\033[m")

    @staticmethod
    def error(msg):
        ColorLog.logger.error(Fore.LIGHTRED_EX + "[ERROR]: " + str(msg) + Style.RESET_ALL)

    @staticmethod
    def critical(msg):
        ColorLog.logger.critical(Fore.LIGHTRED_EX + "[CRITICAL]: " + str(msg) + Style.RESET_ALL)