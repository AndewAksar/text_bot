# bot.py
from os import environ
from dotenv import load_dotenv

from utils.logging import setup_logging


logger = setup_logging()

# Загружаем переменные из файла .env, если он существует
load_dotenv()

# Токен Telegram-бота, полученный от BotFather
TOKEN = environ.get('TELEGRAM_TOKEN')

# ID целевой Telegram-группы, где бот будет обрабатывать сообщения
GROUP_CHAT_ID = int(environ.get('GROUP_CHAT_ID'))

# Проверка наличия обязательных переменных окружения
if not TOKEN or not GROUP_CHAT_ID:
    raise ValueError("Переменные окружения TELEGRAM_TOKEN и GROUP_CHAT_ID должны быть установлены.")
else:
    logger.info(
        'Переменные окружения установлены:\n'
        f'TOKEN: {TOKEN}\n'
        f'GROUP_CHAT_ID: {GROUP_CHAT_ID}'
    )