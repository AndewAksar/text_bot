"""Обработчики текстовых сообщений Telegram-бота.

Обрабатывает входящие текстовые сообщения, проверяя их на наличие триггеров.
"""

import logging
import re
import asyncio
from telegram import Update
from telegram.ext import ContextTypes

from config.bot import GROUP_CHAT_ID
from config.triggers import TRIGGERS
from utils.response import respond


logger = logging.getLogger(__name__)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обрабатывает текстовые сообщения в целевой группе.

    Проверяет сообщение на наличие триггеров и вызывает отправку ответа, если триггер найден.
    Ограничивает частоту ответов до одного каждые 10 секунд.

    Args:
        update: Объект обновления от Telegram.
        context: Контекст обработчика, предоставляемый telegram.ext.
    """
    chat_id = update.message.chat_id
    message_text = update.message.text.lower() if update.message.text else ""

    # Пропускаем пустые сообщения или сообщения из других чатов
    if not message_text or chat_id != GROUP_CHAT_ID:
        logger.debug(f"Пропуск сообщения в чате {chat_id}: пустое или не целевой чат")
        return

    # Проверяем ограничение частоты ответов
    last_response_time = context.bot_data.get(f"last_response_{chat_id}", 0)
    current_time = asyncio.get_event_loop().time()
    if current_time - last_response_time < 10:
        logger.debug(f"Пропуск ответа в чате {chat_id}: слишком частые сообщения")
        return
    context.bot_data[f"last_response_{chat_id}"] = current_time

    # Проверяем каждый триггер
    for trigger in TRIGGERS:
        if re.search(trigger.pattern, message_text, re.IGNORECASE):
            await respond(update, trigger, chat_id)
            return  # Прерываем цикл после первого совпадения

    logger.info(f"Сообщение в чате {chat_id} не содержит триггерных слов")