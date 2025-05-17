import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
logger.addHandler(RotatingFileHandler('app.log', maxBytes=1024*1024, backupCount=5))

def init_logger():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')