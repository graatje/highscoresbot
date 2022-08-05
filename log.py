import logging
import sys
from logging.handlers import TimedRotatingFileHandler
import time
from config import Config
import os


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(logging.Logger, metaclass=Singleton):
    def __init__(
        self,
        log_file=f"{Config.root_folder}\\logs\\{time.time_ns()}.log",
        name="global_logger",
        log_format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        *args,
        **kwargs
    ):
        self.formatter = logging.Formatter(log_format)
        self.log_file = log_file

        super().__init__(name=name, *args, **kwargs)

        self.addHandler(self.get_console_handler())
        if log_file:
            self.addHandler(self.get_file_handler())

        # with this pattern, it's rarely necessary to propagate the| error up to parent
        self.propagate = False

    def get_console_handler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.formatter)
        return console_handler

    def get_file_handler(self):
        file_handler = TimedRotatingFileHandler(self.log_file, when="midnight")
        file_handler.setFormatter(self.formatter)
        return file_handler


if not os.path.isdir(Config.root_folder + "\\logs"):
    os.mkdir(Config.root_folder + "\\logs")
