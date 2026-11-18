price = float(input("Введите сумму: "))
discount = float(input("Введите процент скидки: "))

final_price = price - (price * discount / 100)
print(f"Итоговая цена: {final_price}")