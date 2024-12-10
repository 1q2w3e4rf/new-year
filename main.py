import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from bs4 import BeautifulSoup
import requests
import datetime

TOKEN = '6804594259:AAEu03onfNbMDd4HmS9-QvuWcOqxLfQl--I'

bot = telebot.TeleBot(TOKEN)

def parse_legends(url):
    """Парсинг фактов"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    legends = soup.find_all('p')
    return [legend.text for legend in legends]

legends = parse_legends('https://gainynv-news.ru/news/media/2021/12/6/100-i-1-zabavnyih-faktov-pro-novyij-god/')

def time_until_new_year():
    """Время до Нового года"""
    now = datetime.datetime.now()
    next_year = now.year + 1
    new_year = datetime.datetime(next_year, 1, 1, 0, 0, 0)
    time_left = new_year - now

    days = time_left.days
    hours = time_left.seconds // 3600
    minutes = (time_left.seconds % 3600) // 60
    seconds = time_left.seconds % 60

    return days, hours, minutes, seconds

# --- Команды бота ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Отправка приветственного сообщения"""
    bot.send_message(message.chat.id, f"Приветствую, {message.from_user.first_name}! Я - бот, который будет отправлять тебе 100 и 1 факт про новый год\nКоманда: /fact")

# Обработка команды /time
@bot.message_handler(commands=['time'])
def send_time_until_new_year(message):
    """Отправка времени до Нового года"""
    days, hours, minutes, seconds = time_until_new_year()
    bot.send_message(message.chat.id, f"До Нового года осталось: {days} дней, {hours} часов, {minutes} минут, {seconds} секунд")

# --- Сессия фактов ---
user_removed_numbers = {}
next_fact_number = {}
fact_session_active = {}
seen_facts = {}

# Обработка команды /fact
@bot.message_handler(commands=['fact'])
def send_legends(message):
    """Отправка фактов"""
    user_id = message.chat.id
    # Проверка на активность сессии
    if user_id in fact_session_active and fact_session_active[user_id]:
        bot.send_message(message.chat.id, "Сессия фактов уже активна.")
        return
    """Создаем первый факт"""
    next_fact_number[user_id] = 1
    seen_facts[user_id] = set()
    fact_session_active[user_id] = True # Активируем сессию
    keyboard = ReplyKeyboardMarkup()
    keyboard.add(KeyboardButton('1'))
    bot.send_message(message.chat.id, "Выберите номер факта:", reply_markup=keyboard)

# Обработка текстовых сообщений
@bot.message_handler(content_types=['text'])
def send_fact(message):
    """Обработка текстовых сообщений"""
    user_id = message.chat.id
    """Проверка какой факт отправлять"""
    if user_id not in user_removed_numbers:
        user_removed_numbers[user_id] = set()
        next_fact_number[user_id] = 1
    """Проверка на выбор факта"""
    if message.text == "24" and message.text.isdigit() and int(message.text) == next_fact_number[user_id] and next_fact_number[user_id] <= len(legends):
        fact_number = int(message.text) - 1
        bot.send_message(message.chat.id, legends[fact_number])
        user_removed_numbers[user_id].add(int(message.text))
        keybord = InlineKeyboardMarkup()
        keybord.add(InlineKeyboardButton("Нет", callback_data="no"))
        bot.send_message(message.chat.id, "Ты ничего сказать не хочешь?", reply_markup=keybord)
        return
    """Проверка на выбор факта"""
    if message.text == "52" and message.text.isdigit() and int(message.text) == next_fact_number[user_id] and next_fact_number[user_id] <= len(legends):
        fact_number = int(message.text) - 1
        bot.send_message(message.chat.id, legends[fact_number])
        user_removed_numbers[user_id].add(int(message.text))
        keybord = InlineKeyboardMarkup()
        keybord.add(InlineKeyboardButton("Точно!", callback_data="exactly"))
        bot.send_message(message.chat.id, "ТОЧНО?!", reply_markup=keybord)
        return
    """Проверка на выбор факта"""
    if message.text == "75" and message.text.isdigit() and int(message.text) == next_fact_number[user_id] and next_fact_number[user_id] <= len(legends):
        fact_number = int(message.text) - 1
        bot.send_message(message.chat.id, legends[fact_number])
        user_removed_numbers[user_id].add(int(message.text))
        keybord = InlineKeyboardMarkup()
        keybord.add(InlineKeyboardButton("Что именно?", callback_data="what_exactly"))
        bot.send_message(message.chat.id, "Не ожидал это от тебя", reply_markup=keybord)
        return
    """Проверка на выбор факта"""
    if message.text == "101" and message.text.isdigit() and int(message.text) == next_fact_number[user_id] and next_fact_number[user_id] <= len(legends):
        fact_number = int(message.text) - 1
        bot.send_message(message.chat.id, legends[fact_number])
        keybord = InlineKeyboardMarkup()
        keybord.add(InlineKeyboardButton("Я все понял поздравляю!!!", callback_data="new_year"))
        bot.send_message(message.chat.id, "Может хоть я и бот но может и меня поздравишь с новым годом?", reply_markup=keybord)
        return
    """Проверка на текст"""
    if message.text == "Ну ладно Поздравляю!":
        bot.send_message(message.chat.id, "🎄С Новым годом!🎄")
        return

    """Проверка на выбор факта"""
    if message.text.isdigit() and int(message.text) == next_fact_number[user_id] and next_fact_number[user_id] <= len(legends):
        fact_number = int(message.text) - 1
        bot.send_message(message.chat.id, legends[fact_number])
        user_removed_numbers[user_id].add(int(message.text))
        next_fact_number[user_id] += 1

        """Вывод факта"""
        keyboard = ReplyKeyboardMarkup()
        # Проверяем, есть ли следующий факт
        if next_fact_number[user_id] <= len(legends):
            keyboard.add(KeyboardButton(str(next_fact_number[user_id])))
        bot.send_message(message.chat.id, "Выберите номер факта:", reply_markup=keyboard)
    # Если пользователь ввел неверный номер
    else:
        bot.send_message(message.chat.id, "Неверный номер факта")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """Обработка нажатий кнопок"""
    if call.data == "no":
        user_id = call.message.chat.id
        next_fact_number[user_id] += 1
        keybord = ReplyKeyboardMarkup()
        keybord.add(KeyboardButton("25"))
        bot.send_message(call.message.chat.id, "Ну и ладно!", reply_markup=keybord)

    elif call.data == "exactly":
        user_id = call.message.chat.id
        next_fact_number[user_id] += 1
        keybord = ReplyKeyboardMarkup()
        keybord.add(KeyboardButton("53"))
        bot.send_message(call.message.chat.id, "Хорошо...", reply_markup=keybord)

    elif call.data == "what_exactly":
        user_id = call.message.chat.id
        next_fact_number[user_id] += 1
        keybord = ReplyKeyboardMarkup()
        keybord.add(KeyboardButton("76"))
        bot.send_message(call.message.chat.id, "...", reply_markup=keybord)

    elif call.data == "new_year":
        user_id = call.message.chat.id
        next_fact_number[user_id] += 1
        bot.send_message(call.message.chat.id, "🎄С Новым годом!🎄")

bot.infinity_polling()
