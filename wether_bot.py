import logging
import os
import sys
import time
from http import HTTPStatus

import requests
import telebot
from dotenv import load_dotenv
from telebot import TeleBot

import exceptions

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
API_TOKEN = os.getenv('API_TOKEN')
ENDPOINT = os.getenv('ENDPOINT')


def check_tokens():
    """Функция проверяет доступность переменных окружения."""
    secret_tokens = {
        'API_TOKEN': API_TOKEN,
        'TELEGRAM_TOKEN': TELEGRAM_TOKEN,
        'TELEGRAM_CHAT_ID': TELEGRAM_CHAT_ID,
    }

    unavailible_tokens = []

    for token_name, token_value in secret_tokens.items():
        if token_value is None:
            unavailible_tokens.append(token_name)
    if len(unavailible_tokens) > 0:
        error_message = (
            'Отсутствует обязательная переменная окружения:'
            f'{", ".join(unavailible_tokens)}'
        )
        logging.critical(error_message)
        raise exceptions.TokenError(error_message)
    else:
        return True

