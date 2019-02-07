from datetime import timedelta
# for time check

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
# for models

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
# for

from PhoneEmail.fields import PhoneNumberField
from PhoneEmail.phone_utils import _random_verification_number
# phone number related

from django.conf import settings

User = settings.AUTH_USER_MODEL


class ActivationData(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    # later unallow this to be created when user is already active

    class Meta:
        ordering = ('created', )

    def __str__(self):
        return f"{self.user}:{self.verification_code}:{self.created}"

    # @staticmethod
    # def _generate_activation_verification_number(user, length=25):

    def is_not_expired(self):
        valid = (self.created - timezone.now()) \
            < timedelta(days=settings.USER_ACTIVATION_EMAIL_VALIDITY_TIME[1])
        return valid


class PasswordResetData(models.Model):
    email = models.EmailField(null=False, blank=True, db_index=True)
    user_phone = PhoneNumberField(
        null=False, blank=True, db_index=True, max_length=16)
    verification_code = models.CharField(max_length=30)

    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        unique_together = (('email', 'user_phone', 'verification_code'), )
        ordering = ('created', )

    def __str__(self):
        if self.email:
            return f"{self.email}: {self.verification_code}: {self.created}"
        if self.user_phone:
            return f"{self.user_phone}: {self.verification_code}: {self.created}"

    def clean(self):
        if self.email == '':
            self.email = "null"
        if self.email != "null" and self.user_phone != "null":
            msg = _("Specify only one field!")
            raise ValidationError(msg)
        if self.email == "null" and self.user_phone == "null":
            msg = _("Email or Phone number, specify at least one!")
            raise ValidationError(msg)

    @staticmethod
    def _generate_phone_verification_number(length=8):
        return _random_verification_number(length)

    @property
    def is_not_expired(self):
        if self.email:
            valid = (self.created - timezone.now()) \
                < timedelta(days=settings.PASSWORD_RESET_EMAIL_VALIDITY_TIME[1])
            return valid
        if self.user_phone:
            valid = (self.created - timezone.now()) \
                < timedelta(minutes=settings.PASSWORD_RESET_PHONE_VALIDITY_TIME[1])
            return valid

    def verification_code_matches(self, verification_code):
        return self.verification_code == verification_code
