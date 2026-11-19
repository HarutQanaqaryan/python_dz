# fns.py
import sys
from exp import (
    AppError, 
    MissingFilterTextError, 
    InvalidCommandError, 
    InvalidSortParameterError
)

books = {
    "Война и мир": "Лев Толстой",
    "Анна Каренина": "Лев Толстой",
    "Мастер и Маргарита": "Михаил Булгаков",
    "Преступление и наказание": "Фёдор Достоевский",
    "Идиот": "Фёдор Достоевский"
}


def run(argv: list[str]) -> None:
    # 1. Проверка наличия команды
    if len(argv) < 2:
        raise InvalidCommandError("Не передана команда (filter или sort)")
    
    action = argv[1]

    if action == "filter":
        # 2. Проверка наличия текста для фильтра
        if len(argv) < 3:
            raise MissingFilterTextError("Не передан текст фильтра")
        
        author_to_filter = argv[2]
        filtered_books = filter(
            lambda item: item[1] == author_to_filter, 
            books.items()
        )
        result = list(map(lambda item: f"{item[0]} — {item[1]}", filtered_books))
        print(result)

    elif action == "sort":
        # 3. Проверка параметра сортировки
        if len(argv) < 3:
            raise InvalidSortParameterError("Не передан параметр сортировки (author или book)")
        
        sort_by = argv[2]
        if sort_by not in ("author", "book"):
            raise InvalidSortParameterError(f"Неверный параметр сортировки: '{sort_by}'")

        book_strings = list(
            map(lambda item: f"{item[0]} — {item[1]}", books.items())
        )

        if sort_by == "author":
            book_strings.sort(key=lambda s: s.split(" — ")[1])
        elif sort_by == "book":
            book_strings.sort(key=lambda s: s.split(" — ")[0])

        print(book_strings)

    else:
        # 4. Неизвестная команда
        raise InvalidCommandError(f"Неизвестная команда: '{action}'")


# Точка входа при запуске из командной строки
if __name__ == "__main__":
    try:
        run(sys.argv)
    except AppError as e:
        print(f"Ошибка: {type(e).__name__} — {e}")
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")