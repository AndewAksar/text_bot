"""Конфигурация триггеров и ответов бота.

Определяет класс Trigger для хранения триггеров и список TRIGGERS с настройками ответов.
"""

import random
from dataclasses import dataclass
from typing import Callable, List, Union



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
    pattern: str
    response: Union[str, Callable[[], str]]
    delay: int
    log: str
    root_match: bool = False


# Список ключевых слов для общего триггера
TRIGGER_WORDS = ["сук", "хуй", "хуе", "пизд", "блят", "бляд", "еба", "ёба", "пидор"]


# Список случайных ответов для общего триггера
RESPONSES = [
    'Я бы тебя, ахуевшего, на фронт отправил.',
    "Смерть либералам!",
    "Я бы с огромным удовольствием кого-нибудь порезал и съел... тебя например."
]


# Список всех триггеров с их настройками
TRIGGERS: List[Trigger] = [
    Trigger(
        pattern='|'.join(TRIGGER_WORDS),  # Объединяем слова в одно регулярное выражение
        response=lambda: random.choice(RESPONSES),  # Случайный выбор ответа
        delay=3,
        log="корень ключевого слова",
        root_match=True
    ),
    Trigger(
        pattern=r'^да$',  # Точное совпадение слова "да"
        response='пизда',
        delay=1,
        log="слово 'да'"
    ),
    Trigger(
        pattern='вова',
        response='кому Вова, а кому Владимир Геннадьевич, щегол.',
        delay=6,
        log="корень 'вова'",
        root_match=True
    ),
    Trigger(
        pattern=r'\bволодя\b',  # Точное совпадение слова "володя"
        response='Че вы всё недовольны? Живите по кайфу, пока не сдохли.',
        delay=5,
        log="слово 'володя'"
    ),
    Trigger(
        pattern='путин',
        response='Ты что ссышь блядь за Родину подохнуть?',
        delay=3,
        log="корень 'путин'",
        root_match=True
    ),
    Trigger(
        pattern=r'\bвалить\b',
        response='Ты, нищеброд, куда собрался валить?',
        delay=3,
        log="слово 'валить'"
    ),
    Trigger(
        pattern='войн',
        response='Ты не гони, война это праздник.',
        delay=2,
        log="корень 'войн'",
        root_match=True
    ),
    Trigger(
        pattern='чур',
        response='Ахмат - сила!',
        delay=3,
        log="корень 'чур'",
        root_match=True
    ),
    Trigger(
        pattern='ядер',
        response='Вооружайтесь, парни, большой пиздец не за горами!',
        delay=5,
        log="корень 'ядер'",
        root_match=True
    ),
    Trigger(
        pattern='атом',
        response='Я давно говорю: вооружайтесь - грядут страшные времена.',
        delay=5,
        log="корень 'атом'",
        root_match=True
    ),
    Trigger(
        pattern='хох',
        response='Убивать врагов это так сладко!',
        delay=3,
        log="корень 'хох'",
        root_match=True
    ),
    Trigger(
        pattern='коррупци',
        response='Либерал есть либерал: что ни слово то - пиздешь, что второе - пропаганда. Нахуй вас.',
        delay=3,
        log="корень 'коррупци'",
        root_match=True
    ),
    Trigger(
        pattern='мотоцикл',
        response='Ненавижу хрустов, конченые уроды. Хотят подохнуть - пущай на войну едут. Хоть какая-то польза от этого биомусора.',
        delay=3,
        log="корень 'мотоцикл'",
        root_match=True
    ),
]