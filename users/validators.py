import re
from django.core.exceptions import ValidationError


def validate_password(field):
    pattern = re.compile(r"^[A-Za-z0-9]+$")
    if not bool(re.match(pattern, field)):
        print("Только цифры и латинские буквы")
        raise ValidationError("Только цифры и латинские буквы")
    if not 8 <= len(field) <= 16:
        print("Пароль должен содержать от 8 до 16 символов")
        raise ValidationError("Пароль должен содержать от 8 до 16 символов")