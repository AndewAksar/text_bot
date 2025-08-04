"""Конфигурация триггеров и ответов бота.

Определяет класс Trigger для хранения триггеров и список TRIGGERS с настройками ответов.
"""

import random
import os
import json
from dataclasses import dataclass
from http.client import responses
from typing import Callable, List, Union
from dotenv import load_dotenv


@dataclass
class Trigger:
    """Класс для представления триггера и его ответа.

    Attributes:
        pattern: Регулярное выражение для поиска триггера в тексте.
        response: Строка ответа или функция, возвращающая ответ.
        delay: Задержка в секундах перед отправкой ответа.
        log: Сообщение для логирования при срабатывании триггера.
        root_match: Если True, ищет подстроку, иначе точное совпадение слова.
    """
    pattern: str                                # Регулярное выражение для поиска триггера
    response: Union[str, Callable[[], str]]     # Строка ответа или функция для генерации ответа
    delay: int                                  # Задержка перед отправкой ответа
    log: str                                    # Сообщение для логирования при срабатывании триггера
    root_match: bool = False                    # Использовать подстроку или точное совпадение

# Загружаем переменные из .env
load_dotenv()

# Список случайных ответов для общего триггера
RESPONSES = os.getenv("RESPONSES", "").split("|")

def load_triggers(file_path: str) -> List[Trigger]:
    """Загружает триггеры из JSON-файла."""
    with open(file_path, 'r', encoding='utf-8') as f:
        triggers_data = json.load(f)

    triggers = []
    for trigger_data in triggers_data:
        # Если response — список, используем TRIGGER_WORDS и RESPONSES из .env
        if trigger_data.get('use_env_response', False):
            # Вычисляем случайный ответ и помещаем в переменную
            response_func = lambda: random.choice(RESPONSES)
        else:
            response_func = trigger_data['response']

        triggers.append(Trigger(
            pattern=trigger_data['pattern'],
            response=response_func,
            delay=trigger_data['delay'],
            log=trigger_data['log'],
            root_match=trigger_data['root_match']
        ))
    return triggers

# Загрузка триггеров из файла
TRIGGERS = load_triggers('triggers.json')
