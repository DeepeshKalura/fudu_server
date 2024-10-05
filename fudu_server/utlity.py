import logging

class NullHandler(logging.Handler):
    """ null log handler """
    def emit(self, record):
        pass