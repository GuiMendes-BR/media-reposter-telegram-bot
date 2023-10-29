import logging
from logging.handlers import TimedRotatingFileHandler
from settings.config import config
from datetime import datetime

FORMAT = '%(message)%(levelname)%(name)%(asctime)'

# Create logger
logger = logging.getLogger()

# Set log level to debug
logger.setLevel(logging.INFO)

# Set stream handler
handler = logging.StreamHandler()
# handler.setFormatter(formatter)
logger.addHandler(handler)

# Set a rotating file handler
handler = TimedRotatingFileHandler(
    filename=config.logs_folder / f'{config.process_id}.log', backupCount=10, when='midnight')
logger.addHandler(handler)
