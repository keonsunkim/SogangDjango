from django.db import models
from django.core import checks

import phonenumbers


class PhoneNumberField(models.CharField):

    def __init__(self, allowed_countries, *args, **kwargs):
        self.allowed_countries = allowed_countries
        super(PhoneNumberField, self).__init__(*args, **kwargs)

    def check(self, **kwargs):
        errors = super(PhoneNumberField, self).check(**kwargs)
        errors.extend(self._check_phonenumbers_library_installed())
        return errors

    def _check_phonenumbers_library_installed(self):
        try:
            import phonenumbers  # NOQA
        except ImportError:
            return [
                checks.Error(
                    'Cannot use PhoneNumberField because phonenumbers is not installed.',
                    hint=('Get phonenumbers at https://pypi.org/project/phonenumbers/+ '
                          'or run command "pip install phonenumbers".'),
                    obj=self,
                    id='fields.E999',
                )
            ]
        else:
            return []


    def deconstruct(self):
        name, path, args, kwargs = super(PhoneNumberField, self).deconstruct()
        kwargs['allowed_countries'] = self.allowed_countries
        return name, path, args, kwargs

    def get_prep_value(self, value):
        phone_number = phonenumbers.parse(str(value))
        if str(phone_number.country_code) not in self.allowed_countries:
            val_err_msg = f"doesn't allow {phone_number.country_code} country number"
            raise ValueError(val_err_msg)
        if phonenumbers.is_valid_number(phone_number):
            return_value = phonenumbers.format_number(
                phone_number, phonenumbers.PhoneNumberFormat.E164)
            return return_value
        else:
            raise ValueError("Phone number not valid")
