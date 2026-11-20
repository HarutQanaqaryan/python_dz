from typing import TypedDict, Optional, NotRequired, Unpack
from datetime import datetime, timezone

# --- ТИПЫ ---
class Order(TypedDict):
    id: int
    title: str
    amount: float
    email: str
    status: str
    tags: set[str]
    created_at: str
    due: Optional[str]
    closed_at: Optional[str]

class OrderOptionalFields(TypedDict):
    """Поля, которые можно опционально передать при создании или редактировании."""
    status: NotRequired[str]
    tags: NotRequired[set[str]]
    due: NotRequired[Optional[str]]


# --- ХРАНИЛИЩЕ ---
orders: list[Order] = []


# --- МЕТОДЫ ---
def create_order(
    title: str, 
    amount: float, 
    email: str, 
    **kwargs: Unpack[OrderOptionalFields]
) -> Order:
    """Создает новый заказ и сохраняет его в списке."""
    # Генерируем новый ID
    new_id = max([o["id"] for o in orders], default=0) + 1
    
    # Базовая структура
    order: Order = {
        "id": new_id,
        "title": title,
        "amount": amount,
        "email": email,
        "status": "new",                    # статус по умолчанию
        "tags": set(),                      # пустое множество тегов
        "created_at": datetime.now(timezone.utc).isoformat(),
        "due": None,
        "closed_at": None
    }
    
    # Обновляем опциональные поля, если они переданы в kwargs
    for key, value in kwargs.items():
        order[key] = value
            
    orders.append(order)
    return order


def list_orders() -> list[Order]:
    """Возвращает список всех заказов."""
    return orders


def edit_order(
    order_id: int, 
    **kwargs: Unpack[OrderOptionalFields]
) -> Optional[Order]:
    """Редактирует заказ по ID. Возвращает обновленный заказ или None."""
    for order in orders:
        if order["id"] == order_id:
            # Обновляем переданные поля
            for key, value in kwargs.items():
                order[key] = value
            
            # Логика автоматического обновления даты закрытия
            if order["status"] in ("done", "cancelled"):
                if order["closed_at"] is None:
                    order["closed_at"] = datetime.now(timezone.utc).isoformat()
            else:
                order["closed_at"] = None
                
            return order
    return None


def remove_order(order_id: int) -> bool:
    """Удаляет заказ по ID. Возвращает True при успехе, иначе False."""
    for i, order in enumerate(orders):
        if order["id"] == order_id:
            orders.pop(i)
            return True
    return False