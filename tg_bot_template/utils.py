import logging
from datetime import datetime


def current_date():
    return int(datetime.now().strftime("%Y%m%d"))


def create_logger(logger_name: str, file_name: str = None):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s:%(name)s: %(asctime)s: %(message)s')
    if file_name:
        file_handler = logging.FileHandler(file_name, mode='w')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.propagate = False

    return logger
