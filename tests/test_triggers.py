import unittest
import json
import os
from unittest.mock import patch

from config.triggers import Trigger, load_triggers, RESPONSES


class TestTriggers(unittest.TestCase):
    def setUp(self):
        """Настраивает тестовую среду перед каждым тестом."""
        # Создаём временный JSON-файл с триггерами
        test_triggers = [
            {
                "pattern": r"привет",
                "response": "Привет, как дела?",
                "delay": 1,
                "log": "Ответ на приветствие",
                "root_match": False
            },
            {
                "pattern": r"пока",
                "response": "До свидания!",
                "delay": 0,
                "log": "Ответ на прощание",
                "root_match": True
            },
            {
                "pattern": r"случайный",
                "response": None,
                "delay": 0,
                "log": "Случайный ответ",
                "root_match": False
            }
        ]
        with open("test_triggers.json", "w", encoding="utf-8") as f:
            json.dump(test_triggers, f, ensure_ascii=False, indent=4)

    def tearDown(self):
        """Очищает тестовую среду после каждого теста."""
        # Удаляем тестовые файлы
        if os.path.exists("test_triggers.json"):
            os.remove("test_triggers.json")

    def test_load_triggers(self):
        """Тест загрузки триггеров из JSON-файла и проверки RESPONSES."""
        triggers = load_triggers("test_triggers.json")

        # Проверяем количество триггеров
        self.assertEqual(len(triggers), 3)

        # Проверяем первые триггеры
        self.assertEqual(triggers[0].pattern, r"привет")
        self.assertEqual(triggers[0].response, "Привет, как дела?")
        self.assertEqual(triggers[0].delay, 1)
        self.assertEqual(triggers[0].log, "Ответ на приветствие")
        self.assertFalse(triggers[0].root_match)

        # Проверяем второй триггер
        self.assertEqual(triggers[1].pattern, r"пока")
        self.assertEqual(triggers[1].response, "До свидания!")
        self.assertEqual(triggers[0].delay, 1)
        self.assertEqual(triggers[1].log, "Ответ на прощание")
        self.assertTrue(triggers[1].root_match)

        # Проверяем третий триггер
        self.assertEqual(triggers[2].pattern, r"случайный")
        self.assertIsNone(triggers[2].response, "Ответ третьего триггера должен быть None")
        self.assertEqual(triggers[2].delay, 0)
        self.assertEqual(triggers[2].log, "Случайный ответ")
        self.assertFalse(triggers[2].root_match)

if __name__ == '__main__':
    unittest.main()