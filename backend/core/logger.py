import logging
import sys

def setup_logging():
    fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    handler = logging.StreamHandler(sys.stdout)
    logging.basicConfig(level=logging.INFO, format=fmt, handlers=[handler])
