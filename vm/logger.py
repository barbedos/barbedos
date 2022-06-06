import logging
import time
from logging.handlers import TimedRotatingFileHandler


def logging_setup(logfile):
    logf = logging.Formatter(
        fmt='%(asctime)s.%(msecs)03d - %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S'
    )
    logf.converter = time.gmtime
    logh = TimedRotatingFileHandler(
        logfile, backupCount=14, when="midnight", interval=1,
        encoding=None, utc=True, delay=False)
    logh.setFormatter(logf)
    logh.setLevel(logging.INFO)
    logh.suffix = "%Y%m%d"

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(logh)

    console = logging.StreamHandler()
    console.setFormatter(logf)
    console.setLevel(logging.INFO)
    logger.addHandler(console)

    return logger
