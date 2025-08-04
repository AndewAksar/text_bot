import unittest
import json
import os
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from telegram import Update, Message
from telegram.ext import ContextTypes
from config.triggers import load_triggers
from handlers.message_handlers import handle_message

class TestMessageHandlers(unittest.TestCase):
    def setUp(self):
        """Инициализация перед каждым тестом."""
        self.loop = asyncio.get_event_loop()
        # Создаём временный JSON-файл с триггерами
        self.triggers_data = [
            {
                "pattern": r"привет",
                "response": "Привет, как дела?",
                "delay": 1,
                "log": "Ответ на приветствие",
                "root_match": False
            }
        ]
        with open("test_triggers.json", "w", encoding="utf-8") as f:
            json.dump(self.triggers_data, f, ensure_ascii=False)

        # Мокаем объекты Telegram
        self.update = MagicMock(spec=Update)
        self.context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
        self.update.message = MagicMock(spec=Message)
        self.update.message.chat_id = 12345
        self.update.message.reply_text = AsyncMock()
        self.context.bot_data = {}

    def tearDown(self):
        """Очистка после каждого теста."""
        if os.path.exists("test_triggers.json"):
            os.remove("test_triggers.json")

    async def test_handle_message_trigger_match(self):
        """Тест обработки сообщения с триггером."""
        self.update.message.text = "Привет, мир!"
        self.context.bot_data[f"last_response_{self.update.message.chat_id}"] = 0
        with patch("handlers.message_handlers.TRIGGERS", load_triggers("test_triggers.json")):
            with patch("handlers.message_handlers.GROUP_CHAT_ID", self.update.message.chat_id):
                await handle_message(self.update, self.context)
                self.update.message.reply_text.assert_awaited_with("Привет, как дела?")

    async def test_handle_message_no_trigger(self):
        """Тест обработки сообщения без триггера."""
        self.update.message.text = "Ничего интересного"
        self.context.bot_data[f"last_response_{self.update.message.chat_id}"] = 0
        with patch("handlers.message_handlers.TRIGGERS", load_triggers("test_triggers.json")):
            with patch("handlers.message_handlers.GROUP_CHAT_ID", self.update.message.chat_id):
                await handle_message(self.update, self.context)
                self.update.message.reply_text.assert_not_awaited()

    async def test_handle_message_rate_limit(self):
        """Тест ограничения частоты ответов."""
        self.update.message.text = "Привет, мир!"
        self.context.bot_data[f"last_response_{self.update.message.chat_id}"] = (
            asyncio.get_event_loop().time()
        )
        with patch("handlers.message_handlers.TRIGGERS", load_triggers("test_triggers.json")):
            with patch("handlers.message_handlers.GROUP_CHAT_ID", self.update.message.chat_id):
                await handle_message(self.update, self.context)
                self.update.message.reply_text.assert_not_awaited()

    def test_async_methods(self):
        """Запуск асинхронных тестов."""
        self.loop.run_until_complete(self.test_handle_message_trigger_match())
        self.loop.run_until_complete(self.test_handle_message_no_trigger())
        self.loop.run_until_complete(self.test_handle_message_rate_limit())

if __name__ == "__main__":
    unittest.main()