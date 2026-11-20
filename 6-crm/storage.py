import json
import os
from typing import List, Dict, Any
from orders import Order

FILE_NAME = "orders.json"
TEMP_FILE_NAME = "orders.tmp.json"


def load() -> List[Order]:
    """Загружает заказы из файла. Возвращает пустой список при отсутствии или ошибке."""
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)
            
            # Восстанавливаем set из list после чтения JSON
            for order in data:
                order["tags"] = set(order.get("tags", []))
                
            return data
    except json.JSONDecodeError:
        print(f"Ошибка: Файл {FILE_NAME} поврежден и содержит некорректный JSON.")
        return []
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []


def save(items: List[Order]) -> None:
    """Безопасно сохраняет список заказов в файл JSON."""
    # Явно указываем тип Dict[str, Any], чтобы Pylance не ругался на несовпадение типов
    serializable_items: List[Dict[str, Any]] = []
    
    for order in items:
        order_copy = dict(order)  # Создаем копию словаря
        order_copy["tags"] = sorted(list(order["tags"])) # set -> list
        serializable_items.append(order_copy)

    try:
        # Пишем во временный файл
        with open(TEMP_FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(serializable_items, file, ensure_ascii=False, indent=2)
            
        # Если успешно — атомарно заменяем старый файл новым
        os.replace(TEMP_FILE_NAME, FILE_NAME)
        
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")
        # Удаляем битый временный файл, если он остался
        if os.path.exists(TEMP_FILE_NAME):
            os.remove(TEMP_FILE_NAME)