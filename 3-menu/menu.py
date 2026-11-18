preference = input("Выберите категорию (напиток/суп/десерт): ")

variant = ""

if preference == "напиток":
    variant = input("чай/кофе/сок: ")
elif preference == "суп":
    variant = input("борщ/щи/суп-пюре: ")
elif preference == "десерт":
    variant = input("торт/мороженое/фрукты: ")
else:
    print("Нет такой позиции")

match variant:
    case "чай" | "кофе" | "сок":
        print("Цена: 200")
    case "борщ" | "щи" | "суп-пюре":
        print("Цена: 300")
    case "торт" | "мороженое" | "фрукты":
        print("Цена: 500")
    case _:
        print("Нет такой позиции") 