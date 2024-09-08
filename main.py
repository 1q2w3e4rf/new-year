import telebot
from telebot import types
from bs4 import BeautifulSoup
import requests

TOKEN = '6804594259:AAEu03onfNbMDd4HmS9-QvuWcOqxLfQl--I'

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Приветствую, {0.first_name}! Я - бот, который поможёт тебе найти нужный новогодний факт".format(message.from_user))

def parse_legends(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    legends = soup.find_all('p')
    return [legend.text for legend in legends]

legends = parse_legends('https://gainynv-news.ru/news/media/2021/12/6/100-i-1-zabavnyih-faktov-pro-novyij-god/')

@bot.message_handler(commands=['legends'])
def send_legends(message):
    keyboard = types.InlineKeyboardMarkup()
    for i in range(1, len(legends) + 1):
        keyboard.add(types.InlineKeyboardButton(str(i), callback_data=str(i)))
    bot.send_message(message.chat.id, "Выберите номер факта:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data.isdigit():
        legend_index = int(call.data)
        if 1 <= legend_index <= len(legends):
            legend_text = legends[legend_index - 1]
            if legend_text:
                bot.send_message(call.message.chat.id, legend_text)
            else:
                bot.send_message(call.message.chat.id, "Ошибка: Текст легенды пуст")
        else:
            bot.send_message(call.message.chat.id, "Неправильный номер факта")
    else:
        bot.send_message(call.message.chat.id, "Неправильный формат ввода")

bot.polling()