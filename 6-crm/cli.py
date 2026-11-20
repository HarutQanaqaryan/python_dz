import argparse
import sys
from datetime import datetime, timezone
from typing import Any, Dict, Set, cast
import orders as ord_module
import storage


def print_table(orders_list: list[ord_module.Order]) -> None:
    """Выводит заказы в виде простой текстовой таблицы."""
    if not orders_list:
        print("Заказов нет.")
        return
    
    # Заголовок
    print(f"{'ID':<36} | {'Title':<20} | {'Amount':<10} | {'Status':<10} | {'Due'}")
    print("-" * 95)
    for o in orders_list:
        title = o['title'][:18] + ".." if len(o['title']) > 20 else o['title']
        due = o['due'] if o['due'] else "-"
        print(f"{o['id']:<36} | {title:<20} | {o['amount']:<10.2f} | {o['status']:<10} | {due}")


def handle_list(args: argparse.Namespace) -> None:
    orders = ord_module.list_orders()
    
    # Фильтр по тегу
    tag = cast(str | None, args.tag)
    if tag:
        orders = [o for o in orders if tag in o["tags"]]
        
    # Фильтр по просрочке
    if cast(bool, args.overdue):
        now = datetime.now(timezone.utc).isoformat()
        orders = [
            o for o in orders 
            if o["due"] and o["due"] < now and o["status"] not in ("done", "cancelled")
        ]
        
    # Лимит
    limit = cast(int | None, args.limit)
    if limit is not None:
        orders = orders[:limit]
        
    print_table(orders)


def handle_add(args: argparse.Namespace) -> None:
    tags_str = cast(str | None, args.tags)
    tags_set: Set[str] = set(tags_str.split(",")) if tags_str else set()
    
    order = ord_module.create_order(
        title=cast(str, args.title),
        amount=cast(float, args.amount),
        email=cast(str, args.email),
        due=cast(str | None, args.due),
        tags=tags_set
    )
    print(f"Заказ создан. ID: {order['id']}")


def handle_remove(args: argparse.Namespace) -> None:
    order_id = cast(str, args.id)
    if ord_module.remove_order(order_id):
        print("Заказ удален.")
    else:
        print("Заказ не найден.")


def handle_edit(args: argparse.Namespace) -> None:
    # Собираем только те поля, которые были переданы в CLI
    kwargs: Dict[str, Any] = {}
    
    title = cast(str | None, args.title)
    if title: 
        kwargs["title"] = title
        
    amount = cast(float | None, args.amount)
    if amount is not None: 
        kwargs["amount"] = amount
        
    email = cast(str | None, args.email)
    if email: 
        kwargs["email"] = email
        
    due = cast(str | None, args.due)
    if due: 
        kwargs["due"] = due

    if not kwargs:
        print("Нет данных для обновления.")
        return

    if ord_module.edit_order(cast(str, args.id), **kwargs):
        print("Заказ обновлен.")
    else:
        print("Заказ не найден.")


def handle_tags(args: argparse.Namespace) -> None:
    order_id = cast(str, args.id)
    order = ord_module.get_order(order_id)
    
    if not order:
        print("Заказ не найден.")
        return

    # Копируем текущие теги
    current_tags: Set[str] = set(order["tags"])
    
    add_tags = cast(str | None, args.add)
    if add_tags:
        current_tags.update(add_tags.split(","))
        
    remove_tags = cast(str | None, args.remove)
    if remove_tags:
        current_tags.difference_update(remove_tags.split(","))
        
    ord_module.edit_order(order_id, tags=current_tags)
    print(f"Теги обновлены: {sorted(list(current_tags))}")


def handle_status(args: argparse.Namespace) -> None:
    order_id = cast(str, args.id)
    new_status = cast(str, args.new_status)
    
    if ord_module.edit_order(order_id, status=new_status):
        print(f"Статус изменен на: {new_status}")
    else:
        print("Заказ не найден.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Управление заказами CRM")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- Команда list ---
    parser_list = subparsers.add_parser("list")
    parser_list.add_argument("--overdue", action="store_true", help="Показать только просроченные")
    parser_list.add_argument("--tag", type=str, help="Фильтр по тегу")
    parser_list.add_argument("--limit", type=int, help="Ограничить количество")
    parser_list.set_defaults(func=handle_list)

    # --- Команда add ---
    parser_add = subparsers.add_parser("add")
    parser_add.add_argument("--title", required=True)
    parser_add.add_argument("--amount", type=float, required=True)
    parser_add.add_argument("--email", required=True)
    parser_add.add_argument("--due", type=str, help="Дата в ISO 8601")
    parser_add.add_argument("--tags", type=str, help="Теги через запятую (a,b,c)")
    parser_add.set_defaults(func=handle_add)

    # --- Команда remove ---
    parser_remove = subparsers.add_parser("remove")
    parser_remove.add_argument("--id", required=True)
    parser_remove.set_defaults(func=handle_remove)

    # --- Команда edit ---
    parser_edit = subparsers.add_parser("edit")
    parser_edit.add_argument("--id", required=True)
    parser_edit.add_argument("--title")
    parser_edit.add_argument("--amount", type=float)
    parser_edit.add_argument("--email")
    parser_edit.add_argument("--due")
    parser_edit.set_defaults(func=handle_edit)

    # --- Команда tags ---
    parser_tags = subparsers.add_parser("tags")
    parser_tags.add_argument("--id", required=True)
    parser_tags.add_argument("--add", type=str, help="Добавить теги (a,b)")
    parser_tags.add_argument("--remove", type=str, help="Удалить теги (x,y)")
    parser_tags.set_defaults(func=handle_tags)

    # --- Команда status ---
    parser_status = subparsers.add_parser("status")
    parser_status.add_argument("--id", required=True)
    parser_status.add_argument("new_status", choices=["new", "in_progress", "done", "cancelled"])
    parser_status.set_defaults(func=handle_status)

    # Загружаем данные перед выполнением
    ord_module.orders.extend(storage.load())

    args = parser.parse_args()
    
    # Вызываем нужный обработчик
    args.func(args)
    
    # Сохраняем изменения после выполнения команды
    storage.save(ord_module.list_orders())


if __name__ == "__main__":
    main()