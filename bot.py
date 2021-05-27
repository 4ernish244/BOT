import telebot
import requests
from telebot import types

bot = telebot.TeleBot ('1830224590:AAFnIJme-YVmdNY2IF12PRZCQ6RMjntlCGM')
url = 'https://currate.ru/api/?get=rates&pairs=USDRUB,EURRUB&key=449b73efbd3e90bc28682fc8872a0522'

response = requests.get(url).json()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itembtn1 = types.KeyboardButton('USD')
    itembtn2 = types.KeyboardButton('EUR')
    markup.add(itembtn1, itembtn2)
    msg = bot.send_message(message.chat.id,
                    "Выберите валюту", reply_markup=markup)
    bot.register_next_step_handler(msg, money_step)

def money_step(message):
    try:
       markup = types.ReplyKeyboardRemove(selective=False)

       for money in response:
           if (message.text == money['data']):
              bot.send_message(message.chat.id, printMoney(money['USDRUB'], money['EURRUB']),
                               reply_markup=markup, parse_mode="Markdown")

    except Exception as e:
       bot.reply_to(message, 'Ты шо творишь , малай!')

def printMoney(USDRUB,EURRUB):
    '''Вывод курса пользователю'''
    return " *Курс доллара:* " + str(USDRUB) + " *Курс евра:* " + str(EURRUB)


bot.enable_save_next_step_handlers(delay=2)


bot.load_next_step_handlers()

bot.polling()



