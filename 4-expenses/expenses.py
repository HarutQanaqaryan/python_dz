expenses = [1200, 850, 1500, 700, 1100, 950, 1300]

# Считаем показатели
total = sum(expenses)
average = total / len(expenses)
minimum = min(expenses)
maximum = max(expenses)

summary = (minimum, maximum, total)

print(f"Кортеж (min, max, sum): {summary}")

s = input().strip().lower()
words = s.split()

words = [w for w in words if w]

rub = None
kop = 0

if len(words) == 2 and words[1] == "руб":
    rub = words[0]
elif len(words) == 4 and words[1] == "руб" and words[3] == "коп":
    rub = words[0]
    kop = words[2]
else:
    print("Некорректный формат суммы")
    exit()

if not rub.isdigit():
    print("Некорректный формат суммы")
    exit()

if kop != 0:
    if not kop.isdigit() or int(kop) > 99:
        print("Некорректный формат суммы")
        exit()
    kop = int(kop)
else:
    kop = 0

rub = int(rub)

print(f"{rub}.{kop:02d} ₽")