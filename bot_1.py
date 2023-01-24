import telebot
from config import token, keys
from extentions import APIException, Converter
TOKEN = token
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду в следующем формате:\n<имя базовой валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nУвидить список доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message:telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message:telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException(f'Введите три аргумента в соответствии с инструкцией.')

        base, quote, amount = values
        t_base = Converter.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя:\n'{e}'")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду:\n'{e}'")
    else:    
        text = f"Цена {amount} единиц валюты '{base}', в валюте '{quote}'\n составляет - {round(t_base['result'], 2)}"
        bot.send_message(message.chat.id, text)
bot.polling()


