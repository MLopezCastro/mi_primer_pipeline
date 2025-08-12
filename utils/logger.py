import logging, sys

def get_logger(name: str = "pipeline"):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter(
        "%Y-%m-%d %H:%M:%S | %(levelname)s | %(name)s | %(message)s"
    )
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(fmt)
    logger.addHandler(h)
    return logger
