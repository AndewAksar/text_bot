# commands.py
import logging
from os import environ
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes

from utils.logging import setup_logging


logger = setup_logging()

load_dotenv()

ALLOWED_USER_ID = int(environ.get('ALLOWED_USER_ID'))
GROUP_CHAT_ID = int(environ.get('GROUP_CHAT_ID'))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает команду /start.

    Args:
        update: Объект обновления от Telegram.
        context: Контекст обработчика, предоставляемый telegram.ext.
    """
    chat_id = update.message.chat_id
    user_id = update.message.from_user.id
    username = update.message.from_user.username or "Unknown"

    if chat_id != GROUP_CHAT_ID or user_id != ALLOWED_USER_ID:
        await update.message.reply_text("Доступ запрещён. Бот работает только для администратора в указанном чате.")
        logger.warning(f"Несанкционированный доступ: user_id={user_id}, chat_id={chat_id}")
        return

    logger.info(f"Команда /start вызвана в чате {chat_id} пользователем {username} (ID: {user_id})")

    await update.message.reply_text(f'Привет! Я готов к работе. ID этого чата: {chat_id}')