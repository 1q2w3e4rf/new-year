import telebot
from telebot import types
from bs4 import BeautifulSoup
import requests

TOKEN = '6804594259:AAEu03onfNbMDd4HmS9-QvuWcOqxLfQl--I'

bot = telebot.TeleBot(TOKEN)

# Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Приветствую, {0.first_name}! Я - бот, который будет отправлять тебе 100 и 1 факт про новый год".format(message.from_user))
# Функция для парсинга фактов
def parse_legends(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    legends = soup.find_all('p')
    return [legend.text for legend in legends]

legends = parse_legends('https://gainynv-news.ru/news/media/2021/12/6/100-i-1-zabavnyih-faktov-pro-novyij-god/')

# Обработка команды /fact
@bot.message_handler(commands=['fact'])
def send_legends(message):
    user_id = message.chat.id
    next_fact_number[user_id] = 1 
    user_removed_numbers[user_id] = set()
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.add(types.KeyboardButton('1'))
    bot.send_message(message.chat.id, "Выберите номер факта:", reply_markup=keyboard)

# Переменные
removed_numbers = set()
user_removed_numbers = {}
next_fact_number = {}

# Обработка текстовых сообщений
@bot.message_handler(content_types=['text'])
def send_fact(message):
    user_id = message.chat.id
    # Проверяем, что пользователь ещё не увидел этот факт
    if user_id not in user_removed_numbers:
        user_removed_numbers[user_id] = set()
        next_fact_number[user_id] = 1

    if message.text == "102":
        bot.send_message(message.chat.id, "С Новым годом!")
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

bot.infinity_polling()