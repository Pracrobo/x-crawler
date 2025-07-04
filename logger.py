import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
import os

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)  # 폴더 없으면 자동 생성

date_str = datetime.now().strftime("%Y-%m-%d")
logfile = os.path.join(log_dir, f"x-crawler-{date_str}.log")


def get_logger(name="x-logger"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.hasHandlers():
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)


        # file handler
        file_handler = logging.FileHandler(logfile, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)



        # Fomatter
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)


        # Handler 추가
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)


    return logger