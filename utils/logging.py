"""Настройка логирования для приложения.

Предоставляет функцию для инициализации логгера с единым форматом.
"""

import logging



def setup_logging() -> logging.Logger:
    """Инициализирует и настраивает логгер.

    Устанавливает формат логов и уровень INFO.

    Returns:
        Logger: Настроенный логгер для использования в приложении.
    """
    # Настраиваем формат логов: время, имя модуля, уровень, сообщение
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    return logging.getLogger(__name__)