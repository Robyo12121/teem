# teem/commands/base.py

class Base(object):
    """Base command template for other commands"""

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def run(self):
        raise NotImplementedError("You must implement the run method")

