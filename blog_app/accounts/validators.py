from django.core.exceptions import ValidationError


def validate_letters_dash_only(value):
    for ch in value:
        if not (ch.isalpha() or ch=='-'):
            raise ValidationError('Your name must contain letters or dash only')