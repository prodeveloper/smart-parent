import logging

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('debug.log')
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)

class LogItem:
    def __init__(self, item: str):
        self.item = item

    def log(self):
        logger.info(self.item)