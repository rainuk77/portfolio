import random
import time

users = {}
print("=== Регистрация ===")
username = input("Введите ник: ")
if username in users:
    print("Такой пользователь уже существует.")
    exit()
password = input("Введите пароль: ")
if len(password) < 5 or not password.isalnum():
    print("Пароль должен содержать минимум 5 символов и только латинские буквы и цифры.")
    exit()
users[username] = {
    "password": password,
    "cards": [
        ["Столица Казахстана?", "астана"],
        ["Как зовут человека, который обучает детей?", "учитель"],
        ["Кто крутой?", "я"],
        ["Кто ты?", "человек"],
        ["Кто ментор?", "диана"]
    ],
    "notes": []
}
print("Регистрация успешна!")
print("\n=== Вход ===")
login = input("Введите ник: ")
login_password = input("Введите пароль: ")
if login != username or login_password != password:
    print("Неверный логин или пароль.")
    exit()
print("Вход выполнен!")

while True:
    print("\n1. Добавить карточку")
    print("2. Случайная карточка")
    print("3. Викторина")
    print("4. Добавить заметку")
    print("5. Показать заметки")
    print("6. Удалить заметку")
    print("7. Выход")
    choice = input("Выберите действие: ")

    if choice == "1":
        q = input("Введите вопрос: ")
        a = input("Введите ответ: ").lower()
        users[username]["cards"].append([q, a])
        print("Карточка добавлена.")
    elif choice == "2":
        card = random.choice(users[username]["cards"])
        print("Вопрос:", card[0])
        input("Нажмите Enter...")
        print("Ответ:", card[1])
    elif choice == "3":
        score = 0
        cards = random.sample(users[username]["cards"], len(users[username]["cards"]))
        for card in cards:
            print("\nВопрос:", card[0])
            start = time.time()
            answer = input("Ответ: ").lower()
            finish = time.time()
            if finish - start > 30:
                print("Время вышло!")
                continue
            if answer == card[1]:
                print("Правильно!")
                score += 1
            else:
                print("Неправильно! Правильный ответ:", card[1])
        print(f"\nВаш результат: {score} из {len(cards)}")
    elif choice == "4":
        note = input("Введите заметку: ")
        users[username]["notes"].append(note)
        print("Заметка сохранена.")
    elif choice == "5":
        if not users[username]["notes"]:
            print("Заметок нет.")
        else:
            for i, note in enumerate(users[username]["notes"], 1):
                print(i, "-", note)
    elif choice == "6":
        if not users[username]["notes"]:
            print("Заметок нет.")
        else:
            for i, note in enumerate(users[username]["notes"], 1):
                print(i, "-", note)
            try:
                num = int(input("Введите номер заметки: "))
                if 1 <= num <= len(users[username]["notes"]):
                    users[username]["notes"].pop(num - 1)
                    print("Заметка удалена.")
                else:
                    print("Неверный номер заметки.")
            except ValueError:
                print("Введите корректный номер заметки.")
    elif choice == "7":
        print("До свидания!")
        break
    else:
        print("Неверный выбор")