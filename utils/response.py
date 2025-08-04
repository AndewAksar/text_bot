"""Утилиты для отправки ответов и обработки ошибок Telegram-бота.

Содержит функции для отправки ответов на основе триггеров и обработки ошибок API.
"""

import logging
import asyncio
from telegram import Update
from telegram.error import TelegramError
from config.triggers import Trigger


logger = logging.getLogger(__name__)

async def respond(update: Update, trigger: Trigger, chat_id: int) -> None:
    """Отправляет ответ в чат на основе конфигурации триггера.

    Выполняет задержку перед отправкой и логирует результат.

    Args:
        update: Объект обновления от Telegram.
        trigger: Объект триггера с настройками ответа.
        chat_id: ID чата для логирования.
    """
    # Определяем ответ: вызываем функцию, если response callable, иначе берём строку
    response = trigger.response() if callable(trigger.response) else trigger.response

    try:
        # Выполняем задержку, если она задана
        if trigger.delay > 0:
            await asyncio.sleep(trigger.delay)
        # Отправляем ответ в чат
        await update.message.reply_text(response)
        logger.info(f"Бот ответил в чате {chat_id} ({trigger.log})")
    except TelegramError as e:
        logger.error(f"Ошибка Telegram в чате {chat_id}: {e}")
        # Проверяем типичные ошибки доступа
        if "chat not found" in str(e).lower() or "blocked" in str(e).lower():
            logger.error(f"Бот не имеет доступа к чату {chat_id}. Проверьте права бота.")

async def error_handler(update: Update, context: None) -> None:
    """Обрабатывает ошибки, возникающие при работе бота.

    Логирует ошибки и предоставляет рекомендации для конфликтов getUpdates.

    Args:
        update: Объект обновления от Telegram (может быть None).
        context: Контекст ошибки, содержащий информацию об ошибке.
    """
    error = context.error
    logger.error(f"Ошибка: {error}")
    # Обрабатываем конфликт getUpdates
    if "Conflict" in str(error):
        logger.error(
            "Конфликт getUpdates. Убедитесь, что запущен только один экземпляр бота."
        )