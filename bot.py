import telebot
import requests
from telebot import types

bot = telebot.TeleBot('1830224590:AAFnIJme-YVmdNY2IF12PRZCQ6RMjntlCGM')
url = 'http://data.fixer.io/api/latest?access_key=2d115dcac0b40b1e71c4de44fef23881'

response = requests.get(url).json()
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

itembtn1 = types.KeyboardButton('Узнать курс валюты')
itembtn2 = types.KeyboardButton('Узнать PriceList в очках')
markup.add(itembtn1, itembtn2)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    msg = bot.send_message(message.chat.id, "Выберите валюту", reply_markup=markup)
itembtn1 = types.KeyboardButton('USD')
itembtn2 = types.KeyboardButton('EUR')
markup.add(itembtn1, itembtn2)

@bot.message_handler(content_types='text')
def money_step(message):
    currency = message.text
    if currency not in response["rates"]:
        bot.send_message(message.chat.id, "Неверный курс", reply_markup=markup, parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, convert(currency, 'RUB'), reply_markup=markup, parse_mode="Markdown")


def convert(first, second):
    return round(response['rates'][second] / response['rates'][first], 4)


if __name__ == '__main__':
    bot.polling()
