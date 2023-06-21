import telebot
from config import keys, TOKEN
from utils import ConvertionException, ValueConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n<имя валюты> <в какую валюту перевести>' \
           ' <количество переводимой валюты>\nИмя валюты необходимо вводить в точности, как в списке доступных валют.' \
           '\nПоказать все доступные валюты: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower()
        values = values.split()

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров!')

        quote, base, amount = values
        total_base = ValueConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}!')
    else:
        text = f'Цена {amount} {keys[quote]} в {keys[base]} - {round(float(total_base) * float(amount), 2)}'
        bot.send_message(message.chat.id, text)


bot.polling()
