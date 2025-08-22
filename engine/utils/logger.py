# engine/utils/logger.py
import logging
from logging import handlers
import os
from .config import LOG_DIR

os.makedirs(LOG_DIR, exist_ok=True)
log_file = os.path.join(LOG_DIR, "assistant.log")

logger = logging.getLogger("assistant")
logger.setLevel(logging.DEBUG)

fmt = "%(asctime)s %(levelname)s: %(message)s"
formatter = logging.Formatter(fmt)

fh = handlers.RotatingFileHandler(log_file, maxBytes=2_000_000, backupCount=5)
fh.setFormatter(formatter)
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setFormatter(formatter)
ch.setLevel(logging.INFO)

if not logger.handlers:
    logger.addHandler(fh)
    logger.addHandler(ch)
