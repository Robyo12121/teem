from .base import Base
from json import dumps

class checkin(Base):
    """Make 'post checkin' function calls to Teem
        with parameters passed via CLI"""
    
    def run(self, some_dict):
        print("Received the following options from command line", some_dict)
