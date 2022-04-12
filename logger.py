import logging
from logging import FileHandler, Formatter
import time

date = time.asctime()

logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)
handler = FileHandler(f'logs/{date}.log')
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)
