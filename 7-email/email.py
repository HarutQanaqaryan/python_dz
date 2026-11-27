import asyncio
import random


async def send_email(user: str) -> None:
    """Имитация отправки письма пользователю."""
    # Ждём случайное время от 0.3 до 0.8 секунд
    delay = random.uniform(0.3, 0.8)
    await asyncio.sleep(delay)
    print(f"Email sent to {user}")


async def send_bulk(users: list[str]) -> None:
    """Запускает send_email для каждого пользователя параллельно
    и дожидается завершения всех отправок."""
    tasks = [send_email(user) for user in users]
    await asyncio.gather(*tasks)


async def main() -> None:
    users = ["alice", "bob", "carol", "dave", "eve"]
    await send_bulk(users)


if __name__ == "__main__":
    asyncio.run(main())