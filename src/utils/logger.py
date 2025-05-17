import logging

logger = logging.getLogger(__name__)

def init_logger():
    logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')