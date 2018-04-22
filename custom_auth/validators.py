from django.core.validators import RegexValidator


username_validator = RegexValidator(
    regex='^[a-zA-Z0-9]+$',
    message='Login must contain only lettern and digits.',
    code='invalid_username'
)
