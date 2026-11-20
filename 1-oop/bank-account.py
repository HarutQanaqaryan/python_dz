class BankAccount:
    # Атрибут класса для подсчета всех созданных счетов
    _accounts_created = 0

    def __init__(self, owner: str, account_number: str | int, balance: float = 0) -> None:
        self.owner = owner
        self.account_number = account_number
        
        # Проверка баланса при создании
        if balance < 0:
            raise ValueError("Начальный баланс не может быть отрицательным")
        self.balance = float(balance)
        
        # Увеличиваем счетчик созданных счетов
        BankAccount._accounts_created += 1

    def deposit(self, amount: float) -> None:
        """Пополнение счета на сумму amount."""
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть положительной")
        self.balance += amount

    def withdraw(self, amount: float) -> bool:
        """Снятие денег. Возвращает True, если успешно, и False, если недостаточно средств."""
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительной")
            
        if self.balance >= amount:
            self.balance -= amount
            return True
        else:
            print(f"Ошибка: недостаточно средств на счете {self.account_number}.")
            return False

    def transfer_to(self, other_account: "BankAccount", amount: float) -> bool:
        """Перевод на другой счет. Возвращает True при успехе."""
        # Проверка isinstance убрана, доверяем аннотации типов
        if self.withdraw(amount):
            other_account.deposit(amount)
            return True
        return False

    def info(self) -> str:
        """Возвращает строку с информацией о счете."""
        return f"Владелец: {self.owner}, Счет: {self.account_number}, Баланс: {self.balance:.2f}"

    @classmethod
    def get_accounts_created(cls) -> int:
        """Возвращает количество созданных счетов."""
        return cls._accounts_created