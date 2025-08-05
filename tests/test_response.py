import pytest
import asyncio
import logging
from unittest.mock import AsyncMock, Mock, call
from telegram import Update, Chat, Message
from telegram.error import TelegramError

from utils.response import respond, error_handler
from config.triggers import Trigger


# Фикстура для создания замоканного логгера
@pytest.fixture
def logger(monkeypatch):
    logger = Mock()
    logger.info = Mock()
    logger.error = Mock()
    # Подменяем логгер в модуле response
    monkeypatch.setattr('utils.response.logger', logger)
    return logger


# Фикстура для создания объекта Update
@pytest.fixture
def update():
    update = Mock(spec=Update)
    update.message = Mock(spec=Message)
    update.message.reply_text = AsyncMock()
    update.message.chat_id = -123456789
    return update

# Фикстура для создания объекта Trigger со строковым ответом
@pytest.fixture
def string_trigger():
    return Trigger(
        pattern=r"test",
        response="Test response",
        delay=1,
        log="test trigger",
        root_match=False
    )

# Фикстура для создания объекта Trigger с вызываемым ответом
@pytest.fixture
def callable_trigger():
    def mock_response():
        return "Dynamic response"
    return Trigger(
        pattern=r"test",
        response=mock_response,
        delay=0,
        log="dynamic trigger",
        root_match=False
    )

# Фикстура для создания объекта Context с ошибкой
@pytest.fixture
def context():
    context = Mock()
    return context

# Тест для функции respond со строковым ответом
@pytest.mark.asyncio
async def test_respond_with_string_response(update, string_trigger, logger, monkeypatch):
    # Мокаем asyncio.sleep для проверки вызова задержки
    monkeypatch.setattr(asyncio, 'sleep', AsyncMock())

    await respond(update, string_trigger, update.message.chat_id)

    # Проверки
    update.message.reply_text.assert_awaited_once_with("Test response")
    asyncio.sleep.assert_awaited_once_with(1)
    logger.info.assert_called_with(f"Бот ответил в чате {update.message.chat_id} (test trigger)")

# Тест для функции respond с ошибкой Telegram API
@pytest.mark.asyncio
async def test_respond_with_telegram_error(update, string_trigger, logger):
    # Настраиваем ошибку при вызове reply_text
    update.message.reply_text.side_effect = TelegramError("Chat not found")

    await respond(update, string_trigger, update.message.chat_id)

    update.message.reply_text.assert_awaited_once_with("Test response")
    logger.error.assert_has_calls(
        [
            call(f"Ошибка Telegram в чате {update.message.chat_id}: Chat not found"),
            call(f"Бот не имеет доступа к чату {update.message.chat_id}. Проверьте права бота.")
        ]
    )

# Тест для функции error_handler с конфликтом getUpdates
@pytest.mark.asyncio
async def test_error_handler_with_conflict_error(context, logger):
    # Настраиваем ошибку
    context.error = Exception("Conflict: getUpdates conflict")

    # Выполнение функции
    await error_handler(None, context)

    # Проверки
    logger.error.assert_has_calls(
        [
            call("Ошибка: Conflict: getUpdates conflict"),
            call("Конфликт getUpdates. Убедитесь, что запущен только один экземпляр бота.")
        ]
    )

# Тест для функции error_handler с общей ошибкой
@pytest.mark.asyncio
async def test_error_handler_with_generic_error(context, logger):
    context.error = Exception("Some error")
    await error_handler(None, context)
    logger.error.assert_called_with("Ошибка: Some error")
