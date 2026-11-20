import json
import os
from typing import List, Dict, Any
from orders import Order

FILE_NAME = "orders.json"
TEMP_FILE_NAME = "orders.tmp.json"

def load() -> List[Order]:
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)
            for order in data:
                order["tags"] = set(order.get("tags", []))
            return data
    except Exception as e:
        print(f"Ошибка загрузки: {e}")
        return []

def save(items: List[Order]) -> None:
    serializable_items: List[Dict[str, Any]] = []
    for order in items:
        order_copy = dict(order)
        order_copy["tags"] = sorted(list(order["tags"]))
        serializable_items.append(order_copy)

    try:
        with open(TEMP_FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(serializable_items, file, ensure_ascii=False, indent=2)
        os.replace(TEMP_FILE_NAME, FILE_NAME)
    except Exception as e:
        print(f"Ошибка сохранения: {e}")