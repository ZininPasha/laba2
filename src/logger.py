import logging


def get_logger(name: str) -> logging.Logger:
    """Возвращает настроенный логгер с выводом в консоль.

    Args:
        name: имя логгера (обычно __name__ модуля).

    Returns:
        Экземпляр logging.Logger с уровнем INFO.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        )
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger
