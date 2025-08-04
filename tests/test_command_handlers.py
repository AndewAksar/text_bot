import unittest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from telegram import Update, Message
from telegram.ext import ContextTypes
from handlers.command_handlers import start

class TestCommandHandlers(unittest.TestCase):
    def setUp(self):
        """Инициализация перед каждым тестом."""
        self.loop = asyncio.get_event_loop()
        self.update = MagicMock(spec=Update)
        self.context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
        self.update.message = MagicMock(spec=Message)
        self.update.message.chat_id = 12345
        self.update.message.reply_text = AsyncMock()

    async def test_start_command(self):
        """Тест команды /start."""
        await start(self.update, self.context)
        self.update.message.reply_text.assert_awaited_with(
            f'Привет! Я готов к работе. ID этого чата: {self.update.message.chat_id}'
        )

    def test_async_methods(self):
        """Запуск асинхронных тестов."""
        self.loop.run_until_complete(self.test_start_command())

if __name__ == "__main__":
    unittest.main()