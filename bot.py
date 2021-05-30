import telebot
import requests
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery, Message
from database import new_user, edit_user, get_user
import os

token = os.environ['TOKEN_KEY']
bot = telebot.TeleBot(token)
url = 'https://free.currconv.com/api/v7/convert'
api_key = '30a019dd6866e32564d6'

markup = InlineKeyboardMarkup()
itembtn1 = InlineKeyboardButton('USD', callback_data='usd')
itembtn2 = InlineKeyboardButton('EUR', callback_data='eur')
markup.add(itembtn1, itembtn2)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: Message):
    new_user(message.from_user.id)
    msg = bot.send_message(message.chat.id, "Выберите валюту", reply_markup=markup)


@bot.message_handler(commands=['recent'])
def send_welcome(message: Message):
    new_user(message.from_user.id)
    txt = get_user(message.from_user.id).rate
    msg = bot.send_message(message.chat.id, f"Недавний запрос:\n{txt}", reply_markup=markup)


@bot.callback_query_handler(func=lambda m: True)
def callback_handler(callback: CallbackQuery):
    new_user(callback.from_user.id)
    data = callback.data.upper()
    txt = f"1 {data} -> {convert(data, 'RUB')}р."
    edit_user(callback.from_user.id, rate=txt)
    bot.edit_message_text(txt, callback.from_user.id,
                          callback.message.id, reply_markup=markup)


@bot.message_handler(content_types='text')
def money_step(message: Message):
    new_user(message.from_user.id)
    bot.send_message(message.chat.id, 'Выбери курс:', reply_markup=markup, parse_mode="Markdown")


def convert(first, second):
    params = {'q': f'{first}_{second}', 'compact': 'ultra', 'apiKey': api_key}
    response = requests.get(url, params=params).json()
    res = response[list(response.keys())[0]]
    return round(res, 6)


if __name__ == '__main__':
    bot.polling(none_stop=True)
