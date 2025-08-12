import logging, sys

def get_logger(name: str = "pipeline"):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(formatter)
    logger.addHandler(h)
    return logger

