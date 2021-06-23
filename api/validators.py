from datetime import datetime

from django.core.exceptions import ValidationError


def validate_year(value):
    """ Validate, that year is not grater current one """

    if value > datetime.now().year:
        raise ValidationError(
            'Введенный год больше текущего'
        )
