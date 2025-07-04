import logging
import os
from http import HTTPStatus

import requests
from dotenv import load_dotenv

import exceptions
from constants import DIRECTIONS_WIND

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
