expenses = [1200, 850, 1500, 700, 1100, 950, 1300]

# Считаем показатели
total = sum(expenses)
average = total / len(expenses)
minimum = min(expenses)
maximum = max(expenses)

summary = (minimum, maximum, total)

# print(f"Кортеж (min, max, sum): {summary}")

for i in range(3):
    if i == 1: continue
    print(i)