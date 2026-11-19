# exp.py
from typing import Optional

class AppError(Exception):
    """Базовый класс для ошибок приложения."""
    pass

class MissingFilterTextError(AppError):
    """Не передан текст фильтра."""
    pass

class InvalidCommandError(AppError):
    """Передана кривая команда."""
    pass

class InvalidSortParameterError(AppError):
    """Передан кривой параметр сортировки."""
    pass


def process_command(command: str, param: Optional[str] = None) -> None:
    if not command:
        raise InvalidCommandError("Кривая команда: пустая строка")
    
    if command == "filter":
        if not param:
            raise MissingFilterTextError("Не передан текст фильтра")
    elif command == "sort":
        if param not in ("author", "book"):
            raise InvalidSortParameterError(f"Неверный параметр сортировки: '{param}'")
    else:
        raise InvalidCommandError(f"Неизвестная команда: '{command}'")


# Демонстрация выполняется ТОЛЬКО при прямом запуске exp.py
if __name__ == "__main__":
    try:
        process_command("sort", "unknown_param")
    except AppError as e:
        print(f"Ошибка приложения ({type(e).__name__}): {e}")
    except Exception as e:
        print(f"Непредвиденная ошибка: {e}")