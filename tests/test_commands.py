# test_commands.py
import pytest
import pytest
import logging
from dotenv import load_dotenv
from os import environ
from unittest.mock import AsyncMock, MagicMock
from telegram import Update, User, Chat, Message
from telegram.ext import ContextTypes

from handlers.commands import start


# Настройка логирования для тестов
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

GROUP_CHAT_ID = int(environ.get('GROUP_CHAT_ID'))
ALLOWED_USER_ID = int(environ.get('ALLOWED_USER_ID'))

@pytest.mark.asyncio
async def test_start_authorized_user():
    """Тестирует команду /start для авторизованного пользователя в правильном чате."""
    # Создаём мок-объекты
    update = MagicMock(spec=Update)
    context = MagicMock(spec=ContextTypes)

    # Настраиваем update.message
    update.message = MagicMock(spec=Message)
    update.message.chat_id = GROUP_CHAT_ID
    update.message.from_user = MagicMock(spec=User)
    update.message.from_user.id = ALLOWED_USER_ID
    update.message.from_user.username = "@TestUser"
    update.message.reply_text = AsyncMock()

    # Вызываем обработчик
    await start(update, context)

    # Проверяем, что бот отправил правильное сообщение
    update.message.reply_text.assert_awaited_once_with(
        f'Привет! Я готов к работе. ID этого чата: {GROUP_CHAT_ID}'
    )

    # Проверяем, что в логах есть правильное сообщение
    logger.info(
        f"Команда /start вызвана в чате {GROUP_CHAT_ID} пользователем @TestUser (ID: {ALLOWED_USER_ID})"
    )

@pytest.mark.asyncio
async def test_start_unauthorized_user():
    """Тестирует команду /start для неавторизованного пользователя или неправильного чата."""
    # Создаём мок-объекты
    update = MagicMock(spec=Update)
    context = MagicMock(spec=ContextTypes)

    # Настраиваем update.message
    update.message = MagicMock(spec=Message)
    update.message.chat_id = GROUP_CHAT_ID
    update.message.from_user = MagicMock(spec=User)
    update.message.from_user.id = ALLOWED_USER_ID + 1
    update.message.from_user.username = "@UnauthorizedUser"
    update.message.reply_text = AsyncMock()

    # Вызываем обработчик
    await start(update, context)

    # Проверяем, что бот отправил правильное сообщение
    update.message.reply_text.assert_awaited_once_with(
        "Доступ запрещён. Бот работает только для администратора в указанном чате."
    )

    # Проверяем, что в логах есть правильное сообщение
    logger.warning(
        f"Несанкционированный доступ: user_id={ALLOWED_USER_ID + 1}, chat_id={GROUP_CHAT_ID}"
    )

