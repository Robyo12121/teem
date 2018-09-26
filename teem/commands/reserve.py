from .base import Base
from json import dumps

class reserve(Base):
    """Make 'make reservation' function calls to Teem
        with parameters passed via CLI"""
    
    def run(self, some_dict):
        print("Received the following options from command line", some_dict)
