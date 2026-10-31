import random


def get_computer_choice():
    choices = ["камень", "ножницы", "бумага"]
    return random.choice(choices)


def determine_winner(player, computer):
    if player == computer:
        return "ничья"
        
    if (
        (player == "камень" and computer == "ножницы") or
        (player == "ножницы" and computer == "бумага") or
        (player == "бумага" and computer == "камень")
    ):
        return "игрок"
    
    return "компьютер"


def main():
    player_score = 0
    computer_score = 0

    print("Добро пожаловать в игру \"Камень-Ножницы-Бумага\"!")
    print("Правила:")
    print("- Камень бьет ножницы")
    print("- Ножницы бьют бумагу")
    print("- Бумага бьет камень")
    print("Игра идет до 3 очков.\n")

    while player_score < 3 and computer_score < 3:
        player = input("Введите камень, ножницы или бумага: ").lower()
        if player not in ["камень", "ножницы", "бумага"]:
            print("Неверный ввод! Попробуйте снова.\n")
            continue

        computer = get_computer_choice()
        print("Компьютер выбрал:", computer)
        winner = determine_winner(player, computer)

        if winner == "ничья":
            print("Ничья!")
        elif winner == "игрок":
            print("Вы выиграли раунд!")
            player_score += 1
        else:
            print("Компьютер выиграл раунд!")
            computer_score += 1

        print(f"Счет: Игрок {player_score} : {computer_score} Компьютер\n")

    print("Игра окончена!")
    print(f"Финальный счет: Игрок {player_score}: {computer_score} Компьютер")
    if player_score == 3:
        print("Поздравляем! Вы победили!")
    else:
        print("Победил компьютер!")


if __name__ == "__main__":
    main()