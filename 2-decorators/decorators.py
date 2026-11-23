from functools import wraps
from typing import Callable, Any, TypeVar, ParamSpec

P = ParamSpec("P")
R = TypeVar("R")

def limit_args(max_value: int | float, mode: str = "error") -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            
            def process_val(val: Any) -> Any:
                # Проверяем, что это число (int или float), исключая bool
                if type(val) in (int, float):
                    if val > max_value: # type: ignore
                        if mode == "error":
                            raise ValueError(f"Значение {val} превышает максимум {max_value}")
                        elif mode == "clip":
                            return max_value
                return val

            # Приводим типы для Pylance, так как мы возвращаем те же типы, но с другими значениями
            new_args = tuple(process_val(a) for a in args)
            new_kwargs = {k: process_val(v) for k, v in kwargs.items()}
            
            return func(*new_args, **new_kwargs) # type: ignore
        return wrapper
    return decorator


@limit_args(max_value=10, mode="clip")
def multiply(a: int, b: int) -> int:
    return a * b

print(multiply(2, 3))
print(multiply(100, 3))