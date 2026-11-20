import json
import os
from typing import List
from orders import Order  # Импортируем тип для аннотации

FILE_NAME = "orders.json"

def load() -> List[Order]:
    """Загружает заказы из файла. Возвращает пустой список при отсутствии или ошибке."""
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print(f"Ошибка: Файл {FILE_NAME} поврежден и содержит некорректный JSON.")
        return []
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []

def save(items: List[Order]) -> None:
    """Сохраняет список заказов в файл JSON."""
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(items, file, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")