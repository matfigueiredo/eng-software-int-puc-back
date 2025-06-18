import logging

logger = logging.getLogger(__name__)

def setup_logger(level=logging.INFO):
    handler = logging.StreamHandler()
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.setLevel(level)
    if not logger.hasHandlers():
        logger.addHandler(handler)

def log_info(message):
    logger.info(message)

def log_warning(message):
    logger.warning(message)

def log_error(message):
    logger.error(message)

def log_debug(message):
    logger.debug(message)

