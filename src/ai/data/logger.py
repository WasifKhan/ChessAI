'''
Logging class
'''


import logging


class Logger:
    def __init__(self):
        self.initialize_logger()

    def initialize_logger(self):
        fmt = '%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s:%(message)s'
        datefmt = '%H:%M:%S'
        logging.basicConfig(filemode='w', format=fmt, level=logging.DEBUG,
                datefmt=datefmt)
        logger = logging.getLogger(__name__)

        output = logging.FileHandler('output.log')
        errors = logging.FileHandler('error.log')

        output.setLevel(logging.DEBUG)
        errors.setLevel(logging.WARNING)

        output.addFilter(lambda log: log.levelno <= 20)
        formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)

        output.setFormatter(formatter)
        errors.setFormatter(formatter)

        logger.addHandler(output)
        logger.addHandler(errors)
        self.logger = logger
