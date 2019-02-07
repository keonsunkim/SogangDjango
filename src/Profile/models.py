from django.db import models
from django.contrib.auth import get_user_model

from .fields import PhoneNumberField


from .CONSTANTS import *


User = get_user_model()

class UserProfile(models.Model):
	owner = models.OneToOneField(User, null=False,
		on_delete=models.CASCADE)

	profile_pics = models.ImageField(upload_to="profile_pic/")
	phone_number = PhoneNumberField(allowed_countries=ALLOWED_COUNTRIES, max_length=16)
