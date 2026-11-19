import sys

books = {
    "Война и мир": "Лев Толстой",
    "Анна Каренина": "Лев Толстой",
    "Мастер и Маргарита": "Михаил Булгаков",
    "Преступление и наказание": "Фёдор Достоевский",
    "Идиот": "Фёдор Достоевский"
}

if len(sys.argv) > 1:
    action = sys.argv[1]

    if action == "filter" and len(sys.argv) > 2:
        author_to_filter = sys.argv[2]
        # filter оставляет только книги нужного автора, map форматирует строки
        filtered_books = filter(
            lambda item: item[1] == author_to_filter, books.items())
        result = list(
            map(lambda item: f"{item[0]} — {item[1]}", filtered_books))
        print(result)

    elif action == "sort" and len(sys.argv) > 2:
        sort_by = sys.argv[2]  # ожидается 'author' или 'book'

        # Подготовка списка строк через map
        book_strings = list(
            map(lambda item: f"{item[0]} — {item[1]}", books.items()))

        if sort_by == "author":
            # Сортируем по автору (вторая часть строки после " — ")
            book_strings.sort(key=lambda s: s.split(" — ")[1])
        elif sort_by == "book":
            # Сортируем по названию книги (первая часть строки до " — ")
            book_strings.sort(key=lambda s: s.split(" — ")[0])

        print(book_strings)
