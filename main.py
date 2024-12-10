import telebot
from telebot import types
from bs4 import BeautifulSoup
import requests
import datetime

TOKEN = ''

bot = telebot.TeleBot(TOKEN)

# Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Приветствую, {message.from_user.first_name}! Я - бот, который будет отправлять тебе 100 и 1 факт про новый год\nКоманда: /fact")

# Функция для парсинга фактов
def parse_legends(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    legends = soup.find_all('p')
    return [legend.text for legend in legends]

legends = parse_legends('https://gainynv-news.ru/news/media/2021/12/6/100-i-1-zabavnyih-faktov-pro-novyij-god/')

def time_until_new_year():
    now = datetime.datetime.now()
    next_year = now.year + 1
    new_year = datetime.datetime(next_year, 1, 1, 0, 0, 0)
    time_left = new_year - now

    days = time_left.days
    hours = time_left.seconds // 3600
    minutes = (time_left.seconds % 3600) // 60
    seconds = time_left.seconds % 60

    return days, hours, minutes, seconds

# Обработка команды /time
@bot.message_handler(commands=['time'])
def send_time_until_new_year(message):
    days, hours, minutes, seconds = time_until_new_year()
    bot.send_message(message.chat.id, f"До Нового года осталось: {days} дней, {hours} часов, {minutes} минут, {seconds} секунд")

# Переменные
removed_numbers = set()
user_removed_numbers = {}
next_fact_number = {}
fact_session_active = {}
seen_facts = {}

# Обработка команды /fact
@bot.message_handler(commands=['fact'])
def send_legends(message):
    user_id = message.chat.id
    # Проверка на активность сессии
    if user_id in fact_session_active and fact_session_active[user_id]:
        bot.send_message(message.chat.id, "Сессия фактов уже активна.")
        return

    next_fact_number[user_id] = 1
    seen_facts[user_id] = set()
    fact_session_active[user_id] = True # Активируем сессию
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.add(types.KeyboardButton('1'))
    bot.send_message(message.chat.id, "Выберите номер факта:", reply_markup=keyboard)

# Обработка текстовых сообщений
@bot.message_handler(content_types=['text'])
def send_fact(message):
    user_id = message.chat.id
    # Проверяем, что пользователь ещё не увидел этот факт
    if user_id not in user_removed_numbers:
        user_removed_numbers[user_id] = set()
        next_fact_number[user_id] = 1
    
    if message.text == "24" and message.text.isdigit() and int(message.text) == next_fact_number[user_id] and next_fact_number[user_id] <= len(legends):
        fact_number = int(message.text) - 1
        bot.send_message(message.chat.id, legends[fact_number])
        user_removed_numbers[user_id].add(int(message.text))
        keybord = types.InlineKeyboardMarkup()
        keybord.add(types.InlineKeyboardButton("Нет", callback_data="no"))
        bot.send_message(message.chat.id, "Ты ничего сказать не хочешь?", reply_markup=keybord)
        return

    if message.text == "52" and message.text.isdigit() and int(message.text) == next_fact_number[user_id] and next_fact_number[user_id] <= len(legends):
        fact_number = int(message.text) - 1
        bot.send_message(message.chat.id, legends[fact_number])
        user_removed_numbers[user_id].add(int(message.text))
        keybord = types.InlineKeyboardMarkup()
        keybord.add(types.InlineKeyboardButton("Точно!", callback_data="yes"))
        bot.send_message(message.chat.id, "ТОЧНО?!", reply_markup=keybord)
        return


    if message.text == "75" and message.text.isdigit() and int(message.text) == next_fact_number[user_id] and next_fact_number[user_id] <= len(legends):
        fact_number = int(message.text) - 1
        bot.send_message(message.chat.id, legends[fact_number])
        user_removed_numbers[user_id].add(int(message.text))
        keybord = types.InlineKeyboardMarkup()
        keybord.add(types.InlineKeyboardButton("Что именно?", callback_data="rek"))
        bot.send_message(message.chat.id, "Не ожидал это от тебя", reply_markup=keybord)
        return

    if message.text == "101" and message.text.isdigit() and int(message.text) == next_fact_number[user_id] and next_fact_number[user_id] <= len(legends):
        fact_number = int(message.text) - 1
        bot.send_message(message.chat.id, legends[fact_number])
        keybord = types.InlineKeyboardMarkup()
        keybord.add(types.InlineKeyboardButton("Я все понял поздравляю!!!", callback_data="rek1"))
        bot.send_message(message.chat.id, "Может хоть я и бот но может и меня поздравишь с новым годом?", reply_markup=keybord)
        return
    
    if message.text == "Ну ладно Поздравляю!":
        bot.send_message(message.chat.id, "🎄С Новым годом!🎄")
        return

    # Сравниваем введенный пользователем номер с номером следующего факта
    if message.text.isdigit() and int(message.text) == next_fact_number[user_id] and next_fact_number[user_id] <= len(legends):
        fact_number = int(message.text) - 1
        bot.send_message(message.chat.id, legends[fact_number])
        user_removed_numbers[user_id].add(int(message.text))
        next_fact_number[user_id] += 1


        keyboard = types.ReplyKeyboardMarkup()
        # Проверяем, есть ли следующий факт
        if next_fact_number[user_id] <= len(legends):
            keyboard.add(types.KeyboardButton(str(next_fact_number[user_id])))
        bot.send_message(message.chat.id, "Выберите номер факта:", reply_markup=keyboard)
    # Если пользователь ввел неверный номер
    else:
        bot.send_message(message.chat.id, "Неверный номер факта")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "no":
        user_id = call.message.chat.id
        next_fact_number[user_id] += 1
        keybord = types.ReplyKeyboardMarkup()
        keybord.add(types.KeyboardButton("25"))
        bot.send_message(call.message.chat.id, "Ну и ладно!", reply_markup=keybord)

    elif call.data == "yes":
        user_id = call.message.chat.id
        next_fact_number[user_id] += 1
        keybord = types.ReplyKeyboardMarkup()
        keybord.add(types.KeyboardButton("53"))
        bot.send_message(call.message.chat.id, "Хорошо...", reply_markup=keybord)

    elif call.data == "rek":
        user_id = call.message.chat.id
        next_fact_number[user_id] += 1
        keybord = types.ReplyKeyboardMarkup()
        keybord.add(types.KeyboardButton("76"))
        bot.send_message(call.message.chat.id, "...", reply_markup=keybord)

    elif call.data == "rek1":
        user_id = call.message.chat.id
        next_fact_number[user_id] += 1
        bot.send_message(call.message.chat.id, "🎄С Новым годом!🎄")

bot.infinity_polling()
