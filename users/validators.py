import re
from django.conf import settings
from django.core.exceptions import ValidationError


def validate_password(field):
    pattern = re.compile(r"^[A-Za-z0-9]+$")
    language = settings.LANGUAGE_CODE
    error_messages = [
        {
            "ru-ru": "Только цифры и латинские буквы",
            "en-us": "Only numbers and Latin letters"
        },
        {
            "ru-ru": "Пароль должен содержать от 8 до 16 символов",
            "en-us": "The password must contain from 8 to 16 characters."
        }
    ]

    try:
        if not bool(re.match(pattern, field)):
            print(error_messages[0][language])
            raise ValidationError(error_messages[0][language])
        if not 8 <= len(field) <= 16:
            print(error_messages[1][language])
            raise ValidationError(error_messages[1][language])
    except KeyError:
        print("Language not found")
