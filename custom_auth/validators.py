from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from custom_auth import settings


username_regex_validator = RegexValidator(
    regex='^[a-zA-Z0-9]+$',
    message='Login must contain only letters and digits.',
    code='invalid_username'
)


def password_length_validator(password):
    minimum_password_length = settings.MINIMUM_PASSWORD_LENGTH
    if len(password) < minimum_password_length:
        raise ValidationError(
            f'Password is too short- it must be at '
            f'least {minimum_password_length} characters long.'
        )


def username_length_validator(username):
    minimum_username_length = settings.MINIMUM_USERNAME_LENGTH
    if len(username) < minimum_username_length:
        raise ValidationError(
            f'Username is too short- it must be at '
            f'least {minimum_username_length} characters long.'
        )
