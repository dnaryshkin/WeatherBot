import logging
import os

import requests
import telebot
from dotenv import load_dotenv
import exceptions
from constants import HI_MESSAGE, WEATHER_EMOJIS, DIRECTIONS_WIND, URL_GEO, URL_WEATHER
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

def wind_direction(weather_data):
    """Функция получения направления ветра."""
    deg_wind_speed = weather_data['wind']['deg']
    direction = int((deg_wind_speed + 22.5) % 360 / 45)
    direction_wind = DIRECTIONS_WIND[direction]
    return direction_wind

def check_availible_api():
    """Функция проверки доступности API."""
    try:
        URL = 'http://api.openweathermap.org/'
        response = requests.get(URL)
        if response.status_code != HTTPStatus.OK:
            message_error = f'Возникла ошибка: {response.status_code}'
            logging.error(message_error)
            raise exceptions.RequestResponseError(message_error)
        else:
            response = response.json()
            return response
    except Exception as error:
        logging.error(f'Ошибка доступности API {error}')
        raise exceptions.RequestResponseError(error)

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
    try:
        url = URL_GEO.format(text_message=text_message, API_TOKEN=API_TOKEN)
        response = requests.get(url).json()
        if not response:
            bot.send_message(message.chat.id,
                             f'К сожалению я не смог найти город '
                             f'{text_message}. Проверь пожалуйста '
                             f'правильность написания.')
            return
        lat = response[0]['lat']
        lon = response[0]['lon']
        find_weather(message, lat, lon)
    except Exception as error:
        logging.error(f'Ошибка выполнения запроса {error}')
        raise exceptions.RequestResponseError(error)

def find_weather(message, lat, lon):
    """Функция получения прогноза погоды по долготе и широте."""
    try:
        url = URL_WEATHER.format(lat=lat, lon=lon, API_TOKEN=API_TOKEN)
        weather_data = requests.get(url).json()
        city = weather_data['name']
        country = weather_data['sys']['country']
        temperature = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        weather_icon = weather_data['weather'][0]['icon']
        weather_desc = weather_data['weather'][0]['description']
        humidity = weather_data['main']['humidity']
        pressure = weather_data['main']['pressure']
        wind_speed = weather_data['wind']['speed']
        direction_wind = wind_direction(weather_data)

        weather_report = (
            f'Текущая погода в {city}, страна({country}):\n'
            f'🌡️Температура: {temperature}°C (ощущается как {feels_like}°C)\n'
            f' {WEATHER_EMOJIS[weather_icon]}Состояние: {weather_desc.capitalize()}\n'
            f"💧 Влажность: {humidity}%\n"
            f"📉 Давление: {pressure} гПа\n"
            f"💨 Ветер: {wind_speed} м/с\n"
            f'🧭 Направление ветра: {direction_wind.capitalize()}\n'
        )
        chat = message.chat
        chat_id = chat.id
        bot.send_message(chat_id=chat_id, text=weather_report)

    except Exception as error:
        logging.error(f'Ошибка при получении погоды: {error}')
        bot.send_message(message.chat.id, "⚠️ Не удалось получить погоду.")


bot.polling(10)
def main():
    check_env()
    pass


if __name__ == '__main__':
    main()