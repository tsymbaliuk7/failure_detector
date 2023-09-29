from util.singletone import Singleton


class VersionGenerator(metaclass=Singleton):

    def __init__(self):
        self.version = 0

    @property
    def next_version(self):
        self.version += 1
        return self.version
