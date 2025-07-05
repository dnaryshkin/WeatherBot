import logging
import os
from http import HTTPStatus

import requests
from dotenv import load_dotenv

import exceptions
from constants import DIRECTIONS_WIND, WEATHER_EMOJIS, ENDPOINT

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
API_TOKEN = os.getenv('API_TOKEN')
TELEGRAM_NAME = os.getenv('TELEGRAM_NAME')


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

        logging.info('Все обязательные переменные найдены!')
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
        response = requests.get(ENDPOINT.format(API_key=API_TOKEN))
        if response.status_code != HTTPStatus.OK:
            message_error = f'Возникла ошибка: {response.status_code}'
            logging.error(message_error)
            raise exceptions.RequestResponseError(message_error)
        else:
            response = response.json()
            logging.info('API доступно!')
            return response
    except Exception as error:
        logging.error(f'Ошибка доступности API {error}')
        raise exceptions.RequestResponseError(error)


def report_weather_generation(response):
    """Функция подготовки ответа с прогнозом погоды."""
    city = response['name']
    country = response['sys']['country']
    temperature = response['main']['temp']
    feels_like = response['main']['feels_like']
    weather_icon = response['weather'][0]['icon']
    weather_desc = response['weather'][0]['description']
    humidity = response['main']['humidity']
    pressure = response['main']['pressure']
    wind_speed = response['wind']['speed']
    direction_wind = wind_direction(response)

    weather_report = (
        f'Текущая погода в {city}, страна({country}):\n'
        f'🌡️Температура: {temperature}°C (ощущается как {feels_like}°C)\n'
        f'{WEATHER_EMOJIS[weather_icon]}Состояние: '
        f'{weather_desc.capitalize()}\n'
        f"💧 Влажность: {humidity}%\n"
        f"📉 Давление: {pressure} гПа\n"
        f"💨 Ветер: {wind_speed} м/с\n"
        f'🧭 Направление ветра: {direction_wind.capitalize()}\n'
    )
    return weather_report
