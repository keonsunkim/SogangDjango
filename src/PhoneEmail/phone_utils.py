import random

import phonenumbers
# a google powered phonenumber project!

from django.utils.translation import ugettext_lazy as _

from .CONSTANTS import (ALLOWED_COUNTRY_CODE, )


def _phonenumber_obj_to_e164(phone_number):
    return phonenumbers.format_number(
        phone_number,
        phonenumbers.PhoneNumberFormat.E164)


def _validate_phone_number(value):
    value = str(value)
    phone_number = phonenumbers.parse(value, )
    if phonenumbers.is_valid_number(phone_number):
        if str(phone_number.country_code) in ALLOWED_COUNTRY_CODE.keys():
            return phonenumbers.format_number(
                phone_number,
                phonenumbers.PhoneNumberFormat.E164)
        else:
            msg = _("country code not supported yet and this shouldn't "
                    + "have happened anyways. It should have been checked "
                    + "while registering!")
    else:
        msg = _("phone number is not valid!!")
    raise ValueError(msg)


def _random_verification_number(length):
    return ''.join([str(random.randint(0, 9)) for _ in range(8)])
