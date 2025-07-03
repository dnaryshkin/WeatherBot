class RequestResponseError(Exception):
    """Ошибка при запросе к API."""

class TokenError(Exception):
    """Ошибка обязательных переменных окружения."""

class StatusHomeworkError(Exception):
    """Ошибка статуса домашнего задания."""