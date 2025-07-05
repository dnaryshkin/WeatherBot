import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_NAME = os.getenv('TELEGRAM_NAME')

HI_MESSAGE = (
    'Привет! 👋 Я - твой персональный метеобот! 🌤️ '
    'Я могу подсказать текущую погоду в любом городе мира. Просто напиши мне '
    'название города, и я пришлю актуальный прогноз!\n'
    'Например:\n'
    '• "Москва"\n'
    '• "London"\n'
    '• "Токио"\n'
    'Это мой первый пет-проект, так что если что-то пойдет не так - ты всегда '
    f'можешь написать моему создателю {TELEGRAM_NAME} 😊\n'
    'Попробуем? Напиши мне название города! 🌍'
)

WEATHER_EMOJIS = {
    '01d': '☀️', '01n': '🌙',
    '02d': '⛅', '02n': '☁️',
    '03d': '☁️', '03n': '☁️',
    '04d': '☁️', '04n': '☁️',
    '09d': '🌧️', '09n': '🌧️',
    '10d': '🌦️', '10n': '🌧️',
    '11d': '⛈️', '11n': '⛈️',
    '13d': '❄️', '13n': '❄️',
    '50d': '🌫️', '50n': '🌫️',
}

DIRECTIONS_WIND = (
    'Северный','Северо-восточный', 'Восточный', 'Юго-восточный', 'Южный',
    'Юго-западный', 'Западный', 'Северо-западный',
)

URL_WEATHER = ('https://api.openweathermap.org/data/2.5/weather?q={city_name}'
               '&lang=ru&appid={API_key}&units=metric')

ENDPOINT = ('https://api.openweathermap.org/data/2.5/weather?q=London'
            '&appid={API_key}')