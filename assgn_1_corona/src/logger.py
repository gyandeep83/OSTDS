from datetime import datetime
import logging
import os


def setup_logger(log_level: str) -> logging.Logger:
    timestamp = datetime.now().strftime("%d-%m-%y_%H-%M-%S")
    log_dir = "logs"
    log_filename = os.path.join(log_dir, f"corona_da_{timestamp}.log")

    os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Clear existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(log_filename)

    console_handler.setLevel(log_level)
    file_handler.setLevel(log_level)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
