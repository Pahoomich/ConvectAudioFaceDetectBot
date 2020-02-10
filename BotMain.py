import telebot
import config

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    pass


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Привет, мой создатель')
    elif message.text.lower() == 'пока':
        bot.send_message(message.chat.id, 'Прощай, создатель')


bot.polling()
