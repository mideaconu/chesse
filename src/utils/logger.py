import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def get_logger(name, level=logging.DEBUG) -> logging.Logger:
    """Returns logger object with given name."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    return logger
