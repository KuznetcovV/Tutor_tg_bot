import telebot

bot = telebot.TeleBot('8373059069:AAFQdymiliVXviKBFxB-hmMHLK4QsJaWJI0')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет!')


bot.polling(none_stop=True)