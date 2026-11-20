from typing import TypedDict, Set, Optional

class Order(TypedDict):
    id: int
    title: str
    amount: float
    email: str
    status: str
    tags: Set[str]
    created_at: str
    due: Optional[str]
    closed_at: Optional[str]


def create_order() -> None:
    pass

def list_orders() -> None:
    pass

def edit_order() -> None:
    pass

def remove_order() -> None:
    pass