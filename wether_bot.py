import logging
import os

import requests
import telebot
from dotenv import load_dotenv
import exceptions
from message import HI_MESSAGE, WEATHER_EMOJIS

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
API_TOKEN = os.getenv('API_TOKEN')
TELEGRAM_NAME = os.getenv('TELEGRAM_NAME')

bot = telebot.TeleBot(token=TELEGRAM_TOKEN)

def check_env():
    """Функция проверки всех обязательных значений переменных в .env."""
    secret_token = {
        'TELEGRAM_TOKEN': TELEGRAM_TOKEN,
        'API_TOKEN': API_TOKEN,
        'TELEGRAM_NAME': TELEGRAM_NAME,
    }

    unavailible_tokens = []

    for token_name, token in secret_token.items():
        if token is None:
            unavailible_tokens.append(token_name)
        if len(unavailible_tokens) > 0:
            error_message = (
                'Отсутствует обязательная переменная окружения:'
                f'{", ".join(unavailible_tokens)}'
            )
            logging.error(error_message)
            raise exceptions.TokenError(error_message)
        else:
            return True


def check_availible_api():
    """Функция проверки доступности API."""
    pass

@bot.message_handler(commands=['start'])
def say_hello(message):
    """Функция отправки приветственного сообщения."""
    chat = message.chat
    chat_id = chat.id
    bot.send_message(chat_id=chat_id, text=HI_MESSAGE)

@bot.message_handler(content_types=['text'])
def find_city(message):
    """
    Функция получения от пользователя текста названия города по которому
    необходимо предоставить прогноз.
    """
    text_message = message.text
    chat = message.chat
    chat_id = chat.id
    find_geo(message, text_message)

def find_geo(message, text_message):
    """Функция получения долготы и широты города из текста пользователя."""
    URL = (f'http://api.openweathermap.org/geo/1.0/direct?q={text_message}'
           f'&appid={API_TOKEN}')
    response = requests.get(URL).json()
    lat = response[0]['lat']
    lon = response[0]['lon']
    print(lat, lon)
    find_weather(message, lat, lon)

def find_weather(message, lat, lon):
    """Функция получения прогноза погоды по долготе и широте."""
    URL = (f'https://api.openweathermap.org/data/2.5/weather?lat={lat}'
           f'&lon={lon}&lang=ru&appid={API_TOKEN}&units=metric')
    weather_data = requests.get(URL).json()
    city = weather_data['name']
    country = weather_data['sys']['country']
    temperature = weather_data['main']['temp']
    feels_like = weather_data['main']['feels_like']
    weather_icon = weather_data['weather'][0]['icon']
    weather_desc = weather_data['weather'][0]['description']
    humidity = weather_data['main']['humidity']
    pressure = weather_data['main']['pressure']
    wind_speed = weather_data['wind']['speed']
    deg_wind_speed = weather_data['wind']['deg']

    weather_report = (
        f'Погода в {city}, страна({country}):\n'
        f'🌡️Температура: {temperature}°C (ощущается как {feels_like}°C)\n'
        f' {WEATHER_EMOJIS[weather_icon]}Состояние: {weather_desc.capitalize()}\n'
        f"💧 Влажность: {humidity}%\n"
        f"🎚 Давление: {pressure} гПа\n"
        f"🌬 Ветер: {wind_speed} м/с"
    )
    chat = message.chat
    chat_id = chat.id
    bot.send_message(chat_id=chat_id, text=weather_report)



bot.polling(10)
def main():
    check_env()
    pass


if __name__ == '__main__':
    main()