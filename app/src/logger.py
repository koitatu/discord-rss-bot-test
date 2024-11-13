import logging
from logging.handlers import TimedRotatingFileHandler
import os
import sys


def setup_logging(log_dir="logs", log_file_name="info.log"):
    aws_lambda_path = "/tmp/"
    log_dir = os.path.join(aws_lambda_path, log_dir)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file_path = os.path.join(log_dir, log_file_name)

    logger = logging.getLogger("Logger")
    logger.setLevel(logging.INFO)  # ログレベルの設定

    handler = TimedRotatingFileHandler(
        filename=log_file_path,
        when="midnight",
        interval=1,
        encoding="utf-8",
        backupCount=200,
    )

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    # StreamHandlerの追加
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # ハンドラーをロガーに追加
    logger.addHandler(handler)
    logger.addHandler(console_handler)

    return logger


logger = setup_logging()
