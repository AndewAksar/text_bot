"""Обработчики команд Telegram-бота.

Содержит обработчик команды /start.
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes


logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает команду /start.

    Отправляет приветственное сообщение с ID чата.

    Args:
        update: Объект обновления от Telegram.
        context: Контекст обработчика, предоставляемый telegram.ext.
    """
    chat_id = update.message.chat_id
    await update.message.reply_text(f'Привет! Я готов к работе. ID этого чата: {chat_id}')
    logger.info(f"Команда /start вызвана в чате {chat_id}")