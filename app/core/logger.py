import os

import logging
from logging.handlers import RotatingFileHandler
from colorlog import ColoredFormatter

class AppLogger:
    def __init__(self, name: str = "app", log_dir: str = "logs"):
        self.name = name
        self.log_dir = log_dir
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.propagate = False

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        if not self.logger.handlers:
            self._setup_file_handler()
            self._setup_console_handler()

    def _setup_file_handler(self):
        file_handler = RotatingFileHandler(
            filename=os.path.join(self.log_dir, f"{self.name}.log"),
            maxBytes=5 * 1024 * 1024,  # 5 MB
            backupCount=3,
            encoding="utf-8"
        )
        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def _setup_console_handler(self):
        console_handler = logging.StreamHandler()
        color_formatter = ColoredFormatter(
            fmt="%(log_color)s%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%H:%M:%S",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red"
            }
        )
        console_handler.setFormatter(color_formatter)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)

app_logger = AppLogger(__name__).get_logger()
