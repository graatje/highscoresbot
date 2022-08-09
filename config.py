import os


class Config:
    root_folder = os.path.dirname(os.path.realpath(__file__))
    api_root = "http://127.0.0.1:8000/api/"
