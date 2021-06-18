'''
Logging class
'''

import logging



class Logger:
    def __init__(self):
        self.initialize_logger()


    def initialize_logger(self):
        from sys import stdout, stderr
        fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s:%(message)s'
        datefmt = '%H:%M:%S'
        logger = logging.getLogger(__name__)
        stream = logging.StreamHandler(stdout)
        errstm = logging.StreamHandler(stderr)
        output = logging.FileHandler('output.log', mode='w')
        errors = logging.FileHandler('error.log', mode='a')
        output.addFilter(lambda log: log.levelno <= 20)
        stream.addFilter(lambda log: log.levelno <= 40)
        errstm.addFilter(lambda log: log.levelno >= 100)
        stream.setLevel(logging.INFO)
        output.setLevel(logging.DEBUG)
        errors.setLevel(logging.WARNING)
        logging.basicConfig(format=fmt, level=logging.DEBUG,
                datefmt=datefmt, handlers=[stream,output,errors,errstm])
        self.logger = logger

