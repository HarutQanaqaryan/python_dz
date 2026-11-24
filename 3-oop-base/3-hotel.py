from datetime import date
from typing import List, Optional

class Room:
    def __init__(self, number: str, base_price: float):
        self.number = number
        self.base_price = base_price

    def get_price(self) -> float:
        return self.base_price

    def __str__(self) -> str:
        return f"Номер {self.number} (Базовая цена: {self.base_price})"


class Suite(Room):
    def __init__(self, number: str, base_price: float, multiplier: float):
        super().__init__(number, base_price)
        self.multiplier = multiplier

    def get_price(self) -> float:
        # Люкс умножает базовую цену на свой мультипликатор
        return self.base_price * self.multiplier

    def __str__(self) -> str:
        return f"Люкс {self.number} (Цена: {self.get_price()})"


# --- КЛАСС БРОНИРОВАНИЯ ---
class Booking:
    def __init__(self, room: Room, start_date: date, end_date: date, guest_name: str):
        self.room = room
        self.start_date = start_date
        self.end_date = end_date
        self.guest_name = guest_name
        self.is_active = True

    def cancel(self):
        self.is_active = False

    def overlaps(self, start_date: date, end_date: date) -> bool:
        """Проверяет, пересекаются ли даты брони с заданным диапазоном."""
        # Условие пересечения интервалов: (StartA <= EndB) и (EndA >= StartB)
        return self.start_date <= end_date and self.end_date >= start_date


# --- КЛАСС ОТЕЛЯ ---
class Hotel:
    def __init__(self, name: str):
        self.name = name
        self.rooms: List[Room] = []
        self.bookings: List[Booking] = []

    def add_room(self, room: Room):
        self.rooms.append(room)

    def get_available_rooms(self, start_date: date, end_date: date) -> List[Room]:
        """Возвращает список номеров, свободных на указанные даты."""
        available = []
        for room in self.rooms:
            # Ищем, есть ли активное бронирование на этот номер с пересечением дат
            is_booked = any(
                b.room == room and b.is_active and b.overlaps(
                    start_date, end_date)
                for b in self.bookings
            )
            if not is_booked:
                available.append(room)
        return available

    def book_room(self, room_number: str, start_date: date, end_date: date, guest_name: str) -> Optional[Booking]:
        """Создает бронирование, если номер доступен."""
        # Находим номер по номеру
        room = next((r for r in self.rooms if r.number == room_number), None)

        if not room:
            print(f"Ошибка: Номера {room_number} не существует.")
            return None

        # Проверяем доступность
        if room in self.get_available_rooms(start_date, end_date):
            booking = Booking(room, start_date, end_date, guest_name)
            self.bookings.append(booking)
            print(
                f"Успешно забронирован {room} на имя {guest_name} с {start_date} по {end_date}.")
            return booking
        else:
            print(f"Ошибка: Номер {room_number} уже занят на эти даты.")
            return None

    def cancel_booking(self, booking: Booking):
        """Отменяет конкретное бронирование."""
        if booking in self.bookings:
            booking.cancel()
            print(f"Бронирование номера {booking.room.number} отменено.")

    def get_booked_rooms(self) -> List[Room]:
        """Возвращает список номеров, которые сейчас забронированы (активные брони)."""
        # Используем set, чтобы избежать дубликатов, если на номер было несколько броней
        booked = {b.room for b in self.bookings if b.is_active}
        return list(booked)


if __name__ == "__main__":
    # 1. Создаем отель и добавляем номера
    hotel = Hotel("Гранд Отель")
    hotel.add_room(Room("101", 2000))
    hotel.add_room(Room("102", 2500))
    hotel.add_room(Suite("201", 5000, 1.5))  # Цена будет 7500

    # 2. Проверяем доступные номера на конкретные даты
    d1 = date(2024, 6, 1)
    d2 = date(2024, 6, 5)

    print("--- Доступные номера на начало июня ---")
    for room in hotel.get_available_rooms(d1, d2):
        print(room)

    # 3. Бронируем номер
    print("\n--- Бронирование ---")
    booking1 = hotel.book_room("101", d1, d2, "Иван")
    # Пытаемся снова забронировать 101 номер на эти же даты
    hotel.book_room("101", d1, d2, "Петр")

    # 4. Смотрим забронированные номера
    print("\n--- Забронированные номера ---")
    for room in hotel.get_booked_rooms():
        print(room)

    # 5. Отменяем бронь
    print("\n--- Отмена брони ---")
    if booking1:
        hotel.cancel_booking(booking1)

    # 6. Снова смотрим доступные
    print("\n--- Доступные номера после отмены ---")
    for room in hotel.get_available_rooms(d1, d2):
        print(room)
