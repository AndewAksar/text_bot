import unittest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from telegram import Update, Message, TelegramError
from config.triggers import Trigger
from utils.response import respond

class TestResponse(unittest.TestCase):
    def setUp(self):
        """Инициализация перед каждым тестом."""
        self.loop = asyncio.get_event_loop()
        self.update = MagicMock(spec=Update)
        self.context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
        self.update.message = MagicMock(spec=Message)
        self.update.message.chat_id = 12345
        self.update.message.reply_text = AsyncMock()

    async def test_respond_with_delay(self):
        """Тест отправки ответа с задержкой."""
        trigger = Trigger(
            pattern=r"привет",
            response="Привет, как дела?",
            delay=1,
            log="Ответ на приветствие"
        )
        with patch("asyncio.sleep", AsyncMock()):
            await respond(self.update, trigger, self.update.message.chat_id)
            asyncio.sleep.assert_awaited_with(1)
            self.update.message.reply_text.assert_awaited_with("Привет, как дела?")

    async def test_respond_callable_response(self):
        """Тест отправки ответа с функцией response."""
        trigger = Trigger(
            pattern=r"случайный",
            response=lambda: "Ответ 1",
            delay=0,
            log="Случайный ответ"
        )
        await respond(self.update, trigger, self.update.message.chat_id)
        self.update.message.reply_text.assert_awaited_with("Ответ 1")

    async def test_respond_telegram_error(self):
        """Тест обработки ошибки Telegram."""
        trigger = Trigger(
            pattern=r"привет",
            response="Привет, как дела?",
            delay=0,
            log="Ответ на приветствие"
        )
        self.update.message.reply_text = AsyncMock(side_effect=TelegramError("Chat not found"))
        with self.assertLogs("utils.response", level="ERROR") as cm:
            await respond(self.update, trigger, self.update.message.chat_id)
            self.assertIn("Бот не имеет доступа к чату", cm.output[0])

    def test_async_methods(self):
        """Запуск асинхронных тестов."""
        self.loop.run_until_complete(self.test_respond_with_delay())
        self.loop.run_until_complete(self.test_respond_callable_response())
        self.loop.run_until_complete(self.test_respond_telegram_error())

if __name__ == "__main__":
    unittest.main()