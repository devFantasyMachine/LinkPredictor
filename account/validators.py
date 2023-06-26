from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


# todo update regex
class PhoneValidator(RegexValidator):
    """ Validator for phone number"""

    _regex = r"^-?\d+\Z"

    def __init__(self, message=None, ):
        super().__init__(regex=PhoneValidator._regex, message=message)

    def __call__(self, value):
        if not isinstance(value, str):
            raise ValidationError(self.message, params={"value": value})

        super().__call__(value)
