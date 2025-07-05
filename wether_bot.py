import logging
import os
import sys

import requests
import telebot
from dotenv import load_dotenv

import exceptions
from constants import HI_MESSAGE, WEATHER_EMOJIS, URL_WEATHER
from utils import check_env, wind_direction, report_weather_generation

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
API_TOKEN = os.getenv('API_TOKEN')
TELEGRAM_NAME = os.getenv('TELEGRAM_NAME')

bot = telebot.TeleBot(token=TELEGRAM_TOKEN)


@bot.message_handler(commands=['start'])
def say_hello(message):
    """Функция отправки приветственного сообщения."""
    chat = message.chat
    chat_id = chat.id
    bot.send_message(chat_id=chat_id, text=HI_MESSAGE)


@bot.message_handler(content_types=['text'])
def get_weather_data(message):
    """Функция получения прогноза погоды по тексту пользователя."""
    text_message = message.text
    url = URL_WEATHER.format(city_name=text_message, API_key=API_TOKEN)
    chat_id = message.chat.id

    try:
        response = requests.get(url)

        if response.status_code == 404:
            bot.send_message(
                chat_id=chat_id,
                text='Я не знаю такой город. Проверь правильность написания.'
            )
        elif response.status_code == 200:
            response = response.json()
            bot.send_message(
                chat_id=chat_id,text=report_weather_generation(response))

    except Exception as e:
        logging.error(f'Ошибка запроса к API {e}')
        raise exceptions.RequestResponseError(e)

bot.polling(10)

def main():
    try:
        check_env()
    except exceptions.TokenError:
        logging.critical('Работа бота остановлена!')
        sys.exit()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        filename='program.log',
        encoding='utf-8',
        filemode='w',
        format=(
            '%(asctime)s, '
            '%(levelname)s, '
            '%(message)s, '
            'Название функции: %(funcName)s, '
            'Номер строки: %(lineno)d'
        )
    )
    main()
