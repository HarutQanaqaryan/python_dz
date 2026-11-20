from typing import TypedDict, Optional, NotRequired, Unpack, List
from datetime import datetime, timezone
import uuid

class Order(TypedDict):
    id: str
    title: str
    amount: float
    email: str
    status: str
    tags: set[str]
    created_at: str
    due: Optional[str]
    closed_at: Optional[str]

class OrderOptionalFields(TypedDict):
    status: NotRequired[str]
    tags: NotRequired[set[str]]
    due: NotRequired[Optional[str]]

# Глобальное хранилище
orders: List[Order] = []


def create_order(
    title: str, 
    amount: float, 
    email: str, 
    **kwargs: Unpack[OrderOptionalFields]
) -> Order:
    """Создает новый заказ с UUID."""
    order: Order = {
        "id": str(uuid.uuid4()),  # Генерируем UUID вместо int
        "title": title,
        "amount": amount,
        "email": email,
        "status": "new",
        "tags": set(),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "due": None,
        "closed_at": None
    }
    
    for key, value in kwargs.items():
        order[key] = value
            
    orders.append(order)
    return order


def edit_order(
    order_id: str, 
    **kwargs: Unpack[OrderOptionalFields]
) -> Optional[Order]:
    """Редактирует заказ по UUID."""
    for order in orders:
        if order["id"] == order_id:
            for key, value in kwargs.items():
                order[key] = value
            
            # Логика закрытия заказа
            if order["status"] in ("done", "cancelled"):
                if order["closed_at"] is None:
                    order["closed_at"] = datetime.now(timezone.utc).isoformat()
            else:
                order["closed_at"] = None
                
            return order
    return None


def remove_order(order_id: str) -> bool:
    for i, order in enumerate(orders):
        if order["id"] == order_id:
            orders.pop(i)
            return True
    return False

def get_order(order_id: str) -> Optional[Order]:
    for order in orders:
        if order["id"] == order_id:
            return order
    return None