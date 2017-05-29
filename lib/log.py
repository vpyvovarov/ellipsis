import logging


def get_logger(context=None, logger=None):
    logger = logger or logging.getLogger()
    logger.setLevel(logging.INFO)
    if not len(logger.handlers):
        console_logger = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s-%(message)s')
        console_logger.setFormatter(formatter)
        logger.addHandler(console_logger)
        logger = CustomAdapter(logger, {'context': context})

    return logger


class CustomAdapter(logging.LoggerAdapter):

    def process(self, msg, kwargs):
        return '[%s] %s' % (self.extra['context'], msg), kwargs
