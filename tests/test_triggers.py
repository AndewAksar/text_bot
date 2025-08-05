import json
import os
import unittest
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
        self.assertEqual(len(triggers), 1)

        # Проверяем первыЙ триггер
        self.assertEqual(triggers[0].pattern, r"привет")
        self.assertEqual(triggers[0].response, "Привет, как дела?")
        self.assertEqual(triggers[0].delay, 1)
        self.assertEqual(triggers[0].log, "Ответ на приветствие")
        self.assertFalse(triggers[0].root_match)

    def test_load_triggers_file_not_found(self):
        """Тест на загрузку несуществующего файла."""
        with self.assertRaises(FileNotFoundError):
            load_triggers("nonexistent.json")

    def test_load_triggers_empty_file(self):
        """Тест на загрузку пустого JSON-файла."""
        with open("empty_triggers.json", "w", encoding="utf-8") as f:
            json.dump([], f)
        triggers = load_triggers("empty_triggers.json")
        self.assertEqual(len(triggers), 0)
        os.remove("empty_triggers.json")

    def test_trigger_with_function_response(self):
        """Тест на триггер с функцией ответа."""
        test_triggers = [
            {
                "pattern": r"привет",
                "response": "lambda: 'Динамический ответ'",
                "delay": 1,
                "log": "Функция ответа",
                "root_match": False
            }
        ]
        with open("test_triggers.json", "w", encoding="utf-8") as f:
            json.dump(test_triggers, f, ensure_ascii=False, indent=4)

        triggers = load_triggers("test_triggers.json")
        self.assertEqual(triggers[0].response, "lambda: 'Динамический ответ'")

    def test_test_load_triggers_missing_fields(self):
        """Тест на загрузку триггера с отсутствующими обязательными полями."""
        test_triggers = [
            {
                "response": "Привет!",
                "delay": 1,
                "log": "Ответ на приветствие"
                # Отсутствует pattern
            }
        ]
        with open("test_triggers.json", "w", encoding="utf-8") as f:
            json.dump(test_triggers, f, ensure_ascii=False, indent=4)

        with self.assertRaises(KeyError):
            load_triggers("test_triggers.json")


if __name__ == '__main__':
    unittest.main()