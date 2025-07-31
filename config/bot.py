"""Конфигурация Telegram-бота.

Содержит загрузку переменных окружения для токена бота и ID группы.
"""

from os import environ
from dotenv import load_dotenv



# Загружаем переменные из файла .env, если он существует
load_dotenv()


# Токен Telegram-бота, полученный от BotFather
TOKEN = environ.get('TELEGRAM_TOKEN')


# ID целевой Telegram-группы, где бот будет обрабатывать сообщения
GROUP_CHAT_ID = int(environ.get('GROUP_CHAT_ID'))


# Проверка наличия обязательных переменных окружения
if not TOKEN or not GROUP_CHAT_ID:
    raise ValueError(
        "Переменные окружения TELEGRAM_TOKEN и GROUP_CHAT_ID должны быть установлены."
    )