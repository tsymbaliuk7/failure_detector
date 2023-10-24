from util.singletone import Singleton
from termcolor import colored


class Logger:
    @staticmethod
    def warning(text: str):
        print(colored(text, 'yellow'))

    @staticmethod
    def error(text: str):
        print(colored(text, 'red'))

    @staticmethod
    def success(text: str):
        print(colored(text, 'green'))

    @staticmethod
    def info(text: str):
        print(text)
