from .base import Base
from json import dumps

class rooms(Base):
    """Make 'get rooms' function calls to Teem
        with parameters passed via CLI"""
    
    def run(self, some_dict):
        print("Received the following options from command line", some_dict)
