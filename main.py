"""Точка входа для запуска Telegram-бота.

Инициализирует приложение, регистрирует обработчики и запускает бота в режиме polling.
"""

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from config.bot import TOKEN
from handlers.commands import start
from handlers.messages import handle_message
from utils.logging import setup_logging
from utils.response import error_handler


# Инициализируем логгер
logger = setup_logging()

def main() -> None:
    """Запускает Telegram-бота.

    Создаёт приложение, добавляет обработчики команд и сообщений, а также обработчик ошибок.
    Запускает бота в режиме polling.
    """
    try:
        # Создаём приложение с токеном
        app = ApplicationBuilder().token(TOKEN).build()

        # Регистрируем обработчик команды /start
        app.add_handler(CommandHandler("start", start))

        # Регистрируем обработчик текстовых сообщений (не команд)
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        # Регистрируем обработчик ошибок
        app.add_error_handler(error_handler)

        # Запускаем бота
        logger.info("Бот запущен")
        app.run_polling()
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")

# Запускаем модуль в режиме main
if __name__ == '__main__':
    main()