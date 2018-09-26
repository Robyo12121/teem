from .base import Base
from json import dumps

class reservations(Base):
    """Make 'get reservations' function calls to Teem
        with parameters passed via CLI"""
    
    def run(self, some_dict):
        print("Received the following options from command line", some_dict)

if __name__ == '__main__':
    res = reservations(room='Showcase', loop=True, before='10:30')
    res.run()
    res.args
    
              
