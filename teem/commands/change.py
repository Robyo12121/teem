from .base import Base
from json import dumps

class change(Base):
    """Make 'post change' function calls to Teem
        with parameters passed via CLI"""
    
    def run(self, some_dict):
        print("Received the following options from command line", some_dict)
