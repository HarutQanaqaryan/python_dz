def add_expense(expenses: list[float], value: float) -> None:
    """Добавляет расход в список."""
    expenses.append(value)


def delete_expense(expenses: list[float], index: int) -> bool:
    """Удаляет расход по номеру (1-based). Возвращает True/False."""
    if 1 <= index <= len(expenses):
        expenses.pop(index - 1)
        return True
    return False


def get_total(expenses: list[float]) -> float:
    """Возвращает сумму всех расходов."""
    return sum(expenses)


def get_average(expenses: list[float]) -> float | None:
    """Возвращает средний расход или None, если список пуст."""
    if not expenses:
        return None
    return get_total(expenses) / len(expenses)


def print_report(expenses: list[float]) -> None:
    """Печатает красивый отчёт по расходам."""
    print("\n=== ОТЧЁТ ПО РАСХОДАМ ===")

    if not expenses:
        print("Список расходов пуст.")
        return

    for i, value in enumerate(expenses, start=1):
        print(f"{i}. {value:.2f} руб.")

    print("-" * 30)
    print(f"Всего записей:  {len(expenses)}")
    print(f"Сумма:          {get_total(expenses):.2f} руб.")
    print(f"Средний расход: {get_average(expenses):.2f} руб.")


def main() -> None:
    expenses: list[float] = []

    while True:
        print("\n=== Управление расходами ===")
        print("1. Добавить расход")
        print("2. Показать все расходы")
        print("3. Показать сумму и средний расход")
        print("4. Удалить расход по номеру")
        print("5. Выход")

        choice = input("Выберите пункт меню: ")

        if choice == "1":
            raw = input("Введите сумму расхода: ")
            try:
                value = float(raw)
            except ValueError:
                print("Ошибка: введите число.")
                continue

            if value <= 0:
                print("Сумма должна быть положительной.")
            else:
                add_expense(expenses, value)
                print("Расход добавлен.")

        elif choice == "2":
            print_report(expenses)

        elif choice == "3":
            if not expenses:
                print("Список расходов пуст.")
            else:
                print(f"Сумма:          {get_total(expenses):.2f} руб.")
                print(f"Средний расход: {get_average(expenses):.2f} руб.")

        elif choice == "4":
            if not expenses:
                print("Список расходов пуст — нечего удалять.")
                continue

            print_report(expenses)

            raw = input("Введите номер расхода для удаления: ")
            try:
                index = int(raw)
            except ValueError:
                print("Ошибка: введите целое число.")
                continue

            if delete_expense(expenses, index):
                print("Расход удалён.")
            else:
                print("Нет расхода с таким номером.")

        elif choice == "5":
            print("Выход из программы. До свидания!")
            break

        else:
            print("Неверный пункт меню.")


# if __name__ == "__main__":
#     main()

s = {1, 3, 4}

s.update([6, 7])
s.add(8)
s.remove(1)
s.discard(3)
print(s)
