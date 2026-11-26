import sys
import tracemalloc


class User:
    def __init__(self, name: str, email: str, password: str):
        self.name = name
        self.email = email
        self.password = password


class SlotUser:
    __slots__ = ("name", "email", "password")

    def __init__(self, name: str, email: str, password: str):
        self.name = name
        self.email = email
        self.password = password


def measure(cls, n=100_000):
    tracemalloc.start()
    objs = [cls("Иван", "ivan@example.com", "secret") for _ in range(n)]
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return objs, current


if __name__ == "__main__":
    n = 100_000

    # 1) один экземпляр
    u = User("a", "a@a.a", "p")
    s = SlotUser("a", "a@a.a", "p")
    print("sys.getsizeof одного экземпляра:")
    print(f"  User     : {sys.getsizeof(u)} байт")
    print(f"  SlotUser : {sys.getsizeof(s)} байт")

    # 2) списки по 100 000
    users, mem_user = measure(User, n)
    slot_users, mem_slot = measure(SlotUser, n)

    print(f"\nПамять на {n} экземпляров (tracemalloc):")
    print(f"  User     : {mem_user / 1024 / 1024:.2f} МБ")
    print(f"  SlotUser : {mem_slot / 1024 / 1024:.2f} МБ")
    print(f"  Экономия : {(1 - mem_slot / mem_user) * 100:.1f}%")