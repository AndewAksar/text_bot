"""Настройка логирования для приложения.

Предоставляет функцию для инициализации логгера с единым форматом.
"""
import logging
import os
from datetime import datetime


def setup_logging(log_file: str = os.path.join("logs", "test_bot.log")) -> logging.Logger:
    """Инициализирует и настраивает логгер."""
    # Создаём директорию для логов, если она не существует
    try:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
    except Exception as e:
        print(f"Ошибка при создании директории для логов: {e}")

    # Создаём логгер
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    try:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Ошибка при настройке FileHandler: {e}")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    logger.debug(f"Логгер инициализирован, файл логов: {os.path.abspath(log_file)}")
    return logger