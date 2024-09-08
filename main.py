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
    keyboard = types.ReplyKeyboardMarkup()
    for i in range(1, len(legends) + 1):
        keyboard.add(types.KeyboardButton(str(i)))
    bot.send_message(message.chat.id, "Выберите номер факта:", reply_markup=keyboard)

@bot.message_handler(content_types=['text'])
def send_fact(message):
    bot.send_message(message.chat.id, legends[int(message.text) - 1])


bot.polling()