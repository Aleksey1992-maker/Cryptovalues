import telebot
from config import keys, TOKEN
from extensions import CryptoConverter, APIException

bot = telebot.TeleBot(TOKEN)

# Инструкции:
@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = ('Чтобы начать работу, введите команду боту в следующем формате:\n'
            '<имя валюты, цену которой вы хотите узнать> \
<имя валюты, в которой надо узнать цену первой валюты> \
<количество первой валюты>\n <Увидеть список всех доступных валют: /values>')
    bot.reply_to(message, text)


#Доступные валюты
@bot.message_handler(commands=['values'])
def show_values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):











    try:
        values = message.text.split()
        if len(values) != 3:
            raise APIException('Слишком много параметров.')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except CryptoConverter as e:
        bot.reply_to(message, f'Ошибка пользователя\n {e}')
    except APIException as e:
        bot.reply_to(message, f'Не удалось обработать команду\n {e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()