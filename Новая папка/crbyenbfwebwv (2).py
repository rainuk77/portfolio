import telebot
from telebot import types
import threading
import time
from datetime import datetime

TOKEN = "8873945912:AAFQX5dh_ZXgrsOkQr4htez5VLfE58wBUUI"
bot = telebot.TeleBot(TOKEN)

users = {}

# Клавиатура
def main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("💧 Выпил 250 мл", "💧 Выпил 500 мл")
    markup.row("⚙️ Настройки", "📊 Статистика")
    markup.row("🔔 Включить", "🔕 Выключить")
    return markup

# Start
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.chat.id

    if user_id not in users:
        users[user_id] = {
            "enabled": False,
            "start_time": "08:00",
            "end_time": "22:00",
            "interval": 2,
            "amount": 250,
            "water_today": 0,
            "last_reminder": None,
            "date": datetime.now().date()
        }

    bot.send_message(
        user_id,
        "Привет!\n\n"
        "Я буду напоминать тебе пить воду.\n\n"
        "Нажимай кнопки после того, как выпил воду.",
        reply_markup=main_keyboard()
    )

# Статистика
@bot.message_handler(func=lambda m: m.text == "📊 Статистика")
def statistics(message):
    user_id = message.chat.id
    user = users[user_id]

    reset_day(user)

    bot.send_message(
        user_id,
        f"Статистика за сегодня:\n\n"
        f"Выпито: {user['water_today']} мл\n"
        f"Это примерно {user['water_today'] / 1000:.2f} л\n\n"
        f"Напоминания: "
        f"{'включены' if user['enabled'] else 'выключены'}"
    )

# Выпил 250
@bot.message_handler(func=lambda m: m.text == "💧 Выпил 250 мл")
def drink_250(message):
    add_water(message.chat.id, 250)

# Выпил 500
@bot.message_handler(func=lambda m: m.text == "💧 Выпил 500 мл")
def drink_500(message):
    add_water(message.chat.id, 500)

# Добавление воды
def add_water(user_id, amount):
    user = users[user_id]
    reset_day(user)
    user["water_today"] += amount

    bot.send_message(
        user_id,
        f"Записал +{amount} мл!\n\n"
        f"Сегодня выпито: {user['water_today']} мл",
        reply_markup=main_keyboard()
    )

# Сброс статистики
def reset_day(user):
    today = datetime.now().date()

    if user["date"] != today:
        user["date"] = today
        user["water_today"] = 0
        user["last_reminder"] = None

# Настройки
@bot.message_handler(func=lambda m: m.text == "⚙️ Настройки")
def settings(message):
    user_id = message.chat.id

    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton(
            "Время начала",
            callback_data="start_time"
        )
    )

    markup.add(
        types.InlineKeyboardButton(
            "Время окончания",
            callback_data="end_time"
        )
    )

    markup.add(
        types.InlineKeyboardButton(
            "Интервал",
            callback_data="interval"
        )
    )

    markup.add(
        types.InlineKeyboardButton(
            "Количество",
            callback_data="amount"
        )
    )

    bot.send_message(
        user_id,
        "Настройки напоминаний:",
        reply_markup=markup
    )

# Callback настроек
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    user_id = call.message.chat.id

    if call.data == "start_time":
        bot.send_message(
            user_id,
            "Напиши время начала.\n\nНапример: 08:00"
        )
        bot.register_next_step_handler(
            call.message,
            set_start_time
        )

    elif call.data == "end_time":
        bot.send_message(
            user_id,
            "Напиши время окончания.\n\nНапример: 22:00"
        )
        bot.register_next_step_handler(
            call.message,
            set_end_time
        )

    elif call.data == "interval":
        bot.send_message(
            user_id,
            "Через сколько часов напоминать?\n\n"
            "Например: 1, 2 или 3"
        )
        bot.register_next_step_handler(
            call.message,
            set_interval
        )

    elif call.data == "amount":
        markup = types.InlineKeyboardMarkup()

        markup.add(
            types.InlineKeyboardButton(
                "250 мл",
                callback_data="amount_250"
            )
        )

        markup.add(
            types.InlineKeyboardButton(
                "500 мл",
                callback_data="amount_500"
            )
        )

        bot.send_message(
            user_id,
            "Сколько воды напоминать выпить?",
            reply_markup=markup
        )

    elif call.data == "amount_250":
        users[user_id]["amount"] = 250
        bot.answer_callback_query(call.id, "Установлено 250 мл")
        bot.send_message(user_id, "Теперь напоминание будет на 250 мл.")

    elif call.data == "amount_500":
        users[user_id]["amount"] = 500
        bot.answer_callback_query(call.id, "Установлено 500 мл")
        bot.send_message(user_id, "Теперь напоминание будет на 500 мл.")

# Время начала
def set_start_time(message):
    try:
        datetime.strptime(message.text, "%H:%M")
        users[message.chat.id]["start_time"] = message.text

        bot.send_message(
            message.chat.id,
            f"Начало установлено: {message.text}"
        )

    except ValueError:
        bot.send_message(
            message.chat.id,
            "Неверный формат. Например: 08:00"
        )

# Время окончания
def set_end_time(message):
    try:
        datetime.strptime(message.text, "%H:%M")
        users[message.chat.id]["end_time"] = message.text

        bot.send_message(
            message.chat.id,
            f"Окончание установлено: {message.text}"
        )

    except ValueError:
        bot.send_message(
            message.chat.id,
            "Неверный формат. Например: 22:00"
        )

# Интервал
def set_interval(message):
    try:
        interval = float(message.text.replace(",", "."))

        if interval <= 0:
            raise ValueError

        users[message.chat.id]["interval"] = interval

        bot.send_message(
            message.chat.id,
            f"Напоминание каждые {interval} ч."
        )

    except ValueError:
        bot.send_message(
            message.chat.id,
            "Напиши число, например 2"
        )

# Включить
@bot.message_handler(func=lambda m: m.text == "🔔 Включить")
def enable(message):
    users[message.chat.id]["enabled"] = True

    bot.send_message(
        message.chat.id,
        f"Напоминания включены!\n\n"
        f"С {users[message.chat.id]['start_time']} "
        f"до {users[message.chat.id]['end_time']}\n"
        f"Каждые {users[message.chat.id]['interval']} ч.\n"
        f"По {users[message.chat.id]['amount']} мл"
    )

# Выключить
@bot.message_handler(func=lambda m: m.text == "🔕 Выключить")
def disable(message):
    users[message.chat.id]["enabled"] = False

    bot.send_message(
        message.chat.id,
        "Напоминания выключены."
    )

# Проверка напоминаний
def reminder_loop():
    while True:
        now = datetime.now()

        for user_id, user in list(users.items()):
            try:
                reset_day(user)

                if not user["enabled"]:
                    continue

                start = datetime.strptime(
                    user["start_time"],
                    "%H:%M"
                ).time()

                end = datetime.strptime(
                    user["end_time"],
                    "%H:%M"
                ).time()

                current = now.time()

                if not (start <= current <= end):
                    continue

                interval_seconds = user["interval"] * 3600
                last = user["last_reminder"]

                if last is None:
                    user["last_reminder"] = now

                    bot.send_message(
                        user_id,
                        f"Время пить воду!\n\n"
                        f"Выпей {user['amount']} мл."
                    )

                else:
                    difference = (
                        now - last
                    ).total_seconds()
                    if difference >= interval_seconds:
                        user["last_reminder"] = now

                        bot.send_message(
                            user_id,
                            f"Напоминание!\n\n"
                            f"Выпей {user['amount']} мл воды."
                        )

            except Exception as e:
                print("Ошибка:", e)

        time.sleep(30)

threading.Thread(
    target=reminder_loop,
    daemon=True
).start()

print("Бот запущен!")

bot.infinity_polling()